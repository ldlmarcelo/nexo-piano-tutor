"""
Manejador y Detector de Entrada MIDI para NEXO Piano Tutor (v1.3.0).
Captura eventos NOTE_ON de teclados MIDI físicos (ej: Samson Carbon 49)
vía python-rtmidi y utiliza un buffer de cola con QTimer thread-safe
para garantizar que las señales Qt se procesen limpiamente en el hilo principal GUI.
"""

from collections import deque
from PySide6.QtCore import QObject, Signal, QTimer
try:
    import rtmidi
    HAS_RTMIDI = True
except ImportError:
    HAS_RTMIDI = False


class MidiInputHandler(QObject):
    """Manejador de entrada MIDI física en tiempo real con cola thread-safe."""

    note_played = Signal(int, int)   # (midi_note, velocity)
    note_released = Signal(int)      # (midi_note)
    device_connected = Signal(str)   # nombre del dispositivo conectado
    device_disconnected = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._midiin = rtmidi.MidiIn() if HAS_RTMIDI else None
        self._connected_port_name: str | None = None
        self._is_open = False
        self._queue = deque()

        # Timer de vaciado de cola a 5ms (200Hz) en el hilo principal de Qt
        self._timer = QTimer(self)
        self._timer.setInterval(5)
        self._timer.timeout.connect(self._process_queue)
        self._timer.start()

    def get_available_ports(self) -> list[str]:
        """Devuelve la lista de puertos MIDI de entrada disponibles."""
        if not self._midiin:
            return []
        return self._midiin.get_ports()

    def auto_connect(self) -> bool:
        """
        Intenta conectar automáticamente al Samson Carbon 49 o al primer puerto disponible.
        """
        ports = self.get_available_ports()
        if not ports:
            return False

        # Priorizar Samson Carbon 49 si está presente
        selected_idx = 0
        for idx, port_name in enumerate(ports):
            if "samson" in port_name.lower() or "carbon" in port_name.lower():
                selected_idx = idx
                break

        return self.connect_port(selected_idx)

    def connect_port(self, port_index: int) -> bool:
        """Conecta al puerto MIDI especificado por índice."""
        self.disconnect()
        ports = self.get_available_ports()
        if not (0 <= port_index < len(ports)):
            return False

        try:
            # Ignorar Sysex, Timing y Active Sense
            self._midiin.ignore_types(sysex=True, timing=True, active_sense=True)
            self._midiin.open_port(port_index)
            self._midiin.set_callback(self._midi_callback)
            self._connected_port_name = ports[port_index]
            self._is_open = True
            self.device_connected.emit(self._connected_port_name)
            print(f"[MIDI IN] Conectado exitosamente a: {self._connected_port_name}")
            return True
        except Exception as e:
            print(f"[MIDI IN] Error al conectar puerto MIDI: {e}")
            self._is_open = False
            self.device_disconnected.emit()
            return False

    def disconnect(self):
        """Desconecta el puerto MIDI actual."""
        if self._midiin and self._is_open and self._midiin.is_port_open():
            self._midiin.cancel_callback()
            self._midiin.close_port()
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
        """Callback de rtmidi (corre en el hilo C++ de rtmidi). Encola eventos."""
        message, _delta = event
        if not message or len(message) < 3:
            return

        status = message[0] & 0xF0
        note = message[1]
        velocity = message[2]

        if status == 0x90:  # NOTE_ON
            if velocity > 0:
                self._queue.append(("ON", note, velocity))
            else:
                self._queue.append(("OFF", note, 0))
        elif status == 0x80:  # NOTE_OFF
            self._queue.append(("OFF", note, 0))

    def _process_queue(self):
        """Procesador de la cola ejecutado en el HILO PRINCIPAL de Qt por QTimer."""
        while self._queue:
            evt_type, note, vel = self._queue.popleft()
            if evt_type == "ON":
                self.note_played.emit(note, vel)
            elif evt_type == "OFF":
                self.note_released.emit(note)
