"""
Test unitario para la demostración guiada de audio (Lesson Demo Player).
Verifica que la reproducción automatizada procese notas sin excepciones.
"""

import os
import json
import pytest
from PySide6.QtWidgets import QApplication
from core.lesson import Lesson, TargetNote
from core.evaluator import RealtimeEvaluator
from core.sound_engine import SoundEngine
from gui.main_window import MainWindow

# Inicializar QApplication para pruebas de Qt si no existe
app = QApplication.instance() or QApplication([])


def test_demo_playback_flow(qtbot=None):
    window = MainWindow()
    assert hasattr(window, "_is_demo_playing")
    assert window._is_demo_playing is False

    # Verificar lección cargada
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
