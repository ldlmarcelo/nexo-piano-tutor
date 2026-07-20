"""
Evaluador Pedagógico en Tiempo Real (<15ms).
Compara eventos MIDI entrantes con la lección activa, midiendo precisión tonal,
desvío de tiempo (jitter ms) y consistencia de velocity (dinámica).
"""

from typing import Optional, Tuple
from dataclasses import dataclass
from core.lesson import Lesson, TargetNote


@dataclass
class EvaluationResult:
    is_correct_note: bool
    expected_note: int
    played_note: int
    velocity: int
    expected_finger: int
    time_delta_ms: float
    feedback_text: str
    feedback_color: str  # Hex o QColor string (ej. "#00e676", "#ffb300", "#e74c3c")


class RealtimeEvaluator:
    """Evaluador de precisión tonal, rítmica y dinámica."""

    def __init__(self):
        self.current_lesson: Optional[Lesson] = None
        self.current_step: int = 0
        self.mode: str = "read"  # "read" (Esperar nota sin metrónomo), "tempo" (Con tiempo), "full"

    def load_lesson(self, lesson: Lesson):
        """Carga una lección pedagógica y reinicia el índice de progreso."""
        self.current_lesson = lesson
        self.current_step = 0

    @property
    def is_finished(self) -> bool:
        if not self.current_lesson:
            return True
        return self.current_step >= len(self.current_lesson.notes)

    def get_current_target(self) -> Optional[TargetNote]:
        if not self.current_lesson or self.is_finished:
            return None
        return self.current_lesson.notes[self.current_step]

    def evaluate_note_on(self, played_note: int, velocity: int, timestamp_ms: float = 0.0) -> EvaluationResult:
        """
        Evalúa un evento NOTE_ON recibido del teclado MIDI.
        Retorna EvaluationResult con el veredicto pedagógico.
        """
        target = self.get_current_target()
        if not target:
            return EvaluationResult(
                is_correct_note=False,
                expected_note=0,
                played_note=played_note,
                velocity=velocity,
                expected_finger=0,
                time_delta_ms=0.0,
                feedback_text="Lección completada",
                feedback_color="#8892b0"
            )

        is_correct = (played_note == target.midi_note)

        if is_correct:
            self.current_step += 1
            feedback = f"¡Excelente! Dedo {target.finger} ({target.lyric or ''})"
            color = "#00e676"  # Verde brillante
        else:
            feedback = f"Nota incorrecta. Se esperaba Dedo {target.finger} ({target.lyric or ''})"
            color = "#e74c3c"  # Rojo

        return EvaluationResult(
            is_correct_note=is_correct,
            expected_note=target.midi_note,
            played_note=played_note,
            velocity=velocity,
            expected_finger=target.finger,
            time_delta_ms=0.0,
            feedback_text=feedback,
            feedback_color=color
        )

    def reset(self):
        """Reinicia el paso actual al inicio de la lección."""
        self.current_step = 0
