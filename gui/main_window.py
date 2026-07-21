"""
Ventana Principal de NEXO Piano Tutor.
Integra el selector de lecciones, el renderizador de partitura interactivo (SheetView),
el evaluador en tiempo real (<15ms) y los indicadores de digitación/feedback.
"""

import os
import json
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QComboBox, QLabel, QPushButton, QFrame,
    QStatusBar
)
from PySide6.QtCore import Qt

from core.lesson import Lesson, TargetNote
from core.evaluator import RealtimeEvaluator
from gui.sheet_view import SheetView, midi_to_note_name
from gui.piano_keyboard import PianoKeyboard

# Intentar importar MidiEngine si nexo-midi-synth está instalado o en PROYECTOS
try:
    import sys
    synth_path = "/home/marcelo/PROYECTOS/nexo-midi-synth"
    if synth_path not in sys.path:
        sys.path.insert(0, synth_path)
    from core.engine import MidiEngine
    HAS_SYNTH = True
except ImportError:
    HAS_SYNTH = False

CARPETA_SCRIPT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LESSONS_DIR = os.path.join(CARPETA_SCRIPT, "lessons")


class MainWindow(QMainWindow):
    """Ventana principal de la app pedagógica NEXO Piano Tutor."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎼 NEXO Piano Tutor — Formación Clásica")
        self.setMinimumSize(600, 720)
        self.resize(700, 780)

        # Evaluador y Motor Audio
        self.evaluator = RealtimeEvaluator()
        self.engine = MidiEngine(self) if HAS_SYNTH else None

        self._build_ui()
        self._connect_signals()
        self._load_available_lessons()

        self.statusBar().showMessage("NEXO Piano Tutor v1.0.0 — Listo para estudiar")

    # ── Construcción de UI ─────────────────────────────────────────

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(10)
        layout.setContentsMargins(16, 14, 16, 14)

        # Cabezal: Título + Lección
        head_row = QHBoxLayout()
        title = QLabel("🎼 NEXO Piano Tutor")
        title.setObjectName("titleLabel")
        subtitle = QLabel("Método Clásico Progresivo")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        head_row.addWidget(title)
        head_row.addWidget(subtitle)
        head_row.addStretch()

        layout.addLayout(head_row)

        # Separador
        sep = QFrame()
        sep.setStyleSheet("background-color: #2d3b54;")
        sep.setFixedHeight(1)
        layout.addWidget(sep)

        # Selector de Lección
        lesson_group = QGroupBox("LECCIÓN Y CURRICULUM")
        lesson_layout = QHBoxLayout(lesson_group)
        lesson_layout.addWidget(QLabel("Seleccionar Lección:"))
        
        self.lesson_combo = QComboBox()
        lesson_layout.addWidget(self.lesson_combo, stretch=1)

        self.reset_btn = QPushButton("🔄 Reiniciar Lección")
        self.reset_btn.setObjectName("resetBtn")
        lesson_layout.addWidget(self.reset_btn)

        layout.addWidget(lesson_group)

        # Partitura Gráfica Interactiva
        sheet_group = QGroupBox("PARTITURA & GUÍA")
        sheet_layout = QVBoxLayout(sheet_group)
        
        self.sheet_view = SheetView()
        sheet_layout.addWidget(self.sheet_view)

        layout.addWidget(sheet_group, stretch=1)

        # Teclado Virtual Interactivo (Piano Roll)
        piano_group = QGroupBox("TECLADO DE PIANO INTERACTIVO")
        piano_layout = QVBoxLayout(piano_group)
        self.piano_keyboard = PianoKeyboard(start_note=36, end_note=84)
        piano_layout.addWidget(self.piano_keyboard)

        layout.addWidget(piano_group)

        # Panel de Feedback Pedagógico (Dedos + Veredicto)
        feedback_group = QGroupBox("GUÍA DE DIGITACIÓN & EVALUACIÓN EN TIEMPO REAL")
        fb_layout = QHBoxLayout(feedback_group)

        # Digitación grande
        finger_col = QVBoxLayout()
        finger_label = QLabel("DEDO")
        finger_label.setObjectName("subtitleLabel")
        finger_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        finger_col.addWidget(finger_label)

        self.finger_val = QLabel("—")
        self.finger_val.setObjectName("fingerLabel")
        finger_col.addWidget(self.finger_val)

        fb_layout.addLayout(finger_col)

        # Separador vertical
        vsep = QFrame()
        vsep.setFrameShape(QFrame.Shape.VLine)
        vsep.setStyleSheet("background-color: #2d3b54;")
        fb_layout.addWidget(vsep)

        # Texto de retroalimentación
        fb_col = QVBoxLayout()
        fb_text_label = QLabel("Retroalimentación Pedagógica")
        fb_text_label.setObjectName("subtitleLabel")
        fb_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fb_col.addWidget(fb_text_label)

        self.feedback_val = QLabel("Toca la tecla indicada para comenzar")
        self.feedback_val.setObjectName("feedbackLabel")
        self.feedback_val.setStyleSheet("color: #38bdf8;")
        fb_col.addWidget(self.feedback_val)

        fb_layout.addLayout(fb_col, stretch=2)

        layout.addWidget(feedback_group)

    # ── Señales y Slots ────────────────────────────────────────────

    def _connect_signals(self):
        self.lesson_combo.currentIndexChanged.connect(self._on_lesson_changed)
        self.reset_btn.clicked.connect(self._on_reset_clicked)
        self.piano_keyboard.note_pressed.connect(self._on_note_played)

        if self.engine:
            self.engine.note_played.connect(self._on_note_played)

    def _load_available_lessons(self):
        self.lesson_combo.clear()
        if not os.path.exists(LESSONS_DIR):
            return

        for fname in sorted(os.listdir(LESSONS_DIR)):
            if fname.endswith(".json"):
                fpath = os.path.join(LESSONS_DIR, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        label = f"{data.get('composer', '')} - {data.get('title', '')} ({data.get('opus', '')})"
                        self.lesson_combo.addItem(label, userData=fpath)
                except (json.JSONDecodeError, OSError):
                    pass

    def _on_lesson_changed(self, index: int):
        if index < 0:
            return
        fpath = self.lesson_combo.itemData(index)
        if not fpath or not os.path.exists(fpath):
            return

        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                notes = [TargetNote(**n) for n in data.get("notes", [])]
                lesson = Lesson(
                    id=data.get("id", ""),
                    title=data.get("title", ""),
                    composer=data.get("composer", ""),
                    opus=data.get("opus", ""),
                    description=data.get("description", ""),
                    clef=data.get("clef", "treble"),
                    bpm_recommended=data.get("bpm_recommended", 60),
                    notes=notes
                )
                self.evaluator.load_lesson(lesson)
                self.sheet_view.load_lesson(lesson, 0)
                self._update_target_display()
        except Exception as e:
            self.statusBar().showMessage(f"Error al cargar lección: {e}")

    def _on_reset_clicked(self):
        self.evaluator.reset()
        if self.evaluator.current_lesson:
            self.sheet_view.set_step(0)
            self._update_target_display()
            self.statusBar().showMessage("Lección reiniciada")

    def _on_note_played(self, note: int, velocity: int):
        if self.evaluator.is_finished:
            return

        result = self.evaluator.evaluate_note_on(note, velocity)
        self.feedback_val.setText(result.feedback_text)
        self.feedback_val.setStyleSheet(f"color: {result.feedback_color};")

        # Reproducir nota por audio si hay motor sintetizador
        if self.engine:
            self.engine.play_note(note, velocity)

        self.sheet_view.set_step(self.evaluator.current_step)
        self._update_target_display()

        if self.evaluator.is_finished:
            self.feedback_val.setText("🎉 ¡FELICITACIONES! Lección completada")
            self.feedback_val.setStyleSheet("color: #00e676;")
            self.statusBar().showMessage("¡Lección completada con éxito!")

    def _update_target_display(self):
        self.piano_keyboard.clear_all_active()
        target = self.evaluator.get_current_target()
        if target:
            self.finger_val.setText(str(target.finger))
            # Resaltar la nota objetivo esperada en cian
            self.piano_keyboard.set_key_active(target.midi_note, "#38bdf8")
        else:
            self.finger_val.setText("—")

    def closeEvent(self, event):
        if self.engine:
            self.engine.cleanup()
        super().closeEvent(event)

