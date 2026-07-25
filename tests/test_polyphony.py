"""
Pruebas unitarias e integrales para Acordes Polifónicos y Simultaneidad Bimanual.
"""

import pytest
from core.lesson import Lesson, TargetNote, TargetStep
from core.evaluator import RealtimeEvaluator


def test_target_step_properties():
    # Monofónica
    step_mono = TargetStep(duration_quarter=1.0, notes=[TargetNote(midi_note=60, duration_quarter=1.0, finger=1, hand="R")])
    assert step_mono.is_chord is False
    assert step_mono.is_bimanual is False

    # Acorde en una sola mano (Mano Izquierda)
    step_lh_chord = TargetStep(
        duration_quarter=1.0,
        notes=[
            TargetNote(midi_note=48, duration_quarter=1.0, finger=5, hand="L"),
            TargetNote(midi_note=52, duration_quarter=1.0, finger=3, hand="L"),
            TargetNote(midi_note=55, duration_quarter=1.0, finger=1, hand="L"),
        ]
    )
    assert step_lh_chord.is_chord is True
    assert step_lh_chord.is_bimanual is False

    # Golpe simultáneo bimanual (Mano Derecha + Mano Izquierda)
    step_bimanual = TargetStep(
        duration_quarter=1.0,
        notes=[
            TargetNote(midi_note=48, duration_quarter=1.0, finger=5, hand="L"),
            TargetNote(midi_note=72, duration_quarter=1.0, finger=5, hand="R"),
        ]
    )
    assert step_bimanual.is_chord is True
    assert step_bimanual.is_bimanual is True


def test_evaluator_polyphonic_steps():
    lesson = Lesson(
        id="poly_test",
        title="Test Polifónico",
        composer="Test",
        opus="Op. 1",
        description="Lección de prueba con acordes",
        clef="grand",
        bpm_recommended=60,
        steps=[
            TargetStep(
                duration_quarter=1.0,
                notes=[
                    TargetNote(midi_note=48, duration_quarter=1.0, finger=5, hand="L"),
                    TargetNote(midi_note=60, duration_quarter=1.0, finger=1, hand="R")
                ]
            )
        ]
    )

    evaluator = RealtimeEvaluator()
    evaluator.load_lesson(lesson)

    assert len(evaluator.current_lesson.get_steps()) == 1
    step = evaluator.get_current_step()
    assert step is not None
    assert len(step.notes) == 2
