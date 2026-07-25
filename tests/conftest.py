"""
Fixtures y utilidades compartidas para la suite de pruebas automatizadas con pytest.
"""

import os
import json
import pytest
from core.lesson import Lesson, TargetNote
from core.evaluator import RealtimeEvaluator
from core.user_manager import UserManager, User


@pytest.fixture
def sample_lesson() -> Lesson:
    """Proporciona una lección de prueba sintética estructurada (Posición Fija Do4 a Sol4)."""
    notes = [
        TargetNote(midi_note=60, duration_quarter=1.0, finger=1, hand="R", lyric="Do"),
        TargetNote(midi_note=62, duration_quarter=1.0, finger=2, hand="R", lyric="Re"),
        TargetNote(midi_note=64, duration_quarter=1.0, finger=3, hand="R", lyric="Mi"),
        TargetNote(midi_note=65, duration_quarter=1.0, finger=4, hand="R", lyric="Fa"),
        TargetNote(midi_note=67, duration_quarter=2.0, finger=5, hand="R", lyric="Sol"),
    ]
    return Lesson(
        id="test_beyer_01",
        title="Lección de Prueba 1",
        composer="Ferdinand Beyer",
        opus="Opus 101 Test",
        description="Lección de prueba sintética para tests unitarios.",
        clef="treble",
        bpm_recommended=60,
        time_signature="4/4",
        instrument=0,
        notes=notes
    )


@pytest.fixture
def evaluator(sample_lesson: Lesson) -> RealtimeEvaluator:
    """Devuelve un evaluador en tiempo real cargado con la lección sintética."""
    ev = RealtimeEvaluator()
    ev.load_lesson(sample_lesson)
    return ev


@pytest.fixture
def temp_user_manager(tmp_path) -> UserManager:
    """Devuelve un UserManager aislado operando sobre un archivo users.json temporal."""
    test_json_file = str(tmp_path / "test_users.json")
    return UserManager(filepath=test_json_file)
