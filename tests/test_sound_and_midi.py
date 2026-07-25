"""
Pruebas de Tolerancia y Fallback sin Hardware (Headless) para SoundEngine y MidiInputHandler.
"""

import pytest
from core.sound_engine import SoundEngine
from core.midi_input import MidiInputHandler


def test_sound_engine_headless_safety():
    engine = SoundEngine()
    assert isinstance(engine.active_driver, str)

    # Verificar invocaciones sin fallos
    engine.set_instrument(0)    # Piano de cola
    engine.set_instrument(6)    # Clavecín
    engine.play_note(60, 100)   # Do4
    engine.stop_note(60)
    engine.play_metronome_click(is_downbeat=True)
    engine.play_metronome_click(is_downbeat=False)
    engine.cleanup()


def test_midi_input_handler_headless_safety():
    midi = MidiInputHandler()
    assert midi.is_connected is False
    assert midi.connected_device_name is None

    ports = midi.get_available_ports()
    assert isinstance(ports, list)

    midi.disconnect()
