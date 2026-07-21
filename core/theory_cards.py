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
    ),
    "beyer_op101_03": TheoryCard(
        lesson_id="beyer_op101_03",
        title="Lección 3: Saltos de Terceras en Mano Derecha",
        subtitle="Agilidad en Dedos 1, 3 y 5",
        icon="🎵",
        sections=[
            {
                "topic": "1. El Intervalo de Tercera",
                "text": "Una 'tercera' es la distancia entre dos notas separadas por un grado (ej: Do a Mi, o Re a Fa). En la partitura se ve saltando de línea a línea o de espacio a espacio."
            },
            {
                "topic": "2. Articulación de los Dedos Impares",
                "text": "Esta lección ejercita los dedos 1 (Pulgar), 3 (Mayor) y 5 (Meñique). Mantené apoyados los dedos 2 y 4 relajados sobre las teclas sin presionarlas."
            }
        ]
    ),
    "beyer_op101_04": TheoryCard(
        lesson_id="beyer_op101_04",
        title="Lección 4: Saltos de Terceras en Mano Izquierda",
        subtitle="Agilidad en Dedos 5, 3 y 1 en Clave de Fa",
        icon="🎶",
        sections=[
            {
                "topic": "1. Terceras en Clave de Fa",
                "text": "La mano izquierda realiza saltos entre Do3, Mi3 y Sol3. Observá cómo las notas saltan de espacio a espacio dentro del pentagrama grave."
            },
            {
                "topic": "2. Control del Peso",
                "text": "Dejá caer suavemente el peso de la mano sobre el meñique (5) al tocar Do3 y apoyá el pulgar (1) para Sol3."
            }
        ]
    ),
    "beyer_op101_05": TheoryCard(
        lesson_id="beyer_op101_05",
        title="Lección 5: El Paso del Pulgar (Escala de Do Mayor)",
        subtitle="Extensión Dinámica del Teclado",
        icon="🚀",
        sections=[
            {
                "topic": "1. La Técnica del Paso del Pulgar",
                "text": "Para tocar más de 5 notas seguidas, la mano no 'salta', sino que el pulgar (1) pasa por debajo del dedo mayor (3) para alcanzar la nota Fa4 sin interrumpir el sonido legato."
            },
            {
                "topic": "2. Secuencia de Digitación Ascendente",
                "text": "Do4(1) ➔ Re4(2) ➔ Mi4(3) ➔ [PASO] ➔ Fa4(1) ➔ Sol4(2) ➔ La4(3) ➔ Si4(4) ➔ Do5(5)."
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
