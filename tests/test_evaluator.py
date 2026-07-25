"""
Pruebas Unitarias para el Evaluador Pedagógico en Tiempo Real (RealtimeEvaluator).
"""

import pytest
from core.evaluator import RealtimeEvaluator, EvaluationResult, midi_to_note_name
from core.lesson import Lesson, TargetNote


def test_midi_to_note_name_conversion():
    assert midi_to_note_name(60) == "Do4"
    assert midi_to_note_name(61) == "Do#4"
    assert midi_to_note_name(62) == "Re4"
    assert midi_to_note_name(48) == "Do3"
    assert midi_to_note_name(72) == "Do5"


def test_evaluator_initialization(evaluator: RealtimeEvaluator, sample_lesson: Lesson):
    assert evaluator.current_lesson == sample_lesson
    assert evaluator.current_step == 0
    assert evaluator.range_start == 0
    assert evaluator.range_end == 4
    assert not evaluator.is_finished
    assert evaluator.get_current_target().midi_note == 60


def test_evaluator_correct_note_sequence(evaluator: RealtimeEvaluator):
    # Nota 1: Do4 (60)
    res1 = evaluator.evaluate_note_on(played_note=60, velocity=100)
    assert res1.is_correct_note is True
    assert res1.expected_note == 60
    assert res1.played_note == 60
    assert res1.expected_finger == 1
    assert evaluator.current_step == 1
    assert not evaluator.is_finished

    # Nota 2: Re4 (62)
    res2 = evaluator.evaluate_note_on(played_note=62, velocity=100)
    assert res2.is_correct_note is True
    assert evaluator.current_step == 2

    # Nota 3: Mi4 (64)
    res3 = evaluator.evaluate_note_on(played_note=64, velocity=100)
    assert res3.is_correct_note is True
    assert evaluator.current_step == 3

    # Nota 4: Fa4 (65)
    res4 = evaluator.evaluate_note_on(played_note=65, velocity=100)
    assert res4.is_correct_note is True
    assert evaluator.current_step == 4

    # Nota 5: Sol4 (67) - Última nota de la lección
    res5 = evaluator.evaluate_note_on(played_note=67, velocity=100)
    assert res5.is_correct_note is True
    assert res5.is_rep_complete is True
    assert evaluator.is_finished is True
    assert "EJECUCIÓN IMPECABLE" in res5.feedback_text


def test_evaluator_wrong_note_and_octave_hint(evaluator: RealtimeEvaluator):
    # Se espera Do4 (60). Toca Re4 (62) - nota completamente equivocada
    res_wrong = evaluator.evaluate_note_on(played_note=62, velocity=100)
    assert res_wrong.is_correct_note is False
    assert evaluator.current_step == 0  # El paso NO avanza tras un error
    assert evaluator.wrong_attempts == 1
    assert 0 in evaluator.steps_with_errors
    assert "Tocaste Re4" in res_wrong.feedback_text

    # Se espera Do4 (60). Toca Do5 (72) - mismo pitch (Do), octava distinta arriba
    res_oct_up = evaluator.evaluate_note_on(played_note=72, velocity=100)
    assert res_oct_up.is_correct_note is False
    assert "octava distinta" in res_oct_up.feedback_text
    assert "OCTAVE -" in res_oct_up.feedback_text

    # Se espera Do4 (60). Toca Do3 (48) - mismo pitch (Do), octava distinta abajo
    res_oct_down = evaluator.evaluate_note_on(played_note=48, velocity=100)
    assert res_oct_down.is_correct_note is False
    assert "OCTAVE +" in res_oct_down.feedback_text


def test_evaluator_rhythm_jitter(evaluator: RealtimeEvaluator):
    evaluator.mode = "tempo"

    # Nota 1 con tiempo exacto (0ms)
    res_exact = evaluator.evaluate_note_on(played_note=60, velocity=100, time_delta_ms=10.0)
    assert "Rítmica Exacta" in res_exact.feedback_text

    # Nota 2 en pulso razonable (50ms)
    res_pulse = evaluator.evaluate_note_on(played_note=62, velocity=100, time_delta_ms=50.0)
    assert "En Pulso" in res_pulse.feedback_text

    # Nota 3 con desfase adelantado (-120ms)
    res_early = evaluator.evaluate_note_on(played_note=64, velocity=100, time_delta_ms=-120.0)
    assert "Desfase" in res_early.feedback_text
    assert "Adelantado" in res_early.feedback_text


def test_evaluator_range_ab(evaluator: RealtimeEvaluator):
    # Fijar rango A-B a las notas 1 a 3 (índices 1 a 3 -> Re4, Mi4, Fa4)
    evaluator.set_range(start_step=1, end_step=3)
    assert evaluator.range_start == 1
    assert evaluator.range_end == 3
    assert evaluator.current_step == 1
    assert evaluator.get_current_target().midi_note == 62  # Re4

    # Ejecutar correctamente el rango
    evaluator.evaluate_note_on(played_note=62, velocity=100)  # Re4
    assert evaluator.current_step == 2
    evaluator.evaluate_note_on(played_note=64, velocity=100)  # Mi4
    assert evaluator.current_step == 3

    # Última nota del rango
    res_last = evaluator.evaluate_note_on(played_note=65, velocity=100)  # Fa4
    assert res_last.is_correct_note is True
    assert res_last.is_rep_complete is True
    assert evaluator.is_finished is True


def test_evaluator_repeat_modes(evaluator: RealtimeEvaluator):
    # Modo 3x (Serie de 3 repeticiones)
    evaluator.set_repeat_mode("3x")
    assert evaluator.repeat_target == 3
    assert evaluator.current_rep == 1

    # Completar la repetición 1 (5 notas)
    for note in [60, 62, 64, 65]:
        evaluator.evaluate_note_on(played_note=note, velocity=100)
    res_rep1 = evaluator.evaluate_note_on(played_note=67, velocity=100)

    # Debe haber avanzado a la repetición 2 y haber reiniciado el paso a 0
    assert res_rep1.is_rep_complete is True
    assert evaluator.current_rep == 2
    assert evaluator.current_step == 0
    assert not evaluator.is_finished
    assert "Repetición 1 de 3 completada" in res_rep1.feedback_text


def test_evaluator_reset(evaluator: RealtimeEvaluator):
    evaluator.evaluate_note_on(played_note=60, velocity=100)
    evaluator.evaluate_note_on(played_note=62, velocity=100)
    assert evaluator.current_step == 2

    evaluator.reset()
    assert evaluator.current_step == 0
    assert evaluator.current_rep == 1
    assert evaluator.total_attempts == 0
    assert evaluator.correct_attempts == 0
    assert evaluator.wrong_attempts == 0
    assert len(evaluator.steps_with_errors) == 0
