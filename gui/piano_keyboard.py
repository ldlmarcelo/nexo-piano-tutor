"""
Widget de Teclado de Piano Virtual Interactivo (PySide6).
Renderiza 49 teclas (C2 a C6) con respuesta a eventos de ratón y MIDI.
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, QRectF
from PySide6.QtGui import QColor, QPainter, QBrush, QPen, QFont


# Notas MIDI: 36 (C2) a 84 (C6) -> 49 Teclas
START_NOTE = 36  # Do2
END_NOTE = 84    # Do6

# Patrón de notas negras por octava (0=Do, 1=Do#, 2=Re, 3=Re#, 4=Mi, 5=Fa, 6=Fa#, 7=Sol, 8=Sol#, 9=La, 10=La#, 11=Si)
BLACK_KEYS_OCTAVE = {1, 3, 6, 8, 10}


class PianoKeyboard(QWidget):
    """Widget de teclado interactivo para visualización y prueba pedagógica."""

    note_pressed = Signal(int, int)  # (midi_note, velocity)
    note_released = Signal(int)     # (midi_note)

    def __init__(self, parent=None, start_note: int = 36, end_note: int = 84):
        super().__init__(parent)
        self.start_note = start_note
        self.end_note = end_note
        self.setFixedHeight(120)
        self.setMinimumWidth(500)

        # Estado de teclas activadas: note -> color hex/QColor
        self._active_keys: dict[int, str] = {}
        self._mouse_pressed_note: int | None = None

        self.setMouseTracking(True)

    def set_key_active(self, midi_note: int, color: str = "#38bdf8"):
        """Resalta una tecla con un color específico (ej: nota actual o jugada)."""
        self._active_keys[midi_note] = color
        self.update()

    def clear_key_active(self, midi_note: int):
        """Quita el resaltado de una tecla."""
        if midi_note in self._active_keys:
            del self._active_keys[midi_note]
            self.update()

    def clear_all_active(self):
        """Limpia todos los resaltados."""
        self._active_keys.clear()
        self.update()

    # ── Geometría de Teclas ────────────────────────────────────────

    def _get_white_keys(self) -> list[int]:
        return [note for note in range(self.start_note, self.end_note + 1) if (note % 12) not in BLACK_KEYS_OCTAVE]

    def _get_black_keys(self) -> list[int]:
        return [note for note in range(self.start_note, self.end_note + 1) if (note % 12) in BLACK_KEYS_OCTAVE]

    def _get_key_rects(self) -> tuple[dict[int, QRectF], dict[int, QRectF]]:
        """Calcula los rectángulos en coordenadas locales de teclas blancas y negras."""
        white_notes = self._get_white_keys()
        total_white = len(white_notes)
        if total_white == 0:
            return {}, {}

        w = self.width()
        h = self.height()

        white_width = w / total_white
        black_width = white_width * 0.6
        black_height = h * 0.6

        white_rects = {}
        black_rects = {}

        # Mapear nota blanca a su índice visual
        white_indices = {note: idx for idx, note in enumerate(white_notes)}

        for note in range(self.start_note, self.end_note + 1):
            is_black = (note % 12) in BLACK_KEYS_OCTAVE
            if not is_black:
                idx = white_indices[note]
                x = idx * white_width
                white_rects[note] = QRectF(x, 0, white_width, h)
            else:
                # La tecla negra está entre la nota blanca anterior y posterior
                prev_white = note - 1
                if prev_white in white_indices:
                    idx = white_indices[prev_white]
                    x = (idx + 1) * white_width - (black_width / 2)
                    black_rects[note] = QRectF(x, 0, black_width, black_height)

        return white_rects, black_rects

    def _note_at_pos(self, x: float, y: float) -> int | None:
        white_rects, black_rects = self._get_key_rects()

        # Prioridad a teclas negras
        for note, rect in black_rects.items():
            if rect.contains(x, y):
                return note

        for note, rect in white_rects.items():
            if rect.contains(x, y):
                return note

        return None

    # ── Pintado del Widget ─────────────────────────────────────────

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        white_rects, black_rects = self._get_key_rects()

        # 1. Dibujar Teclas Blancas
        for note, rect in white_rects.items():
            if note in self._active_keys:
                brush = QBrush(QColor(self._active_keys[note]))
            else:
                brush = QBrush(QColor("#f8fafc"))

            pen = QPen(QColor("#334155"), 1)
            painter.setPen(pen)
            painter.setBrush(brush)
            painter.drawRoundedRect(rect, 2, 2)

            # Etiqueta de nota en C4 (Do central - MIDI 60)
            if note == 60:
                painter.setPen(QPen(QColor("#0284c7")))
                painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
                painter.drawText(rect, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, "C4")

        # 2. Dibujar Teclas Negras
        for note, rect in black_rects.items():
            if note in self._active_keys:
                brush = QBrush(QColor(self._active_keys[note]))
            else:
                brush = QBrush(QColor("#0f172a"))

            pen = QPen(QColor("#1e293b"), 1)
            painter.setPen(pen)
            painter.setBrush(brush)
            painter.drawRoundedRect(rect, 3, 3)

    # ── Manejo de Eventos de Ratón ─────────────────────────────────

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            note = self._note_at_pos(pos.x(), pos.y())
            if note is not None:
                self._mouse_pressed_note = note
                self.set_key_active(note, "#38bdf8")
                self.note_pressed.emit(note, 100)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self._mouse_pressed_note is not None:
            note = self._mouse_pressed_note
            self.clear_key_active(note)
            self.note_released.emit(note)
            self._mouse_pressed_note = None
