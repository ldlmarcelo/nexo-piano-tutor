"""
Widget de Autenticación, Selección de Perfil y Registro de Estudiante para NEXO Piano Tutor.
Implementa el Blueprint de la Sección 5 de PEDAGOGIA_CLASICA.md.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QListWidget, QListWidgetItem,
    QGroupBox, QStackedWidget, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor

from core.user_manager import UserManager, User


class LoginWidget(QWidget):
    """Widget autónomo de selección de cuenta / registro de estudiante."""

    authenticated = Signal(User)

    def __init__(self, user_manager: UserManager, parent=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self.selected_user: User | None = None
        self._build_ui()
        self.refresh_user_list()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(16)

        # Cabezal de Bienvenida
        header_box = QVBoxLayout()
        title = QLabel("🎼 NEXO Piano Tutor")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #38bdf8;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Plataforma Soberana de Formación Clásica — Selección de Estudiante")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: #94a3b8;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_box.addWidget(title)
        header_box.addWidget(subtitle)
        main_layout.addLayout(header_box)

        # Separador
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #334155;")
        main_layout.addWidget(sep)

        # Contenedor con StackedWidget (Página 1: Seleccionar Usuario / Página 2: Nuevo Usuario)
        self.stacked = QStackedWidget()

        # ── PÁGINA 1: Lista de Usuarios Registrados ────────────────────────
        page_select = QWidget()
        layout_select = QVBoxLayout(page_select)

        group_select = QGroupBox("ESTUDIANTES REGISTRADOS")
        layout_group = QVBoxLayout(group_select)

        self.user_list = QListWidget()
        self.user_list.setStyleSheet("""
            QListWidget {
                background-color: #0f172a;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 6px;
                color: #f8fafc;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 6px;
                margin-bottom: 4px;
            }
            QListWidget::item:hover {
                background-color: #1e293b;
            }
            QListWidget::item:selected {
                background-color: #0284c7;
                color: #ffffff;
                font-weight: bold;
            }
        """)
        layout_group.addWidget(self.user_list)

        # Formulario de PIN (si el usuario tiene PIN)
        self.pin_frame = QFrame()
        layout_pin = QHBoxLayout(self.pin_frame)
        layout_pin.setContentsMargins(0, 0, 0, 0)
        layout_pin.addWidget(QLabel("Código PIN (4 dígitos):"))
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pin_input.setMaxLength(4)
        self.pin_input.setPlaceholderText("••••")
        self.pin_input.setFixedWidth(80)
        layout_pin.addWidget(self.pin_input)
        layout_pin.addStretch()
        self.pin_frame.setVisible(False)
        layout_group.addWidget(self.pin_frame)

        # Botones de Acción
        btn_row = QHBoxLayout()
        self.btn_login = QPushButton("▶ Ingresar a Estudiar")
        self.btn_login.setStyleSheet("background-color: #0284c7; color: white; font-weight: bold; padding: 10px 18px; border-radius: 6px;")
        
        self.btn_new = QPushButton("➕ Crear Nuevo Estudiante")
        self.btn_new.setStyleSheet("background-color: #334155; color: #cbd5e1; padding: 10px 18px; border-radius: 6px;")

        btn_row.addWidget(self.btn_login)
        btn_row.addWidget(self.btn_new)
        layout_group.addLayout(btn_row)

        layout_select.addWidget(group_select)
        self.stacked.addWidget(page_select)

        # ── PÁGINA 2: Registro de Nuevo Usuario ───────────────────────────
        page_register = QWidget()
        layout_reg = QVBoxLayout(page_register)

        group_reg = QGroupBox("REGISTRO DE NUEVO ESTUDIANTE")
        reg_form = QVBoxLayout(group_reg)

        reg_form.addWidget(QLabel("Nombre del Estudiante (Universal):"))
        self.reg_name_input = QLineEdit()
        self.reg_name_input.setPlaceholderText("Ej. Gael, Fer, Marcelo...")
        self.reg_name_input.setStyleSheet("padding: 8px; border-radius: 4px; background-color: #0f172a; border: 1px solid #334155; color: white;")
        reg_form.addWidget(self.reg_name_input)

        reg_form.addWidget(QLabel("Código PIN opcional (4 dígitos):"))
        self.reg_pin_input = QLineEdit()
        self.reg_pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_pin_input.setMaxLength(4)
        self.reg_pin_input.setPlaceholderText("Dejar en blanco si no requiere PIN")
        self.reg_pin_input.setStyleSheet("padding: 8px; border-radius: 4px; background-color: #0f172a; border: 1px solid #334155; color: white;")
        reg_form.addWidget(self.reg_pin_input)

        reg_form.addSpacing(10)

        reg_btn_row = QHBoxLayout()
        self.btn_create_user = QPushButton("✔ Crear Perfil")
        self.btn_create_user.setStyleSheet("background-color: #16a34a; color: white; font-weight: bold; padding: 10px 18px; border-radius: 6px;")
        
        self.btn_cancel_reg = QPushButton("🗙 Cancelar")
        self.btn_cancel_reg.setStyleSheet("background-color: #334155; color: #cbd5e1; padding: 10px 18px; border-radius: 6px;")

        reg_btn_row.addWidget(self.btn_create_user)
        reg_btn_row.addWidget(self.btn_cancel_reg)
        reg_form.addLayout(reg_btn_row)

        layout_reg.addWidget(group_reg)
        self.stacked.addWidget(page_register)

        main_layout.addWidget(self.stacked)

        # Mensaje de Error / Estado
        self.msg_label = QLabel("")
        self.msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msg_label.setStyleSheet("color: #ef4444; font-size: 12px; font-weight: bold;")
        main_layout.addWidget(self.msg_label)

        # Conexión de Señales
        self.user_list.itemSelectionChanged.connect(self._on_user_selected)
        self.btn_login.clicked.connect(self._on_login_clicked)
        self.btn_new.clicked.connect(lambda: self.stacked.setCurrentIndex(1))
        self.btn_cancel_reg.clicked.connect(lambda: self.stacked.setCurrentIndex(0))
        self.btn_create_user.clicked.connect(self._on_create_user_clicked)

    def refresh_user_list(self):
        """Actualiza la lista visual de usuarios almacenados."""
        self.user_list.clear()
        self.user_manager.load()
        users = list(self.user_manager.users.values())

        if not users:
            item = QListWidgetItem("No hay estudiantes registrados. Crea uno nuevo.")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.user_list.addItem(item)
            self.btn_login.setEnabled(False)
            return

        self.btn_login.setEnabled(True)
        for u in users:
            pin_badge = " 🔒" if u.pin else ""
            reps = u.stats.completed_reps
            item = QListWidgetItem(f"👤  {u.username}{pin_badge}   —   {reps} repeticiones completadas")
            item.setData(Qt.ItemDataRole.UserRole, u.id)
            self.user_list.addItem(item)

        self.user_list.setCurrentRow(0)

    def _on_user_selected(self):
        items = self.user_list.selectedItems()
        if not items:
            self.selected_user = None
            self.pin_frame.setVisible(False)
            return

        user_id = items[0].data(Qt.ItemDataRole.UserRole)
        if user_id in self.user_manager.users:
            self.selected_user = self.user_manager.users[user_id]
            self.pin_frame.setVisible(bool(self.selected_user.pin))
            self.pin_input.clear()
        else:
            self.selected_user = None
            self.pin_frame.setVisible(False)

    def _on_login_clicked(self):
        if not self.selected_user:
            self.msg_label.setText("Por favor selecciona un perfil de estudiante.")
            return

        pin = self.pin_input.text() if self.selected_user.pin else None
        ok, msg, user = self.user_manager.authenticate(self.selected_user.id, pin)
        if ok and user:
            self.msg_label.setText("")
            self.authenticated.emit(user)
        else:
            self.msg_label.setText(msg)

    def _on_create_user_clicked(self):
        name = self.reg_name_input.text()
        pin = self.reg_pin_input.text()

        ok, msg, user = self.user_manager.register_user(name, pin)
        if ok and user:
            self.reg_name_input.clear()
            self.reg_pin_input.clear()
            self.msg_label.setText("")
            self.refresh_user_list()
            self.stacked.setCurrentIndex(0)
            self.authenticated.emit(user)
        else:
            self.msg_label.setText(msg)
