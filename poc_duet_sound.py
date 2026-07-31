"""
Prueba de Concepto Aislada (PoC) para Validación de Audio Multicanal y Acompañamiento a 4 Manos.
Ejecutar en Windows con: python poc_duet_sound.py
"""

import os
import sys
import time

# Impedir la escritura y carga de archivos bytecode .pyc obsoletos
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.sound_engine import SoundEngine


def run_poc():
    print("=" * 65)
    print("  NEXO PIANO TUTOR - PRUEBA DE CONCEPTO AISLADA (PoC AUDIO DUETO)")
    print("=" * 65)

    engine = SoundEngine()
    print(f"\n[AUDIO] Motor de Sonido Activo: {engine.active_driver}")

    print("\n------------------------------------------------------------")
    print("[1] PROBANDO NOTA DEL ALUMNO SOLO (Canal 0 - Do4)")
    print("    Escuchá la nota aguda solitaria durante 3 segundos...")
    print("------------------------------------------------------------")
    engine.play_note(60, 95, 0)
    time.sleep(3.0)
    engine.stop_note(60, 0)
    time.sleep(1.5)

    print("\n------------------------------------------------------------")
    print("[2] PROBANDO ACORDE DE ACOMPAÑAMIENTO DEL TUTOR SOLO (Canal 1)")
    print("    Escuchá el colchón de acordes graves (Do-Mi-Sol) durante 4 segundos...")
    print("------------------------------------------------------------")
    tutor_chord = [48, 52, 55]  # Do3 - Mi3 - Sol3 (Acorde Do Mayor Grave)
    for note in tutor_chord:
        engine.play_note(note, 90, 1)
    time.sleep(4.0)
    for note in tutor_chord:
        engine.stop_note(note, 1)
    time.sleep(1.5)

    print("\n------------------------------------------------------------")
    print("[3] PROBANDO DUETO SIMULTÁNEO A 4 MANOS (Canal 0 + Canal 1)")
    print("    Escuchá la melodía del alumno Y el acorde del tutor sonar juntos durante 5 segundos...")
    print("------------------------------------------------------------")
    engine.play_note(60, 95, 0)
    for note in tutor_chord:
        engine.play_note(note, 90, 1)
    time.sleep(5.0)

    engine.stop_note(60, 0)
    for note in tutor_chord:
        engine.stop_note(note, 1)

    print("\n[4] Liberando recursos de audio...")
    engine.cleanup()
    print("=" * 65)
    print("  PoC COMPLETADO EXITOSAMENTE")
    print("=" * 65)


if __name__ == "__main__":
    run_poc()
