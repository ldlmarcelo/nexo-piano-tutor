"""
Biblioteca de Tarjetas Teóricas y Glosario Pedagógico para NEXO Piano Tutor (v1.0.0).
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
    "beyer_op101_01": TheoryCard(
        lesson_id="beyer_op101_01",
        title="Lección 1: Pentagrama, Clave de Sol y Digitación",
        subtitle="Fundamentos de Lectura para Mano Derecha",
        icon="🎼",
        sections=[
            {
                "topic": "1. El Pentagrama",
                "text": "El pentagrama es el conjunto de 5 líneas paralelas y 4 espacios donde se escriben las notas musicales. Se cuentan siempre de abajo hacia arriba (Línea 1 a Línea 5)."
            },
            {
                "topic": "2. La Clave de Sol (𝄞)",
                "text": "La Clave de Sol fija la posición de la nota Sol4 en la 2ª línea del pentagrama. Se utiliza para escribir las notas agudas que interpreta habitualmente la Mano Derecha."
            },
            {
                "topic": "3. Digitación de la Mano Derecha (1 al 5)",
                "text": "En el piano, los dedos se numeran de forma científica:\n• Dedo 1 = Pulgar\n• Dedo 2 = Índice\n• Dedo 3 = Mayor\n• Dedo 4 = Anular\n• Dedo 5 = Meñique\nEn esta lección, apoyá tu Dedo 1 (Pulgar) en la tecla Do4 sin mover la mano."
            }
        ]
    ),
    "beyer_op101_02": TheoryCard(
        lesson_id="beyer_op101_02",
        title="Lección 2: La Clave de Fa y la Mano Izquierda",
        subtitle="Fundamentos de Lectura para Registros Graves",
        icon="𝄢",
        sections=[
            {
                "topic": "1. La Clave de Fa (𝄢)",
                "text": "La Clave de Fa fija la posición de la nota Fa3 en la 4ª línea del pentagrama (entre sus dos puntos). Se utiliza para escribir los sonidos graves interpretados por la Mano Izquierda."
            },
            {
                "topic": "2. Digitación de la Mano Izquierda",
                "text": "Al igual que la mano derecha, los dedos van del 1 (Pulgar) al 5 (Meñique).\nEn esta lección de posición fija:\n• Dedo 5 (Meñique) en Do3\n• Dedo 4 (Anular) en Re3\n• Dedo 3 (Mayor) en Mi3\n• Dedo 2 (Índice) en Fa3\n• Dedo 1 (Pulgar) en Sol3."
            },
            {
                "topic": "3. Relajación de Muñeca",
                "text": "Mantené el peso de la mano descansando sobre las yemas y evitá levantar los hombros o tensionar el brazo."
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
