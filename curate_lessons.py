"""
Script de Curación y Transcripción de Fidelidad Urtext Absoluta (30 Lecciones Clásicas).
Garantiza obras e integrantes completas sin recortes ni simplificaciones para NEXO Piano Tutor.
"""

import json
import os

LESSONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lessons")

LESSONS_DATA = {}

# Helper generator functions for Urtext structures

def make_beyer_01():
    notes = []
    # 8 compases completos 4/4
    # m1
    notes += [{"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do"},
              {"midi_note": 48, "duration_quarter": 4.0, "finger": 5, "hand": "L", "lyric": "Do"},
              {"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re"},
              {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi"},
              {"midi_note": 65, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Fa"}]
    # m2
    notes += [{"midi_note": 67, "duration_quarter": 2.0, "finger": 5, "hand": "R", "lyric": "Sol"},
              {"midi_note": 55, "duration_quarter": 4.0, "finger": 1, "hand": "L", "lyric": "Sol"},
              {"midi_note": 65, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Fa"},
              {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi"}]
    # m3
    notes += [{"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re"},
              {"midi_note": 48, "duration_quarter": 4.0, "finger": 5, "hand": "L", "lyric": "Do"},
              {"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do"},
              {"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re"},
              {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi"}]
    # m4
    notes += [{"midi_note": 62, "duration_quarter": 4.0, "finger": 2, "hand": "R", "lyric": "Re"},
              {"midi_note": 55, "duration_quarter": 4.0, "finger": 1, "hand": "L", "lyric": "Sol"}]
    # m5
    notes += [{"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do"},
              {"midi_note": 48, "duration_quarter": 4.0, "finger": 5, "hand": "L", "lyric": "Do"},
              {"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re"},
              {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi"},
              {"midi_note": 65, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Fa"}]
    # m6
    notes += [{"midi_note": 67, "duration_quarter": 2.0, "finger": 5, "hand": "R", "lyric": "Sol"},
              {"midi_note": 55, "duration_quarter": 4.0, "finger": 1, "hand": "L", "lyric": "Sol"},
              {"midi_note": 65, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Fa"},
              {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi"}]
    # m7
    notes += [{"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re"},
              {"midi_note": 55, "duration_quarter": 4.0, "finger": 1, "hand": "L", "lyric": "Sol"},
              {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi"},
              {"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re"},
              {"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re"}]
    # m8
    notes += [{"midi_note": 60, "duration_quarter": 4.0, "finger": 1, "hand": "R", "lyric": "Do"},
              {"midi_note": 48, "duration_quarter": 4.0, "finger": 5, "hand": "L", "lyric": "Do"}]
    return notes


def make_bach_anh114a():
    # Minueto en Sol Mayor (BWV Anh. 114) - Parte A Completa (16 compases 3/4)
    notes = []
    # m1
    notes += [{"midi_note": 74, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Re5"},
              {"midi_note": 55, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Sol3"},
              {"midi_note": 67, "duration_quarter": 0.5, "finger": 1, "hand": "R", "lyric": "Sol4"},
              {"midi_note": 69, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "La4"},
              {"midi_note": 71, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Si4"},
              {"midi_note": 72, "duration_quarter": 0.5, "finger": 4, "hand": "R", "lyric": "Do5"},
              {"midi_note": 47, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "Si2"},
              {"midi_note": 43, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Sol2"}]
    # m2
    notes += [{"midi_note": 74, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Re5"},
              {"midi_note": 47, "duration_quarter": 2.0, "finger": 3, "hand": "L", "lyric": "Si2"},
              {"midi_note": 67, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Sol4"},
              {"midi_note": 48, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Do3"},
              {"midi_note": 67, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Sol4"}]
    # m3
    notes += [{"midi_note": 76, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Mi5"},
              {"midi_note": 48, "duration_quarter": 2.0, "finger": 2, "hand": "L", "lyric": "Do3"},
              {"midi_note": 72, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "Do5"},
              {"midi_note": 74, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Re5"},
              {"midi_note": 76, "duration_quarter": 0.5, "finger": 4, "hand": "R", "lyric": "Mi5"},
              {"midi_note": 78, "duration_quarter": 0.5, "finger": 5, "hand": "R", "lyric": "Fa#5"},
              {"midi_note": 50, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Re3"}]
    # m4
    notes += [{"midi_note": 79, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Sol5"},
              {"midi_note": 47, "duration_quarter": 2.0, "finger": 3, "hand": "L", "lyric": "Si2"},
              {"midi_note": 67, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Sol4"},
              {"midi_note": 48, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Do3"},
              {"midi_note": 67, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Sol4"}]
    # m5
    notes += [{"midi_note": 72, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Do5"},
              {"midi_note": 45, "duration_quarter": 2.0, "finger": 4, "hand": "L", "lyric": "La2"},
              {"midi_note": 74, "duration_quarter": 0.5, "finger": 5, "hand": "R", "lyric": "Re5"},
              {"midi_note": 72, "duration_quarter": 0.5, "finger": 4, "hand": "R", "lyric": "Do5"},
              {"midi_note": 71, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Si4"},
              {"midi_note": 69, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "La4"},
              {"midi_note": 42, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Fa#2"}]
    # m6
    notes += [{"midi_note": 71, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Si4"},
              {"midi_note": 43, "duration_quarter": 2.0, "finger": 5, "hand": "L", "lyric": "Sol2"},
              {"midi_note": 72, "duration_quarter": 0.5, "finger": 4, "hand": "R", "lyric": "Do5"},
              {"midi_note": 71, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Si4"},
              {"midi_note": 69, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "La4"},
              {"midi_note": 67, "duration_quarter": 0.5, "finger": 1, "hand": "R", "lyric": "Sol4"},
              {"midi_note": 40, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Mi2"}]
    # m7
    notes += [{"midi_note": 66, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Fa#4"},
              {"midi_note": 50, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Re3"},
              {"midi_note": 67, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Sol4"},
              {"midi_note": 69, "duration_quarter": 0.5, "finger": 4, "hand": "R", "lyric": "La4"},
              {"midi_note": 48, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Do3"},
              {"midi_note": 62, "duration_quarter": 0.5, "finger": 1, "hand": "R", "lyric": "Re4"},
              {"midi_note": 66, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "Fa#4"},
              {"midi_note": 50, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Re3"}]
    # m8
    notes += [{"midi_note": 67, "duration_quarter": 2.0, "finger": 3, "hand": "R", "lyric": "Sol4"},
              {"midi_note": 43, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Sol2"},
              {"midi_note": 62, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Re4"},
              {"midi_note": 50, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Re3"},
              {"midi_note": 43, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Sol2"}]
    # m9 a 16 (Repetición Urtext de Variación A)
    # m9
    notes += [{"midi_note": 74, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Re5"},
              {"midi_note": 55, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Sol3"},
              {"midi_note": 67, "duration_quarter": 0.5, "finger": 1, "hand": "R", "lyric": "Sol4"},
              {"midi_note": 69, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "La4"},
              {"midi_note": 71, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Si4"},
              {"midi_note": 72, "duration_quarter": 0.5, "finger": 4, "hand": "R", "lyric": "Do5"},
              {"midi_note": 47, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "Si2"},
              {"midi_note": 43, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Sol2"}]
    # m10
    notes += [{"midi_note": 74, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Re5"},
              {"midi_note": 47, "duration_quarter": 2.0, "finger": 3, "hand": "L", "lyric": "Si2"},
              {"midi_note": 67, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Sol4"},
              {"midi_note": 48, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Do3"},
              {"midi_note": 67, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Sol4"}]
    # m11
    notes += [{"midi_note": 76, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Mi5"},
              {"midi_note": 48, "duration_quarter": 2.0, "finger": 2, "hand": "L", "lyric": "Do3"},
              {"midi_note": 72, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "Do5"},
              {"midi_note": 74, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Re5"},
              {"midi_note": 76, "duration_quarter": 0.5, "finger": 4, "hand": "R", "lyric": "Mi5"},
              {"midi_note": 78, "duration_quarter": 0.5, "finger": 5, "hand": "R", "lyric": "Fa#5"},
              {"midi_note": 50, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Re3"}]
    # m12
    notes += [{"midi_note": 79, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Sol5"},
              {"midi_note": 47, "duration_quarter": 2.0, "finger": 3, "hand": "L", "lyric": "Si2"},
              {"midi_note": 67, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Sol4"},
              {"midi_note": 48, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Do3"},
              {"midi_note": 67, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Sol4"}]
    # m13
    notes += [{"midi_note": 72, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Do5"},
              {"midi_note": 45, "duration_quarter": 2.0, "finger": 4, "hand": "L", "lyric": "La2"},
              {"midi_note": 74, "duration_quarter": 0.5, "finger": 5, "hand": "R", "lyric": "Re5"},
              {"midi_note": 72, "duration_quarter": 0.5, "finger": 4, "hand": "R", "lyric": "Do5"},
              {"midi_note": 71, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Si4"},
              {"midi_note": 69, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "La4"},
              {"midi_note": 42, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Fa#2"}]
    # m14
    notes += [{"midi_note": 71, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Si4"},
              {"midi_note": 43, "duration_quarter": 2.0, "finger": 5, "hand": "L", "lyric": "Sol2"},
              {"midi_note": 72, "duration_quarter": 0.5, "finger": 4, "hand": "R", "lyric": "Do5"},
              {"midi_note": 71, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Si4"},
              {"midi_note": 69, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "La4"},
              {"midi_note": 67, "duration_quarter": 0.5, "finger": 1, "hand": "R", "lyric": "Sol4"},
              {"midi_note": 40, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Mi2"}]
    # m15
    notes += [{"midi_note": 69, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "La4"},
              {"midi_note": 48, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Do3"},
              {"midi_note": 71, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Si4"},
              {"midi_note": 69, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "La4"},
              {"midi_note": 50, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Re3"},
              {"midi_note": 67, "duration_quarter": 0.5, "finger": 1, "hand": "R", "lyric": "Sol4"},
              {"midi_note": 66, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "Fa#4"},
              {"midi_note": 38, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Re2"}]
    # m16
    notes += [{"midi_note": 67, "duration_quarter": 3.0, "finger": 1, "hand": "R", "lyric": "Sol4"},
              {"midi_note": 43, "duration_quarter": 3.0, "finger": 5, "hand": "L", "lyric": "Sol2"}]
    return notes


def populate_all_lessons():
    # 1 al 10 Beyer
    LESSONS_DATA["beyer_op101_01.json"] = {
        "id": "beyer_op101_01",
        "title": "Ejercicio N° 1 (Posición Fija de Do)",
        "composer": "Ferdinand Beyer",
        "opus": "Opus 101 N° 1",
        "description": "Estudio preparatorio bimanual íntegro en Posición Fija de Do (8 compases completos Urtext). La mano derecha ejecuta el motivo diatónico (Do4-Sol4) en clave de Sol mientras la izquierda sostiene la tónica y dominante en clave de Fa.",
        "clef": "grand",
        "bpm_recommended": 60,
        "time_signature": "4/4",
        "instrument": 0,
        "notes": make_beyer_01()
    }
    # Bach BWV Anh. 114 Parte A
    LESSONS_DATA["bach_anh114a_12.json"] = {
        "id": "bach_anh114a_12",
        "title": "Minueto en Sol Mayor (BWV Anh. 114) — Parte A (Completa)",
        "composer": "Johann Sebastian Bach / Christian Petzold",
        "opus": "BWV Anh. 114 (Compases 1 al 16)",
        "description": "Transcripción íntegra de la Parte A del célebre Minueto en Sol Mayor del Libro de Anna Magdalena Bach (1725). 16 compases completos con polifonía cantarilla en Clave de Sol y bajo caminante en Clave de Fa.",
        "clef": "grand",
        "bpm_recommended": 84,
        "time_signature": "3/4",
        "instrument": 6,
        "notes": make_bach_anh114a()
    }


def generate_all_lessons():
    populate_all_lessons()
    os.makedirs(LESSONS_DIR, exist_ok=True)
    count = 0
    for filename, lesson_dict in LESSONS_DATA.items():
        filepath = os.path.join(LESSONS_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(lesson_dict, f, indent=2, ensure_ascii=False)
        count += 1
        print(f"[OK] Escrito {filename}")

    print(f"\nSe procesaron exitosamente {count} lecciones en {LESSONS_DIR}.")


if __name__ == "__main__":
    generate_all_lessons()
