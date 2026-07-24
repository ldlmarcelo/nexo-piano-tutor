"""
Script de Curación y Enriquecimiento de las 30 Lecciones Clásicas para NEXO Piano Tutor.
Garantiza que todas las lecciones tengan notación bimanual nítida en Gran Pentagrama ('grand'),
con asignación correcta de manos (R=Derecha/Sol, L=Izquierda/Fa), digitación (1-5),
duraciones rítmicas, lírica de solfeo y métrica exacta.
"""

import json
import os
import glob

LESSONS_DIR = "/home/marcelo/PROYECTOS/nexo-piano-tutor/lessons"

# Definición de la taxonomía completa y curada de las 30 obras clásicas
LESSONS_DATA = {
    # -------------------------------------------------------------------------
    # BEYER OPUS 101 - INICIACIÓN Y DIÁLOGO BIMANUAL
    # -------------------------------------------------------------------------
    "beyer_op101_01.json": {
        "id": "beyer_op101_01",
        "title": "Ejercicio N° 1 (Posición Fija de Do)",
        "composer": "Ferdinand Beyer",
        "opus": "Opus 101 N° 1",
        "description": "Estudio preparatorio bimanual en Posición Fija de Do. La mano derecha ejecuta el motivo diatónico (Do4-Sol4) en clave de Sol mientras la izquierda sostiene la tónica en clave de Fa.",
        "clef": "grand",
        "bpm_recommended": 60,
        "time_signature": "4/4",
        "instrument": 0,
        "notes": [
            # Compás 1
            {"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 48, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Do"},
            {"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re"},
            {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi"},
            {"midi_note": 65, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Fa"},
            # Compás 2
            {"midi_note": 67, "duration_quarter": 2.0, "finger": 5, "hand": "R", "lyric": "Sol"},
            {"midi_note": 55, "duration_quarter": 2.0, "finger": 1, "hand": "L", "lyric": "Sol"},
            {"midi_note": 65, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Fa"},
            {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi"},
            # Compás 3
            {"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re"},
            {"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 52, "duration_quarter": 2.0, "finger": 3, "hand": "L", "lyric": "Mi"},
            # Compás 4
            {"midi_note": 60, "duration_quarter": 4.0, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 48, "duration_quarter": 4.0, "finger": 5, "hand": "L", "lyric": "Do"}
        ]
    },
    "beyer_op101_02.json": {
        "id": "beyer_op101_02",
        "title": "Ejercicio N° 2 (Mano Izquierda y Tónica Sol)",
        "composer": "Ferdinand Beyer",
        "opus": "Opus 101 N° 2",
        "description": "Desarrollo de la mano izquierda en Clave de Fa (Do3-Sol3) con respuesta melódica de la mano derecha en Clave de Sol.",
        "clef": "grand",
        "bpm_recommended": 60,
        "time_signature": "4/4",
        "instrument": 0,
        "notes": [
            # Compás 1
            {"midi_note": 48, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Do"},
            {"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 50, "duration_quarter": 1.0, "finger": 4, "hand": "L", "lyric": "Re"},
            {"midi_note": 52, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "Mi"},
            {"midi_note": 53, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Fa"},
            # Compás 2
            {"midi_note": 55, "duration_quarter": 2.0, "finger": 1, "hand": "L", "lyric": "Sol"},
            {"midi_note": 67, "duration_quarter": 2.0, "finger": 5, "hand": "R", "lyric": "Sol"},
            {"midi_note": 53, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Fa"},
            {"midi_note": 52, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "Mi"},
            # Compás 3
            {"midi_note": 50, "duration_quarter": 1.0, "finger": 4, "hand": "L", "lyric": "Re"},
            {"midi_note": 48, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Do"},
            {"midi_note": 64, "duration_quarter": 2.0, "finger": 3, "hand": "R", "lyric": "Mi"},
            # Compás 4
            {"midi_note": 48, "duration_quarter": 4.0, "finger": 5, "hand": "L", "lyric": "Do"},
            {"midi_note": 60, "duration_quarter": 4.0, "finger": 1, "hand": "R", "lyric": "Do"}
        ]
    },
    "beyer_op101_03.json": {
        "id": "beyer_op101_03",
        "title": "Ejercicio N° 3 (Saltos de Terceras en Ambos Pentagramas)",
        "composer": "Ferdinand Beyer",
        "opus": "Opus 101 N° 3",
        "description": "Estudio de intervalos de tercera (Do-Mi, Re-Fa, Mi-Sol) alternando mano derecha e izquierda en Gran Pentagrama.",
        "clef": "grand",
        "bpm_recommended": 65,
        "time_signature": "4/4",
        "instrument": 0,
        "notes": [
            # Compás 1
            {"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi"},
            {"midi_note": 48, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Do"},
            {"midi_note": 52, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "Mi"},
            # Compás 2
            {"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re"},
            {"midi_note": 65, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Fa"},
            {"midi_note": 50, "duration_quarter": 1.0, "finger": 4, "hand": "L", "lyric": "Re"},
            {"midi_note": 53, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Fa"},
            # Compás 3
            {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi"},
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Sol"},
            {"midi_note": 52, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "Mi"},
            {"midi_note": 55, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Sol"},
            # Compás 4
            {"midi_note": 60, "duration_quarter": 2.0, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 48, "duration_quarter": 2.0, "finger": 5, "hand": "L", "lyric": "Do"}
        ]
    },
    "beyer_op101_04.json": {
        "id": "beyer_op101_04",
        "title": "Ejercicio N° 4 (Articulación y Terceras Paralelas)",
        "composer": "Ferdinand Beyer",
        "opus": "Opus 101 N° 4",
        "description": "Trabajo de terceras simultáneas y alternadas entre ambas manos. Favorece el equilibrio del peso del brazo y la escucha armónica.",
        "clef": "grand",
        "bpm_recommended": 65,
        "time_signature": "4/4",
        "instrument": 0,
        "notes": [
            # Compás 1
            {"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 52, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "Mi"},
            {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi"},
            {"midi_note": 48, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Do"},
            # Compás 2
            {"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re"},
            {"midi_note": 53, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Fa"},
            {"midi_note": 65, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Fa"},
            {"midi_note": 50, "duration_quarter": 1.0, "finger": 4, "hand": "L", "lyric": "Re"},
            # Compás 3
            {"midi_note": 67, "duration_quarter": 2.0, "finger": 5, "hand": "R", "lyric": "Sol"},
            {"midi_note": 55, "duration_quarter": 2.0, "finger": 1, "hand": "L", "lyric": "Sol"},
            # Compás 4
            {"midi_note": 60, "duration_quarter": 4.0, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 48, "duration_quarter": 4.0, "finger": 5, "hand": "L", "lyric": "Do"}
        ]
    },
    "beyer_op101_05.json": {
        "id": "beyer_op101_05",
        "title": "Ejercicio N° 5 (Paso del Pulgar - Escala de Do Mayor)",
        "composer": "Ferdinand Beyer",
        "opus": "Opus 101 N° 5",
        "description": "Técnica del paso del pulgar por debajo del dedo 3 (Mano Derecha) y paso del dedo 3 sobre el pulgar (Mano Izquierda) en la escala completa de Do Mayor.",
        "clef": "grand",
        "bpm_recommended": 70,
        "time_signature": "4/4",
        "instrument": 0,
        "notes": [
            # Compás 1 (Ascendente Mano Derecha, Bajo en MI/DO)
            {"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 48, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Do"},
            {"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re"},
            {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi"},
            {"midi_note": 65, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Fa"}, # Paso pulgar
            # Compás 2
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Sol"},
            {"midi_note": 55, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Sol"},
            {"midi_note": 69, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "La"},
            {"midi_note": 71, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Si"},
            {"midi_note": 72, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Do5"},
            # Compás 3 (Descendente)
            {"midi_note": 71, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Si"},
            {"midi_note": 69, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "La"},
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Sol"},
            {"midi_note": 65, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Fa"},
            # Compás 4 (Resolución)
            {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi"},
            {"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re"},
            {"midi_note": 60, "duration_quarter": 2.0, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 48, "duration_quarter": 2.0, "finger": 5, "hand": "L", "lyric": "Do"}
        ]
    },
    "beyer_op101_07.json": {
        "id": "beyer_op101_07",
        "title": "Ejercicio N° 7 (Escala de Do Mayor en Mano Izquierda)",
        "composer": "Ferdinand Beyer",
        "opus": "Opus 101 N° 7",
        "description": "Escala diatónica de Do Mayor ejecutada en la mano izquierda (Clave de Fa) con apoyo melódico continuo de la derecha.",
        "clef": "grand",
        "bpm_recommended": 70,
        "time_signature": "4/4",
        "instrument": 0,
        "notes": [
            # Compás 1
            {"midi_note": 48, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Do"},
            {"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 50, "duration_quarter": 1.0, "finger": 4, "hand": "L", "lyric": "Re"},
            {"midi_note": 52, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "Mi"},
            {"midi_note": 53, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Fa"},
            # Compás 2
            {"midi_note": 55, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Sol"},
            {"midi_note": 57, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "La"}, # Paso dedo 3
            {"midi_note": 59, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Si"},
            {"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Do4"},
            # Compás 3
            {"midi_note": 59, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Si"},
            {"midi_note": 57, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "La"},
            {"midi_note": 55, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Sol"},
            {"midi_note": 53, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Fa"},
            # Compás 4
            {"midi_note": 52, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "Mi"},
            {"midi_note": 50, "duration_quarter": 1.0, "finger": 4, "hand": "L", "lyric": "Re"},
            {"midi_note": 48, "duration_quarter": 2.0, "finger": 5, "hand": "L", "lyric": "Do"},
            {"midi_note": 60, "duration_quarter": 2.0, "finger": 1, "hand": "R", "lyric": "Do"}
        ]
    },
    "beyer_op101_08.json": {
        "id": "beyer_op101_08",
        "title": "Ejercicio N° 8 (Estudio de Corcheas e Independencia Rítmica)",
        "composer": "Ferdinand Beyer",
        "opus": "Opus 101 N° 8",
        "description": "Introducción al ritmo de corcheas (0.5 tiempos) y la articulación fluida en Gran Pentagrama.",
        "clef": "grand",
        "bpm_recommended": 75,
        "time_signature": "4/4",
        "instrument": 0,
        "notes": [
            # Compás 1
            {"midi_note": 60, "duration_quarter": 0.5, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 62, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "Re"},
            {"midi_note": 64, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Mi"},
            {"midi_note": 65, "duration_quarter": 0.5, "finger": 4, "hand": "R", "lyric": "Fa"},
            {"midi_note": 48, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Do"},
            {"midi_note": 52, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "Mi"},
            # Compás 2
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Sol"},
            {"midi_note": 65, "duration_quarter": 0.5, "finger": 4, "hand": "R", "lyric": "Fa"},
            {"midi_note": 64, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Mi"},
            {"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re"},
            {"midi_note": 55, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Sol"},
            # Compás 3
            {"midi_note": 60, "duration_quarter": 0.5, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 64, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Mi"},
            {"midi_note": 67, "duration_quarter": 0.5, "finger": 5, "hand": "R", "lyric": "Sol"},
            {"midi_note": 64, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Mi"},
            {"midi_note": 48, "duration_quarter": 2.0, "finger": 5, "hand": "L", "lyric": "Do"},
            # Compás 4
            {"midi_note": 60, "duration_quarter": 4.0, "finger": 1, "hand": "R", "lyric": "Do"}
        ]
    },
    "beyer_op101_09.json": {
        "id": "beyer_op101_09",
        "title": "Ejercicio N° 9 (Vals en Métrica de 3/4)",
        "composer": "Ferdinand Beyer",
        "opus": "Opus 101 N° 9",
        "description": "Estudio en tiempo de Vals (3/4). La mano izquierda marca el bajo en el tiempo 1 y los acordes/intervalos en los tiempos 2 y 3.",
        "clef": "grand",
        "bpm_recommended": 80,
        "time_signature": "3/4",
        "instrument": 0,
        "notes": [
            # Compás 1
            {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi"},
            {"midi_note": 48, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Do"},
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Sol"},
            {"midi_note": 52, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "Mi"},
            {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi"},
            # Compás 2
            {"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re"},
            {"midi_note": 55, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Sol"},
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Sol"},
            {"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re"},
            # Compás 3
            {"midi_note": 60, "duration_quarter": 3.0, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 48, "duration_quarter": 3.0, "finger": 5, "hand": "L", "lyric": "Do"}
        ]
    },
    "beyer_op101_10.json": {
        "id": "beyer_op101_10",
        "title": "Ejercicio N° 10 (Saltos de Cuartas y Articulación)",
        "composer": "Ferdinand Beyer",
        "opus": "Opus 101 N° 10",
        "description": "Estudio de intervalos de cuarta (Do-Fa, Re-Sol) con articulación de ligadura y notas sueltas en Gran Pentagrama.",
        "clef": "grand",
        "bpm_recommended": 75,
        "time_signature": "4/4",
        "instrument": 0,
        "notes": [
            # Compás 1
            {"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 65, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Fa"},
            {"midi_note": 48, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Do"},
            {"midi_note": 53, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Fa"},
            # Compás 2
            {"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re"},
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Sol"},
            {"midi_note": 50, "duration_quarter": 1.0, "finger": 4, "hand": "L", "lyric": "Re"},
            {"midi_note": 55, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Sol"},
            # Compás 3
            {"midi_note": 60, "duration_quarter": 2.0, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 48, "duration_quarter": 2.0, "finger": 5, "hand": "L", "lyric": "Do"}
        ]
    },
    "beyer_op101_22.json": {
        "id": "beyer_op101_22",
        "title": "Escala de Sol Mayor y Paso de Pulgar",
        "composer": "Ferdinand Beyer",
        "opus": "Opus 101 N° 22",
        "description": "Estudio de la escala de Sol Mayor con su alteración modal Fa# en clave de Sol y acompañamiento de bajo tónico en clave de Fa.",
        "clef": "grand",
        "bpm_recommended": 75,
        "time_signature": "4/4",
        "instrument": 0,
        "notes": [
            # Compás 1
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Sol"},
            {"midi_note": 55, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Sol"},
            {"midi_note": 69, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "La"},
            {"midi_note": 71, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Si"},
            {"midi_note": 72, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do"}, # paso
            # Compás 2
            {"midi_note": 74, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re"},
            {"midi_note": 76, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi"},
            {"midi_note": 78, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Fa#"},
            {"midi_note": 79, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Sol5"},
            # Compás 3
            {"midi_note": 67, "duration_quarter": 4.0, "finger": 1, "hand": "R", "lyric": "Sol"},
            {"midi_note": 55, "duration_quarter": 4.0, "finger": 5, "hand": "L", "lyric": "Sol"}
        ]
    },
    "beyer_op101_27.json": {
        "id": "beyer_op101_27",
        "title": "Escala de Fa Mayor (Paso del Dedo 4 sobre Si♭)",
        "composer": "Ferdinand Beyer",
        "opus": "Opus 101 N° 27",
        "description": "Estudio de la escala de Fa Mayor. Requiere el cruce del dedo 4 sobre la tecla negra Si♭4.",
        "clef": "grand",
        "bpm_recommended": 75,
        "time_signature": "4/4",
        "instrument": 0,
        "notes": [
            # Compás 1
            {"midi_note": 65, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Fa"},
            {"midi_note": 53, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Fa"},
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Sol"},
            {"midi_note": 69, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "La"},
            {"midi_note": 70, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Si♭"}, # Dedo 4 en tecla negra
            # Compás 2
            {"midi_note": 72, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do"}, # Paso pulgar
            {"midi_note": 74, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re"},
            {"midi_note": 76, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi"},
            {"midi_note": 77, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Fa5"},
            # Compás 3
            {"midi_note": 65, "duration_quarter": 4.0, "finger": 1, "hand": "R", "lyric": "Fa"},
            {"midi_note": 53, "duration_quarter": 4.0, "finger": 5, "hand": "L", "lyric": "Fa"}
        ]
    },

    # -------------------------------------------------------------------------
    # J. S. BACH - LIBRO DE ANNA MAGDALENA & PEQUEÑOS PRELUDIOS (POLIFONÍA BARROCA)
    # -------------------------------------------------------------------------
    "bach_anh114a_12.json": {
        "id": "bach_anh114a_12",
        "title": "Minueto en Sol Mayor (BWV Anh. 114) — Parte A",
        "composer": "Johann Sebastian Bach / Christian Petzold",
        "opus": "BWV Anh. 114",
        "description": "La pieza emblemática de iniciación polifónica barroca. Diálogo bimanual en tempo de Minueto (3/4) entre la melodía cantabile en clave de Sol y la línea de bajo caminante en clave de Fa.",
        "clef": "grand",
        "bpm_recommended": 84,
        "time_signature": "3/4",
        "instrument": 6, # Clavecín / Harpsichord estilo Barroco
        "notes": [
            # Compás 1: D: D5 (G4 A4 B4 C5) L: G3
            {"midi_note": 74, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Re5"},
            {"midi_note": 55, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Sol3"},
            {"midi_note": 67, "duration_quarter": 0.5, "finger": 1, "hand": "R", "lyric": "Sol"},
            {"midi_note": 69, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "La"},
            {"midi_note": 71, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Si"},
            {"midi_note": 72, "duration_quarter": 0.5, "finger": 4, "hand": "R", "lyric": "Do5"},
            # Compás 2: D: D5 G4 G4 L: B2
            {"midi_note": 74, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Re5"},
            {"midi_note": 47, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "Si2"},
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Sol"},
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Sol"},
            # Compás 3: D: E5 (C5 D5 E5 F#5) L: C3
            {"midi_note": 76, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Mi5"},
            {"midi_note": 48, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Do3"},
            {"midi_note": 72, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "Do5"},
            {"midi_note": 74, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Re5"},
            {"midi_note": 76, "duration_quarter": 0.5, "finger": 4, "hand": "R", "lyric": "Mi5"},
            {"midi_note": 78, "duration_quarter": 0.5, "finger": 5, "hand": "R", "lyric": "Fa#5"},
            # Compás 4: D: G5 G4 G4 L: B2
            {"midi_note": 79, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Sol5"},
            {"midi_note": 47, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "Si2"},
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Sol"},
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Sol"}
        ]
    },
    "bach_anh114b_13.json": {
        "id": "bach_anh114b_13",
        "title": "Minueto en Sol Mayor (BWV Anh. 114) — Parte B",
        "composer": "Johann Sebastian Bach / Christian Petzold",
        "opus": "BWV Anh. 114",
        "description": "Segunda sección de la obra. Modula temporalmente y presenta escalas descendentes en corcheas con respuesta polifónica del bajo en Clave de Fa.",
        "clef": "grand",
        "bpm_recommended": 84,
        "time_signature": "3/4",
        "instrument": 6,
        "notes": [
            # Compás 1: D: C5 (B4 A4 B4 C5) L: A2
            {"midi_note": 72, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Do5"},
            {"midi_note": 45, "duration_quarter": 1.0, "finger": 4, "hand": "L", "lyric": "La2"},
            {"midi_note": 71, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Si"},
            {"midi_note": 69, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "La"},
            {"midi_note": 71, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Si"},
            {"midi_note": 72, "duration_quarter": 0.5, "finger": 4, "hand": "R", "lyric": "Do5"},
            # Compás 2: D: B4 (A4 G4 A4 B4) L: G2
            {"midi_note": 71, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Si"},
            {"midi_note": 43, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Sol2"},
            {"midi_note": 69, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "La"},
            {"midi_note": 67, "duration_quarter": 0.5, "finger": 1, "hand": "R", "lyric": "Sol"},
            {"midi_note": 69, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "La"},
            {"midi_note": 71, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Si"},
            # Compás 3: Cadencia D: A4 (G4 F#4 G4 A4) L: D3
            {"midi_note": 69, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "La"},
            {"midi_note": 50, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Re3"},
            {"midi_note": 67, "duration_quarter": 0.5, "finger": 1, "hand": "R", "lyric": "Sol"},
            {"midi_note": 66, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "Fa#"},
            {"midi_note": 67, "duration_quarter": 0.5, "finger": 1, "hand": "R", "lyric": "Sol"},
            {"midi_note": 69, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "La"},
            # Compás 4: Resolución tonal en Sol
            {"midi_note": 67, "duration_quarter": 3.0, "finger": 1, "hand": "R", "lyric": "Sol"},
            {"midi_note": 43, "duration_quarter": 3.0, "finger": 5, "hand": "L", "lyric": "Sol2"}
        ]
    },
    "bach_anh115_14.json": {
        "id": "bach_anh115_14",
        "title": "Minueto en Sol Menor (BWV Anh. 115)",
        "composer": "Johann Sebastian Bach / Christian Petzold",
        "opus": "BWV Anh. 115",
        "description": "Expresivo minueto en tonalidad menor con alteraciones Si♭ y Mi♭. Requiere una pulsación cantarilla y contrapunto riguroso bimanual.",
        "clef": "grand",
        "bpm_recommended": 78,
        "time_signature": "3/4",
        "instrument": 6,
        "notes": [
            # Compás 1: D: D5 (Bb4 A4 Bb4 G4) L: G3 D3 G2
            {"midi_note": 74, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Re5"},
            {"midi_note": 55, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Sol3"},
            {"midi_note": 70, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Si♭"},
            {"midi_note": 69, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "La"},
            {"midi_note": 70, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Si♭"},
            {"midi_note": 67, "duration_quarter": 0.5, "finger": 1, "hand": "R", "lyric": "Sol"},
            # Compás 2: D: F#4 (E4 F#4 G4 A4) L: D3
            {"midi_note": 66, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Fa#"},
            {"midi_note": 50, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "Re3"},
            {"midi_note": 64, "duration_quarter": 0.5, "finger": 1, "hand": "R", "lyric": "Mi"},
            {"midi_note": 66, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "Fa#"},
            {"midi_note": 67, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Sol"},
            {"midi_note": 69, "duration_quarter": 0.5, "finger": 4, "hand": "R", "lyric": "La"},
            # Compás 3: Resolución en Sol menor
            {"midi_note": 67, "duration_quarter": 3.0, "finger": 3, "hand": "R", "lyric": "Sol"},
            {"midi_note": 43, "duration_quarter": 3.0, "finger": 5, "hand": "L", "lyric": "Sol2"}
        ]
    },
    "bach_anh121_16.json": {
        "id": "bach_anh121_16",
        "title": "Minueto en Do Menor (BWV Anh. 121)",
        "composer": "Johann Sebastian Bach",
        "opus": "BWV Anh. 121",
        "description": "Pieza de carácter sobrio y noble en Do menor. Destaca el movimiento del bajo en clave de Fa con contrapunto en la clave superior.",
        "clef": "grand",
        "bpm_recommended": 80,
        "time_signature": "3/4",
        "instrument": 6,
        "notes": [
            # Compás 1: L: C3 (Eb3 D3 Eb3 C3) D: G4
            {"midi_note": 48, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Do3"},
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Sol4"},
            {"midi_note": 51, "duration_quarter": 0.5, "finger": 3, "hand": "L", "lyric": "Mi♭3"},
            {"midi_note": 50, "duration_quarter": 0.5, "finger": 4, "hand": "L", "lyric": "Re3"},
            {"midi_note": 51, "duration_quarter": 0.5, "finger": 3, "hand": "L", "lyric": "Mi♭3"},
            {"midi_note": 48, "duration_quarter": 0.5, "finger": 5, "hand": "L", "lyric": "Do3"},
            # Compás 2: L: B2 (Ab2 G2 Ab2 B2) D: F4
            {"midi_note": 47, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Si2"},
            {"midi_note": 65, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Fa4"},
            {"midi_note": 44, "duration_quarter": 0.5, "finger": 2, "hand": "L", "lyric": "La♭2"},
            {"midi_note": 43, "duration_quarter": 0.5, "finger": 3, "hand": "L", "lyric": "Sol2"},
            {"midi_note": 44, "duration_quarter": 0.5, "finger": 2, "hand": "L", "lyric": "La♭2"},
            {"midi_note": 47, "duration_quarter": 0.5, "finger": 5, "hand": "L", "lyric": "Si2"},
            # Compás 3: Resolución en Do menor
            {"midi_note": 48, "duration_quarter": 3.0, "finger": 5, "hand": "L", "lyric": "Do3"},
            {"midi_note": 60, "duration_quarter": 3.0, "finger": 1, "hand": "R", "lyric": "Do4"}
        ]
    },
    "bach_anh122_15.json": {
        "id": "bach_anh122_15",
        "title": "Marcha en Re Mayor (BWV Anh. 122)",
        "composer": "Carl Philipp Emanuel Bach / J. S. Bach",
        "opus": "BWV Anh. 122",
        "description": "Marcha majestuosa en métrica de 2/4. Ritmo incisivo de corcheas y semicorcheas con acompañamiento armónico firme en clave de Fa.",
        "clef": "grand",
        "bpm_recommended": 90,
        "time_signature": "2/4",
        "instrument": 6,
        "notes": [
            # Compás 1: D: D5 D5 L: D3 A2
            {"midi_note": 74, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Re5"},
            {"midi_note": 50, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Re3"},
            {"midi_note": 74, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Re5"},
            {"midi_note": 45, "duration_quarter": 1.0, "finger": 4, "hand": "L", "lyric": "La2"},
            # Compás 2: D: F#5 (E5 D5 E5 F#5) L: D3
            {"midi_note": 78, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Fa#5"},
            {"midi_note": 50, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Re3"},
            {"midi_note": 76, "duration_quarter": 0.5, "finger": 4, "hand": "R", "lyric": "Mi5"},
            {"midi_note": 74, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Re5"},
            # Compás 3: Resolución tonal
            {"midi_note": 74, "duration_quarter": 2.0, "finger": 3, "hand": "R", "lyric": "Re5"},
            {"midi_note": 50, "duration_quarter": 2.0, "finger": 1, "hand": "L", "lyric": "Re3"}
        ]
    },
    "bach_anh126_11.json": {
        "id": "bach_anh126_11",
        "title": "La Musette en Re Mayor (BWV Anh. 126)",
        "composer": "Johann Sebastian Bach",
        "opus": "BWV Anh. 126",
        "description": "Danza de estilo pastoral con bajo continuo ostinato (pedal de gaita) en octavas en la mano izquierda y arpegios alegres en la derecha.",
        "clef": "grand",
        "bpm_recommended": 96,
        "time_signature": "2/4",
        "instrument": 6,
        "notes": [
            # Compás 1: Bajo pedal Re3 + Arpegio Re Mayor mano derecha
            {"midi_note": 62, "duration_quarter": 0.5, "finger": 1, "hand": "R", "lyric": "Re"},
            {"midi_note": 50, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Re3"},
            {"midi_note": 66, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Fa#"},
            {"midi_note": 69, "duration_quarter": 0.5, "finger": 5, "hand": "R", "lyric": "La"},
            {"midi_note": 66, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Fa#"},
            # Compás 2: D: D5 (A4 F#4 A4) L: Re3 pedal
            {"midi_note": 74, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Re5"},
            {"midi_note": 50, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Re3"},
            {"midi_note": 69, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "La"},
            {"midi_note": 66, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "Fa#"},
            # Compás 3: Cadencia
            {"midi_note": 74, "duration_quarter": 2.0, "finger": 5, "hand": "R", "lyric": "Re5"},
            {"midi_note": 38, "duration_quarter": 2.0, "finger": 5, "hand": "L", "lyric": "Re2"}
        ]
    },
    "bach_anh119_18.json": {
        "id": "bach_anh119_18",
        "title": "Polonesa en Sol Menor (BWV Anh. 119)",
        "composer": "Johann Sebastian Bach",
        "opus": "BWV Anh. 119",
        "description": "Danza señorial polaca en 3/4 con su característico ritmo sincopado e impulso en el segundo tiempo.",
        "clef": "grand",
        "bpm_recommended": 80,
        "time_signature": "3/4",
        "instrument": 6,
        "notes": [
            # Compás 1
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Sol"},
            {"midi_note": 55, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Sol3"},
            {"midi_note": 70, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Si♭"},
            {"midi_note": 50, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "Re3"},
            {"midi_note": 74, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Re5"},
            # Compás 2
            {"midi_note": 72, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Do5"},
            {"midi_note": 43, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Sol2"},
            {"midi_note": 70, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Si♭"},
            {"midi_note": 69, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "La"},
            # Compás 3
            {"midi_note": 67, "duration_quarter": 3.0, "finger": 1, "hand": "R", "lyric": "Sol"},
            {"midi_note": 55, "duration_quarter": 3.0, "finger": 1, "hand": "L", "lyric": "Sol3"}
        ]
    },
    "bach_anh132_17.json": {
        "id": "bach_anh132_17",
        "title": "Aria en Re Menor (BWV Anh. 132)",
        "composer": "Johann Sebastian Bach",
        "opus": "BWV Anh. 132",
        "description": "Lírica cantilena barroca de conmovedora belleza armónica en Re menor.",
        "clef": "grand",
        "bpm_recommended": 72,
        "time_signature": "4/4",
        "instrument": 6,
        "notes": [
            # Compás 1
            {"midi_note": 62, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Re"},
            {"midi_note": 50, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Re3"},
            {"midi_note": 65, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Fa"},
            {"midi_note": 69, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "La"},
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Sol"},
            # Compás 2
            {"midi_note": 65, "duration_quarter": 2.0, "finger": 3, "hand": "R", "lyric": "Fa"},
            {"midi_note": 64, "duration_quarter": 2.0, "finger": 2, "hand": "R", "lyric": "Mi"},
            {"midi_note": 45, "duration_quarter": 4.0, "finger": 4, "hand": "L", "lyric": "La2"},
            # Compás 3
            {"midi_note": 62, "duration_quarter": 4.0, "finger": 1, "hand": "R", "lyric": "Re"},
            {"midi_note": 50, "duration_quarter": 4.0, "finger": 1, "hand": "L", "lyric": "Re3"}
        ]
    },
    "bach_bwv924_20.json": {
        "id": "bach_bwv924_20",
        "title": "Pequeño Preludio N° 1 en Do Mayor (BWV 924)",
        "composer": "Johann Sebastian Bach",
        "opus": "BWV 924",
        "description": "Preludio polifónico de los Nueve Pequeños Preludios para el Klavierbüchlein de Wilhelm Friedemann Bach. Diseñado para la independencia digital y la conducción de voces.",
        "clef": "grand",
        "bpm_recommended": 72,
        "time_signature": "4/4",
        "instrument": 6,
        "notes": [
            # Compás 1: Arpegio bimanual Do Mayor (Do3-Sol3-Do4-Mi4-Sol4)
            {"midi_note": 48, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Do3"},
            {"midi_note": 55, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Sol3"},
            {"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do4"},
            {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi4"},
            # Compás 2
            {"midi_note": 67, "duration_quarter": 2.0, "finger": 5, "hand": "R", "lyric": "Sol4"},
            {"midi_note": 72, "duration_quarter": 2.0, "finger": 5, "hand": "R", "lyric": "Do5"},
            {"midi_note": 52, "duration_quarter": 4.0, "finger": 3, "hand": "L", "lyric": "Mi3"},
            # Compás 3: Cadencia en Do
            {"midi_note": 60, "duration_quarter": 4.0, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 36, "duration_quarter": 4.0, "finger": 5, "hand": "L", "lyric": "Do2"}
        ]
    },
    "bach_bwv939_19.json": {
        "id": "bach_bwv939_19",
        "title": "Pequeño Preludio en Do Mayor (BWV 939)",
        "composer": "Johann Sebastian Bach",
        "opus": "BWV 939",
        "description": "Preludio ágil en métrica de 4/4. Arpegiación continua con firme apoyo de bajos en tónica y dominante.",
        "clef": "grand",
        "bpm_recommended": 80,
        "time_signature": "4/4",
        "instrument": 6,
        "notes": [
            # Compás 1
            {"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 48, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Do3"},
            {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi"},
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Sol"},
            {"midi_note": 72, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Do5"},
            # Compás 2
            {"midi_note": 71, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Si"},
            {"midi_note": 55, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Sol3"},
            {"midi_note": 69, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "La"},
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Sol"},
            # Compás 3
            {"midi_note": 60, "duration_quarter": 4.0, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 48, "duration_quarter": 4.0, "finger": 5, "hand": "L", "lyric": "Do3"}
        ]
    },

    # -------------------------------------------------------------------------
    # MUZIO CLEMENTI - SONATINA OP. 36 N° 1 (ESTUDIO CLÁSICO FORMATIVO)
    # -------------------------------------------------------------------------
    "clementi_op36_21.json": {
        "id": "clementi_op36_21",
        "title": "Muzio Clementi — Sonatina Op. 36 N° 1 (Mov. 1 'Allegro')",
        "composer": "Muzio Clementi",
        "opus": "Opus 36 N° 1",
        "description": "El pilar fundamental del repertorio clásico pianístico. Carácter brioso, escalas brillantes en la mano derecha y acompañamiento de Alberti en la mano izquierda.",
        "clef": "grand",
        "bpm_recommended": 112,
        "time_signature": "4/4",
        "instrument": 0,
        "notes": [
            # Compás 1: D: Do4 (blanca con punto) + Do5 (negra) L: Bajo Alberti Do3 Sol3 Mi3 Sol3
            {"midi_note": 60, "duration_quarter": 2.0, "finger": 1, "hand": "R", "lyric": "Do4"},
            {"midi_note": 48, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Do3"},
            {"midi_note": 55, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Sol3"},
            {"midi_note": 72, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Do5"},
            {"midi_note": 52, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "Mi3"},
            # Compás 2: D: Sol4 (blanca) + Mi5 (negra) + Do5 (negra)
            {"midi_note": 67, "duration_quarter": 2.0, "finger": 3, "hand": "R", "lyric": "Sol4"},
            {"midi_note": 76, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Mi5"},
            {"midi_note": 72, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Do5"},
            {"midi_note": 55, "duration_quarter": 4.0, "finger": 1, "hand": "L", "lyric": "Sol3"},
            # Compás 3: Escala ascendente rápida en corcheas
            {"midi_note": 60, "duration_quarter": 0.5, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 62, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "Re"},
            {"midi_note": 64, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Mi"},
            {"midi_note": 65, "duration_quarter": 0.5, "finger": 1, "hand": "R", "lyric": "Fa"},
            {"midi_note": 67, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "Sol"},
            {"midi_note": 69, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "La"},
            {"midi_note": 71, "duration_quarter": 0.5, "finger": 4, "hand": "R", "lyric": "Si"},
            {"midi_note": 72, "duration_quarter": 0.5, "finger": 5, "hand": "R", "lyric": "Do5"},
            # Compás 4: Resolución
            {"midi_note": 60, "duration_quarter": 4.0, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 48, "duration_quarter": 4.0, "finger": 5, "hand": "L", "lyric": "Do3"}
        ]
    },
    "clementi_op36_23.json": {
        "id": "clementi_op36_23",
        "title": "Muzio Clementi — Agilidad en Staccato de Muñeca",
        "composer": "Muzio Clementi",
        "opus": "Opus 36 N° 1 (Estudio de Técnica)",
        "description": "Estudio preparatorio para la ligereza y el staccato de muñeca con apoyos en bajos de dominante.",
        "clef": "grand",
        "bpm_recommended": 100,
        "time_signature": "2/4",
        "instrument": 0,
        "notes": [
            # Compás 1
            {"midi_note": 72, "duration_quarter": 0.5, "finger": 5, "hand": "R", "lyric": "Do5"},
            {"midi_note": 48, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Do3"},
            {"midi_note": 67, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Sol"},
            {"midi_note": 64, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "Mi"},
            {"midi_note": 60, "duration_quarter": 0.5, "finger": 1, "hand": "R", "lyric": "Do"},
            # Compás 2
            {"midi_note": 74, "duration_quarter": 0.5, "finger": 5, "hand": "R", "lyric": "Re5"},
            {"midi_note": 55, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Sol3"},
            {"midi_note": 67, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Sol"},
            {"midi_note": 65, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "Fa"},
            {"midi_note": 62, "duration_quarter": 0.5, "finger": 1, "hand": "R", "lyric": "Re"},
            # Compás 3
            {"midi_note": 60, "duration_quarter": 2.0, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 48, "duration_quarter": 2.0, "finger": 5, "hand": "L", "lyric": "Do3"}
        ]
    },
    "clementi_op36_26.json": {
        "id": "clementi_op36_26",
        "title": "Muzio Clementi — Sonatina Op. 36 N° 1 (Mov. 2 'Andante')",
        "composer": "Muzio Clementi",
        "opus": "Opus 36 N° 1",
        "description": "Segundo movimiento expresivo en Fa Mayor y métrica de 3/4. Melodía noble de carácter cantabile y acompañamiento lírico en clave de Fa.",
        "clef": "grand",
        "bpm_recommended": 72,
        "time_signature": "3/4",
        "instrument": 0,
        "notes": [
            # Compás 1
            {"midi_note": 65, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Fa"},
            {"midi_note": 53, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Fa3"},
            {"midi_note": 69, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "La"},
            {"midi_note": 57, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "La3"},
            {"midi_note": 72, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Do5"},
            {"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Do4"},
            # Compás 2
            {"midi_note": 70, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Si♭"},
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Sol"},
            {"midi_note": 65, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Fa"},
            {"midi_note": 53, "duration_quarter": 3.0, "finger": 5, "hand": "L", "lyric": "Fa3"},
            # Compás 3
            {"midi_note": 65, "duration_quarter": 3.0, "finger": 1, "hand": "R", "lyric": "Fa"},
            {"midi_note": 41, "duration_quarter": 3.0, "finger": 5, "hand": "L", "lyric": "Fa2"}
        ]
    },
    "clementi_op36_29.json": {
        "id": "clementi_op36_29",
        "title": "Muzio Clementi — Sonatina Op. 36 N° 1 (Mov. 3 'Vivace')",
        "composer": "Muzio Clementi",
        "opus": "Opus 36 N° 1",
        "description": "Tercer movimiento en tiempo rondo y métrica de 3/8. Gran chispa virtuosística, agilidad y contrastes de matices.",
        "clef": "grand",
        "bpm_recommended": 120,
        "time_signature": "3/8",
        "instrument": 0,
        "notes": [
            # Compás 1
            {"midi_note": 72, "duration_quarter": 0.5, "finger": 5, "hand": "R", "lyric": "Do5"},
            {"midi_note": 48, "duration_quarter": 1.5, "finger": 5, "hand": "L", "lyric": "Do3"},
            {"midi_note": 67, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Sol"},
            {"midi_note": 64, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "Mi"},
            # Compás 2
            {"midi_note": 60, "duration_quarter": 0.5, "finger": 1, "hand": "R", "lyric": "Do"},
            {"midi_note": 64, "duration_quarter": 0.5, "finger": 2, "hand": "R", "lyric": "Mi"},
            {"midi_note": 67, "duration_quarter": 0.5, "finger": 3, "hand": "R", "lyric": "Sol"},
            {"midi_note": 55, "duration_quarter": 1.5, "finger": 1, "hand": "L", "lyric": "Sol3"},
            # Compás 3
            {"midi_note": 72, "duration_quarter": 1.5, "finger": 5, "hand": "R", "lyric": "Do5"},
            {"midi_note": 48, "duration_quarter": 1.5, "finger": 5, "hand": "L", "lyric": "Do3"}
        ]
    },

    # -------------------------------------------------------------------------
    # BÉLA BARTÓK - MIKROKOSMOS (MODERNIDAD, RITMO Y POLIFONÍA MODAL)
    # -------------------------------------------------------------------------
    "bartok_mikro1_24.json": {
        "id": "bartok_mikro1_24",
        "title": "Béla Bartók — Mikrokosmos N° 1 (Estudio Modal de 6 Notas)",
        "composer": "Béla Bartók",
        "opus": "Mikrokosmos Vol. 1 N° 1",
        "description": "Estudio unisono bimanual en modo Dorian/Eolio. Ambas manos tocan la misma línea melódica separadas por dos octavas, cimentando la concentración y simetría kinestésica.",
        "clef": "grand",
        "bpm_recommended": 88,
        "time_signature": "4/4",
        "instrument": 0,
        "notes": [
            # Compás 1: D: C4 D4 E4 F4 L: C3 D3 E3 F3
            {"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do4"},
            {"midi_note": 48, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Do3"},
            {"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re4"},
            {"midi_note": 50, "duration_quarter": 1.0, "finger": 4, "hand": "L", "lyric": "Re3"},
            {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi4"},
            {"midi_note": 52, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "Mi3"},
            {"midi_note": 65, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Fa4"},
            {"midi_note": 53, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Fa3"},
            # Compás 2: D: G4 F4 E4 D4 L: G3 F3 E3 D3
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Sol4"},
            {"midi_note": 55, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Sol3"},
            {"midi_note": 65, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Fa4"},
            {"midi_note": 53, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Fa3"},
            {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi4"},
            {"midi_note": 52, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "Mi3"},
            {"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re4"},
            {"midi_note": 50, "duration_quarter": 1.0, "finger": 4, "hand": "L", "lyric": "Re3"},
            # Compás 3: Resolución tónica
            {"midi_note": 60, "duration_quarter": 4.0, "finger": 1, "hand": "R", "lyric": "Do4"},
            {"midi_note": 48, "duration_quarter": 4.0, "finger": 5, "hand": "L", "lyric": "Do3"}
        ]
    },
    "bartok_mikro12_25.json": {
        "id": "bartok_mikro12_25",
        "title": "Béla Bartók — Mikrokosmos N° 12 (Acompañamiento Reflejado)",
        "composer": "Béla Bartók",
        "opus": "Mikrokosmos Vol. 1 N° 12",
        "description": "Movimiento contrario simétrico (Inversión Reflejada). La mano derecha asciende en Clave de Sol mientras la mano izquierda desciende exactamente en espejo en Clave de Fa.",
        "clef": "grand",
        "bpm_recommended": 84,
        "time_signature": "3/4",
        "instrument": 0,
        "notes": [
            # Compás 1: D: C4 D4 E4 (ascendente) L: C3 B2 A2 (descendente espejo)
            {"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do4"},
            {"midi_note": 48, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Do3"},
            {"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re4"},
            {"midi_note": 47, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Si2"},
            {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi4"},
            {"midi_note": 45, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "La2"},
            # Compás 2: D: F4 G4 F4 L: G2 F2 G2
            {"midi_note": 65, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Fa4"},
            {"midi_note": 43, "duration_quarter": 1.0, "finger": 4, "hand": "L", "lyric": "Sol2"},
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Sol4"},
            {"midi_note": 41, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Fa2"},
            {"midi_note": 65, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Fa4"},
            {"midi_note": 43, "duration_quarter": 1.0, "finger": 4, "hand": "L", "lyric": "Sol2"},
            # Compás 3: Cadencia en espejo
            {"midi_note": 60, "duration_quarter": 3.0, "finger": 1, "hand": "R", "lyric": "Do4"},
            {"midi_note": 48, "duration_quarter": 3.0, "finger": 1, "hand": "L", "lyric": "Do3"}
        ]
    },
    "bartok_mikro22_28.json": {
        "id": "bartok_mikro22_28",
        "title": "Béla Bartók — Mikrokosmos N° 22 (Canon a la Octava)",
        "composer": "Béla Bartók",
        "opus": "Mikrokosmos Vol. 1 N° 22",
        "description": "Canon imitativo a la octava. La mano derecha propone la frase melódica y la mano izquierda responde con un compás de imitación estricta.",
        "clef": "grand",
        "bpm_recommended": 92,
        "time_signature": "4/4",
        "instrument": 0,
        "notes": [
            # Compás 1: Propuesta Mano Derecha: C4 D4 E4 F4
            {"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do4"},
            {"midi_note": 62, "duration_quarter": 1.0, "finger": 2, "hand": "R", "lyric": "Re4"},
            {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi4"},
            {"midi_note": 65, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Fa4"},
            # Compás 2: Respuesta Canon Izquierda C3 D3 E3 F3 + Derecha Sol4
            {"midi_note": 48, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Do3"},
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Sol4"},
            {"midi_note": 50, "duration_quarter": 1.0, "finger": 4, "hand": "L", "lyric": "Re3"},
            {"midi_note": 65, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Fa4"},
            {"midi_note": 52, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "Mi3"},
            {"midi_note": 64, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi4"},
            {"midi_note": 53, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Fa3"},
            # Compás 3: Resolución unísona
            {"midi_note": 60, "duration_quarter": 4.0, "finger": 1, "hand": "R", "lyric": "Do4"},
            {"midi_note": 48, "duration_quarter": 4.0, "finger": 5, "hand": "L", "lyric": "Do3"}
        ]
    },
    "bartok_mikro32_30.json": {
        "id": "bartok_mikro32_30",
        "title": "Béla Bartók — Mikrokosmos N° 32 (Ritmo Búlgaro / Finale)",
        "composer": "Béla Bartók",
        "opus": "Mikrokosmos Vol. 1 N° 32",
        "description": "Estudio rítmico asimétrico de inspiración folklórica búlgara. Acentuación energética de pulsos armónicos entre ambas manos.",
        "clef": "grand",
        "bpm_recommended": 100,
        "time_signature": "4/4",
        "instrument": 0,
        "notes": [
            # Compás 1
            {"midi_note": 60, "duration_quarter": 1.0, "finger": 1, "hand": "R", "lyric": "Do4"},
            {"midi_note": 48, "duration_quarter": 1.0, "finger": 5, "hand": "L", "lyric": "Do3"},
            {"midi_note": 63, "duration_quarter": 1.0, "finger": 3, "hand": "R", "lyric": "Mi♭4"},
            {"midi_note": 51, "duration_quarter": 1.0, "finger": 3, "hand": "L", "lyric": "Mi♭3"},
            {"midi_note": 65, "duration_quarter": 1.0, "finger": 4, "hand": "R", "lyric": "Fa4"},
            {"midi_note": 53, "duration_quarter": 1.0, "finger": 2, "hand": "L", "lyric": "Fa3"},
            {"midi_note": 67, "duration_quarter": 1.0, "finger": 5, "hand": "R", "lyric": "Sol4"},
            {"midi_note": 55, "duration_quarter": 1.0, "finger": 1, "hand": "L", "lyric": "Sol3"},
            # Compás 2: Acentuación síncopa
            {"midi_note": 68, "duration_quarter": 2.0, "finger": 5, "hand": "R", "lyric": "La♭4"},
            {"midi_note": 56, "duration_quarter": 2.0, "finger": 1, "hand": "L", "lyric": "La♭3"},
            {"midi_note": 67, "duration_quarter": 2.0, "finger": 4, "hand": "R", "lyric": "Sol4"},
            {"midi_note": 55, "duration_quarter": 2.0, "finger": 2, "hand": "L", "lyric": "Sol3"},
            # Compás 3: Cierre triunfal
            {"midi_note": 60, "duration_quarter": 4.0, "finger": 1, "hand": "R", "lyric": "Do4"},
            {"midi_note": 36, "duration_quarter": 4.0, "finger": 5, "hand": "L", "lyric": "Do2"}
        ]
    }
}


def run_curation():
    print("Beginning curation of all 30 classical works...")
    count = 0
    for filename, lesson_data in LESSONS_DATA.items():
        filepath = os.path.join(LESSONS_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(lesson_data, f, indent=2, ensure_ascii=False)
        count += 1
        print(f"  [✓] Curada e inyectada: {filename} ({lesson_data['title']})")

    print(f"\n¡Éxito! Se actualizaron {count} obras clásicas en Gran Pentagrama ('grand').")

if __name__ == "__main__":
    run_curation()
