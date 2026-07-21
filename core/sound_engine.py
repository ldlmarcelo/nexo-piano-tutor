"""
Motor de Síntesis Audio Soberano para NEXO Piano Tutor (v1.2.0).
Soporta:
1. FluidSynth (.sf2 vía pyfluidsynth) — Sintetizador SoundFont General MIDI de alta fidelidad.
2. Windows Native WINMM API (ctypes.windll.winmm) — Sintetizador General MIDI 64-bit NATIVO de Windows.
3. rtmidi.MidiOut — Sintetizador para Linux / macOS.
"""

import os
import sys
import glob
import ctypes

CARPETA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Registrar directorios de DLLs en Windows (nexo-piano-tutor y nexo-midi-synth)
if sys.platform == "win32":
    dll_candidates = [
        CARPETA_RAIZ,
        os.path.join(CARPETA_RAIZ, "..", "nexo-midi-synth"),
        "C:\\Users\\argen\\OneDrive\\Escritorio\\nexo-midi-synth",
        os.path.join(os.environ.get("USERPROFILE", ""), "OneDrive", "Escritorio", "nexo-midi-synth"),
        os.path.join(os.environ.get("USERPROFILE", ""), "Desktop", "nexo-midi-synth"),
    ]
    for d in dll_candidates:
        if os.path.exists(d):
            if hasattr(os, "add_dll_directory"):
                try:
                    os.add_dll_directory(d)
                except (FileNotFoundError, OSError):
                    pass
            os.environ["PATH"] = d + os.pathsep + os.environ.get("PATH", "")

try:
    import fluidsynth
    HAS_FLUIDSYNTH = True
    FLUIDSYNTH_ERROR = None
except Exception as e:
    HAS_FLUIDSYNTH = False
    FLUIDSYNTH_ERROR = str(e)

try:
    import rtmidi
    HAS_RTMIDI = True
except ImportError:
    HAS_RTMIDI = False


