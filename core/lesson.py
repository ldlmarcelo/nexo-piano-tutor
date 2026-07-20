"""
Modelos de Datos para Lecciones Pedagógicas de Piano.
Representa notas esperadas, digitación sugerida, compases y modos de evaluación.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TargetNote:
    """Una nota esperada dentro de una lección."""
    midi_note: int            # Número de nota MIDI (ej: 60 = C4)
    duration_quarter: float   # Duración en tiempos (1.0 = Negra, 0.5 = Corchea, 2.0 = Blanca)
    finger: int               # Digitación recomendada (1 = Pulgar, 5 = Meñique)
    hand: str = "R"           # 'R' (Mano Derecha / Clave de Sol) o 'L' (Mano Izquierda / Clave de Fa)
    lyric: Optional[str] = None # Texto o sílaba descriptiva (ej. "Do", "Re", "Mi")


@dataclass
class Lesson:
    """Lección pedagógica estructurada."""
    id: str
    title: str
    composer: str
    opus: str
    description: str
    clef: str                 # "treble" (Sol), "bass" (Fa), "grand" (Ambas)
    bpm_recommended: int
    notes: List[TargetNote] = field(default_factory=list)
