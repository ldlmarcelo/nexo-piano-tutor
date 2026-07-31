"""
Estructura y Taxonomía de Capítulos Pedagógicos de NEXO Piano Tutor.
Organiza las lecciones del repertorio en Capítulos de desarrollo progresivo.
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
        description="Estudios preparatorios de Beyer Op. 101. Posición fija de 5 notas en Do Mayor y dueto a 4 manos con acompañamiento del tutor.",
        lesson_ids=[
            "beyer_op101_001",
            "beyer_op101_002",
        ]
    ),
    ChapterInfo(
        id="capitulo_2",
        number=2,
        title="Capítulo II: Obras Clásicas y Polifónicas del Barroco",
        short_title="Capítulo II: Obras Barrocas",
        icon="🎼",
        level="Intermedio (Grado 2)",
        description="Piezas del Cuaderno de Anna Magdalena Bach. Métrica en 3/4 (Minuet) y contrapunto clásico en clavecín y piano.",
        lesson_ids=[
            "bach_bwv_anh114",
        ]
    )
]


def get_chapter_for_lesson(lesson_id: str) -> Optional[ChapterInfo]:
    """Devuelve el objeto ChapterInfo al que pertenece la lección por su ID."""
    for ch in CHAPTERS:
        if lesson_id in ch.lesson_ids:
            return ch
    return None
