"""
Test unitario para la demostración guiada de audio (Lesson Demo Player).
Verifica que la reproducción automatizada procese notas sin excepciones.
"""

import os
import json
import pytest
from PySide6.QtWidgets import QApplication
from core.lesson import Lesson, TargetNote, TargetStep
from core.evaluator import RealtimeEvaluator
from core.sound_engine import SoundEngine
from gui.main_window import MainWindow

# Inicializar QApplication para pruebas de Qt si no existe
app = QApplication.instance() or QApplication([])


def test_demo_playback_flow(qtbot=None):
    window = MainWindow()
    assert hasattr(window, "_is_demo_playing")
    assert window._is_demo_playing is False

    # Cargar lección explícita de prueba
    fpath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lessons", "beyer_op101_01.json")
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            notes = [TargetNote(**n) for n in data.get("notes", [])]
            steps = [TargetStep(duration_quarter=s.get("duration_quarter", 1.0), notes=[TargetNote(**n) for n in s.get("notes", [])]) for s in data.get("steps", [])]
            lesson = Lesson(id=data["id"], title=data["title"], composer=data["composer"], opus=data["opus"], description=data["description"], clef=data["clef"], bpm_recommended=data["bpm_recommended"], notes=notes, steps=steps)
            window.evaluator.load_lesson(lesson)
            window.sheet_view.load_lesson(lesson, 0)
    assert window.evaluator.current_lesson is not None

    # Iniciar demo
    window._start_demo_playback()
    assert window._is_demo_playing is True
    assert window.demo_btn.text() == "⏹ Detener Demo"

    # Ejecutar 3 ticks de prueba
    window._on_demo_tick()
    window._on_demo_tick()
    window._on_demo_tick()

    # Detener demo
    window._stop_demo_playback()
    assert window._is_demo_playing is False
    assert window.demo_btn.text() == "🎧 Escuchar"
    window.close()
