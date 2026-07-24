"""
Ventana Principal de NEXO Piano Tutor (v1.1.0).
Integra:
1. Pantalla de Autenticación / Selección de Estudiante (LoginWidget).
2. Control de Transporte Completo (▶ Iniciar, ⏸ Pausar, ⏹ Detener, 🔄 Reiniciar, ⏮/⏭ Pasos).
3. Metrónomo Visual Interactivo (BPM SpinBox, Indicadores de Pulso LEDs 1..4).
4. Práctica por Secciones (Rango A-B con destaque en partitura).
5. Renderizador de Partitura Interactivo (SheetView) y Teclado Virtual (PianoKeyboard).
6. Evaluador en Tiempo Real (<15ms) y Motor de Audio (SoundEngine).
"""

import os
import time
import json
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QComboBox, QLabel, QPushButton, QFrame,
    QStackedWidget, QStatusBar, QSpinBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from core.lesson import Lesson, TargetNote
from core.evaluator import RealtimeEvaluator
from core.midi_input import MidiInputHandler
from core.sound_engine import SoundEngine
from core.user_manager import UserManager, User
from core.theory_cards import get_theory_card
from gui.sheet_view import SheetView, midi_to_note_name
from gui.piano_keyboard import PianoKeyboard
from gui.login_widget import LoginWidget
from gui.theory_dialog import TheoryDialog, LibraryDialog
from gui.dashboard_dialog import DashboardDialog

CARPETA_SCRIPT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LESSONS_DIR = os.path.join(CARPETA_SCRIPT, "lessons")


