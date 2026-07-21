"""
Diálogo y Popup Pedagógico de Tarjetas Teóricas y Biblioteca de la Fragua (v1.0.0).
Implementa la Sección 6.2 de PEDAGOGIA_CLASICA.md.
"""

from PySide6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextBrowser, QFrame, QDialogButtonBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from core.theory_cards import TheoryCard, get_theory_card, THEORY_CARDS_DATABASE, HISTORIA_PIANO_CARD


class TheoryDialog(QDialog):
    """Diálogo de Tarjeta Teórica Introductiva por Lección."""

    def __init__(self, card: TheoryCard, parent=None):
        super().__init__(parent)
        self.card = card
        self.setWindowTitle(f"📖 {card.title}")
        self.setMinimumSize(520, 440)
        self.resize(560, 480)
        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
                color: #f8fafc;
            }
            QLabel#headerTitle {
                color: #38bdf8;
                font-size: 18px;
                font-weight: bold;
            }
            QLabel#headerSub {
                color: #94a3b8;
                font-size: 12px;
            }
            QFrame#topicBox {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 12px;
                margin-bottom: 8px;
            }
            QLabel#topicTitle {
                color: #00e676;
                font-size: 13px;
                font-weight: bold;
            }
            QLabel#topicText {
                color: #cbd5e1;
                font-size: 12px;
                line-height: 1.4;
            }
        """)

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        # Header con Ícono + Título + Subtítulo
        head_row = QHBoxLayout()
        icon_label = QLabel(self.card.icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 32))
        head_row.addWidget(icon_label)

        head_col = QVBoxLayout()
        t_label = QLabel(self.card.title)
        t_label.setObjectName("headerTitle")
        sub_label = QLabel(self.card.subtitle)
        sub_label.setObjectName("headerSub")
        head_col.addWidget(t_label)
        head_col.addWidget(sub_label)

        head_row.addLayout(head_col, stretch=1)
        layout.addLayout(head_row)

        # Separador
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #334155;")
        layout.addWidget(sep)

        # Contenido de Secciones Teóricas
        for sec in self.card.sections:
            box = QFrame()
            box.setObjectName("topicBox")
            box_layout = QVBoxLayout(box)
            box_layout.setContentsMargins(10, 8, 10, 8)
            box_layout.setSpacing(4)

            title_lbl = QLabel(sec.get("topic", ""))
            title_lbl.setObjectName("topicTitle")
            text_lbl = QLabel(sec.get("text", ""))
            text_lbl.setObjectName("topicText")
            text_lbl.setWordWrap(True)

            box_layout.addWidget(title_lbl)
            box_layout.addWidget(text_lbl)
            layout.addWidget(box)

        layout.addStretch()

        # Botón de Inicio / Entendido
        btn_row = QHBoxLayout()
        btn_start = QPushButton("▶ ¡Entendido! Empezar Lección")
        btn_start.setStyleSheet("background-color: #0284c7; color: white; font-weight: bold; padding: 10px 20px; border-radius: 6px; font-size: 13px;")
        btn_start.clicked.connect(self.accept)
        btn_row.addStretch()
        btn_row.addWidget(btn_start)
        btn_row.addStretch()

        layout.addLayout(btn_row)


class LibraryDialog(QDialog):
    """Diálogo consultable de 'La Biblioteca de la Fragua' (Glosario Teórico Completo)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🏛️ La Biblioteca de la Fragua — Glosario Teórico")
        self.setMinimumSize(600, 520)
        self.resize(650, 560)
        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
                color: #f8fafc;
            }
        """)

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("🏛️ La Biblioteca de la Fragua")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #38bdf8;")
        layout.addWidget(title)

        browser = QTextBrowser()
        browser.setStyleSheet("""
            QTextBrowser {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 14px;
                color: #cbd5e1;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
            }
        """)

        # Generar HTML del Glosario
        html = ["<h2 style='color:#00e676;'>📖 Compendio Teórico de Formación Pianística</h2>"]
        
        cards = list(THEORY_CARDS_DATABASE.values()) + [HISTORIA_PIANO_CARD]
        for card in cards:
            html.append(f"<h3 style='color:#38bdf8;'>{card.icon} {card.title}</h3>")
            html.append(f"<p style='color:#94a3b8; font-style:italic;'>{card.subtitle}</p>")
            for sec in card.sections:
                html.append(f"<h4 style='color:#f59e0b;'>{sec['topic']}</h4>")
                text_formatted = sec['text'].replace('\n', '<br>')
                html.append(f"<p>{text_formatted}</p>")
            html.append("<hr style='border:1px solid #334155;'/>")

        browser.setHtml("".join(html))
        layout.addWidget(browser)

        btn_close = QPushButton("Cerrar Biblioteca")
        btn_close.setStyleSheet("background-color: #334155; color: white; padding: 8px 16px; border-radius: 6px;")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close, alignment=Qt.AlignmentFlag.AlignRight)
