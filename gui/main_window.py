"""
Ventana Principal de NEXO Piano Tutor.
Integra la Pantalla de Autenticación / Selección de Estudiante (LoginWidget),
el Selector de Lecciones, el Renderizador de Partitura Interactivo (SheetView),
el Evaluador en Tiempo Real (<15ms) y la Persistencia por Usuario (UserManager).
"""

import os
import json
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QComboBox, QLabel, QPushButton, QFrame,
    QStackedWidget, QStatusBar
)
from PySide6.QtCore import Qt

from core.lesson import Lesson, TargetNote
from core.evaluator import RealtimeEvaluator
from core.midi_input import MidiInputHandler
from core.sound_engine import SoundEngine
from core.user_manager import UserManager, User
from gui.sheet_view import SheetView, midi_to_note_name
from gui.piano_keyboard import PianoKeyboard
from gui.login_widget import LoginWidget

CARPETA_SCRIPT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LESSONS_DIR = os.path.join(CARPETA_SCRIPT, "lessons")


class MainWindow(QMainWindow):
    """Ventana principal de la app pedagógica NEXO Piano Tutor."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎼 NEXO Piano Tutor — Formación Clásica")
        self.setMinimumSize(640, 740)
        self.resize(720, 800)

        # Gestor de Usuarios, Evaluador, Entrada MIDI física y Motor Audio
        self.user_manager = UserManager()
        self.evaluator = RealtimeEvaluator()
        self.midi_input = MidiInputHandler(self)
        self.sound_engine = SoundEngine()

        self._build_ui()
        self._connect_signals()
        self._load_available_lessons()

        # Verificar si hay usuario activo previamente autenticado
        active_user = self.user_manager.get_active_user()
        if active_user:
            self._on_user_authenticated(active_user)
        else:
            self.stacked_widget.setCurrentIndex(0)

        self.statusBar().showMessage(f"NEXO Piano Tutor v1.0.0 — Audio: {self.sound_engine.active_driver}")

    # ── Construcción de UI ─────────────────────────────────────────

    def _build_ui(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # PÁGINA 0: Widget de Autenticación / Selección de Estudiante
        self.login_widget = LoginWidget(self.user_manager)
        self.stacked_widget.addWidget(self.login_widget)

        # PÁGINA 1: Interfaz Principal de Aprendizaje (Estudio)
        self.study_widget = QWidget()
        study_layout = QVBoxLayout(self.study_widget)
        study_layout.setSpacing(10)
        study_layout.setContentsMargins(16, 14, 16, 14)

        # Cabezal: Título + Usuario Activo + Insignia MIDI + Cerrar Sesión
        head_row = QHBoxLayout()
        title = QLabel("🎼 NEXO Piano Tutor")
        title.setObjectName("titleLabel")

        self.user_badge = QLabel("👤 Estudiante: —")
        self.user_badge.setStyleSheet("color: #38bdf8; font-weight: bold; font-size: 13px; background-color: #0f172a; padding: 4px 10px; border-radius: 6px; border: 1px solid #0284c7;")

        self.midi_badge = QLabel("🔌 Escaneando MIDI...")
        self.midi_badge.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold; background-color: #1e293b; padding: 4px 8px; border-radius: 4px;")

        self.logout_btn = QPushButton("🚪 Cerrar Sesión")
        self.logout_btn.setStyleSheet("background-color: #334155; color: #f8fafc; font-size: 11px; padding: 4px 8px; border-radius: 4px;")

        head_row.addWidget(title)
        head_row.addWidget(self.user_badge)
        head_row.addStretch()
        head_row.addWidget(self.midi_badge)
        head_row.addWidget(self.logout_btn)

        study_layout.addLayout(head_row)

        # Separador
        sep = QFrame()
        sep.setStyleSheet("background-color: #2d3b54;")
        sep.setFixedHeight(1)
        study_layout.addWidget(sep)

        # Selector de Lección y Repetidor Bucle xN
        lesson_group = QGroupBox("LECCIÓN, REPETICIÓN Y CURRICULUM")
        lesson_layout = QHBoxLayout(lesson_group)
        lesson_layout.addWidget(QLabel("Lección:"))
        
        self.lesson_combo = QComboBox()
        lesson_layout.addWidget(self.lesson_combo, stretch=2)

        lesson_layout.addWidget(QLabel("Bucle:"))
        self.repeat_combo = QComboBox()
        self.repeat_combo.addItems(["1x (Normal)", "3x (Serie x3)", "5x (Serie x5)", "♾️ Bucle Infinito"])
        lesson_layout.addWidget(self.repeat_combo, stretch=1)

        self.reset_btn = QPushButton("🔄 Reiniciar")
        self.reset_btn.setObjectName("resetBtn")
        lesson_layout.addWidget(self.reset_btn)

        study_layout.addWidget(lesson_group)

        # Partitura Gráfica Interactiva
        sheet_group = QGroupBox("PARTITURA & GUÍA")
        sheet_layout = QVBoxLayout(sheet_group)
        
        self.sheet_view = SheetView()
        sheet_layout.addWidget(self.sheet_view)

        study_layout.addWidget(sheet_group, stretch=1)

        # Teclado Virtual Interactivo (Piano Roll)
        piano_group = QGroupBox("TECLADO DE PIANO INTERACTIVO")
        piano_layout = QVBoxLayout(piano_group)
        self.piano_keyboard = PianoKeyboard(start_note=36, end_note=84)
        piano_layout.addWidget(self.piano_keyboard)

        study_layout.addWidget(piano_group)

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

        study_layout.addWidget(feedback_group)
        self.stacked_widget.addWidget(self.study_widget)

    # ── Señales y Slots ────────────────────────────────────────────

    def _connect_signals(self):
        # Autenticación y Cierre de Sesión
        self.login_widget.authenticated.connect(self._on_user_authenticated)
        self.logout_btn.clicked.connect(self._on_logout_clicked)

        self.lesson_combo.currentIndexChanged.connect(self._on_lesson_changed)
        self.repeat_combo.currentIndexChanged.connect(self._on_repeat_mode_changed)
        self.reset_btn.clicked.connect(self._on_reset_clicked)
        self.piano_keyboard.note_pressed.connect(self._on_note_played)
        self.piano_keyboard.note_released.connect(self.sound_engine.stop_note)

        # Captura de Teclado Físico (Samson Carbon 49)
        self.midi_input.note_played.connect(self._on_note_played)
        self.midi_input.note_released.connect(self.sound_engine.stop_note)
        self.midi_input.device_connected.connect(self._on_midi_device_connected)
        self.midi_input.device_disconnected.connect(self._on_midi_device_disconnected)

        # Auto-conectar al inicio
        success, msg = self.midi_input.auto_connect()
        if success:
            dev_name = self.midi_input.connected_device_name
            self._on_midi_device_connected(dev_name)
        else:
            self._on_midi_device_disconnected()

    def _on_user_authenticated(self, user: User):
        """Maneja el ingreso de un estudiante autenticado."""
        self.user_badge.setText(f"👤 Estudiante: {user.username}")
        self.stacked_widget.setCurrentIndex(1)
        
        # Cargar lección preferida del usuario
        active_id = user.active_lesson_id
        for idx in range(self.lesson_combo.count()):
            fpath = self.lesson_combo.itemData(idx)
            if fpath and active_id in fpath:
                self.lesson_combo.setCurrentIndex(idx)
                break

        self.statusBar().showMessage(f"Sesión activa: {user.username} | Precisión: {user.stats.accuracy_pct}%")

    def _on_logout_clicked(self):
        """Cierra la sesión y vuelve a la pantalla de Login."""
        self.user_manager.logout()
        self.user_badge.setText("👤 Estudiante: —")
        self.login_widget.refresh_user_list()
        self.stacked_widget.setCurrentIndex(0)
        self.statusBar().showMessage("Sesión cerrada. Por favor selecciona un estudiante.")

    def _on_midi_device_connected(self, device_name: str):
        display_name = device_name if device_name else "Teclado MIDI"
        self.midi_badge.setText(f"🎹 {display_name}")
        self.midi_badge.setStyleSheet("color: #00e676; font-size: 11px; font-weight: bold; background-color: #064e3b; padding: 4px 8px; border-radius: 4px;")
        self.statusBar().showMessage(f"Teclado MIDI conectado: {display_name} | Audio: {self.sound_engine.active_driver}")

    def _on_midi_device_disconnected(self):
        self.midi_badge.setText("⌨️ Teclado Virtual Activo (Sin MIDI Físico)")
        self.midi_badge.setStyleSheet("color: #38bdf8; font-size: 11px; font-weight: bold; background-color: #0c4a6e; padding: 4px 8px; border-radius: 4px;")

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

    def _on_repeat_mode_changed(self, index: int):
        modes = ["1x", "3x", "5x", "loop"]
        mode = modes[index] if 0 <= index < len(modes) else "1x"
        self.evaluator.set_repeat_mode(mode)
        self.sheet_view.set_step(self.evaluator.current_step)
        self._update_target_display()

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
                    instrument=data.get("instrument", 0),
                    notes=notes
                )
                self.evaluator.load_lesson(lesson)
                self.sound_engine.set_instrument(lesson.instrument)
                self.sheet_view.load_lesson(lesson, 0)
                self._update_target_display()

                # Guardar lección activa en el perfil del usuario
                user = self.user_manager.get_active_user()
                if user:
                    user.active_lesson_id = lesson.id
                    self.user_manager.save()
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

        # Reproducir nota por audio mediante SoundEngine
        self.sound_engine.play_note(note, velocity)

        self.sheet_view.set_step(self.evaluator.current_step)
        self._update_target_display()

        # Registrar progreso en el User Manager
        if self.evaluator.current_lesson:
            self.user_manager.record_progress(
                lesson_id=self.evaluator.current_lesson.id,
                completed=self.evaluator.is_finished,
                notes_played=1,
                correct=result.is_correct_note
            )

        if self.evaluator.is_finished:
            self.statusBar().showMessage("¡Serie de repeticiones completada con éxito!")

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
        self.midi_input.disconnect()
        self.sound_engine.cleanup()
        super().closeEvent(event)
