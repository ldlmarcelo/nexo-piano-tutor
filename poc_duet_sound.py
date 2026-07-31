"""
Prueba de Concepto Aislada (PoC) para Validación de Audio Multicanal y Acompañamiento a 4 Manos.
Ejecutar con: python poc_duet_sound.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.sound_engine import SoundEngine


def run_poc():
    print("=" * 60)
    print("  NEXO PIANO TUTOR - PRUEBA DE CONCEPTO AISLADA (PoC AUDIO)")
    print("=" * 60)

    engine = SoundEngine()
    print(f"\n[1] Motor de Audio Detectado: {engine.active_driver}")

    print("\n[2] Probando Melodía del Alumno (Canal 0 - Do4)...")
    engine.play_note(60, velocity=95, channel=0)
    time.sleep(1.0)
    engine.stop_note(60, channel=0)
    time.sleep(0.5)

    print("[3] Probando Acorde de Acompañamiento del Tutor (Canal 1 - Do Mayor Grave)...")
    tutor_chord = [48, 52, 55]  # Do3 - Mi3 - Sol3
    for note in tutor_chord:
        engine.play_note(note, velocity=90, channel=1)
    time.sleep(1.5)
    for note in tutor_chord:
        engine.stop_note(note, channel=1)
    time.sleep(0.5)

    print("[4] Probando DUETO SIMULTÁNEO (Alumno Do4 en Ch0 + Acorde Tutor en Ch1)...")
    engine.play_note(60, velocity=95, channel=0)
    for note in tutor_chord:
        engine.play_note(note, velocity=90, channel=1)
    time.sleep(2.0)

    engine.stop_note(60, channel=0)
    for note in tutor_chord:
        engine.stop_note(note, channel=1)

    print("\n[5] Liberando recursos de audio...")
    engine.cleanup()
    print("=" * 60)
    print("  PoC COMPLETADO EXITOSAMENTE")
    print("=" * 60)


if __name__ == "__main__":
    run_poc()
