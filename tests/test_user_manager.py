"""
Pruebas Unitarias e Integración para Gestor de Usuarios y Persistencia (UserManager).
"""

import os
import pytest
from core.user_manager import UserManager, User, UserStats, SessionLog


def test_user_manager_empty_initialization(temp_user_manager: UserManager):
    assert len(temp_user_manager.users) == 0
    assert temp_user_manager.active_user_id is None
    assert temp_user_manager.get_active_user() is None


def test_user_registration_success(temp_user_manager: UserManager):
    ok, msg, user = temp_user_manager.register_user(username="Marcelo", pin="1234")
    assert ok is True
    assert "registrado con éxito" in msg
    assert user is not None
    assert user.username == "Marcelo"
    assert user.pin == "1234"
    assert temp_user_manager.active_user_id == user.id
    assert temp_user_manager.get_active_user() == user


def test_user_registration_validation(temp_user_manager: UserManager):
    # Intentar registrar nombre vacío
    ok1, msg1, _ = temp_user_manager.register_user(username="  ")
    assert ok1 is False
    assert "vacío" in msg1

    # Registrar usuario 1
    temp_user_manager.register_user(username="Ana")

    # Intentar registrar duplicado (case-insensitive)
    ok2, msg2, _ = temp_user_manager.register_user(username="ana")
    assert ok2 is False
    assert "ya está registrado" in msg2


def test_user_authentication(temp_user_manager: UserManager):
    _, _, user = temp_user_manager.register_user(username="Sofia", pin="4321")
    user_id = user.id

    # Cerrar sesión
    temp_user_manager.logout()
    assert temp_user_manager.get_active_user() is None

    # Autenticar con PIN incorrecto
    ok_fail, msg_fail, _ = temp_user_manager.authenticate(user_id=user_id, pin="0000")
    assert ok_fail is False
    assert "PIN incorrecto" in msg_fail

    # Autenticar con PIN correcto
    ok_win, msg_win, auth_user = temp_user_manager.authenticate(user_id=user_id, pin="4321")
    assert ok_win is True
    assert auth_user.id == user_id
    assert temp_user_manager.get_active_user() == auth_user


def test_user_record_progress_and_accuracy(temp_user_manager: UserManager):
    _, _, user = temp_user_manager.register_user(username="Pedro")

    # Registrar 8 notas correctas y 2 incorrectas
    temp_user_manager.record_progress(lesson_id="beyer_op101_01", completed=False, notes_played=8, correct=True)
    temp_user_manager.record_progress(lesson_id="beyer_op101_01", completed=False, notes_played=2, correct=False)

    active_user = temp_user_manager.get_active_user()
    assert active_user.stats.total_notes_played == 10
    assert active_user.stats.correct_notes == 8
    assert active_user.stats.accuracy_pct == 80.0

    # Marcar lección completada
    temp_user_manager.record_progress(lesson_id="beyer_op101_01", completed=True, notes_played=1, correct=True)
    assert "beyer_op101_01" in active_user.completed_lessons
    assert active_user.stats.completed_reps == 1


def test_user_persistence_save_load(temp_user_manager: UserManager):
    filepath = temp_user_manager.filepath

    # Registrar usuario y progreso
    _, _, user = temp_user_manager.register_user(username="Lucia", pin="9999")
    temp_user_manager.record_progress(lesson_id="beyer_op101_05", completed=True, notes_played=20, correct=True)
    temp_user_manager.record_session_log(
        lesson_id="beyer_op101_05",
        mode="tempo",
        notes_played=20,
        accuracy_pct=100.0
    )

    # Reinstanciar el UserManager leyendo del mismo archivo JSON
    new_manager = UserManager(filepath=filepath)
    assert len(new_manager.users) == 1
    assert new_manager.active_user_id == user.id

    loaded_user = new_manager.get_active_user()
    assert loaded_user.username == "Lucia"
    assert loaded_user.pin == "9999"
    assert loaded_user.active_lesson_id == "beyer_op101_05"
    assert "beyer_op101_05" in loaded_user.completed_lessons
    assert loaded_user.stats.total_notes_played == 20
    assert loaded_user.stats.accuracy_pct == 100.0
    assert len(loaded_user.history) == 1
    assert loaded_user.history[0].mode == "tempo"
