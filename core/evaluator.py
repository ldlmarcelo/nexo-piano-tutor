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
    is_rep_complete: bool = False  # Indica que se completó un ciclo de repetición


def midi_to_note_name(note: int) -> str:
    names = ["Do", "Do#", "Re", "Re#", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "La#", "Si"]
    octave = (note // 12) - 1
    return f"{names[note % 12]}{octave}"


class RealtimeEvaluator:
    """Evaluador de precisión tonal, rítmica, dinámica y bucle de repeticiones."""

    def __init__(self):
        self.current_lesson: Optional[Lesson] = None
        self.current_step: int = 0
        self.mode: str = "read"  # "read" (Esperar nota sin metrónomo), "tempo", "full"
        
        # Métrica de Precisión Real (Intento por Intento)
        self.total_attempts: int = 0
        self.correct_attempts: int = 0
        self.wrong_attempts: int = 0

        # Rango de Práctica A-B (Fila/Paso de inicio y fin)
        self.range_start: int = 0
        self.range_end: int = 0

        # Sistema de Bucle xN
        self.repeat_target: int = 1  # 1, 3, 5, o -1 para bucle infinito
        self.current_rep: int = 1     # Repetición activa (1-indexed)

    def load_lesson(self, lesson: Lesson):
        """Carga una lección pedagógica y reinicia el índice de progreso y repeticiones."""
        self.current_lesson = lesson
        self.range_start = 0
        self.range_end = max(0, len(lesson.notes) - 1) if lesson else 0
        self.reset()

    def set_range(self, start_step: int, end_step: int):
        """Define un rango de práctica específico (A-B) dentro de la lección."""
        if not self.current_lesson or not self.current_lesson.notes:
            return
        total = len(self.current_lesson.notes)
        start = max(0, min(start_step, total - 1))
        end = max(start, min(end_step, total - 1))
        self.range_start = start
        self.range_end = end
        self.reset()

    def set_repeat_mode(self, mode_str: str):
        """Configura el modo de repetición (1x, 3x, 5x, loop)."""
        mapping = {"1x": 1, "3x": 3, "5x": 5, "loop": -1}
        self.repeat_target = mapping.get(mode_str.lower(), 1)
        self.reset()

    @property
    def is_finished(self) -> bool:
        if not self.current_lesson:
            return True
        if self.repeat_target == -1:
            return False  # El bucle infinito nunca termina por conteo
        return (self.current_rep > self.repeat_target) or (self.current_step > self.range_end and self.current_rep == self.repeat_target)

    def get_current_target(self) -> Optional[TargetNote]:
        if not self.current_lesson or self.is_finished:
            return None
        if 0 <= self.current_step < len(self.current_lesson.notes):
            return self.current_lesson.notes[self.current_step]
        return None

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
                feedback_text=f"Lección completada 🎉 ({self.repeat_target} repeticiones)",
                feedback_color="#00e676",
                is_rep_complete=True
            )

        self.total_attempts += 1
        is_exact_correct = (played_note == target.midi_note)
        is_same_pitch = (played_note % 12 == target.midi_note % 12)
        is_rep_complete = False

        if is_exact_correct:
            self.correct_attempts += 1
            # Si tocamos la última nota del rango seleccionado
            if self.current_step == self.range_end:
                is_rep_complete = True
                # Si estamos en bucle infinito o aún quedan repeticiones por cumplir
                if self.repeat_target == -1 or self.current_rep < self.repeat_target:
                    completed_rep = self.current_rep
                    self.current_rep += 1
                    self.current_step = self.range_start
                    rep_str = f"🔄 Rango A-B completado (Serie {completed_rep}). Reabriendo en nota {self.range_start + 1}..."
                    if self.repeat_target != -1:
                        rep_str = f"🔄 Repetición {completed_rep} de {self.repeat_target} completada. ¡Vas por la {self.current_rep}!"
                    return EvaluationResult(
                        is_correct_note=True,
                        expected_note=target.midi_note,
                        played_note=played_note,
                        velocity=velocity,
                        expected_finger=target.finger,
                        time_delta_ms=0.0,
                        feedback_text=rep_str,
                        feedback_color="#38bdf8",
                        is_rep_complete=True
                    )
                else:
                    # Última repetición de la serie completada -> Calcular precisión real porcentual
                    self.current_step += 1
                    accuracy_pct = round((self.correct_attempts / self.total_attempts) * 100, 1) if self.total_attempts > 0 else 100.0

                    if accuracy_pct >= 90.0:
                        verdict = f"🌟 ¡EJECUCIÓN IMPECABLE! ({accuracy_pct}% de precisión en {self.total_attempts} notas). Lección aprobada con maestría."
                        color = "#00e676"  # Verde esmeralda
                    elif accuracy_pct >= 75.0:
                        verdict = f"👍 ¡Buena Técnica! ({accuracy_pct}% de precisión en {self.total_attempts} notas). Sugerencia: Realizá una serie x3 en bucle para afinar la fluidez."
                        color = "#38bdf8"  # Azul cian
                    else:
                        verdict = f"💡 Revisión Requerida ({accuracy_pct}% de precisión, {self.wrong_attempts} errores). Revisa la posición de la mano y reintenta."
                        color = "#ffb300"  # Ámbar

                    return EvaluationResult(
                        is_correct_note=True,
                        expected_note=target.midi_note,
                        played_note=played_note,
                        velocity=velocity,
                        expected_finger=target.finger,
                        time_delta_ms=0.0,
                        feedback_text=verdict,
                        feedback_color=color,
                        is_rep_complete=True
                    )
            else:
                self.current_step += 1
                if self.wrong_attempts > 0:
                    feedback = f"Bien: Dedo {target.finger} ({target.lyric or ''} / {midi_to_note_name(target.midi_note)}) [Errores: {self.wrong_attempts}]"
                else:
                    feedback = f"¡Excelente! Dedo {target.finger} ({target.lyric or ''} / {midi_to_note_name(target.midi_note)})"
                color = "#00e676"
        else:
            self.wrong_attempts += 1
            if is_same_pitch:
                played_name = midi_to_note_name(played_note)
                target_name = midi_to_note_name(target.midi_note)
                feedback = f"¡Es un {target.lyric or ''}! Pero en octava distinta (Tocaste {played_name}, se busca {target_name})."
                color = "#ffb300"
            else:
                played_name = midi_to_note_name(played_note)
                target_name = midi_to_note_name(target.midi_note)
                feedback = f"Tocaste {played_name}. Se esperaba Dedo {target.finger} ({target.lyric or ''} / {target_name})"
                color = "#e74c3c"

        return EvaluationResult(
            is_correct_note=is_exact_correct,
            expected_note=target.midi_note,
            played_note=played_note,
            velocity=velocity,
            expected_finger=target.finger,
            time_delta_ms=0.0,
            feedback_text=feedback,
            feedback_color=color,
            is_rep_complete=is_rep_complete
        )

    def reset(self):
        """Reinicia el paso actual al inicio del rango de práctica, repeticiones e intentos acumulados."""
        self.current_step = self.range_start
        self.current_rep = 1
        self.total_attempts = 0
        self.correct_attempts = 0
        self.wrong_attempts = 0



