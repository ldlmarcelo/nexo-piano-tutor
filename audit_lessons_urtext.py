"""
Script de Auditoría Urtext y Verificación Métrica para las 30 Lecciones Clásicas.
Inspecciona cada archivo JSON en lessons/, calcula la duración rítmica por compás,
valida las notas MIDI, la digitación, la distribución bimanual (R/L) y emite un informe detallado.
"""

import os
import json
import math
from typing import Dict, List, Any

LESSONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lessons")

TIME_SIGNATURE_BEATS = {
    "4/4": 4.0,
    "3/4": 3.0,
    "2/4": 2.0,
    "3/8": 1.5,
    "6/8": 3.0,
    "5/8": 2.5
}


def parse_time_sig_beats(ts_str: str) -> float:
    if ts_str in TIME_SIGNATURE_BEATS:
        return TIME_SIGNATURE_BEATS[ts_str]
    try:
        num, den = ts_str.split("/")
        return (float(num) / float(den)) * 4.0
    except Exception:
        return 4.0


def audit_single_lesson(filepath: str) -> Dict[str, Any]:
    filename = os.path.basename(filepath)
    report = {
        "filename": filename,
        "valid": True,
        "errors": [],
        "warnings": [],
        "total_notes": 0,
        "total_measures": 0,
        "composer": "",
        "title": "",
        "opus": "",
        "time_signature": ""
    }

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        report["valid"] = False
        report["errors"].append(f"Error al leer JSON: {e}")
        return report

    report["composer"] = data.get("composer", "Desconocido")
    report["title"] = data.get("title", "Sin título")
    report["opus"] = data.get("opus", "")
    report["time_signature"] = data.get("time_signature", "4/4")

    notes = data.get("notes", [])
    report["total_notes"] = len(notes)

    if not notes:
        report["valid"] = False
        report["errors"].append("La lección no contiene notas.")
        return report

    beats_per_measure = parse_time_sig_beats(report["time_signature"])

    current_time_r = 0.0
    current_time_l = 0.0

    for idx, note in enumerate(notes):
        midi = note.get("midi_note")
        dur = note.get("duration_quarter", 0)
        finger = note.get("finger")
        hand = note.get("hand", "R")

        # Validaciones de nota
        if not isinstance(midi, int) or not (21 <= midi <= 108):
            report["errors"].append(f"Nota #{idx+1}: midi_note {midi} fuera de rango piano (21-108).")
            report["valid"] = False
        if not isinstance(dur, (int, float)) or dur <= 0:
            report["errors"].append(f"Nota #{idx+1}: duration_quarter {dur} inválido.")
            report["valid"] = False
        if not isinstance(finger, int) or not (1 <= finger <= 5):
            report["errors"].append(f"Nota #{idx+1}: finger {finger} fuera de rango (1-5).")
            report["valid"] = False
        if hand not in ("R", "L"):
            report["errors"].append(f"Nota #{idx+1}: hand '{hand}' inválida.")
            report["valid"] = False

        if hand == "R":
            current_time_r += dur
        else:
            current_time_l += dur

    max_beats = max(current_time_r, current_time_l)
    total_measures = max_beats / beats_per_measure if beats_per_measure > 0 else 0
    report["total_measures"] = round(total_measures, 2)
    report["beats_r"] = current_time_r
    report["beats_l"] = current_time_l

    if abs(current_time_r - current_time_l) > 0.01 and current_time_l > 0:
        report["warnings"].append(
            f"Desbalance rítmico total entre manos: R={current_time_r}t, L={current_time_l}t"
        )

    return report


def run_full_audit():
    if not os.path.exists(LESSONS_DIR):
        print(f"ERROR: No se encontró la carpeta {LESSONS_DIR}")
        return

    files = sorted([f for f in os.listdir(LESSONS_DIR) if f.endswith(".json")])
    print("========================================================================")
    print(f"INFORME DE AUDITORIA DE LECCIONES CLASICAS ({len(files)} ARCHIVOS)")
    print("========================================================================\n")

    total_valid = 0
    total_errors = 0
    total_warnings = 0

    for f in files:
        path = os.path.join(LESSONS_DIR, f)
        rep = audit_single_lesson(path)
        status_str = "OK" if rep["valid"] and not rep["warnings"] else ("ALERTA" if rep["valid"] else "ERROR")

        if rep["valid"]:
            total_valid += 1
        else:
            total_errors += 1
        if rep["warnings"]:
            total_warnings += 1

        print(f"[{status_str}] {rep['filename']}")
        print(f"     Compositor: {rep['composer']} | Obra: {rep['opus']}")
        print(f"     Compas: {rep['time_signature']} | Total Notas: {rep['total_notes']} | Compases Est.: {rep['total_measures']}")

        if rep["errors"]:
            for err in rep["errors"]:
                print(f"     [ERR] {err}")
        if rep["warnings"]:
            for warn in rep["warnings"]:
                print(f"     [WARN] {warn}")
        print("- " * 35)

    print("\n" + "=" * 70)
    print(f"RESUMEN AUDITORÍA: {total_valid}/{len(files)} VÁLIDOS | {total_errors} ERRORES | {total_warnings} ADVERTENCIAS")
    print("=" * 70)


if __name__ == "__main__":
    run_full_audit()
