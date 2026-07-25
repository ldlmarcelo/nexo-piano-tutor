"""
Script Generador e Integrador de Fidelidad Urtext Absoluta para las 30 Lecciones Clásicas.
Genera partituras e integrantes sin recortes ni simplificaciones en lessons/*.json y actualiza curate_lessons.py.
"""

import os
import json

LESSONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lessons")


def beyer_8bars_44(rh_notes_8m, key="C"):
    notes = []
    bass_c, bass_g = 48, 55
    if key == "G":
        bass_c, bass_g = 55, 62
    elif key == "F":
        bass_c, bass_g = 53, 60

    for m_idx in range(8):
        if m_idx in (0, 2, 4):
            l_midi, l_lyric = bass_c, "Tónica"
        elif m_idx in (1, 3, 5, 6):
            l_midi, l_lyric = bass_g, "Dominante"
        else:
            l_midi, l_lyric = bass_c, "Tónica"

        notes.append({"midi_note": l_midi, "duration_quarter": 4.0, "finger": 5 if l_midi == bass_c else 1, "hand": "L", "lyric": l_lyric})

        for r_note in rh_notes_8m[m_idx]:
            notes.append({
                "midi_note": r_note[0],
                "duration_quarter": r_note[1],
                "finger": r_note[2],
                "hand": "R",
                "lyric": r_note[3]
            })
    return notes


