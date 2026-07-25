"""
Script Conversor de Lecciones a Pasos Polifónicos Simultáneos.
Agrupa notas que ocurren en el mismo instante temporal (beat_offset) en un solo TargetStep (Acordes y Simultaneidad Bimanual).
"""

import os
import json

LESSONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lessons")


def convert_lesson_notes_to_polyphonic_steps(notes, time_signature="4/4"):
    rh_time = 0.0
    lh_time = 0.0
    events = {}

    for n in notes:
        hand = n.get("hand", "R")
        dur = float(n.get("duration_quarter", 1.0))
        t_start = rh_time if hand == "R" else lh_time
        t_key = round(t_start, 4)

        if t_key not in events:
            events[t_key] = []
        events[t_key].append((dur, n))

        if hand == "R":
            rh_time += dur
        else:
            lh_time += dur

    sorted_times = sorted(events.keys())
    steps = []

    for idx, t_key in enumerate(sorted_times):
        step_notes = [item[1] for item in events[t_key]]
        if idx + 1 < len(sorted_times):
            step_duration = round(sorted_times[idx + 1] - t_key, 4)
        else:
            step_duration = min(item[0] for item in events[t_key])

        steps.append({
            "duration_quarter": max(0.25, step_duration),
            "notes": step_notes
        })

    return steps


def process_all_lessons():
    print("[CONVERT] Procesando y convirtiendo las 30 lecciones a Pasos Polifónicos Simultáneos...")
    converted_count = 0

    for fname in sorted(os.listdir(LESSONS_DIR)):
        if fname.endswith(".json"):
            fpath = os.path.join(LESSONS_DIR, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)

            notes = data.get("notes", [])
            ts = data.get("time_signature", "4/4")
            if notes:
                poly_steps = convert_lesson_notes_to_polyphonic_steps(notes, ts)
                data["steps"] = poly_steps
                with open(fpath, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                converted_count += 1
                chord_steps = sum(1 for s in poly_steps if len(s["notes"]) > 1)
                print(f"  [OK] {fname}: {len(poly_steps)} pasos polifónicos ({chord_steps} eventos simultáneos/acordes)")

    print(f"[CONVERT OK] {converted_count} lecciones convertidas a polifonía simultánea real.")


if __name__ == "__main__":
    process_all_lessons()
