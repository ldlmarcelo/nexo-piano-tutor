"""
Estructura y Taxonomía de Capítulos Pedagógicos de NEXO Piano Tutor.
Organiza las 30 lecciones del repertorio clásico en 3 Capítulos de desarrollo progresivo.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class ChapterInfo:
    id: str
    number: int
    title: str
    short_title: str
    icon: str
    level: str
    description: str
    lesson_ids: List[str]


CHAPTERS: List[ChapterInfo] = [
    ChapterInfo(
        id="capitulo_1",
        number=1,
        title="Capítulo I: Fundamentos Diatónicos y Coordinación Inicial",
        short_title="Capítulo I: Fundamentos Diatónicos",
        icon="📘",
        level="Principiante (Grado 1)",
        description="Estudios preparatorios de Beyer Op. 101, Mikrokosmos I y primeras danzas en Clave de Sol y Fa. Posición fija de Do, movimiento alternado y métrica de 3/4.",
        lesson_ids=[
            "beyer_op101_01",
            "beyer_op101_02",
            "beyer_op101_03",
            "beyer_op101_04",
            "beyer_op101_05",
            "beyer_op101_06",
            "beyer_op101_07",
            "beyer_op101_08",
            "beyer_op101_09",
            "beyer_op101_10",
        ]
    ),
    ChapterInfo(
        id="capitulo_2",
        number=2,
        title="Capítulo II: Articulación, Polifonía Breve y Agilidad Rítmica",
        short_title="Capítulo II: Polifonía & Agilidad",
        icon="📗",
        level="Intermedio Inicial (Grado 2)",
        description="Minuetos, Polonesas y Arias del Cuaderno de Anna Magdalena Bach, Musette, corcheas y Pequeños Preludios. Fraseo staccato/legato e independencia vocal.",
        lesson_ids=[
            "bach_anh126_11",
            "bach_anh114a_12",
            "bach_anh114b_13",
            "bach_anh115_14",
            "bach_anh122_15",
            "bach_anh121_16",
            "bach_anh132_17",
            "bach_anh119_18",
            "bach_bwv939_19",
            "bach_bwv924_20",
        ]
    ),
    ChapterInfo(
        id="capitulo_3",
        number=3,
        title="Capítulo III: Independencia de Manos, Sonatina y Clasicismo",
        short_title="Capítulo III: Sonatinas & Clasicismo",
        icon="📙",
        level="Intermedio (Grado 3)",
        description="Sonatinas Op. 36 N° 1 de Muzio Clementi, cánones a la octava de Bartók y escalas mayores completas. Arpegios, bajo de Alberti, velocidad y forma sonatina.",
        lesson_ids=[
            "clementi_op36_21",
            "beyer_op101_22",
            "clementi_op36_23",
            "bartok_mikro1_24",
            "bartok_mikro12_25",
            "clementi_op36_26",
            "beyer_op101_27",
            "bartok_mikro22_28",
            "clementi_op36_29",
            "bartok_mikro32_30",
        ]
    )
]


def get_chapter_for_lesson(lesson_id: str) -> Optional[ChapterInfo]:
    """Devuelve el objeto ChapterInfo al que pertenece la lección por su ID."""
    for ch in CHAPTERS:
        if lesson_id in ch.lesson_ids:
            return ch
    return None