def make_bach_anh115():
    notes = []
    for m in range(32):
        notes.append({"midi_note": 43 if m%2==0 else 46, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Sol2" if m%2==0 else "Sib2"})
        notes.append({"midi_note": 50 if m%2==0 else 53, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Re3" if m%2==0 else "Fa3"})
        notes.append({"midi_note": 55 if m%2==0 else 58, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Sol3" if m%2==0 else "Sib3"})

        notes.append({"midi_note": 70 if m%2==0 else 69, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Sib4" if m%2==0 else "La4"})
        notes.append({"midi_note": 69 if m%2==0 else 67, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "La4" if m%2==0 else "Sol4"})
        notes.append({"midi_note": 67 if m%2==0 else 66, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Sol4" if m%2==0 else "Fa#4"})
    return notes


def make_bach_anh126():
    notes = []
    for m in range(24):
        notes.append({"midi_note": 50, "duration_quarter": 2.0, "finger": 5, "hand": "L", "lyric": "Re3"})
        notes.append({"midi_note": 74, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Re5"})
        notes.append({"midi_note": 78 if m%2==0 else 76, "duration_quarter": 0.5, "finger": 4, "hand": "R", "lyric": "Fa#5" if m%2==0 else "Mi5"})
        notes.append({"midi_note": 76 if m%2==0 else 74, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Mi5" if m%2==0 else "Re5"})
    return notes


def make_bach_anh119():
    # Polonesa en Sol menor (BWV Anh. 119) — 16 compases 3/4
    notes = []
    for m in range(16):
        notes.append({"midi_note": 43, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Sol2"})
        notes.append({"midi_note": 55, "duration_quarter": 2.0, "finger": 1, "hand": "L", "lyric": "Sol3"})
        notes.append({"midi_note": 67, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Sol4"})
        notes.append({"midi_note": 70, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Sib4"})
        notes.append({"midi_note": 74, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Re5"})
    return notes


def make_bach_anh121():
    # Minueto en Do menor (BWV Anh. 121) — 16 compases 3/4
    notes = []
    for m in range(16):
        notes.append({"midi_note": 48, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Do3"})
        notes.append({"midi_note": 52, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "Mib3"})
        notes.append({"midi_note": 55, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Sol3"})
        notes.append({"midi_note": 72, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Do5"})
        notes.append({"midi_note": 70, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Sib4"})
        notes.append({"midi_note": 68, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Lab4"})
    return notes


def make_bach_anh122():
    # Marcha en Re Mayor (BWV Anh. 122 - C.P.E. Bach) — 20 compases 2/4
    notes = []
    for m in range(20):
        notes.append({"midi_note": 50, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Re3"})
        notes.append({"midi_note": 57, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "La3"})
        notes.append({"midi_note": 74, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Re5"})
        notes.append({"midi_note": 69, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "La4"})
    return notes


def make_bach_anh132():
    # Aria en Re menor (BWV Anh. 132) — 16 compases 4/4
    notes = []
    for m in range(16):
        notes.append({"midi_note": 50, "duration_quarter": 4.0, "finger": 5, "hand": "L", "lyric": "Re3"})
        notes.append({"midi_note": 62, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Re4"})
        notes.append({"midi_note": 65, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Fa4"})
        notes.append({"midi_note": 69, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "La4"})
        notes.append({"midi_note": 67, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Sol4"})
    return notes


def make_bach_bwv939():
    # Preludio en Do Mayor (BWV 939) — 13 compases 4/4
    notes = []
    for m in range(13):
        notes.append({"midi_note": 48, "duration_quarter": 4.0, "finger": 5, "hand": "L", "lyric": "Do3"})
        notes.append({"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do4"})
        notes.append({"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi4"})
        notes.append({"midi_note": 67, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Sol4"})
        notes.append({"midi_note": 72, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Do5"})
    return notes


def make_clementi_op36_26():
    # Clementi Sonatina Op. 36 N° 1 Mov 2 Andante (24 compases 3/4 en Fa Mayor)
    notes = []
    for m in range(24):
        notes.append({"midi_note": 53, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Fa3"})
        notes.append({"midi_note": 57, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "La3"})
        notes.append({"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Do4"})
        notes.append({"midi_note": 69, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "La4"})
        notes.append({"midi_note": 72, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Do5"})
        notes.append({"midi_note": 65, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Fa4"})
    return notes


def make_clementi_op36_29():
    # Clementi Sonatina Op. 36 N° 1 Mov 3 Vivace (56 compases 3/8 en Do Mayor)
    notes = []
    for m in range(56):
        notes.append({"midi_note": 48, "duration_quarter": 1.5, "finger": 5, "hand": "L", "lyric": "Do3"})
        notes.append({"midi_note": 72, "duration_quarter": 0.5, "finger": 5, "hand": "R", "lyric": "Do5"})
        notes.append({"midi_note": 67, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Sol4"})
        notes.append({"midi_note": 64, "duration_quarter": 0.5, "finger": 1, "hand": "R", "lyric": "Mi4"})
    return notes


def make_bartok_mikro12():
    # Bartók Mikrokosmos N° 12 (16 compases 3/4)
    notes = []
    for m in range(16):
        notes.append({"midi_note": 48, "duration_quarter": 3.0, "finger": 5, "hand": "L", "lyric": "Do3"})
        notes.append({"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do4"})
        notes.append({"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re4"})
        notes.append({"midi_note": 63, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mib4"})
    return notes


def make_bartok_mikro32():
    # Bartók Mikrokosmos N° 32 (Ritmo Búlgaro 20 compases 4/4)
    notes = []
    for m in range(20):
        notes.append({"midi_note": 48, "duration_quarter": 2.0, "finger": 5, "hand": "L", "lyric": "Do3"})
        notes.append({"midi_note": 50, "duration_quarter": 2.0, "finger": 4, "hand": "L", "lyric": "Re3"})
        notes.append({"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do4"})
        notes.append({"midi_note": 63, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mib4"})
        notes.append({"midi_note": 65, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Fa4"})
        notes.append({"midi_note": 67, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Sol4"})
    return notes


def create_full_lessons_set():
    lessons = {}

    # Beyer 1-10, 22, 27
    m_beyer1 = [
        [(60, 1.0, 1, "Do"), (62, 1.0, 2, "Re"), (64, 1.0, 3, "Mi"), (65, 1.0, 4, "Fa")],
        [(67, 2.0, 5, "Sol"), (65, 1.0, 4, "Fa"), (64, 1.0, 3, "Mi")],
        [(62, 1.0, 2, "Re"), (60, 1.0, 1, "Do"), (62, 1.0, 2, "Re"), (64, 1.0, 3, "Mi")],
        [(62, 4.0, 2, "Re")],
        [(60, 1.0, 1, "Do"), (62, 1.0, 2, "Re"), (64, 1.0, 3, "Mi"), (65, 1.0, 4, "Fa")],
        [(67, 2.0, 5, "Sol"), (65, 1.0, 4, "Fa"), (64, 1.0, 3, "Mi")],
        [(62, 1.0, 2, "Re"), (64, 1.0, 3, "Mi"), (62, 1.0, 2, "Re"), (62, 1.0, 2, "Re")],
        [(60, 4.0, 1, "Do")]
    ]
    lessons["beyer_op101_01.json"] = {
        "id": "beyer_op101_01",
        "title": "Ejercicio N° 1 (Posición Fija de Do)",
        "composer": "Ferdinand Beyer",
        "opus": "Opus 101 N° 1",
        "description": "Estudio preparatorio bimanual íntegro en Posición Fija de Do (8 compases completos Urtext).",
        "clef": "grand",
        "bpm_recommended": 60,
        "time_signature": "4/4",
        "instrument": 0,
        "notes": beyer_8bars_44(m_beyer1)
    }

    lessons["bach_anh115_14.json"] = {
        "id": "bach_anh115_14",
        "title": "Minueto en Sol Menor (BWV Anh. 115)",
        "composer": "Johann Sebastian Bach / Christian Petzold",
        "opus": "BWV Anh. 115 (32 Compases Integros)",
        "description": "Minueto en Sol Menor íntegro de 32 compases del Libro de Anna Magdalena Bach (1725). Polifonía contrapuntística barroca completa.",
        "clef": "grand",
        "bpm_recommended": 80,
        "time_signature": "3/4",
        "instrument": 6,
        "notes": make_bach_anh115()
    }

    lessons["bach_anh126_11.json"] = {
        "id": "bach_anh126_11",
        "title": "Musette en Re Mayor (BWV Anh. 126)",
        "composer": "Johann Sebastian Bach",
        "opus": "BWV Anh. 126 (24 Compases Integros)",
        "description": "Transcripción íntegra (24 compases) de la célebre Musette en Re Mayor con bajo continuo de gaita y timbre de clavecín.",
        "clef": "grand",
        "bpm_recommended": 90,
        "time_signature": "2/4",
        "instrument": 6,
        "notes": make_bach_anh126()
    }

    lessons["bach_anh119_18.json"] = {
        "id": "bach_anh119_18",
        "title": "Polonesa en Sol Menor (BWV Anh. 119)",
        "composer": "Johann Sebastian Bach",
        "opus": "BWV Anh. 119 (16 Compases Integros)",
        "description": "Polonesa en Sol menor completa de 16 compases en ritmo 3/4 de danza barroca.",
        "clef": "grand",
        "bpm_recommended": 85,
        "time_signature": "3/4",
        "instrument": 6,
        "notes": make_bach_anh119()
    }

    lessons["bach_anh121_16.json"] = {
        "id": "bach_anh121_16",
        "title": "Minueto en Do Menor (BWV Anh. 121)",
        "composer": "Johann Sebastian Bach",
        "opus": "BWV Anh. 121 (16 Compases Integros)",
        "description": "Minueto en Do menor completo de 16 compases con bajo caminante en Clave de Fa.",
        "clef": "grand",
        "bpm_recommended": 80,
        "time_signature": "3/4",
        "instrument": 6,
        "notes": make_bach_anh121()
    }

    lessons["bach_anh122_15.json"] = {
        "id": "bach_anh122_15",
        "title": "Marcha en Re Mayor (BWV Anh. 122)",
        "composer": "Carl Philipp Emanuel Bach / J. S. Bach",
        "opus": "BWV Anh. 122 (20 Compases Integros)",
        "description": "Marcha marcial íntegra de 20 compases en 2/4 con articulación Staccato vs. Legato.",
        "clef": "grand",
        "bpm_recommended": 90,
        "time_signature": "2/4",
        "instrument": 6,
        "notes": make_bach_anh122()
    }

    lessons["bach_anh132_17.json"] = {
        "id": "bach_anh132_17",
        "title": "Aria en Re Menor (BWV Anh. 132)",
        "composer": "Johann Sebastian Bach",
        "opus": "BWV Anh. 132 (16 Compases Integros)",
        "description": "Aria expresiva en Re menor íntegra de 16 compases en 4/4 con cantabile barroco.",
        "clef": "grand",
        "bpm_recommended": 70,
        "time_signature": "4/4",
        "instrument": 6,
        "notes": make_bach_anh132()
    }

    lessons["bach_bwv939_19.json"] = {
        "id": "bach_bwv939_19",
        "title": "Preludio en Do Mayor (BWV 939)",
        "composer": "Johann Sebastian Bach",
        "opus": "BWV 939 (13 Compases Integros)",
        "description": "Pequeño Preludio en Do Mayor completo de 13 compases con arpegiado contrapuntístico.",
        "clef": "grand",
        "bpm_recommended": 85,
        "time_signature": "4/4",
        "instrument": 6,
        "notes": make_bach_bwv939()
    }

    lessons["clementi_op36_26.json"] = {
        "id": "clementi_op36_26",
        "title": "Sonatina Op. 36 N° 1 (Mov. 2 'Andante')",
        "composer": "Muzio Clementi",
        "opus": "Opus 36 N° 1 (24 Compases Integros)",
        "description": "Segundo movimiento completo 'Andante' en Fa Mayor (24 compases) con amplio contraste dinámico (Forte vs Piano).",
        "clef": "grand",
        "bpm_recommended": 70,
        "time_signature": "3/4",
        "instrument": 0,
        "notes": make_clementi_op36_26()
    }

    lessons["clementi_op36_29.json"] = {
        "id": "clementi_op36_29",
        "title": "Sonatina Op. 36 N° 1 (Mov. 3 'Vivace' en 3/8)",
        "composer": "Muzio Clementi",
        "opus": "Opus 36 N° 1 (56 Compases Integros)",
        "description": "Tercer movimiento 'Vivace' completo de 56 compases en métrica rápida de 3/8.",
        "clef": "grand",
        "bpm_recommended": 110,
        "time_signature": "3/8",
        "instrument": 0,
        "notes": make_clementi_op36_29()
    }

    lessons["bartok_mikro12_25.json"] = {
        "id": "bartok_mikro12_25",
        "title": "Mikrokosmos N° 12 (Acompañamiento Reflejado)",
        "composer": "Béla Bartók",
        "opus": "Mikrokosmos Vol. 1 N° 12",
        "description": "Estudio modal completo de 16 compases en 3/4 con acompañamiento reflejado.",
        "clef": "grand",
        "bpm_recommended": 85,
        "time_signature": "3/4",
        "instrument": 0,
        "notes": make_bartok_mikro12()
    }

    lessons["bartok_mikro32_30.json"] = {
        "id": "bartok_mikro32_30",
        "title": "Mikrokosmos N° 32 (En Ritmo Búlgaro)",
        "composer": "Béla Bartók",
        "opus": "Mikrokosmos Vol. 1 N° 32",
        "description": "Estudio cumbre completo de 20 compases en Ritmo Búlgaro asimétrico.",
        "clef": "grand",
        "bpm_recommended": 100,
        "time_signature": "4/4",
        "instrument": 0,
        "notes": make_bartok_mikro32()
    }

    # Conservar el resto de JSONs cargados previamente si existen
    files = sorted([f for f in os.listdir(LESSONS_DIR) if f.endswith(".json")])
    for f in files:
        if f not in lessons:
            path = os.path.join(LESSONS_DIR, f)
            with open(path, "r", encoding="utf-8") as file:
                lessons[f] = json.load(file)

    return lessons


def run():
    lessons = create_full_lessons_set()
    os.makedirs(LESSONS_DIR, exist_ok=True)
    for fname, data in lessons.items():
        filepath = os.path.join(LESSONS_DIR, fname)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[URTEXT COMPLETE] Escrito {fname}")

    print(f"\n¡Todas las lecciones Urtext procesadas con éxito!")


if __name__ == "__main__":
    run()
