"""
Manejador y Detector de Entrada MIDI para NEXO Piano Tutor (v1.9.0).
Captura eventos NOTE_ON del teclado MIDI físico (Samson Carbon 49)
abriendo open_port() PRIMERO antes de establecer ignore_types() para evitar fallos de WinMM en Windows.
"""

import time
from PySide6.QtCore import QObject, Signal
try:
    import rtmidi
    HAS_RTMIDI = True
except ImportError:
    HAS_RTMIDI = False


class MidiInputHandler(QObject):
    """Manejador de entrada MIDI física en tiempo real."""

    note_played = Signal(int, int)   # (midi_note, velocity)
    note_released = Signal(int)      # (midi_note)
    device_connected = Signal(str)   # nombre del dispositivo conectado
    device_disconnected = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._midiin = rtmidi.MidiIn() if HAS_RTMIDI else None
        self._connected_port_name: str | None = None
        self._is_open = False

    def get_available_ports(self) -> list[str]:
        """Devuelve la lista de puertos MIDI de entrada disponibles."""
        if not self._midiin:
            return []
        try:
            return self._midiin.get_ports()
        except Exception:
            return []

    def auto_connect(self) -> tuple[bool, str]:
        """
        Intenta conectar al Samson Carbon 49 probando el puerto preferido
        y luego iterando sobre TODOS los puertos disponibles.
        """
        if not self._midiin:
            return False, "rtmidi no está disponible."

        ports = self.get_available_ports()
        if not ports:
            return False, "No se detectó ningún teclado MIDI USB."

        print(f"[MIDI IN] Escaneando {len(ports)} puerto(s) MIDI de entrada:")
        for idx, p in enumerate(ports):
            print(f"  [{idx}] '{p}'")

        # Priorizar índices que contengan 'samson' o 'carbon'
        candidate_indices = []
        for idx, port_name in enumerate(ports):
            if "samson" in port_name.lower() or "carbon" in port_name.lower():
                candidate_indices.append(idx)

        for idx in range(len(ports)):
            if idx not in candidate_indices:
                candidate_indices.append(idx)

        last_err = ""
        for idx in candidate_indices:
            print(f"[MIDI IN] Intentando abrir puerto [{idx}] '{ports[idx]}'...")
            ok, msg = self.connect_port(idx)
            if ok:
                print(f"[MIDI IN OK] Conexión establecida en puerto [{idx}] '{ports[idx]}'")
                return True, msg
            else:
                last_err = msg

        return False, f"No se pudo abrir ningún puerto MIDI. Último error: {last_err}"

    def connect_port(self, port_index: int) -> tuple[bool, str]:
        """Conecta al puerto MIDI especificado por índice con orden correcto WinMM."""
        if not self._midiin:
            return False, "rtmidi no está disponible."

        # Si el puerto ya está abierto, cerrarlo limpiamente primero
        if self._midiin.is_port_open():
            try:
                self._midiin.cancel_callback()
                self._midiin.close_port()
            except Exception:
                pass
            self._is_open = False
            time.sleep(0.1)

        ports = self.get_available_ports()
        if not (0 <= port_index < len(ports)):
            return False, "Índice de puerto inválido."

        port_name = ports[port_index]

        try:
            # ORDEN CRÍTICO WINMM: Abrir puerto PRIMERO, luego ignorar tipos
            self._midiin.open_port(port_index)
            self._midiin.ignore_types(sysex=True, timing=True, active_sense=True)
            self._midiin.set_callback(self._midi_callback)
            self._connected_port_name = port_name
            self._is_open = True
            self.device_connected.emit(self._connected_port_name)
            return True, f"Conectado a {port_name}"
        except Exception as e:
            err_msg = str(e)
            self._is_open = False
            self._connected_port_name = None
            self.device_disconnected.emit()
            user_msg = f"Error al abrir '{port_name}': {err_msg}"
            return False, user_msg

    def disconnect(self):
        """Desconecta el puerto MIDI actual."""
        if self._midiin and self._midiin.is_port_open():
            try:
                self._midiin.cancel_callback()
                self._midiin.close_port()
            except Exception:
                pass
        self._is_open = False
        self._connected_port_name = None
        self.device_disconnected.emit()

    @property
    def is_connected(self) -> bool:
        return self._is_open

    @property
    def connected_device_name(self) -> str | None:
        return self._connected_port_name

    def _midi_callback(self, event, data=None):
        """Callback directo de rtmidi."""
        message, _delta = event
        if not message or len(message) < 3:
            return

        status = message[0] & 0xF0
        note = message[1]
        velocity = message[2]

        if status == 0x90:  # NOTE_ON
            if velocity > 0:
                print(f"[MIDI HARDWARE] NOTE_ON -> Nota: {note}, Velocity: {velocity}")
                self.note_played.emit(note, velocity)
            else:
                print(f"[MIDI HARDWARE] NOTE_OFF -> Nota: {note}")
                self.note_released.emit(note)
        elif status == 0x80:  # NOTE_OFF
            print(f"[MIDI HARDWARE] NOTE_OFF -> Nota: {note}")
            self.note_released.emit(note)
