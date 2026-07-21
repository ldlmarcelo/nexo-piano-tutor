"""
Gestor de Usuarios, Autenticación y Persistencia de Progreso Soberano (v1.0.0).
Implementa la Sección 5 de PEDAGOGIA_CLASICA.md bajo la Ley de Universalidad Semántica.
"""

import os
import json
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass, field, asdict

CARPETA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_FILE = os.path.join(CARPETA_RAIZ, "users.json")


@dataclass
class UserStats:
    total_notes_played: int = 0
    correct_notes: int = 0
    completed_reps: int = 0
    accuracy_pct: float = 100.0


@dataclass
class User:
    id: str
    username: str
    pin: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    active_lesson_id: str = "beyer_op101_01"
    completed_lessons: list[str] = field(default_factory=list)
    stats: UserStats = field(default_factory=UserStats)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "pin": self.pin,
            "created_at": self.created_at,
            "active_lesson_id": self.active_lesson_id,
            "completed_lessons": self.completed_lessons,
            "stats": asdict(self.stats)
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "User":
        stats_data = data.get("stats", {})
        stats = UserStats(**stats_data) if isinstance(stats_data, dict) else UserStats()
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            username=data.get("username", "Estudiante"),
            pin=data.get("pin"),
            created_at=data.get("created_at", datetime.now().isoformat()),
            active_lesson_id=data.get("active_lesson_id", "beyer_op101_01"),
            completed_lessons=data.get("completed_lessons", []),
            stats=stats
        )


class UserManager:
    """Gestor de autenticación, usuarios y guardado de progreso."""

    def __init__(self, filepath: str = USERS_FILE):
        self.filepath = filepath
        self.users: Dict[str, User] = {}
        self.active_user_id: Optional[str] = None
        self.load()

    def load(self):
        """Carga usuarios almacenados en users.json."""
        if not os.path.exists(self.filepath):
            self.users = {}
            return

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.users = {uid: User.from_dict(u) for uid, u in data.get("users", {}).items()}
                self.active_user_id = data.get("active_user_id")
        except Exception:
            self.users = {}
            self.active_user_id = None

    def save(self):
        """Guarda la base de usuarios en users.json."""
        try:
            data = {
                "active_user_id": self.active_user_id,
                "users": {uid: u.to_dict() for uid, u in self.users.items()}
            }
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[USER MANAGER ERROR] Error al guardar users.json: {e}")

    def register_user(self, username: str, pin: Optional[str] = None) -> tuple[bool, str, Optional[User]]:
        """Registra un nuevo usuario abstracto en el sistema."""
        username_clean = username.strip()
        if not username_clean:
            return False, "El nombre de usuario no puede estar vacío.", None

        # Verificar duplicados por nombre (case-insensitive)
        for u in self.users.values():
            if u.username.lower() == username_clean.lower():
                return False, f"El usuario '{username_clean}' ya está registrado.", None

        new_user = User(
            id=str(uuid.uuid4()),
            username=username_clean,
            pin=pin.strip() if pin else None
        )
        self.users[new_user.id] = new_user
        self.active_user_id = new_user.id
        self.save()
        return True, f"Usuario '{username_clean}' registrado con éxito.", new_user

    def authenticate(self, user_id: str, pin: Optional[str] = None) -> tuple[bool, str, Optional[User]]:
        """Autentica un usuario existente."""
        if user_id not in self.users:
            return False, "Usuario no encontrado.", None

        user = self.users[user_id]
        if user.pin:
            if not pin or pin.strip() != user.pin:
                return False, "PIN incorrecto.", None

        self.active_user_id = user.id
        self.save()
        return True, f"Bienvenido, {user.username}.", user

    def logout(self):
        """Cierra la sesión activa."""
        self.active_user_id = None
        self.save()

    def get_active_user(self) -> Optional[User]:
        """Devuelve el objeto User del estudiante actualmente autenticado."""
        if self.active_user_id and self.active_user_id in self.users:
            return self.users[self.active_user_id]
        return None

    def record_progress(self, lesson_id: str, completed: bool = False, notes_played: int = 1, correct: bool = True):
        """Registra el avance de una lección para el usuario activo."""
        user = self.get_active_user()
        if not user:
            return

        user.active_lesson_id = lesson_id
        user.stats.total_notes_played += notes_played
        if correct:
            user.stats.correct_notes += notes_played

        if user.stats.total_notes_played > 0:
            user.stats.accuracy_pct = round((user.stats.correct_notes / user.stats.total_notes_played) * 100, 1)

        if completed:
            if lesson_id not in user.completed_lessons:
                user.completed_lessons.append(lesson_id)
            user.stats.completed_reps += 1

        self.save()
