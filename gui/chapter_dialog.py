"""
Diálogo / Explorador Pedagógico por Capítulos para NEXO Piano Tutor.
Permite navegar por Capítulo I, II y III, consultar objetivos pedagógicos,
ver estadísticas de avance por módulo y cargar cualquier lección de la biblioteca.
"""

from typing import Optional, Callable
from PySide6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QProgressBar, QTabWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

from core.chapters import CHAPTERS, ChapterInfo
from core.user_manager import User


class ChapterDialog(QDialog):
    """Diálogo explorador interactivo de los Capítulos Pedagógicos y Lecciones."""

    def __init__(self, user: Optional[User], on_select_lesson: Callable[[str], None], parent=None):
        super().__init__(parent)
        self.setWindowTitle("📚 Explorador de Capítulos Pedagógicos — NEXO Piano Tutor")
        self.setMinimumSize(820, 620)
        self.resize(880, 680)

        self._user = user
        self._on_select_lesson = on_select_lesson
        self.selected_lesson_id: Optional[str] = None

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        # Header Title
        title_row = QHBoxLayout()
        icon_label = QLabel("📚")
        icon_label.setFont(QFont("Segoe UI Emoji", 24))
        
        t_box = QVBoxLayout()
        t_main = QLabel("Navegador Pedagógico de Capítulos")
        t_main.setStyleSheet("font-size: 20px; font-weight: bold; color: #38bdf8;")
        t_sub = QLabel("Formación Clásica Progresiva: Beyer, Bartók, Bach & Clementi (30 Lecciones)")
        t_sub.setStyleSheet("font-size: 12px; color: #94a3b8;")
        t_box.addWidget(t_main)
        t_box.addWidget(t_sub)

        title_row.addWidget(icon_label)
        title_row.addLayout(t_box)
        title_row.addStretch()

        layout.addLayout(title_row)

        # Separador
        sep = QFrame()
        sep.setStyleSheet("background-color: #1f293d;")
        sep.setFixedHeight(1)
        layout.addWidget(sep)

        # Tabs por Capítulo
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #1f293d;
                border-radius: 8px;
                background-color: #0b0f19;
            }
            QTabBar::tab {
                background-color: #111827;
                color: #94a3b8;
                border: 1px solid #1f293d;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 4px;
            }
            QTabBar::tab:selected {
                background-color: #0284c7;
                color: #ffffff;
                border-color: #0284c7;
            }
            QTabBar::tab:hover:!selected {
                background-color: #1e293b;
                color: #38bdf8;
            }
        """)

        for ch in CHAPTERS:
            tab_widget = self._create_chapter_tab(ch)
            self.tabs.addTab(tab_widget, f"{ch.icon} {ch.short_title}")

        layout.addWidget(self.tabs, stretch=1)

        # Footer Actions
        footer = QHBoxLayout()
        close_btn = QPushButton("Cerrar")
        close_btn.setStyleSheet("background-color: #334155; color: white; font-weight: bold; padding: 6px 16px; border-radius: 6px;")
        close_btn.clicked.connect(self.accept)
        
        footer.addStretch()
        footer.addWidget(close_btn)
        layout.addLayout(footer)

    def _create_chapter_tab(self, ch: ChapterInfo) -> QWidget:
        widget = QWidget()
        w_layout = QVBoxLayout(widget)
        w_layout.setContentsMargins(14, 12, 14, 12)
        w_layout.setSpacing(10)

        # Chapter Header Banner
        banner = QFrame()
        banner.setStyleSheet("background-color: #111827; border: 1px solid #1f293d; border-radius: 8px; padding: 10px;")
        b_layout = QVBoxLayout(banner)
        b_layout.setSpacing(4)

        b_title = QLabel(f"{ch.icon} {ch.title}")
        b_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #38bdf8;")

        b_level = QLabel(f"🎯 Nivel: {ch.level}")
        b_level.setStyleSheet("font-size: 11px; font-weight: bold; color: #fbbf24;")

        b_desc = QLabel(ch.description)
        b_desc.setWordWrap(True)
        b_desc.setStyleSheet("font-size: 12px; color: #cbd5e1;")

        b_layout.addWidget(b_title)
        b_layout.addWidget(b_level)
        b_layout.addWidget(b_desc)

        # Calcular Estadísticas de Avance del Capítulo
        total_lessons = len(ch.lesson_ids)
        completed_count = 0

        if self._user and hasattr(self._user, "completed_lessons"):
            for lid in ch.lesson_ids:
                if lid in self._user.completed_lessons:
                    completed_count += 1

        pct_completed = int((completed_count / max(1, total_lessons)) * 100)

        p_row = QHBoxLayout()
        p_label = QLabel(f"Avance del Capítulo: {completed_count}/{total_lessons} lecciones completadas ({pct_completed}%)")
        p_label.setStyleSheet("font-size: 11px; color: #00e676; font-weight: bold;")
        
        p_bar = QProgressBar()
        p_bar.setRange(0, 100)
        p_bar.setValue(pct_completed)
        p_bar.setFixedHeight(10)
        p_bar.setStyleSheet("""
            QProgressBar {
                background-color: #0f172a;
                border: 1px solid #1f293d;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #00e676;
                border-radius: 4px;
            }
        """)

        p_row.addWidget(p_label)
        b_layout.addLayout(p_row)
        b_layout.addWidget(p_bar)

        w_layout.addWidget(banner)

        # Lista de Lecciones Scrollable
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 4, 0, 4)
        scroll_layout.setSpacing(6)

        # Cargar tarjetas de cada lección del capítulo
        import os, json
        CARPETA_SCRIPT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        LESSONS_DIR = os.path.join(CARPETA_SCRIPT, "lessons")

        for idx, lid in enumerate(ch.lesson_ids, 1):
            fpath = os.path.join(LESSONS_DIR, f"{lid}.json")
            if os.path.exists(fpath):
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        card = self._create_lesson_card(idx, lid, data, fpath)
                        scroll_layout.addWidget(card)
                except Exception:
                    pass

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        w_layout.addWidget(scroll, stretch=1)

        return widget

    def _create_lesson_card(self, num: int, lid: str, data: dict, fpath: str) -> QFrame:
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #0f172a;
                border: 1px solid #1f293d;
                border-radius: 6px;
                padding: 6px;
            }
            QFrame:hover {
                border-color: #0284c7;
                background-color: #141f36;
            }
        """)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(8, 4, 8, 4)

        # Badge número
        num_lbl = QLabel(f"L.{num}")
        num_lbl.setStyleSheet("font-size: 12px; font-weight: bold; color: #38bdf8; background-color: #1e293b; padding: 4px 8px; border-radius: 4px;")
        layout.addWidget(num_lbl)

        # Info lección
        vbox = QVBoxLayout()
        vbox.setSpacing(2)

        t_str = f"{data.get('composer', '')} — {data.get('title', '')}"
        title_lbl = QLabel(t_str)
        title_lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #f8fafc;")

        clef = "Clave de Sol" if data.get("clef") == "treble" else "Clave de Fa"
        bpm = data.get("bpm_recommended", 60)
        sub_str = f"{clef} | {data.get('opus', '')} | ⏱️ {bpm} BPM | {data.get('description', '')[:75]}..."
        sub_lbl = QLabel(sub_str)
        sub_lbl.setStyleSheet("font-size: 11px; color: #94a3b8;")

        vbox.addWidget(title_lbl)
        vbox.addWidget(sub_lbl)
        layout.addLayout(vbox, stretch=1)

        # Estado de Usuario
        status_lbl = QLabel("📖 Por estudiar")
        status_lbl.setStyleSheet("font-size: 11px; font-weight: bold; color: #64748b; background-color: #1e293b; padding: 3px 6px; border-radius: 4px;")

        if self._user and hasattr(self._user, "completed_lessons") and lid in self._user.completed_lessons:
            status_lbl.setText("🌟 Completada")
            status_lbl.setStyleSheet("font-size: 11px; font-weight: bold; color: #00e676; background-color: #064e3b; padding: 3px 6px; border-radius: 4px;")

        layout.addWidget(status_lbl)

        # Botón Cargar
        load_btn = QPushButton("▶ Cargar")
        load_btn.setStyleSheet("background-color: #0284c7; color: white; font-weight: bold; padding: 4px 10px; border-radius: 4px;")
        load_btn.clicked.connect(lambda: self._select_and_close(fpath))
        layout.addWidget(load_btn)

        return card

    def _select_and_close(self, fpath: str):
        self.selected_lesson_id = fpath
        if self._on_select_lesson:
            self._on_select_lesson(fpath)
        self.accept()