class SoundEngine:
    """Motor de síntesis de sonido multi-driver para piano."""

    def __init__(self):
        self._hwinmm = None
        self._fluidsynth = None
        self._midiout = None
        self._sfid = None
        self._active_driver = "Ninguno"
        self._current_program = 0

        self._init_audio()

    def _init_audio(self):
        """Inicializa el mejor driver de audio disponible."""

        # 1. Intentar FluidSynth si hay un archivo .sf2 presente
        sf_path = self._find_soundfont()
        if sf_path:
            print(f"[AUDIO] SoundFont encontrado en: {sf_path}")
            if HAS_FLUIDSYNTH:
                try:
                    self._fluidsynth = fluidsynth.Synth()
                    driver = "dsound" if sys.platform == "win32" else None
                    try:
                        # midi_driver=None es CRÍTICO: impide que FluidSynth abra
                        # su propio driver winmm de ENTRADA MIDI, que tomaría el
                        # puerto del Carbon 49 antes que nuestro rtmidi.MidiIn.
                        if driver:
                            self._fluidsynth.start(driver=driver, midi_driver=None)
                        else:
                            self._fluidsynth.start(midi_driver=None)
                    except Exception:
                        self._fluidsynth.start(midi_driver=None)

                    self._sfid = self._fluidsynth.sfload(sf_path)
                    self._fluidsynth.program_select(0, self._sfid, 0, self._current_program)
                    self._active_driver = f"FluidSynth ({os.path.basename(sf_path)})"
                    print(f"[AUDIO] Motor Activo: {self._active_driver}")
                    return
                except Exception as e:
                    print(f"[AUDIO] FluidSynth sfload fallo: {e}")
                    self._fluidsynth = None
            else:
                print(f"[AUDIO] pyfluidsynth no pudo cargar la DLL de FluidSynth: {FLUIDSYNTH_ERROR}")

        # 2. En Windows: Intentar sintetizador WINMM nativo 64-bit vía ctypes (Microsoft GS Wavetable Synth)
        if sys.platform == "win32":
            try:
                hmidi = ctypes.c_void_p()
                # Probar MIDIMAPPER (0xFFFFFFFF) y luego puerto 0 (Default GS Wavetable)
                res = ctypes.windll.winmm.midiOutOpen(ctypes.byref(hmidi), ctypes.c_uint(0xFFFFFFFF), 0, 0, 0)
                if res != 0:
                    res = ctypes.windll.winmm.midiOutOpen(ctypes.byref(hmidi), ctypes.c_uint(0), 0, 0, 0)

                if res == 0:
                    self._hwinmm = hmidi
                    self._active_driver = "Windows Native WINMM (General MIDI)"
                    print(f"[AUDIO] Motor Activo: {self._active_driver}")
                    return
                else:
                    print(f"[AUDIO] winmm.midiOutOpen retorno codigo {res}")
            except Exception as e:
                print(f"[AUDIO] Error con winmm ctypes: {e}")
                self._hwinmm = None

        # 3. Intentar rtmidi.MidiOut (Linux / macOS o respaldo Windows)
        if HAS_RTMIDI:
            try:
                self._midiout = rtmidi.MidiOut()
                ports = self._midiout.get_ports()
                for idx, port_name in enumerate(ports):
                    try:
                        self._midiout.open_port(idx)
                        self._active_driver = f"rtmidi ({port_name})"
                        print(f"[AUDIO] Motor Activo: {self._active_driver}")
                        return
                    except Exception:
                        continue
            except Exception as e:
                print(f"[AUDIO] Error al abrir rtmidi output: {e}")
                self._midiout = None

        print("[AUDIO WARN] No se pudo activar ningun motor de sonido.")

    def _find_soundfont(self) -> str | None:
        """Busca insensible a mayúsculas archivos .sf2 en el proyecto y carpetas vecinas."""
        search_dirs = [
            CARPETA_RAIZ,
            os.getcwd(),
            os.path.join(CARPETA_RAIZ, "soundfonts"),
            os.path.join(CARPETA_RAIZ, "..", "nexo-midi-synth"),
            "C:\\Users\\argen\\OneDrive\\Escritorio\\nexo-midi-synth",
            "C:\\Users\\argen\\OneDrive\\Escritorio\\nexo-piano-tutor",
        ]
        for path in search_dirs:
            if os.path.exists(path):
                try:
                    for filename in os.listdir(path):
                        if filename.lower().endswith(".sf2"):
                            return os.path.join(path, filename)
                except OSError:
                    pass
        return None

    def set_instrument(self, program: int = 0):
        """
        Cambia el instrumento General MIDI (0-127).
        Ejemplos:
          0 = Piano de Cola Acústico (Beyer / Clementi / Mozart)
          6 = Clavecín / Harpsichord (J. S. Bach / Barroco)
          19 = Órgano de Iglesia (J. S. Bach)
        """
        self._current_program = max(0, min(127, program))
        if self._fluidsynth and self._sfid is not None:
            try:
                self._fluidsynth.program_select(0, self._sfid, 0, self._current_program)
                print(f"[AUDIO] Instrumento cambiado a Program GM {self._current_program}")
            except Exception as e:
                print(f"[AUDIO] Error al cambiar programa en FluidSynth: {e}")
        elif self._hwinmm:
            # Mensaje Program Change MIDI: 0xC0 | (program << 8)
            msg = 0xC0 | (self._current_program << 8)
            ctypes.windll.winmm.midiOutShortMsg(self._hwinmm, msg)
            print(f"[AUDIO] Instrumento cambiado a Program GM {self._current_program} (WINMM)")

    def play_note(self, note: int, velocity: int = 100):
        """Reproduce una nota (NOTE_ON)."""
        velocity = max(1, min(127, velocity))
        note = max(0, min(127, note))

        if self._fluidsynth:
            self._fluidsynth.noteon(0, note, velocity)

        elif self._hwinmm:
            # Mensaje MIDI de 32 bits: Status 0x90 | (Note << 8) | (Velocity << 16)
            msg = 0x90 | (note << 8) | (velocity << 16)
            ctypes.windll.winmm.midiOutShortMsg(self._hwinmm, msg)

        elif self._midiout and self._midiout.is_port_open():
            self._midiout.send_message([0x90, note, velocity])

    def stop_note(self, note: int):
        """Detiene una nota (NOTE_OFF)."""
        note = max(0, min(127, note))

        if self._fluidsynth:
            self._fluidsynth.noteoff(0, note)

        elif self._hwinmm:
            # NOTE_OFF: Status 0x80 | (Note << 8)
            msg = 0x80 | (note << 8) | (0 << 16)
            ctypes.windll.winmm.midiOutShortMsg(self._hwinmm, msg)

        elif self._midiout and self._midiout.is_port_open():
            self._midiout.send_message([0x80, note, 0])

    @property
    def active_driver(self) -> str:
        return self._active_driver

    def cleanup(self):
        """Libera recursos de audio."""
        if self._hwinmm:
            ctypes.windll.winmm.midiOutClose(self._hwinmm)
            self._hwinmm = None
        if self._fluidsynth:
            self._fluidsynth.delete()
            self._fluidsynth = None
        if self._midiout and self._midiout.is_port_open():
            self._midiout.close_port()
            self._midiout = None
