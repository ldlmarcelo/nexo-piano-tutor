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
class TargetStep:
    """Un paso temporal pedagógico que puede contener 1 nota (melódica) o varias notas simultáneas (acorde/unísono)."""
    duration_quarter: float = 1.0
    notes: List[TargetNote] = field(default_factory=list)

    @property
    def is_chord(self) -> bool:
        return len(self.notes) > 1

    @property
    def is_bimanual(self) -> bool:
        hands = {n.hand for n in self.notes}
        return len(hands) > 1


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
    time_signature: str = "4/4" # Compás musical ("4/4", "3/4", "2/4", etc.)
    instrument: int = 0       # Programa General MIDI (0 = Piano, 6 = Clavecín, 19 = Órgano)
    duet_mode: bool = False
    secondo_tutor: Optional[dict] = None
    notes: List[TargetNote] = field(default_factory=list)
    steps: List[TargetStep] = field(default_factory=list)

    def get_steps(self) -> List[TargetStep]:
        """Retorna la lista de Pasos Polifónicos. Si la lección fue cargada desde notas planas, los convierte dinámicamente."""
        if self.steps:
            return self.steps
        res = []
        for n in self.notes:
            res.append(TargetStep(duration_quarter=n.duration_quarter, notes=[n]))
        return res


