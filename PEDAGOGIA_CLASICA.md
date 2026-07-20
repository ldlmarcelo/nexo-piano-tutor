# NEXO Piano Tutor — FUNDAMENTACIÓN PEDAGÓGICA Y MANIFIESTO CIENTÍFICO

Este documento consolida la arquitectura pedagógica, científica y filosófica de **NEXO Piano Tutor**.

> **"La excelencia en el piano no emerge del automatismo pasivo, sino del desacoplamiento consciente de la carga cognitiva y el refinamiento del gesto motor."**

---

## 🏛️ 1. Declaración de Principios

`nexo-piano-tutor` nace con un propósito claro: **brindar una formación de piano clásico científicamente rigurosa para niños**, distanciándose deliberadamente de las aplicaciones comerciales basadas en barras cayendo estilo arcade (*Guitar Hero*). 

Las interfaces tipo arcade generan adicción visual y reflejos oculares pasivos, pero **anulan la lectura de partitura real, destruyen la noción del pulso interno y no desarrollan memoria muscular ni control biomecánico**.

Nuestra propuesta se fundamenta en tres ciencias:
1. **Neurociencia del Aprendizaje Motor** (Mielenización y bucles de realimentación inmediata).
2. **Biomecánica Pianística** (Escuela Taubman y Suzuki: peso del brazo, libertad articular y digitación activa).
3. **Psicología Cognitiva de Sweller** (Teoría de la Carga Cognitiva).

---

## 🔬 2. Los 4 Pilares Neuro-Pedagógicos

### Pillar I: Desacoplamiento de Carga Cognitiva
Para evitar la saturación en el cerebro infantil, cada lección se aborda en tres fases secuenciales:

1. **Modo Lectura & Digitación (Cero Presión de Tiempo)**
   - El metrónomo está desactivado.
   - El cursor gráfico sobre la partitura **no avanza** hasta que el estudiante presione la tecla física correcta en el controlador MIDI.
   - Se entrena la asociación espacial: *Nota en Pentagrama ➔ Dedo Físico (1 al 5) ➔ Tecla en el Teclado*.

2. **Modo Tiempo y Pulso (Subdivisión Rítmica)**
   - Se activa el pulso de metrónomo.
   - Se evalúa exclusivamente el *timing* y la estabilidad rítmica.

3. **Modo Expresión & Examen (Integración)**
   - Se combinan Notación + Tiempo + Control de Dinámica (*Velocity*).

---

### Pillar II: Realimentación Inmediata de Ultra-Baja Latencia (<15ms)
El aprendizaje motor requiere que la corrección del error ocurra dentro de la ventana de asociación neuro-sináptica (<100ms).

El motor `RealtimeEvaluator` analiza cada evento `NOTE_ON`:
- **Precisión Tonal**: Coincidencia exacta del pitch MIDI.
- **Tolerancia Rítmica (Delta)**:
  - `±25ms`: **Perfecto**
  - `±60ms`: **Aceptable**
  - `>100ms`: **Desfase Rítmico**
- **Control de Dinámica (Velocity Meter)**: Detección de acentos involuntarios entre dedos adyacentes (desarrollo del control fino de pulgar y meñique).

---

### Pillar III: Aislamiento Atómico de Errores (Repetición Espaciada)
Cuando el estudiante falla en un pasaje:
1. El sistema **no reinicia la obra desde el principio** (evita el hábito frustrante de re-ensayar lo que ya sale bien).
2. El algoritmo aísla el **micro-compás problemático** (bucle de 2 a 4 notas).
3. Se reduce el tempo (BPM) automáticamente un 30% y se exige una racha de 3 ejecuciones limpias antes de retornar a la obra completa.

---

### Pillar IV: Notación Musical Interactiva en Pentagrama Real
- Partitura real en **Clave de Sol** (mano derecha) y **Clave de Fa** (mano izquierda).
- Indicación clara de digitación recomendada (dedos 1-Pulgar al 5-Meñique).
- Renderizado adaptativo que responde iluminando las notas a medida que se ejecutan.

---

## 📚 3. Curriculum Clásico de Dominio Público

El plan de estudios prescinde de notas aleatorias sin sentido armónico y se basa 100% en las obras maestras pedagógicas de la historia:

### Nivel 1: Los Fundamentos de Beyer
- **Obra**: Ferdinand Beyer — *Opus 101 (Escuela Preparatoria de Piano)*.
- **Enfoque**: Posición fija de 5 dedos (Do a Sol). Independencia mano a mano.

### Nivel 2: Polifonía e Independencia Barroca
- **Obra**: J. S. Bach — *El Libro de Clavecin de Anna Magdalena Bach* (Minuetos Anh. 114, Anh. 115, Musettes).
- **Enfoque**: Contrapunto inicial bimanual (ambas manos llevan líneas melódicas con igual jerarquía).

### Nivel 3: Agilidad y Fraseo Clásico
- **Obras**: 
  - Muzio Clementi — *Sonatinas Opus 36*.
  - Béla Bartók — *Mikrokosmos (Vol. 1 y 2)*.
- **Enfoque**: Paso del pulgar, escalas completas, *staccato*, *legato* y ritmos folclóricos europeos.

---

## 🎭 4. Gamificación y Rigor Narrativo

Para mantener la motivación infantil sin caer en trivialidades:

1. **Viaje Timbrico Histórico**:
   - Las piezas de Bach suenan automáticamente a **Clavecín Barroco** u **Órgano de Catedral**.
   - Las piezas de Mozart y Beethoven suenan a **Piano de Cola de Concierto**.
2. **Contexto Histórico Dramático**:
   - Tarjetas breves antes de cada obra narrando la historia humana detrás del compositor.
3. **Capítulos Épicos**:
   - Capítulo I: *Los Secretos del Barroco*
   - Capítulo II: *La Claridad Clásica*
   - Capítulo III: *La Tempestad Romántica*

---

*Documento de diseño pedagógico consolidado el 2026-07-19 en el Terroir de Marcelo y NEXO.*
