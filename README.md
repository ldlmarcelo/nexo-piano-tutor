# nexo-piano-tutor

Tutor de piano científico, pedagógico y riguroso orientado a la formación clásica para niños.

> **Pedagogía científica de precisión.** Sin barras cayendo estilo arcade. Basado en notación de pentagrama real (Clave de Sol y Fa), desacoplamiento de carga cognitiva (Tono, Tiempo, Dinámica), evaluación MIDI en tiempo real (<15ms) y curva de repetición espaciada atómica.

---

## 🏛️ Curriculum Clásico

1. **Capítulo I: Los Fundamentos de Beyer (Opus 101)**
   - Lectura progresiva en 5 notas fijas (Do-Sol).
   - Independencia de mano derecha (Clave de Sol) e izquierda (Clave de Fa).
2. **Capítulo II: Polifonía e Independencia (J. S. Bach)**
   - Piezas del *Libro de Clavecin de Anna Magdalena Bach*.
   - Contrapunto inicial bimanual.
3. **Capítulo III: Claridad y Técnica (Muzio Clementi - Op. 36 & Béla Bartók - Mikrokosmos)**
   - Paso del pulgar, escalas y fraseo articulado (*legato* / *staccato*).

---

## 🧪 Pilares Neuro-Pedagógicos

1. **Desacoplamiento de Carga Cognitiva**:
   - *Modo Lectura*: Evaluación de notas/dedos sin metrónomo.
   - *Modo Tiempo*: Evaluación de pulso rítmico.
   - *Modo Integración*: Ejecución real completa.
2. **Evaluación de Tiempo Real (MIDI <15ms)**:
   - Medición de precisión tonal, desvío rítmico (jitter en ms) y mapa de fuerza (*Velocity*).
3. **Aislamiento Atómico de Errores**:
   - Detección de pasajes problemáticos y repetición en bucle adaptativo a velocidad reducida.

---

## Stack Técnico

- **Lenguaje**: Python 3.10+
- **Interfaz**: PySide6 (Qt6)
- **Audio & MIDI**: `python-rtmidi` + `pyfluidsynth` (vía `nexo-midi-synth`)
- **Partitura**: Notación interactiva en `QGraphicsScene` / Notación vectorial
- **Persistencia**: SQLite (`progress.db`)

---

## Instalación y Uso

```bash
git clone https://github.com/ldlmarcelo/nexo-piano-tutor.git
cd nexo-piano-tutor
pip install -r requirements.txt
python main.py
```

---

## Origen

Módulo federado del ecosistema NEXO, diseñado para la formación musical clásica de los hijos de Marcelo.

## Licencia

MIT
