"""
Motor de Síntesis Audio Soberano para NEXO Piano Tutor.
Soporta sintetizador nativo de Windows (rtmidi) y sintetizador de SoundFonts (.sf2 vía pyfluidsynth).
Garantiza compatibilidad total de codificación ASCII en consolas Windows (cp1252).
"""

import os
import sys
import glob

CARPETA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    import rtmidi
    HAS_RTMIDI = True
except ImportError:
    HAS_RTMIDI = False

try:
    import fluidsynth
    HAS_FLUIDSYNTH = True
except ImportError:
    HAS_FLUIDSYNTH = False


class SoundEngine:
    """Motor de reproducción de notas de piano."""

    def __init__(self):
        self._midiout = None
        self._fluidsynth = None
        self._sfid = None
        self._active_driver = "Ninguno"

        self._init_audio()

    def _init_audio(self):
        """Inicializa el sintetizador de audio (FluidSynth .sf2 o Windows MidiOut)."""
        # 1. Priorizar FluidSynth si existe un archivo .sf2 en la raíz del proyecto
        sf_path = self._find_soundfont()
        if sf_path and HAS_FLUIDSYNTH:
            try:
                self._fluidsynth = fluidsynth.Synth()
                driver = "dsound" if sys.platform == "win32" else None
                try:
                    if driver:
                        self._fluidsynth.start(driver=driver)
                    else:
                        self._fluidsynth.start()
                except Exception:
                    self._fluidsynth.start()

                self._sfid = self._fluidsynth.sfload(sf_path)
                self._fluidsynth.program_select(0, self._sfid, 0, 0)  # General MIDI Program 0 (Acoustic Grand Piano)
                self._active_driver = f"FluidSynth ({os.path.basename(sf_path)})"
                print(f"[AUDIO] Motor Activo: {self._active_driver}")
                return
            except Exception as e:
                print(f"[AUDIO] Fallo al iniciar FluidSynth: {e}")
                self._fluidsynth = None

        # 2. Respaldo: Intentar rtmidi.MidiOut (Sintetizador General MIDI Nativo de Windows)
        if HAS_RTMIDI:
            try:
                self._midiout = rtmidi.MidiOut()
                ports = self._midiout.get_ports()
                if ports:
                    target_idx = 0
                    for idx, name in enumerate(ports):
                        if "wavetable" in name.lower() or "microsoft" in name.lower() or "synth" in name.lower():
                            target_idx = idx
                            break
                    self._midiout.open_port(target_idx)
                    self._active_driver = f"Windows MidiOut ({ports[target_idx]})"
                    print(f"[AUDIO] Motor Activo: {self._active_driver}")
                    return
            except Exception as e:
                print(f"[AUDIO] No se pudo inicializar MidiOut: {e}")
                self._midiout = None

        print("[AUDIO WARN] Sin dispositivo de salida sintetizado. Coloca un archivo .sf2 en la raiz del proyecto.")

    def _find_soundfont(self) -> str | None:
        """Busca archivos .sf2 en la carpeta raíz del proyecto y subcarpetas."""
        search_dirs = [
            CARPETA_RAIZ,
            os.getcwd(),
            os.path.join(CARPETA_RAIZ, "soundfonts"),
            os.path.join(CARPETA_RAIZ, "..", "nexo-midi-synth"),
        ]
        for path in search_dirs:
            if os.path.exists(path):
                pattern = os.path.join(path, "*.sf2")
                sf_files = glob.glob(pattern)
                if sf_files:
                    return sf_files[0]
        return None

    def play_note(self, note: int, velocity: int = 100):
        """Reproduce una nota (NOTE_ON)."""
        velocity = max(1, min(127, velocity))
        note = max(0, min(127, note))

        if self._fluidsynth:
            self._fluidsynth.noteon(0, note, velocity)

        if self._midiout and self._midiout.is_port_open():
            self._midiout.send_message([0x90, note, velocity])

    def stop_note(self, note: int):
        """Detiene una nota (NOTE_OFF)."""
        note = max(0, min(127, note))

        if self._fluidsynth:
            self._fluidsynth.noteoff(0, note)

        if self._midiout and self._midiout.is_port_open():
            self._midiout.send_message([0x80, note, 0])

    @property
    def active_driver(self) -> str:
        return self._active_driver

    def cleanup(self):
        """Libera los recursos de audio."""
        if self._midiout and self._midiout.is_port_open():
            self._midiout.close_port()
            self._midiout = None
        if self._fluidsynth:
            self._fluidsynth.delete()
            self._fluidsynth = None