class MainWindow(QMainWindow):
    """Ventana principal de la app pedagógica NEXO Piano Tutor."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎼 NEXO Piano Tutor — Formación Clásica")
        self.setMinimumSize(780, 840)
        self.resize(840, 890)

        # Gestor de Usuarios, Evaluador, Entrada MIDI física y Motor Audio
        self.user_manager = UserManager()
        self.evaluator = RealtimeEvaluator()
        self.midi_input = MidiInputHandler(self)
        self.sound_engine = SoundEngine()

        # Timer de Metrónomo y estado de reproducción
        self.metronome_timer = QTimer(self)
        self.metronome_timer.timeout.connect(self._on_metronome_tick)
        self._is_playing = False
        self._is_countdown = False
        self._countdown_count = 4
        self._metronome_beat = 0
        self._in_countdown_evaluation_paused = False
        self._is_finishing_lesson = False
        self._last_beat_timestamp = 0.0

        self._build_ui()
        self._connect_signals()
        self._load_available_lessons()

        # Verificar si hay usuario activo previamente autenticado
        active_user = self.user_manager.get_active_user()
        if active_user:
            self._on_user_authenticated(active_user)
        else:
            self.stacked_widget.setCurrentIndex(0)

        self.statusBar().showMessage(f"NEXO Piano Tutor v1.1.0 — Audio: {self.sound_engine.active_driver}")

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
        study_layout.setSpacing(6)
        study_layout.setContentsMargins(14, 10, 14, 10)

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

        # Panel 1: LECCIÓN, MODO Y BIBLIOTECA
        lesson_group = QGroupBox("LECCIÓN, MODO Y BIBLIOTECA")
        lesson_layout = QHBoxLayout(lesson_group)
        lesson_layout.setContentsMargins(10, 6, 10, 6)

        lesson_layout.addWidget(QLabel("Lección:"))
        self.lesson_combo = QComboBox()
        lesson_layout.addWidget(self.lesson_combo, stretch=2)

        lesson_layout.addWidget(QLabel("Modo:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "📖 Lectura (Sin tiempo)",
            "⏱️ Tiempo (Metrónomo)",
            "🎭 Expresión (Integración)"
        ])
        lesson_layout.addWidget(self.mode_combo, stretch=1)

        lesson_layout.addWidget(QLabel("Bucle:"))
        self.repeat_combo = QComboBox()
        self.repeat_combo.addItems(["1x (Normal)", "3x (Serie x3)", "5x (Serie x5)", "♾️ Bucle Infinito"])
        lesson_layout.addWidget(self.repeat_combo, stretch=1)

        self.dashboard_btn = QPushButton("📊 Bitácora")
        self.dashboard_btn.setStyleSheet("background-color: #16a34a; color: white; font-weight: bold; padding: 5px 10px; border-radius: 4px;")
        lesson_layout.addWidget(self.dashboard_btn)

        self.theory_btn = QPushButton("📖 Teoría")
        self.theory_btn.setStyleSheet("background-color: #0284c7; color: white; font-weight: bold; padding: 5px 10px; border-radius: 4px;")
        lesson_layout.addWidget(self.theory_btn)

        self.library_btn = QPushButton("🏛️ Biblioteca")
        self.library_btn.setStyleSheet("background-color: #1e293b; color: #38bdf8; font-weight: bold; border: 1px solid #0284c7; padding: 5px 10px; border-radius: 4px;")
        lesson_layout.addWidget(self.library_btn)

        study_layout.addWidget(lesson_group)

        # Panel 2: CONTROL DE TRANSPORTE, METRÓNOMO VISUAL Y SECCIÓN A-B
        control_group = QGroupBox("CONTROL DE REPRODUCCIÓN, METRÓNOMO VISUAL Y PRÁCTICA SECCIÓN (A-B)")
        control_layout = QVBoxLayout(control_group)
        control_layout.setContentsMargins(10, 6, 10, 6)
        control_layout.setSpacing(6)

        # Fila A: Botonera de Transporte (Play, Pause, Stop, Reset, Prev, Next)
        transport_row = QHBoxLayout()

        self.play_btn = QPushButton("▶ INICIAR LECCIÓN")
        self.play_btn.setStyleSheet("background-color: #0284c7; color: white; font-size: 13px; font-weight: bold; padding: 6px 16px; border-radius: 6px;")

        self.pause_btn = QPushButton("⏸ Pausar")
        self.pause_btn.setStyleSheet("background-color: #d97706; color: white; font-weight: bold; padding: 6px 12px; border-radius: 6px;")

        self.stop_btn = QPushButton("⏹ Detener")
        self.stop_btn.setStyleSheet("background-color: #dc2626; color: white; font-weight: bold; padding: 6px 12px; border-radius: 6px;")

        self.reset_btn = QPushButton("🔄 Reiniciar")
        self.reset_btn.setStyleSheet("background-color: #475569; color: white; font-weight: bold; padding: 6px 12px; border-radius: 6px;")

        self.step_prev_btn = QPushButton("⏮ Nota Anterior")
        self.step_prev_btn.setStyleSheet("background-color: #1e293b; color: #cbd5e1; font-weight: bold; padding: 6px 10px; border-radius: 6px; border: 1px solid #334155;")

        self.step_next_btn = QPushButton("⏭ Nota Siguiente")
        self.step_next_btn.setStyleSheet("background-color: #1e293b; color: #cbd5e1; font-weight: bold; padding: 6px 10px; border-radius: 6px; border: 1px solid #334155;")

        transport_row.addWidget(self.play_btn)
        transport_row.addWidget(self.pause_btn)
        transport_row.addWidget(self.stop_btn)
        transport_row.addWidget(self.reset_btn)
        transport_row.addSpacing(10)
        transport_row.addWidget(self.step_prev_btn)
        transport_row.addWidget(self.step_next_btn)
        transport_row.addStretch()

        control_layout.addLayout(transport_row)

        # Fila B: Metrónomo Visual & BPM + Selección de Rango A-B
        tools_row = QHBoxLayout()

        # Metrónomo & BPM Selector
        bpm_box = QHBoxLayout()
        bpm_label = QLabel("⏱️ Metrónomo BPM:")
        bpm_label.setStyleSheet("color: #38bdf8; font-weight: bold;")
        bpm_box.addWidget(bpm_label)

        self.bpm_spin = QSpinBox()
        self.bpm_spin.setRange(30, 240)
        self.bpm_spin.setValue(60)
        self.bpm_spin.setFixedWidth(65)
        self.bpm_spin.setStyleSheet("background-color: #0f172a; color: #00e676; font-size: 13px; font-weight: bold; padding: 3px; border: 1px solid #0284c7; border-radius: 4px;")
        bpm_box.addWidget(self.bpm_spin)

        btn_minus5 = QPushButton("-5")
        btn_minus5.setFixedWidth(30)
        btn_minus5.setStyleSheet("background-color: #334155; color: white; font-weight: bold;")
        btn_minus5.clicked.connect(lambda: self.bpm_spin.setValue(self.bpm_spin.value() - 5))

        btn_plus5 = QPushButton("+5")
        btn_plus5.setFixedWidth(30)
        btn_plus5.setStyleSheet("background-color: #334155; color: white; font-weight: bold;")
        btn_plus5.clicked.connect(lambda: self.bpm_spin.setValue(self.bpm_spin.value() + 5))

        bpm_box.addWidget(btn_minus5)
        bpm_box.addWidget(btn_plus5)

        # Indicadores Visuales de Pulso (LEDs / Cajas de Beat 1, 2, 3, 4)
        bpm_box.addSpacing(10)
        self.beat_indicators_layout = QHBoxLayout()
        self.beat_boxes: list[QLabel] = []
        for i in range(4):
            lbl = QLabel(f" {i+1} ")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFixedSize(26, 26)
            lbl.setFont(QFont("Consolas", 10, QFont.Weight.Bold))
            lbl.setStyleSheet("background-color: #0f172a; color: #64748b; border: 1px solid #334155; border-radius: 4px;")
            self.beat_boxes.append(lbl)
            self.beat_indicators_layout.addWidget(lbl)

        bpm_box.addLayout(self.beat_indicators_layout)
        tools_row.addLayout(bpm_box)

        # Separador vertical
        vsep_tools = QFrame()
        vsep_tools.setFrameShape(QFrame.Shape.VLine)
        vsep_tools.setStyleSheet("background-color: #334155;")
        tools_row.addWidget(vsep_tools)

        # Práctica de Sección (Rango A-B)
        range_box = QHBoxLayout()
        r_label = QLabel("🎯 Rango A-B:")
        r_label.setStyleSheet("color: #fbbf24; font-weight: bold;")
        range_box.addWidget(r_label)

        range_box.addWidget(QLabel("Desde (A):"))
        self.range_start_spin = QSpinBox()
        self.range_start_spin.setRange(1, 99)
        self.range_start_spin.setValue(1)
        self.range_start_spin.setFixedWidth(50)
        self.range_start_spin.setStyleSheet("background-color: #0f172a; color: #f8fafc; font-weight: bold; border: 1px solid #d97706; border-radius: 4px;")
        range_box.addWidget(self.range_start_spin)

        range_box.addWidget(QLabel("Hasta (B):"))
        self.range_end_spin = QSpinBox()
        self.range_end_spin.setRange(1, 99)
        self.range_end_spin.setValue(10)
        self.range_end_spin.setFixedWidth(50)
        self.range_end_spin.setStyleSheet("background-color: #0f172a; color: #f8fafc; font-weight: bold; border: 1px solid #d97706; border-radius: 4px;")
        range_box.addWidget(self.range_end_spin)

        self.apply_range_btn = QPushButton("🎯 Fijar Rango")
        self.apply_range_btn.setStyleSheet("background-color: #d97706; color: white; font-weight: bold; padding: 4px 8px; border-radius: 4px;")

        self.reset_range_btn = QPushButton("🔄 Toda la Partitura")
        self.reset_range_btn.setStyleSheet("background-color: #1e293b; color: #fbbf24; font-weight: bold; border: 1px solid #d97706; padding: 4px 8px; border-radius: 4px;")

        range_box.addWidget(self.apply_range_btn)
        range_box.addWidget(self.reset_range_btn)

        tools_row.addLayout(range_box)

        # Separador vertical y Botón de Unión Rítmica (Beaming)
        vsep_beam = QFrame()
        vsep_beam.setFrameShape(QFrame.Shape.VLine)
        vsep_beam.setStyleSheet("background-color: #334155;")
        tools_row.addWidget(vsep_beam)

        self.beaming_btn = QPushButton("🔗 Unidas (Beams)")
        self.beaming_btn.setStyleSheet("background-color: #0284c7; color: white; font-weight: bold; padding: 4px 8px; border-radius: 4px;")
        tools_row.addWidget(self.beaming_btn)

        control_layout.addLayout(tools_row)

        study_layout.addWidget(control_group)

        # Partitura Gráfica Interactiva
        sheet_group = QGroupBox("PARTITURA & GUÍA DE LECTURA")
        sheet_layout = QVBoxLayout(sheet_group)

        self.sheet_view = SheetView()
        sheet_layout.addWidget(self.sheet_view)

        study_layout.addWidget(sheet_group, stretch=3)

        # Teclado Virtual Interactivo (Piano Roll)
        piano_group = QGroupBox("TECLADO DE PIANO INTERACTIVO")
        piano_group.setFixedHeight(140)
        piano_layout = QVBoxLayout(piano_group)
        piano_layout.setContentsMargins(6, 6, 6, 6)
        self.piano_keyboard = PianoKeyboard(start_note=36, end_note=84)
        piano_layout.addWidget(self.piano_keyboard)

        study_layout.addWidget(piano_group, stretch=0)

        # Panel de Feedback Pedagógico (Dedos + Veredicto)
        feedback_group = QGroupBox("GUÍA DE DIGITACIÓN & EVALUACIÓN EN TIEMPO REAL")
        feedback_group.setFixedHeight(95)
        fb_layout = QHBoxLayout(feedback_group)
        fb_layout.setContentsMargins(10, 4, 10, 4)

        finger_col = QVBoxLayout()
        finger_label = QLabel("DEDO")
        finger_label.setObjectName("subtitleLabel")
        finger_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        finger_col.addWidget(finger_label)

        self.finger_val = QLabel("—")
        self.finger_val.setObjectName("fingerLabel")
        finger_col.addWidget(self.finger_val)

        fb_layout.addLayout(finger_col)

        vsep = QFrame()
        vsep.setFrameShape(QFrame.Shape.VLine)
        vsep.setStyleSheet("background-color: #2d3b54;")
        fb_layout.addWidget(vsep)

        fb_col = QVBoxLayout()
        fb_text_label = QLabel("Retroalimentación Pedagógica")
        fb_text_label.setObjectName("subtitleLabel")
        fb_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fb_col.addWidget(fb_text_label)

        self.feedback_val = QLabel("Presiona ▶ INICIAR LECCIÓN para comenzar")
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
        self.mode_combo.currentIndexChanged.connect(self._on_study_mode_changed)
        self.repeat_combo.currentIndexChanged.connect(self._on_repeat_mode_changed)

        # Botonera de Transporte
        self.play_btn.clicked.connect(self._on_play_clicked)
        self.pause_btn.clicked.connect(self._on_pause_clicked)
        self.stop_btn.clicked.connect(self._on_stop_clicked)
        self.reset_btn.clicked.connect(self._on_reset_clicked)
        self.step_prev_btn.clicked.connect(self._on_step_prev_clicked)
        self.step_next_btn.clicked.connect(self._on_step_next_clicked)

        # Metrónomo & Rango A-B & Unión Rítmica (Beaming)
        self.bpm_spin.valueChanged.connect(self._on_bpm_changed)
        self.apply_range_btn.clicked.connect(self._on_apply_range_clicked)
        self.reset_range_btn.clicked.connect(self._on_reset_range_clicked)
        self.beaming_btn.clicked.connect(self._on_toggle_beaming)

        self.dashboard_btn.clicked.connect(self._show_dashboard_dialog)
        self.theory_btn.clicked.connect(self._show_theory_dialog)
        self.library_btn.clicked.connect(self._show_library_dialog)

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

    def _show_dashboard_dialog(self):
        user = self.user_manager.get_active_user()
        if user:
            dlg = DashboardDialog(user, self)
            dlg.exec()

    def _show_theory_dialog(self):
        if not self.evaluator.current_lesson:
            return
        card = get_theory_card(self.evaluator.current_lesson.id)
        if card:
            dlg = TheoryDialog(card, self)
            dlg.exec()
        else:
            self.statusBar().showMessage(f"No hay tarjeta teórica registrada para {self.evaluator.current_lesson.title}")

    def _show_library_dialog(self):
        dlg = LibraryDialog(self)
        dlg.exec()

    def _on_user_authenticated(self, user: User):
        self.user_badge.setText(f"👤 Estudiante: {user.username}")
        self.stacked_widget.setCurrentIndex(1)
        
        active_id = user.active_lesson_id
        for idx in range(self.lesson_combo.count()):
            fpath = self.lesson_combo.itemData(idx)
            if fpath and active_id in fpath:
                self.lesson_combo.setCurrentIndex(idx)
                break

        self.statusBar().showMessage(f"Sesión activa: {user.username} | Precisión: {user.stats.accuracy_pct}%")

    def _on_logout_clicked(self):
        self._stop_metronome()
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

    # ── Lógica de Transporte y Metrónomo ──────────────────────────

    def _on_play_clicked(self):
        """Inicia la lección evaluando el modo activo."""
        if not self.evaluator.current_lesson:
            return

        self._is_playing = True
        self.play_btn.setText("▶ EN EJECUCIÓN")
        self.play_btn.setStyleSheet("background-color: #16a34a; color: white; font-size: 13px; font-weight: bold; padding: 6px 16px; border-radius: 6px;")

        # El metrónomo solo se activa en Modo Tiempo y Expresión (en Modo Lectura es cero presión)
        if self.evaluator.mode in ("tempo", "full"):
            self._start_metronome_and_countdown()
        else:
            self._stop_metronome()
            self._in_countdown_evaluation_paused = False
            target = self.evaluator.get_current_target()
            target_name = midi_to_note_name(target.midi_note) if target else ""
            self.feedback_val.setText(f"📖 Modo Lectura — Tocá la nota iluminada (Dedo {target.finger if target else '-'} / {target_name})")
            self.feedback_val.setStyleSheet("color: #38bdf8; font-size: 14px; font-weight: bold;")

    def _on_pause_clicked(self):
        """Pausa el metrónomo y detiene la evaluación sin reiniciar el paso."""
        self._is_playing = False
        self.metronome_timer.stop()
        self.play_btn.setText("▶ CONTINUAR")
        self.play_btn.setStyleSheet("background-color: #0284c7; color: white; font-size: 13px; font-weight: bold; padding: 6px 16px; border-radius: 6px;")
        self.feedback_val.setText("⏸ Lección Pausada")
        self.feedback_val.setStyleSheet("color: #fbbf24; font-weight: bold;")
        self._clear_beat_highlights()

    def _on_stop_clicked(self):
        """Detiene el metrónomo y vuelve la posición al inicio del rango de práctica."""
        self._is_finishing_lesson = False
        self._is_playing = False
        self._stop_metronome()
        self.evaluator.reset()
        self.sheet_view.set_error_steps(self.evaluator.steps_with_errors)
        self.sheet_view.set_note_results(self.evaluator.note_results)
        self.sheet_view.set_step(self.evaluator.current_step)
        self._update_target_display()
        self.play_btn.setText("▶ INICIAR LECCIÓN")
        self.play_btn.setStyleSheet("background-color: #0284c7; color: white; font-size: 13px; font-weight: bold; padding: 6px 16px; border-radius: 6px;")
        self.feedback_val.setText("⏹ Lección Detenida — Listo para Iniciar")
        self.feedback_val.setStyleSheet("color: #94a3b8;")

    def _on_reset_clicked(self):
        """Reinicia la lección desde el inicio del rango y reactiva el estado de ejecución."""
        self._is_finishing_lesson = False
        self.evaluator.reset()
        self.sheet_view.set_error_steps(self.evaluator.steps_with_errors)
        self.sheet_view.set_note_results(self.evaluator.note_results)
        self._is_playing = True
        self.play_btn.setText("▶ EN EJECUCIÓN")
        self.play_btn.setStyleSheet("background-color: #16a34a; color: white; font-size: 13px; font-weight: bold; padding: 6px 16px; border-radius: 6px;")

        if self.evaluator.current_lesson:
            self.sheet_view.set_step(self.evaluator.range_start)
            self._update_target_display()
            self.statusBar().showMessage("Lección reiniciada al inicio del rango")
            if self.evaluator.mode in ("tempo", "full"):
                self._start_metronome_and_countdown()
            else:
                self._stop_metronome()
                self._in_countdown_evaluation_paused = False
                target = self.evaluator.get_current_target()
                target_name = midi_to_note_name(target.midi_note) if target else ""
                self.feedback_val.setText(f"📖 Modo Lectura — Tocá la nota iluminada (Dedo {target.finger if target else '-'} / {target_name})")
                self.feedback_val.setStyleSheet("color: #38bdf8; font-size: 14px; font-weight: bold;")

    def _on_step_prev_clicked(self):
        """Retrocede manualmente 1 nota."""
        if self.evaluator.current_step > self.evaluator.range_start:
            self.evaluator.current_step -= 1
            self.sheet_view.set_step(self.evaluator.current_step)
            self._update_target_display()

    def _on_step_next_clicked(self):
        """Avanza manualmente 1 nota."""
        if self.evaluator.current_step < self.evaluator.range_end:
            self.evaluator.current_step += 1
            self.sheet_view.set_step(self.evaluator.current_step)
            self._update_target_display()

    def _on_bpm_changed(self, value: int):
        """Actualiza el tempo del metrónomo en tiempo real."""
        if self.metronome_timer.isActive():
            interval_ms = int((60.0 / max(30, min(240, value))) * 1000)
            self.metronome_timer.setInterval(interval_ms)

    def _on_study_mode_changed(self, index: int):
        modes = ["read", "tempo", "full"]
        if 0 <= index < len(modes):
            mode = modes[index]
            self.evaluator.mode = mode
            if self._is_playing and mode in ("tempo", "full"):
                self._start_metronome_and_countdown()
            else:
                self._stop_metronome()

    def _start_metronome_and_countdown(self):
        """Inicia el metrónomo y la cuenta regresiva previa de 4 pulsos."""
        self.metronome_timer.stop()
        bpm = self.bpm_spin.value()
        interval_ms = int((60.0 / max(30, min(240, bpm))) * 1000)
        self.metronome_timer.setInterval(interval_ms)

        self._is_countdown = True
        self._countdown_count = 4
        self._metronome_beat = 0
        self._in_countdown_evaluation_paused = True

        self.feedback_val.setText("⏱️ ¡Preparados! Cuenta Regresiva: 4...")
        self.feedback_val.setStyleSheet("color: #fbbf24; font-size: 14px; font-weight: bold;")
        self.metronome_timer.start()

    def _stop_metronome(self):
        """Detiene el metrónomo y reinicia el estado de conteo."""
        self.metronome_timer.stop()
        self._is_countdown = False
        self._in_countdown_evaluation_paused = False
        self._metronome_beat = 0
        self._clear_beat_highlights()

    def _clear_beat_highlights(self):
        for idx, lbl in enumerate(self.beat_boxes):
            lbl.setStyleSheet("background-color: #0f172a; color: #64748b; border: 1px solid #334155; border-radius: 4px;")

    def _on_metronome_tick(self):
        """Maneja cada pulso del timer de metrónomo (Audio + Animación Visual LED)."""
        lesson = self.evaluator.current_lesson
        ts_str = getattr(lesson, "time_signature", "4/4") if lesson else "4/4"
        try:
            beats_per_measure = int(ts_str.split("/")[0])
        except Exception:
            beats_per_measure = 4

        self._last_beat_timestamp = time.time() * 1000.0
        if self._is_countdown:
            is_downbeat = (self._countdown_count == 4)
            self.sound_engine.play_metronome_click(is_downbeat)

            # Destacar visualmente la luz del pulso actual en la cuenta regresiva
            beat_idx = (4 - self._countdown_count) % len(self.beat_boxes)
            self._highlight_beat_box(beat_idx, is_downbeat)

            colors = {4: "#fbbf24", 3: "#f59e0b", 2: "#eab308", 1: "#84cc16"}
            cur_color = colors.get(self._countdown_count, "#fbbf24")
            self.feedback_val.setText(f"⏱️ Cuenta Regresiva: {self._countdown_count}... (¡Escuchá el pulso!)")
            self.feedback_val.setStyleSheet(f"color: {cur_color}; font-size: 15px; font-weight: bold;")

            self._countdown_count -= 1
            if self._countdown_count == 0:
                self._is_countdown = False
                self._in_countdown_evaluation_paused = False
                self._metronome_beat = 0
                self.feedback_val.setText("🎵 ¡A TOCAR! Mantené el pulso constante")
                self.feedback_val.setStyleSheet("color: #00e676; font-size: 14px; font-weight: bold;")
        else:
            is_downbeat = (self._metronome_beat == 0)
            self.sound_engine.play_metronome_click(is_downbeat)
            self._highlight_beat_box(self._metronome_beat % len(self.beat_boxes), is_downbeat)
            self._metronome_beat = (self._metronome_beat + 1) % beats_per_measure

    def _highlight_beat_box(self, index: int, is_downbeat: bool):
        self._clear_beat_highlights()
        if 0 <= index < len(self.beat_boxes):
            lbl = self.beat_boxes[index]
            if is_downbeat:
                lbl.setStyleSheet("background-color: #00e676; color: #09090b; border: 2px solid #22c55e; border-radius: 4px; font-weight: bold;")
            else:
                lbl.setStyleSheet("background-color: #38bdf8; color: #09090b; border: 2px solid #0284c7; border-radius: 4px; font-weight: bold;")

    def _on_toggle_beaming(self):
        """Alterna el modo de unión de notas rítmicas (Beaming vs. Flags)."""
        new_state = not self.sheet_view._beaming_enabled
        self.sheet_view.set_beaming_enabled(new_state)
        if new_state:
            self.beaming_btn.setText("🔗 Unidas (Beams)")
            self.beaming_btn.setStyleSheet("background-color: #0284c7; color: white; font-weight: bold; padding: 4px 8px; border-radius: 4px;")
            self.statusBar().showMessage("Barras de unión rítmicas (Beaming por tiempo) activadas")
        else:
            self.beaming_btn.setText("🚩 Separadas (Flags)")
            self.beaming_btn.setStyleSheet("background-color: #334155; color: #94a3b8; font-weight: bold; padding: 4px 8px; border-radius: 4px;")
            self.statusBar().showMessage("Corchetes individuales (Flags) activados")

    # ── Lógica de Rango A-B (Sección de Práctica) ───────────────────

    def _on_apply_range_clicked(self):
        start_idx = self.range_start_spin.value() - 1
        end_idx = self.range_end_spin.value() - 1
        self.evaluator.set_range(start_idx, end_idx)
        self.sheet_view.set_range(self.evaluator.range_start, self.evaluator.range_end)
        self.sheet_view.set_step(self.evaluator.current_step)
        self._update_target_display()
        self.statusBar().showMessage(f"Rango A-B fijado: Notas {start_idx + 1} a {end_idx + 1}")

    def _on_reset_range_clicked(self):
        if self.evaluator.current_lesson and self.evaluator.current_lesson.notes:
            total = len(self.evaluator.current_lesson.notes)
            self.range_start_spin.setValue(1)
            self.range_end_spin.setValue(total)
            self.evaluator.set_range(0, total - 1)
            self.sheet_view.set_range(0, total - 1)
            self.sheet_view.set_step(0)
            self._update_target_display()
            self.statusBar().showMessage("Rango restablecido a toda la partitura")

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
                
                # Ajustar SpinBoxes de Rango
                total_notes = max(1, len(notes))
                self.range_start_spin.setRange(1, total_notes)
                self.range_end_spin.setRange(1, total_notes)
                self.range_start_spin.setValue(1)
                self.range_end_spin.setValue(total_notes)
                
                self.bpm_spin.setValue(lesson.bpm_recommended)
                self.sheet_view.load_lesson(lesson, 0)
                self.sheet_view.set_range(0, total_notes - 1)
                self._update_target_display()

                user = self.user_manager.get_active_user()
                if user:
                    user.active_lesson_id = lesson.id
                    self.user_manager.save()

                if self._is_playing and self.evaluator.mode in ("tempo", "full"):
                    self._start_metronome_and_countdown()
                else:
                    self._stop_metronome()
        except Exception as e:
            self.statusBar().showMessage(f"Error al cargar lección: {e}")

    # ── Eventos de Notas MIDI ──────────────────────────────────────

    def _on_note_played(self, note: int, velocity: int):
        # SIEMPRE emitir el sonido de la nota pulsada (Teclado siempre activo para audio)
        self.sound_engine.play_note(note, velocity)

        # Si la lección ya finalizó o está en proceso de cierre rítmico, no evaluar
        if self.evaluator.is_finished or self._is_finishing_lesson:
            return

        # Durante la cuenta regresiva previa, no evaluar avance
        if self._in_countdown_evaluation_paused:
            return

        # Capturar la nota objetivo y su duración rítmica antes de avanzar el paso
        target = self.evaluator.get_current_target()
        duration_q = getattr(target, "duration_quarter", 1.0) if target else 1.0

        # Calcular desvío rítmico en milisegundos respecto al pulso del metrónomo
        time_delta_ms = 0.0
        if self.evaluator.mode in ("tempo", "full") and self._last_beat_timestamp > 0:
            now_ms = time.time() * 1000.0
            bpm = self.bpm_spin.value()
            interval_ms = (60.0 / max(30, min(240, bpm))) * 1000.0
            elapsed = now_ms - self._last_beat_timestamp
            rem = elapsed % interval_ms
            if rem > (interval_ms / 2.0):
                time_delta_ms = rem - interval_ms
            else:
                time_delta_ms = rem

        result = self.evaluator.evaluate_note_on(note, velocity, time_delta_ms)
        self.feedback_val.setText(result.feedback_text)
        self.feedback_val.setStyleSheet(f"color: {result.feedback_color}; font-weight: bold;")

        # Si la nota fue incorrecta, iluminar la tecla equivocada en rojo carmesí en el teclado virtual
        if not result.is_correct_note:
            self.piano_keyboard.set_key_active(note, "#ef4444")
            QTimer.singleShot(450, lambda: self.piano_keyboard.clear_key_active(note))

        self.sheet_view.set_error_steps(self.evaluator.steps_with_errors)
        self.sheet_view.set_note_results(self.evaluator.note_results)
        self.sheet_view.set_step(self.evaluator.current_step)
        self._update_target_display()

        user = self.user_manager.get_active_user()
        if user and self.evaluator.current_lesson:
            self.user_manager.record_progress(
                lesson_id=self.evaluator.current_lesson.id,
                completed=self.evaluator.is_finished,
                notes_played=1,
                correct=result.is_correct_note
            )

        # Si la lección o serie se completó en este golpe
        if self.evaluator.is_finished:
            self._is_finishing_lesson = True
            bpm = self.bpm_spin.value()
            duration_ms = int(duration_q * (60.0 / max(30, min(240, bpm))) * 1000)
            duration_ms = max(500, min(6000, duration_ms))

            # Respetar el tempo completo de la última nota antes de detener metrónomo y finalizar
            QTimer.singleShot(duration_ms, lambda: self._finish_lesson(result))

    def _finish_lesson(self, result):
        """Finaliza limpiamente la lección tras cumplir la duración de la última nota."""
        if not self._is_finishing_lesson:
            return

        self._stop_metronome()
        self._is_playing = False
        self._is_finishing_lesson = False
        self.play_btn.setText("▶ INICIAR LECCIÓN")
        self.play_btn.setStyleSheet("background-color: #0284c7; color: white; font-size: 13px; font-weight: bold; padding: 6px 16px; border-radius: 6px;")

        self.feedback_val.setText(result.feedback_text)
        self.feedback_val.setStyleSheet(f"color: {result.feedback_color}; font-weight: bold;")
        self.statusBar().showMessage("¡Serie de repeticiones completada con éxito!")

        user = self.user_manager.get_active_user()
        if user and self.evaluator.current_lesson:
            acc = round((self.evaluator.correct_attempts / max(1, self.evaluator.total_attempts)) * 100, 1)
            self.user_manager.record_session_log(
                lesson_id=self.evaluator.current_lesson.id,
                mode=self.evaluator.mode,
                notes_played=self.evaluator.total_attempts,
                accuracy_pct=acc
            )

    def _update_target_display(self):
        self.piano_keyboard.clear_all_active()
        target = self.evaluator.get_current_target()
        if target:
            self.finger_val.setText(str(target.finger))
            self.piano_keyboard.set_key_active(target.midi_note, "#38bdf8")
        else:
            self.finger_val.setText("—")

    def closeEvent(self, event):
        self.midi_input.disconnect()
        self.sound_engine.cleanup()
        super().closeEvent(event)
