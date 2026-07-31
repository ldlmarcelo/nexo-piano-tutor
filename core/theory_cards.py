"""
Biblioteca de Tarjetas Teóricas y Glosario Pedagógico para NEXO Piano Tutor (v1.1.0).
Implementa la Sección 6.2 de PEDAGOGIA_CLASICA.md.
"""

from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class TheoryCard:
    lesson_id: str
    title: str
    subtitle: str
    icon: str
    sections: List[Dict[str, str]]


THEORY_CARDS_DATABASE: Dict[str, TheoryCard] = {
    "beyer_op101_001": TheoryCard(
        lesson_id="beyer_op101_001",
        title="Lección 1: Posición Fija de Do Mayor (Mano Derecha)",
        subtitle="Fundamentos de Lectura y Digitación para Mano Derecha",
        icon="🎼",
        sections=[
            {
                "topic": "1. Posición Fija de 5 Notas",
                "text": "Apoyá tu Dedo 1 (Pulgar) en la tecla Do4 (C4) y asigná un dedo a cada tecla consecutiva hasta Sol4 (Dedo 5). La mano se mantiene curva y articulada sin mover la muñeca."
            },
            {
                "topic": "2. La Métrica de 4/4 y la Clave de Sol",
                "text": "Cada compás suma 4 tiempos (4/4). La Clave de Sol fija la posición de las notas en la parte media/aguda del teclado."
            }
        ]
    ),
    "beyer_op101_002": TheoryCard(
        lesson_id="beyer_op101_002",
        title="Lección 2: Dueto a 4 Manos y Textura Polifónica",
        subtitle="Mano Derecha (Primo) + Acompañamiento Armónico del Tutor (Secondo)",
        icon="🎹",
        sections=[
            {
                "topic": "1. El Concepto de Dueto (4 Manos)",
                "text": "El dueto permite al estudiante concentrarse en la articulación de su melodía mientras el tutor sostiene el ritmo y la armonía con los bajos y acordes en la parte grave."
            },
            {
                "topic": "2. Escucha Activa y Pulso Compartido",
                "text": "Escuchá cómo los acordes de Do Mayor y Sol7 del tutor completan la música. Mantené la pulsación constante respetando los 4 tiempos del compás."
            }
        ]
    )
}

HISTORIA_PIANO_CARD = TheoryCard(
    lesson_id="historia_piano",
    title="La Fragua del Instrumento: Historia del Piano",
    subtitle="De Bartolomeo Cristofori al Piano Moderno",
    icon="🎹",
    sections=[
        {
            "topic": "1. El Nacimiento en Padua (1700)",
            "text": "El piano fue inventado en Italia por Bartolomeo Cristofori hacia el año 1700. Se llamó originalmente 'Gravicembalo col piano e forte' (Clavecín con suave y fuerte) porque permitía controlar la dinámica según la fuerza del dedo."
        },
        {
            "topic": "2. La Evolución de la Mecánica",
            "text": "A diferencia del clavecín (que pellizcaba las cuerdas con plumas), el piano utiliza percutores (martillos de fieltro) que golpean la cuerda y retornan instantáneamente, permitiendo notas cortadas o sostenidas."
        }
    ]
)


def get_theory_card(lesson_id: str) -> TheoryCard | None:
    return THEORY_CARDS_DATABASE.get(lesson_id)
