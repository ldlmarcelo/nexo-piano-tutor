"""
Pruebas Unitarias para la Taxonomía de Capítulos y Tarjetas Teóricas.
"""

import os
import pytest
from core.chapters import CHAPTERS, get_chapter_for_lesson
from core.theory_cards import get_theory_card, THEORY_CARDS_DATABASE, HISTORIA_PIANO_CARD

CARPETA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LESSONS_DIR = os.path.join(CARPETA_RAIZ, "lessons")


def test_chapters_structure():
    assert len(CHAPTERS) == 3

    cap1, cap2, cap3 = CHAPTERS
    assert cap1.number == 1
    assert cap2.number == 2
    assert cap3.number == 3

    assert len(cap1.lesson_ids) == 10
    assert len(cap2.lesson_ids) == 10
    assert len(cap3.lesson_ids) == 10


def test_all_chapter_lesson_ids_exist_on_disk():
    all_json_ids = {
        f.replace(".json", "")
        for f in os.listdir(LESSONS_DIR)
        if f.endswith(".json")
    }

    for ch in CHAPTERS:
        for lid in ch.lesson_ids:
            assert lid in all_json_ids, f"Lección '{lid}' referenciada en {ch.title} no existe en carpeta lessons/."


def test_get_chapter_for_lesson():
    ch1 = get_chapter_for_lesson("beyer_op101_01")
    assert ch1 is not None
    assert ch1.id == "capitulo_1"

    ch2 = get_chapter_for_lesson("bach_bwv924_20")
    assert ch2 is not None
    assert ch2.id == "capitulo_2"

    ch3 = get_chapter_for_lesson("bartok_mikro32_30")
    assert ch3 is not None
    assert ch3.id == "capitulo_3"

    ch_none = get_chapter_for_lesson("invalido_999")
    assert ch_none is None


def test_theory_cards_retrieval():
    card1 = get_theory_card("beyer_op101_01")
    assert card1 is not None
    assert "Clave de Sol" in card1.title
    assert len(card1.sections) >= 2

    card_invalid = get_theory_card("leccion_inexistente")
    assert card_invalid is None

    assert HISTORIA_PIANO_CARD.title == "La Fragua del Instrumento: Historia del Piano"
