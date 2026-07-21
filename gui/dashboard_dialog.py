"""
Diálogo de Bitácora del Estudiante / Dashboard de Progreso (v1.0.0).
Implementa la Sección 6.3 de PEDAGOGIA_CLASICA.md.
"""

from PySide6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QListWidget, QListWidgetItem, QGroupBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from core.user_manager import User


class DashboardDialog(QDialog):
    """Ficha y Bitácora del Estudiante (Progreso, Precisión e Insignias)."""

    def __init__(self, user: User, parent=None):
        super().__init__(parent)
        self.user = user
        self.setWindowTitle(f"📊 Bitácora Pedagógica — {user.username}")
        self.setMinimumSize(560, 480)
        self.resize(600, 520)
        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
                color: #f8fafc;
            }
            QLabel#dashTitle {
                color: #38bdf8;
                font-size: 18px;
                font-weight: bold;
            }
            QFrame#statCard {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 12px;
            }
            QLabel#statVal {
                color: #00e676;
                font-size: 22px;
                font-weight: bold;
            }
            QLabel#statName {
                color: #94a3b8;
                font-size: 11px;
                font-weight: bold;
            }
        """)

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        # Header
        head_row = QHBoxLayout()
        icon = QLabel("👤")
        icon.setFont(QFont("Segoe UI Emoji", 28))
        head_row.addWidget(icon)

        head_col = QVBoxLayout()
        t_label = QLabel(f"Estudiante: {self.user.username}")
        t_label.setObjectName("dashTitle")
        sub_label = QLabel(f"Perfil Soberano — Registrado el {self.user.created_at[:10]}")
        sub_label.setStyleSheet("color: #94a3b8; font-size: 12px;")
        head_col.addWidget(t_label)
        head_col.addWidget(sub_label)

        head_row.addLayout(head_col, stretch=1)
        layout.addLayout(head_row)

        # Separador
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #334155;")
        layout.addWidget(sep)

        # 3 Tarjetas de Métricas de Progreso
        stats_row = QHBoxLayout()

        # Tarjeta 1: Precisión %
        card1 = QFrame()
        card1.setObjectName("statCard")
        l1 = QVBoxLayout(card1)
        l1.addWidget(QLabel("PRECISIÓN ACUMULADA", objectName="statName"))
        v1 = QLabel(f"{self.user.stats.accuracy_pct}%", objectName="statVal")
        l1.addWidget(v1)
        stats_row.addWidget(card1)

        # Tarjeta 2: Repeticiones Completadas
        card2 = QFrame()
        card2.setObjectName("statCard")
        l2 = QVBoxLayout(card2)
        l2.addWidget(QLabel("SERIES REPETIDAS", objectName="statName"))
        v2 = QLabel(f"{self.user.stats.completed_reps} 🔄", objectName="statVal")
        v2.setStyleSheet("color: #38bdf8;")
        l2.addWidget(v2)
        stats_row.addWidget(card2)

        # Tarjeta 3: Total Notas Tocadas
        card3 = QFrame()
        card3.setObjectName("statCard")
        l3 = QVBoxLayout(card3)
        l3.addWidget(QLabel("NOTAS EJECUTADAS", objectName="statName"))
        v3 = QLabel(f"{self.user.stats.total_notes_played}", objectName="statVal")
        v3.setStyleSheet("color: #f59e0b;")
        l3.addWidget(v3)
        stats_row.addWidget(card3)

        layout.addLayout(stats_row)

        # Registro de Lecciones Aprobadas
        group_lessons = QGroupBox("HISTORIAL DE LECCIONES Y MAESTRÍA")
        group_layout = QVBoxLayout(group_lessons)

        self.lesson_list = QListWidget()
        self.lesson_list.setStyleSheet("""
            QListWidget {
                background-color: #0f172a;
                border: 1px solid #334155;
                border-radius: 6px;
                color: #cbd5e1;
                font-size: 13px;
                padding: 6px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #1e293b;
            }
        """)

        completed = self.user.completed_lessons
        if completed:
            for lid in completed:
                item = QListWidgetItem(f"🌟 Lección Aprobada: {lid}")
                self.lesson_list.addItem(item)
        else:
            item = QListWidgetItem("📖 En progreso — Lección 1 activa")
            self.lesson_list.addItem(item)

        group_layout.addWidget(self.lesson_list)
        layout.addWidget(group_lessons)

        # Botón de Continuar Estudiando
        btn_close = QPushButton("▶ Continuar Lección")
        btn_close.setStyleSheet("background-color: #0284c7; color: white; font-weight: bold; padding: 10px 20px; border-radius: 6px;")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close, alignment=Qt.AlignmentFlag.AlignRight)
