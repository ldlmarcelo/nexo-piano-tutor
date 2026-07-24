"""
Renderizador gráfico interactivo de la partitura y la lección en tiempo real.
Muestra el pentagrama (Clave de Sol / Fa), signo de clave, métrica de compás (4/4, 3/4),
figuras rítmicas (redondas, blancas, negras, corchetes, semicorcheas), barras de unión (beaming),
batuta visual de tiempo/pulso, plicas, líneas divisoras de compás,
digitación (1-5 por mano) y cursor de avance en tiempo real.
"""

from typing import Any, Dict, List
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QFontMetrics, QPen, QBrush, QPainter

from core.lesson import Lesson
from gui.smufl import (
    get_smufl_font,
    CLEF_TREBLE,
    CLEF_BASS,
    NOTEHEAD_BLACK,
    NOTEHEAD_HALF,
    NOTEHEAD_WHOLE,
    TIME_SIG_DIGITS,
    FLAG_8TH_UP,
    FLAG_8TH_DOWN,
    FLAG_16TH_UP,
    FLAG_16TH_DOWN,
)

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
SEMITONE_TO_DIATONIC_IN_OCTAVE = [0, 0, 1, 1, 2, 3, 3, 4, 4, 5, 5, 6]


def midi_to_note_name(note: int) -> str:
    octave = (note // 12) - 1
    name = NOTE_NAMES[note % 12]
    return f"{name}{octave}"


def midi_to_diatonic_step(note: int) -> int:
    """Devuelve el índice diatónico absoluto de una nota MIDI (C0 = paso 0, C4 = paso 28)."""
    octave = (note // 12) - 1
    semitone = note % 12
    diatonic_in_octave = SEMITONE_TO_DIATONIC_IN_OCTAVE[semitone]
    return octave * 7 + diatonic_in_octave


class SheetView(QGraphicsView):
    """Vista gráfica interactiva de la lección con notación musical rítmica completa."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sheetView")
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Desactivar barras de desplazamiento manuales (Auto-seguimiento dinámico)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        self._lesson: Lesson = None
        self._current_step: int = 0
        self._range_start: int = 0
        self._range_end: int = -1
        self._error_steps: set[int] = set()
        self._note_results: dict[int, Any] = {}

        # Opciones pedagógicas y visuales avanzadas
        self._beaming_enabled: bool = True
        self._current_beat: int = 1
        self._total_beats: int = 4

    def set_beaming_enabled(self, enabled: bool):
        """Activa o desactiva la unión rítmica de corcheas y semicorcheas (Beaming)."""
        self._beaming_enabled = enabled
        self.redraw()
        self.viewport().update()

    def set_beat(self, beat: int, total_beats: int = 4):
        """Actualiza el tiempo activo de la batuta pedagógica en el compás (1..total_beats)."""
        self._current_beat = max(1, min(beat, total_beats))
        self._total_beats = total_beats
        self.redraw()

    def set_error_steps(self, error_steps: set[int]):
        self._error_steps = set(error_steps)
        self.redraw()

    def set_note_results(self, note_results: dict[int, Any]):
        self._note_results = dict(note_results)
        self.redraw()

    def load_lesson(self, lesson: Lesson, step: int = 0):
        self._lesson = lesson
        self._current_step = step
        self._range_start = 0
        self._range_end = len(lesson.notes) - 1 if lesson and lesson.notes else -1
        self._error_steps.clear()
        self._note_results.clear()
        self.redraw()
        self.center_on_active_step()

    def set_range(self, start_step: int, end_step: int):
        self._range_start = start_step
        self._range_end = end_step
        self.redraw()
        self.center_on_active_step()

    def set_step(self, step: int):
        self._current_step = step
        self.redraw()
        self.center_on_active_step()

    def center_on_active_step(self):
        """Centra automáticamente la vista sobre la nota activa para evitar scroll manual."""
        if not self._lesson or not self._lesson.notes:
            return
        x_start = 135
        x_step = 54
        x_active = x_start + self._current_step * x_step
        self.centerOn(x_active, 110)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.center_on_active_step()

    def redraw(self):
        self._scene.clear()
        if not self._lesson:
            return

        # Geometría del pentagrama (Clave Única vs Gran Pentagrama a Dos Manos)
        is_grand_staff = (self._lesson.clef == "grand" or self._lesson.clef == "both")

        staff_y_treble = 70 if is_grand_staff else 80
        staff_y_bass = 190 if is_grand_staff else 80
        line_spacing = 14
        half_spacing = line_spacing / 2  # 7px por paso diatónico

        # Métrica / Compás (ej: "4/4" -> 4 tiempos de negra por compás)
        ts_str = getattr(self._lesson, "time_signature", "4/4")
        try:
            ts_num, ts_den = map(int, ts_str.split("/"))
        except Exception:
            ts_num, ts_den = 4, 4

        beats_per_measure = float(ts_num)
        self._total_beats = ts_num

        # Ancho adaptable de escena
        x_start = 135  # Espacio tras clave + métrica
        x_step = 54
        width = max(600, len(self._lesson.notes) * x_step + x_start + 60)
        scene_h = 320 if is_grand_staff else 220
        self._scene.setSceneRect(0, 0, width, scene_h)

        pen_staff = QPen(QColor("#475569"), 2)

        if is_grand_staff:
            # 1. DIBUJAR PENTAGRAMA SUPERIOR (Clave de Sol - Mano Derecha)
            for i in range(5):
                y = staff_y_treble + i * line_spacing
                self._scene.addLine(20, y, width - 20, y, pen_staff)

            # 2. DIBUJAR PENTAGRAMA INFERIOR (Clave de Fa - Mano Izquierda)
            for i in range(5):
                y = staff_y_bass + i * line_spacing
                self._scene.addLine(20, y, width - 20, y, pen_staff)

            # 3. LLAVE DE SISTEMA DE PIANO (System Brace & Barra Conectora Izquierda)
            # Linea vertical izquierda uniendo ambos pentagramas
            self._scene.addLine(16, staff_y_treble, 16, staff_y_bass + 4 * line_spacing, pen_staff)
            
            # Llave curva SMuFL (Brace \uE000 / \uE003)
            brace_font = get_smufl_font(52)
            brace_item = self._scene.addText("\uE000", brace_font)
            brace_item.setDefaultTextColor(QColor("#0284c7"))
            brace_item.setPos(4, staff_y_treble - 10)

            # 4. SIGNOS DE CLAVE EN AMBOS PENTAGRAMAS
            clef_font_sol = get_smufl_font(36)
            fm_sol = QFontMetrics(clef_font_sol)
            item_sol = self._scene.addText(CLEF_TREBLE, clef_font_sol)
            item_sol.setDefaultTextColor(QColor("#38bdf8"))
            item_sol.setPos(18, (staff_y_treble + 3 * line_spacing) - fm_sol.ascent())

            clef_font_fa = get_smufl_font(34)
            fm_fa = QFontMetrics(clef_font_fa)
            item_fa = self._scene.addText(CLEF_BASS, clef_font_fa)
            item_fa.setDefaultTextColor(QColor("#38bdf8"))
            item_fa.setPos(20, (staff_y_bass + 1 * line_spacing) - fm_fa.ascent())

            # 5. MÉTRICA DE COMPÁS EN AMBOS PENTAGRAMAS
            smufl_num = TIME_SIG_DIGITS.get(str(ts_num), str(ts_num))
            smufl_den = TIME_SIG_DIGITS.get(str(ts_den), str(ts_den))
            ts_smufl_font = get_smufl_font(26)
            fm_ts = QFontMetrics(ts_smufl_font)

            # Métrica en Pentagrama Superior
            num_item1 = self._scene.addText(smufl_num, ts_smufl_font)
            num_item1.setDefaultTextColor(QColor("#0284c7"))
            num_item1.setPos(70, (staff_y_treble + 1 * line_spacing) - fm_ts.ascent())
            den_item1 = self._scene.addText(smufl_den, ts_smufl_font)
            den_item1.setDefaultTextColor(QColor("#0284c7"))
            den_item1.setPos(70, (staff_y_treble + 3 * line_spacing) - fm_ts.ascent())

            # Métrica en Pentagrama Inferior
            num_item2 = self._scene.addText(smufl_num, ts_smufl_font)
            num_item2.setDefaultTextColor(QColor("#0284c7"))
            num_item2.setPos(70, (staff_y_bass + 1 * line_spacing) - fm_ts.ascent())
            den_item2 = self._scene.addText(smufl_den, ts_smufl_font)
            den_item2.setDefaultTextColor(QColor("#0284c7"))
            den_item2.setPos(70, (staff_y_bass + 3 * line_spacing) - fm_ts.ascent())

        else:
            # PENTAGRAMA ÚNICO (Clave de Sol o Clave de Fa)
            for i in range(5):
                y = staff_y_treble + i * line_spacing
                self._scene.addLine(20, y, width - 20, y, pen_staff)

            is_treble = (self._lesson.clef == "treble")
            clef_symbol = CLEF_TREBLE if is_treble else CLEF_BASS
            clef_font = get_smufl_font(36 if is_treble else 34)
            fm_clef = QFontMetrics(clef_font)
            clef_item = self._scene.addText(clef_symbol, clef_font)
            clef_item.setDefaultTextColor(QColor("#38bdf8"))
            clef_y_origin = 122 if is_treble else 94
            clef_item.setPos(18 if is_treble else 20, clef_y_origin - fm_clef.ascent())

            smufl_num = TIME_SIG_DIGITS.get(str(ts_num), str(ts_num))
            smufl_den = TIME_SIG_DIGITS.get(str(ts_den), str(ts_den))
            ts_smufl_font = get_smufl_font(26)
            fm_ts = QFontMetrics(ts_smufl_font)

            num_item = self._scene.addText(smufl_num, ts_smufl_font)
            num_item.setDefaultTextColor(QColor("#0284c7"))
            num_item.setPos(70, 94 - fm_ts.ascent())

            den_item = self._scene.addText(smufl_den, ts_smufl_font)
            den_item.setDefaultTextColor(QColor("#0284c7"))
            den_item.setPos(70, 122 - fm_ts.ascent())

        # Título de la lección y clave
        if is_grand_staff:
            clef_title = "Gran Pentagrama de Piano (Doble Clave: Sol & Fa)"
        else:
            clef_title = "Clave de Sol (Mano Derecha)" if self._lesson.clef == "treble" else "Clave de Fa (Mano Izquierda)"

        beaming_title_suffix = " [Barras Unidas]" if self._beaming_enabled else " [Corchetes Separados]"
        title_text = self._scene.addText(f"{clef_title} — {self._lesson.title} [{ts_str}]{beaming_title_suffix}", QFont("Segoe UI", 10, QFont.Weight.Bold))
        title_text.setDefaultTextColor(QColor("#94a3b8"))
        title_text.setPos(75, 6)

        # Dibujar Cuadro Traslúcido de Rango Seleccionado A-B
        total_notes = len(self._lesson.notes)
        if 0 <= self._range_start <= self._range_end < total_notes:
            if not (self._range_start == 0 and self._range_end == total_notes - 1):
                x_a = x_start + self._range_start * x_step - 8
                x_b = x_start + self._range_end * x_step + 22
                w_box = x_b - x_a
                box_h = 240 if is_grand_staff else 140
                self._scene.addRect(x_a, 35, w_box, box_h, QPen(QColor("#38bdf8"), 2, Qt.PenStyle.DashLine), QBrush(QColor(56, 189, 248, 30)))
                t_a = self._scene.addText("[A]", QFont("Consolas", 10, QFont.Weight.Bold))
                t_a.setDefaultTextColor(QColor("#38bdf8"))
                t_a.setPos(x_a - 4, 33)
                t_b = self._scene.addText("[B]", QFont("Consolas", 10, QFont.Weight.Bold))
                t_b.setDefaultTextColor(QColor("#38bdf8"))
                t_b.setPos(x_b - 16, 33)

        # Pre-procesamiento de posiciones, compases y tiempos para Beaming y Batuta
        note_data: List[Dict[str, Any]] = []
        cumulative_beats = 0.0

        for idx, note in enumerate(self._lesson.notes):
            x = x_start + idx * x_step
            diatonic_val = midi_to_diatonic_step(note.midi_note)
            hand = getattr(note, "hand", None)

            if is_grand_staff:
                if hand == "L" or (hand is None and note.midi_note < 60):
                    # Pentagrama Inferior (Clave de Fa) -> Línea 4 Fa3 es 204
                    y_center = 204 - (diatonic_val - 24) * half_spacing
                    stem_up = (y_center > 218)
                else:
                    # Pentagrama Superior (Clave de Sol) -> Línea 2 Sol4 es 112
                    y_center = 112 - (diatonic_val - 32) * half_spacing
                    stem_up = (y_center > 98)
            else:
                is_tr = (self._lesson.clef == "treble")
                y_center = 122 - (diatonic_val - 32) * half_spacing if is_tr else 94 - (diatonic_val - 24) * half_spacing
                stem_up = (y_center > (108 if is_tr else 94))

            duration = getattr(note, "duration_quarter", 1.0)
            measure_idx = int(cumulative_beats // beats_per_measure)
            beat_in_measure = int(cumulative_beats % beats_per_measure)

            note_data.append({
                "idx": idx,
                "note": note,
                "x": x,
                "y_center": y_center,
                "duration": duration,
                "measure_idx": measure_idx,
                "beat_in_measure": beat_in_measure,
                "is_current": (idx == self._current_step),
                "is_past": (idx < self._current_step),
                "stem_up": stem_up,
                "beamed": False
            })
            cumulative_beats += duration
            cumulative_beats += duration

        # Identificar y agrupar corcheas/semicorcheas para Beaming por Tiempo
        beam_groups: List[List[Dict[str, Any]]] = []
        if self._beaming_enabled:
            current_group: List[Dict[str, Any]] = []
            for nd in note_data:
                if nd["duration"] <= 0.5:
                    if not current_group:
                        current_group.append(nd)
                    else:
                        prev = current_group[-1]
                        # Agrupar si pertenecen al mismo compás y mismo tiempo entero
                        if prev["measure_idx"] == nd["measure_idx"] and prev["beat_in_measure"] == nd["beat_in_measure"]:
                            current_group.append(nd)
                        else:
                            if len(current_group) >= 2:
                                beam_groups.append(current_group)
                            current_group = [nd]
                else:
                    if len(current_group) >= 2:
                        beam_groups.append(current_group)
                    current_group = []
            if len(current_group) >= 2:
                beam_groups.append(current_group)

            for bg in beam_groups:
                for nd in bg:
                    nd["beamed"] = True

        # Renderizar la Batuta de Dirección Pedagógica (Conductor's Baton) sobre la nota/compás activo
        active_nd = note_data[self._current_step] if 0 <= self._current_step < len(note_data) else None
        if active_nd:
            baton_x = active_nd["x"]
            baton_y = 38
            # Dibujar la batuta con esfera luminosa indicando el pulso (1, 2, 3, 4)
            pen_baton = QPen(QColor("#00e676"), 2)
            # Varilla de batuta en ángulo 35°
            self._scene.addLine(baton_x - 12, baton_y + 12, baton_x + 2, baton_y - 2, pen_baton)
            # Esfera reflectante en la punta de la batuta
            self._scene.addEllipse(baton_x, baton_y - 5, 8, 8, QPen(QColor("#00e676"), 2), QBrush(QColor("#00e676")))

            # Badge de Tiempo / Pulso Rebotante
            b_text = self._scene.addText(f"🪄 Pulso {self._current_beat}/{self._total_beats}", QFont("Segoe UI", 9, QFont.Weight.Bold))
            b_text.setDefaultTextColor(QColor("#00e676"))
            b_text.setPos(baton_x + 10, baton_y - 12)

        # 4. Dibujar notas musicales SMuFL, plicas, digitación y barlines
        cumulative_beats = 0.0
        pen_barline = QPen(QColor("#64748b"), 2)

        for idx, nd in enumerate(note_data):
            note = nd["note"]
            x = nd["x"]
            y_center = nd["y_center"]
            is_current = nd["is_current"]
            is_past = nd["is_past"]
            duration = nd["duration"]
            hand = getattr(note, "hand", None)

            has_error = (idx in self._error_steps)
            note_res = self._note_results.get(idx)
            status_key = getattr(note_res, "status", None) if note_res else None

            # Colores e indicadores de estado rítmico/tonal
            if status_key == "EARLY":
                color_note = QColor("#ef4444")
                badge = self._scene.addText("🡠 ✗", QFont("Segoe UI", 9, QFont.Weight.Bold))
                badge.setDefaultTextColor(QColor("#ef4444"))
                badge.setPos(x - 14, 28)
            elif status_key == "LATE":
                color_note = QColor("#ef4444")
                badge = self._scene.addText("✗ 🡢", QFont("Segoe UI", 9, QFont.Weight.Bold))
                badge.setDefaultTextColor(QColor("#ef4444"))
                badge.setPos(x + 10, 28)
            elif status_key == "WRONG_NOTE" or (is_current and has_error):
                color_note = QColor("#ef4444")
                cross_item = self._scene.addText("✗", QFont("Segoe UI", 10, QFont.Weight.Bold))
                cross_item.setDefaultTextColor(QColor("#ef4444"))
                cross_item.setPos(x, 28)
            elif is_current:
                color_note = QColor("#38bdf8")  # Azul cian brillante sin círculo ambiguo
            elif is_past:
                if has_error:
                    color_note = QColor("#f59e0b")
                    check_item = self._scene.addText("✓", QFont("Segoe UI", 9, QFont.Weight.Bold))
                    check_item.setDefaultTextColor(QColor("#f59e0b"))
                    check_item.setPos(x, 28)
                else:
                    color_note = QColor("#22c55e")
                    check_item = self._scene.addText("✓", QFont("Segoe UI", 9, QFont.Weight.Bold))
                    check_item.setDefaultTextColor(QColor("#22c55e"))
                    check_item.setPos(x, 28)
            else:
                color_note = QColor("#94a3b8")

            # A. Líneas Adicionales (Ledger Lines)
            if is_grand_staff:
                if hand == "L" or (hand is None and note.midi_note < 60):
                    # Pentagrama Inferior (Clave de Fa): líneas en 190 (A3), 204 (F3), 218 (D3), 232 (B2), 246 (G2)
                    if y_center <= 176:  # C4 (176) o superior (entre pentagramas)
                        y_ledger = 176
                        while y_ledger >= y_center:
                            pen_ledger = QPen(color_note if (is_current or is_past) else QColor("#64748b"), 2)
                            self._scene.addLine(x - 10, y_ledger, x + 10, y_ledger, pen_ledger)
                            y_ledger -= 14
                    elif y_center >= 260:  # E2 (260) o inferior
                        y_ledger = 260
                        while y_ledger <= y_center:
                            pen_ledger = QPen(color_note if (is_current or is_past) else QColor("#64748b"), 2)
                            self._scene.addLine(x - 10, y_ledger, x + 10, y_ledger, pen_ledger)
                            y_ledger += 14
                else:
                    # Pentagrama Superior (Clave de Sol): líneas en 70 (F5), 84 (D5), 98 (B4), 112 (G4), 126 (E4)
                    if y_center >= 140:  # C4 (140) o inferior (entre pentagramas)
                        y_ledger = 140
                        while y_ledger <= y_center:
                            pen_ledger = QPen(color_note if (is_current or is_past) else QColor("#64748b"), 2)
                            self._scene.addLine(x - 10, y_ledger, x + 10, y_ledger, pen_ledger)
                            y_ledger += 14
                    elif y_center <= 56:  # A5 (56) o superior
                        y_ledger = 56
                        while y_ledger >= y_center:
                            pen_ledger = QPen(color_note if (is_current or is_past) else QColor("#64748b"), 2)
                            self._scene.addLine(x - 10, y_ledger, x + 10, y_ledger, pen_ledger)
                            y_ledger -= 14
            else:
                # Pentagrama Único
                if y_center >= 150:
                    y_ledger = 150
                    while y_ledger <= y_center:
                        pen_ledger = QPen(color_note if (is_current or is_past) else QColor("#64748b"), 2)
                        self._scene.addLine(x - 10, y_ledger, x + 10, y_ledger, pen_ledger)
                        y_ledger += 14
                elif y_center <= 66:
                    y_ledger = 66
                    while y_ledger >= y_center:
                        pen_ledger = QPen(color_note if (is_current or is_past) else QColor("#64748b"), 2)
                        self._scene.addLine(x - 10, y_ledger, x + 10, y_ledger, pen_ledger)
                        y_ledger -= 14

            # B. Renderizado de Cabeza de Nota SMuFL Vectorial
            if duration >= 4.0:
                head_glyph = NOTEHEAD_WHOLE
            elif duration >= 2.0:
                head_glyph = NOTEHEAD_HALF
            else:
                head_glyph = NOTEHEAD_BLACK

            head_font = get_smufl_font(28)
            fm_head = QFontMetrics(head_font)
            head_item = self._scene.addText(head_glyph, head_font)
            head_item.setDefaultTextColor(color_note)
            head_item.setPos(x - 9, y_center - fm_head.ascent() - 4)

            # C. Plica (Stem) y Corchete (Flag) individual si no pertenece a grupo de Beaming
            if duration < 4.0 and not nd["beamed"]:
                stem_up = nd["stem_up"]
                pen_stem = QPen(color_note, 2)
                if stem_up:
                    stem_x = x + 5
                    stem_y1 = y_center - 2
                    stem_y2 = y_center - 32
                    self._scene.addLine(stem_x, stem_y1, stem_x, stem_y2, pen_stem)
                    if duration <= 0.5:
                        flag_font = get_smufl_font(28)
                        flag_symbol = FLAG_8TH_UP if duration > 0.25 else FLAG_16TH_UP
                        flag_item = self._scene.addText(flag_symbol, flag_font)
                        flag_item.setDefaultTextColor(color_note)
                        flag_item.setPos(stem_x - 1, stem_y2 - 6)
                else:
                    stem_x = x - 5
                    stem_y1 = y_center + 2
                    stem_y2 = y_center + 32
                    self._scene.addLine(stem_x, stem_y1, stem_x, stem_y2, pen_stem)
                    if duration <= 0.5:
                        flag_font = get_smufl_font(28)
                        flag_symbol = FLAG_8TH_DOWN if duration > 0.25 else FLAG_16TH_DOWN
                        flag_item = self._scene.addText(flag_symbol, flag_font)
                        flag_item.setDefaultTextColor(color_note)
                        flag_item.setPos(stem_x - 1, stem_y2 - 20)

            # D. Digitación (1 al 5)
            if is_grand_staff:
                if hand == "L" or (hand is None and note.midi_note < 60):
                    finger_y = 168
                else:
                    finger_y = 48
                is_r_hand = (hand == "R" or (hand is None and note.midi_note >= 60))
            else:
                is_r_hand = (self._lesson.clef == "treble")
                finger_y = 48 if is_r_hand else 152

            finger_color = QColor("#38bdf8") if is_current else (QColor("#22c55e") if is_past else (QColor("#38bdf8") if is_r_hand else QColor("#22c55e")))
            finger_text = self._scene.addText(str(note.finger), QFont("Consolas", 11, QFont.Weight.Bold))
            finger_text.setDefaultTextColor(finger_color)
            finger_text.setPos(x - 2, finger_y)

            # E. Nombre / Lírica debajo del pentagrama correspondiente
            name_str = note.lyric or midi_to_note_name(note.midi_note)
            lyric_color = QColor("#38bdf8") if is_current else (QColor("#22c55e") if is_past else QColor("#64748b"))
            lyric_weight = QFont.Weight.Bold if (is_current or is_past) else QFont.Weight.Normal
            lyric_text = self._scene.addText(name_str, QFont("Segoe UI", 9, lyric_weight))
            lyric_text.setDefaultTextColor(lyric_color)

            if is_grand_staff:
                if hand == "L" or (hand is None and note.midi_note < 60):
                    lyric_y = 262  # Debajo del pentagrama de Fa (y = 246)
                else:
                    lyric_y = 142  # Debajo del pentagrama de Sol (y = 126)
            else:
                lyric_y = 172

            lyric_text.setPos(x - 4, lyric_y)

            # F. Línea Divisora de Compás
            cumulative_beats += duration
            if cumulative_beats >= beats_per_measure and idx < len(self._lesson.notes) - 1:
                x_bar = x + (x_step / 2) + 6
                y_bar_top = staff_y_treble
                y_bar_bottom = (staff_y_bass + 4 * line_spacing) if is_grand_staff else (staff_y_treble + 4 * line_spacing)
                self._scene.addLine(x_bar, y_bar_top, x_bar, y_bar_bottom, pen_barline)
                cumulative_beats = 0.0

        # Draw Beams for grouped corcheas / semicorcheas
        for bg in beam_groups:
            # Determinar dirección predominante del grupo
            group_stem_up = (sum(1 for nd in bg if nd["stem_up"]) >= len(bg) / 2.0)
            group_color = QColor("#38bdf8") if any(nd["is_current"] for nd in bg) else QColor("#22c55e") if all(nd["is_past"] for nd in bg) else QColor("#94a3b8")
            pen_stem_group = QPen(group_color, 2)
            pen_beam_primary = QPen(group_color, 4)
            pen_beam_secondary = QPen(group_color, 3)

            # Calcular altura de barra de unión (Beam Line Y)
            if group_stem_up:
                beam_y = min(nd["y_center"] for nd in bg) - 28
            else:
                beam_y = max(nd["y_center"] for nd in bg) + 28

            stem_x_coords = []
            for nd in bg:
                sx = nd["x"] + (5 if group_stem_up else -5)
                sy1 = nd["y_center"] + (-2 if group_stem_up else 2)
                self._scene.addLine(sx, sy1, sx, beam_y, pen_stem_group)
                stem_x_coords.append(sx)

            # Barra Primaria (Corcheas - 1 barra)
            self._scene.addLine(stem_x_coords[0], beam_y, stem_x_coords[-1], beam_y, pen_beam_primary)

            # Barra Secundaria (Semicorcheas - 2da barra paralela offset 6px)
            if any(nd["duration"] <= 0.25 for nd in bg):
                secondary_y = beam_y + 6 if group_stem_up else beam_y - 6
                self._scene.addLine(stem_x_coords[0], secondary_y, stem_x_coords[-1], secondary_y, pen_beam_secondary)

        # Línea final de cierre del pentagrama (Doble barra de compás final)
        x_final = x_start + len(self._lesson.notes) * x_step - 15
        y_bar_top = staff_y_treble
        y_bar_bottom = (staff_y_bass + 4 * line_spacing) if is_grand_staff else (staff_y_treble + 4 * line_spacing)
        self._scene.addLine(x_final - 4, y_bar_top, x_final - 4, y_bar_bottom, QPen(QColor("#64748b"), 1))
        self._scene.addLine(x_final, y_bar_top, x_final, y_bar_bottom, QPen(QColor("#cbd5e1"), 3))
