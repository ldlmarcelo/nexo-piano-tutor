"""
Script de Diagnostico Quirurgico y Aislado para NEXO Piano Tutor (ASCII 100% puro).
Ejecutar con: python diagnose_midi.py
"""

import sys
import os
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

print("=" * 60)
print(" NEXO Piano Tutor -- Script de Diagnostico Sistematico")
print("=" * 60)
print(f"Python Version: {sys.version}")
print(f"Plataforma: {sys.platform}")
print(f"Carpeta: {os.getcwd()}")
print("-" * 60)

# 1. Test de rtmidi (Entrada MIDI de Hardware)
print("\n[PASO 1] Verificando python-rtmidi (Captura de Teclado)...")
try:
    import rtmidi
    midiin = rtmidi.MidiIn()
    in_ports = midiin.get_ports()
    print(f" -> Puertos MIDI de Entrada detectados ({len(in_ports)}):")
    for idx, port in enumerate(in_ports):
        print(f"    [{idx}] {port}")
    if not in_ports:
        print(" [!] ALERTA: No se detectaron teclados MIDI de entrada.")
except Exception as e:
    print(f" [!] ERROR al importar/inicializar rtmidi: {e}")
    midiin = None
    in_ports = []

# 2. Test de Salida de Audio (SoundEngine)
print("\n[PASO 2] Verificando Motor de Audio (SoundEngine)...")
try:
    from core.sound_engine import SoundEngine
    engine = SoundEngine()
    print(f" -> Driver Activo: {engine.active_driver}")
    print(" -> Emitiendo nota de prueba (Do4 / MIDI 60) por 1 segundo...")
    engine.play_note(60, 100)
    time.sleep(1.0)
    engine.stop_note(60)
    print(" -> Nota de prueba finalizada.")
except Exception as e:
    print(f" [!] ERROR en SoundEngine: {e}")

# 3. Test de Evaluador Pedagogico (RealtimeEvaluator)
print("\n[PASO 3] Verificando Evaluador (RealtimeEvaluator)...")
try:
    from core.evaluator import RealtimeEvaluator, midi_to_note_name
    from core.lesson import Lesson, TargetNote

    lesson = Lesson(
        id="test", title="Test", composer="Test", opus="Op.1",
        description="Test", clef="treble", bpm_recommended=60,
        notes=[TargetNote(midi_note=60, duration_quarter=1.0, finger=1, lyric="Do")]
    )
    evaluator = RealtimeEvaluator()
    evaluator.load_lesson(lesson)

    print(f" -> Leccion cargada. Nota esperada: {evaluator.get_current_target()}")
    
    # Test 1: Misma nota, otra octava (MIDI 48 = Do3 vs 60 = Do4)
    res_octave = evaluator.evaluate_note_on(48, 100)
    print(f" -> Test Nota 48 (Do3): Veredicto='{res_octave.feedback_text}', Color='{res_octave.feedback_color}', Avance={evaluator.current_step}")
    
    # Test 2: Nota exacta (MIDI 60 = Do4)
    evaluator.reset()
    res_exact = evaluator.evaluate_note_on(60, 100)
    print(f" -> Test Nota 60 (Do4): Veredicto='{res_exact.feedback_text}', Color='{res_exact.feedback_color}', Avance={evaluator.current_step}")
except Exception as e:
    print(f" [!] ERROR en Evaluador: {e}")

# 4. Test Escucha MIDI en Tiempo Real (30 segundos)
if in_ports and midiin:
    print("\n" + "=" * 60)
    print(" ESCUCHA EN TIEMPO REAL DEL TECLADO MIDI (30 segundos)")
    print(" Por favor toca varias teclas en tu Samson Carbon 49...")
    print("=" * 60)

    selected_port = 0
    for idx, port_name in enumerate(in_ports):
        if "samson" in port_name.lower() or "carbon" in port_name.lower():
            selected_port = idx
            break

    def raw_callback(event, data=None):
        msg, delta = event
        if msg:
            status = msg[0] & 0xF0
            note = msg[1] if len(msg) > 1 else 0
            vel = msg[2] if len(msg) > 2 else 0
            print(f"\n [EVENTO MIDI DETECTADO] Raw: {msg} | Status: 0x{status:02X} | Nota: {note} ({midi_to_note_name(note)}) | Velocity: {vel}")

    try:
        midiin.ignore_types(sysex=True, timing=True, active_sense=True)
        midiin.open_port(selected_port)
        midiin.set_callback(raw_callback)
        print(f" -> Escuchando en puerto [{selected_port}]: {in_ports[selected_port]}")
        
        for i in range(30, 0, -1):
            sys.stdout.write(f"\r Escuchando... {i}s restantes ")
            sys.stdout.flush()
            time.sleep(1.0)
        print("\n -> Finalizada sesion de prueba de 30 segundos.")
        midiin.close_port()
    except Exception as e:
        print(f"\n [!] ERROR en captura de eventos MIDI: {e}")

print("\n" + "=" * 60)
print(" Diagnostico Finalizado.")
print("=" * 60)
