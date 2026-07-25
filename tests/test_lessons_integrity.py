"""
Pruebas de Integridad y Validación de Esquema de las 30 Lecciones Clásicas JSON.
"""

import os
import json
import pytest

CARPETA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LESSONS_DIR = os.path.join(CARPETA_RAIZ, "lessons")


def get_all_lesson_files():
    """Devuelve la lista de rutas absolutas de todos los archivos .json en lessons/."""
    if not os.path.exists(LESSONS_DIR):
        return []
    return [
        os.path.join(LESSONS_DIR, f)
        for f in sorted(os.listdir(LESSONS_DIR))
        if f.endswith(".json")
    ]


def test_lessons_directory_exists_and_count():
    assert os.path.exists(LESSONS_DIR), f"La carpeta {LESSONS_DIR} no existe."
    files = get_all_lesson_files()
    assert len(files) == 30, f"Se esperaban 30 lecciones clásicas en JSON, pero se encontraron {len(files)}."


@pytest.mark.parametrize("filepath", get_all_lesson_files())
def test_individual_lesson_json_schema(filepath: str):
    filename = os.path.basename(filepath)
    assert os.path.exists(filepath), f"El archivo {filename} no existe."

    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Error de sintaxis JSON en {filename}: {e}")

    # 1. Validar Campos de Nivel Superior
    required_top_fields = ["id", "title", "composer", "opus", "description", "clef", "bpm_recommended", "notes"]
    for field in required_top_fields:
        assert field in data, f"Campo obligatorio '{field}' ausente en {filename}."

    assert isinstance(data["id"], str) and len(data["id"]) > 0, f"'id' inválido en {filename}."
    assert isinstance(data["title"], str) and len(data["title"]) > 0, f"'title' inválido en {filename}."
    assert isinstance(data["composer"], str), f"'composer' inválido en {filename}."
    assert data["clef"] in ("treble", "bass", "grand"), f"Clave '{data['clef']}' inválida en {filename}."
    assert isinstance(data["bpm_recommended"], (int, float)) and data["bpm_recommended"] > 0, f"BPM inválido en {filename}."

    # 2. Validar Estructura de Notas
    notes = data["notes"]
    assert isinstance(notes, list), f"'notes' debe ser una lista en {filename}."
    assert len(notes) > 0, f"La lección {filename} no contiene notas."

    for idx, note in enumerate(notes):
        # Campos obligatorios de cada nota
        assert "midi_note" in note, f"Nota #{idx+1} en {filename} no tiene 'midi_note'."
        assert "duration_quarter" in note, f"Nota #{idx+1} en {filename} no tiene 'duration_quarter'."
        assert "finger" in note, f"Nota #{idx+1} en {filename} no tiene 'finger'."

        midi = note["midi_note"]
        duration = note["duration_quarter"]
        finger = note["finger"]
        hand = note.get("hand", "R")

        # Rangos válidos
        assert isinstance(midi, int) and 21 <= midi <= 108, f"midi_note {midi} fuera de rango (21-108) en nota #{idx+1} de {filename}."
        assert isinstance(duration, (int, float)) and duration > 0, f"duration_quarter {duration} inválida en nota #{idx+1} de {filename}."
        assert isinstance(finger, int) and 1 <= finger <= 5, f"finger {finger} fuera de rango (1-5) en nota #{idx+1} de {filename}."
        assert hand in ("R", "L"), f"hand '{hand}' inválida en nota #{idx+1} de {filename}."
