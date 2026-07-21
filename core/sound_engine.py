"""
Motor de Síntesis Audio Soberano para NEXO Piano Tutor.
Combina Microsoft GS Wavetable Synth (vía rtmidi.MidiOut en Windows)
y FluidSynth (.sf2) como respaldo para audio de ultra-baja latencia sin lag.
"""

import os
import sys
import glob

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
        self._active_driver = "ninguno"

        self._init_audio()

    def _init_audio(self):
        """Inicializa primero el sintetizador nativo de Windows (MidiOut) o FluidSynth."""
        # 1. Intentar rtmidi.MidiOut (Sintetizador General MIDI Nativo de Windows: Microsoft GS Wavetable)
        if HAS_RTMIDI:
            try:
                self._midiout = rtmidi.MidiOut()
                ports = self._midiout.get_ports()
                if ports:
                    # Buscar Microsoft GS Wavetable Synth o primer puerto de salida
                    target_idx = 0
                    for idx, name in enumerate(ports):
                        if "wavetable" in name.lower() or "microsoft" in name.lower() or "synth" in name.lower():
                            target_idx = idx
                            break
                    self._midiout.open_port(target_idx)
                    self._active_driver = f"rtmidi ({ports[target_idx]})"
                    print(f"🎵 Motor de Audio Activo: {self._active_driver}")
                    return
            except Exception as e:
                print(f"No se pudo inicializar MidiOut: {e}")
                self._midiout = None

        # 2. Intentar FluidSynth si hay un SoundFont disponible
        if HAS_FLUIDSYNTH:
            sf_path = self._find_soundfont()
            if sf_path:
                try:
                    self._fluidsynth = fluidsynth.Synth()
                    # En Windows dsound o winmm
                    driver = "dsound" if sys.platform == "win32" else "alsa"
                    self._fluidsynth.start(driver=driver)
                    self._sfid = self._fluidsynth.sfload(sf_path)
                    self._fluidsynth.program_select(0, self._sfid, 0, 0)  # Piano de cola (Program 0)
                    self._active_driver = f"fluidsynth ({os.path.basename(sf_path)})"
                    print(f"🎵 Motor de Audio Activo: {self._active_driver}")
                    return
                except Exception as e:
                    print(f"No se pudo inicializar FluidSynth: {e}")
                    self._fluidsynth = None

        print("⚠️ Advertencia: No se detectó dispositivo de salida de audio sintetizado.")

    def _find_soundfont(self) -> str | None:
        """Busca archivos .sf2 en la carpeta actual o proyectos adyacentes."""
        search_paths = [
            os.getcwd(),
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "/home/marcelo/PROYECTOS/nexo-midi-synth",
            "C:\\Users\\argen\\OneDrive\\Escritorio\\nexo-midi-synth",
        ]
        for path in search_paths:
            if os.path.exists(path):
                sf_files = glob.glob(os.path.join(path, "*.sf2"))
                if sf_files:
                    return sf_files[0]
        return None

    def play_note(self, note: int, velocity: int = 100):
        """Reproduce una nota (NOTE_ON)."""
        velocity = max(1, min(127, velocity))
        note = max(0, min(127, note))

        if self._midiout and self._midiout.is_port_open():
            # Mensaje NOTE_ON: 0x90, nota, velocity
            self._midiout.send_message([0x90, note, velocity])

        if self._fluidsynth:
            self._fluidsynth.noteon(0, note, velocity)

    def stop_note(self, note: int):
        """Detiene una nota (NOTE_OFF)."""
        note = max(0, min(127, note))

        if self._midiout and self._midiout.is_port_open():
            # Mensaje NOTE_OFF: 0x80, nota, 0
            self._midiout.send_message([0x80, note, 0])

        if self._fluidsynth:
            self._fluidsynth.noteoff(0, note)

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
