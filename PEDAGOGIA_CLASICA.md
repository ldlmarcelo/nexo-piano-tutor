# NEXO Piano Tutor — FUNDAMENTACIÓN PEDAGÓGICA Y MANIFIESTO CIENTÍFICO

Este documento consolida la arquitectura pedagógica, científica y filosófica de **NEXO Piano Tutor**.

> **"La excelencia en el piano no emerge del automatismo pasivo, sino del desacoplamiento consciente de la carga cognitiva y el refinamiento del gesto motor."**

---

## 🏛️ 1. Declaración de Principios

`nexo-piano-tutor` nace con un propósito claro: **brindar una formación de piano clásico científicamente rigurosa para estudiantes de todas las edades (niños, jóvenes y adultos)**, distanciándose deliberadamente de las aplicaciones comerciales basadas en barras cayendo estilo arcade (*Guitar Hero*). 

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

## 🔐 5. Blueprint de Autenticación y Gestión de Perfiles Soberanos

### 5.1. Fundamentación y Ley de Universalidad Semántica
El diseño del sistema de perfiles se rige de forma estricta por la **Ley de Universalidad Semántica (Ley VI de NEXO)**:

> **"El código opera sobre abstracciones de sistema (User, Session, Progress, Auth), nunca sobre nombres customizados o constantes mágicas hardcodeadas."**

Prohibimos explícitamente la presencia de cadenas de texto de nombres de usuario dentro del código fuente. La aplicación trata a los estudiantes como entidades dinámicas desacopladas, garantizando que el sistema sea 100% extensible, reutilizable y soberano.

---

### 5.2. Justificación Neuro-Pedagógica de la Sesión Aislada
Para un entorno multitutor familiar:
1. **Aislamiento de Muestras Rítmicas y Progreso**: Cada estudiante posee su propia velocidad de mielenización, racha de días consecutivos y curva de precisión tonal (tolerancia en ms). La mezcla de perfiles contaminaría la curva de aprendizaje del evaluador en tiempo real (`RealtimeEvaluator`).
2. **Foco e Inmunidad Visual**: Una vez autenticado el estudiante, la interfaz principal de estudio **debe quedar libre de ruido administrativo**. Se elimina cualquier widget o selector permanente de la pantalla de la partitura. En el cabezal solo se exhibe la insignia del estudiante activo y el botón **`[ 🚪 Cerrar Sesión ]`**.

---

### 5.3. Modelo de Entidades y Lógica de Negocio

```
┌─────────────────────────────────────────────────────────────┐
│                      ESTRUCTURA USER                        │
├─────────────────────────────────────────────────────────────┤
│ - id: str (UUIDv4)                                          │
│ - username: str (Nombre de pantalla universal)              │
│ - pin: str (PIN opcional de 4 dígitos para privacidad)      │
│ - created_at: str (ISO-8601)                                │
│ - active_lesson_id: str                                     │
│ - completed_lessons: list[str]                              │
│ - stats: UserStats (total_notes, accuracy_pct, streak_days) │
│ - history: list[SessionLog]                                 │
└─────────────────────────────────────────────────────────────┘
```

---

### 5.4. Flujo de Navegación de Sesión

1. **Arranque de Aplicación (Estado Desconectado)**:
   - Al iniciar `main.py`, se verifica la persistencia en `users.json`.
   - Si no hay sesión activa guardada, la ventana presenta el **Panel de Bienvenida y Autenticación** (`LoginWidget`), permitiendo:
     - Seleccionar un perfil existente (e ingresar PIN si fuere requerido).
     - Registrar un nuevo perfil de estudiante.

2. **Transición a Pantalla de Estudio (Estado Autenticado)**:
   - Al autenticarse con éxito, el `LoginWidget` se retira y se despliega la interfaz de Partitura, Teclado e Indicadores.
   - Se cargan automáticamente las lecciones aprobadas y la última lección activa del perfil.

3. **Cierre de Sesión (Logout)**:
   - Al presionar **`[ 🚪 Cerrar Sesión ]`**, la aplicación guarda el progreso pendiente en `users.json`, limpia el estado del evaluador y retorna limpiamente a la pantalla de Autenticación.

---

## 📈 6. Blueprint de Evaluación Realista, Tarjetas Teóricas y Bitácora

### 6.1. Evaluación Realista e Inmunidad a las Felicitaciones Ciegas
En concordancia con el Pilar II (Realimentación Inmediata de Baja Latencia), el evaluador no debe emitir mensajes de "Excelente" si el estudiante cometió desvíos tonales o de octava:
- **Cálculo de Precisión (%)**: $(N_{correctas} / N_{totales}) \times 100$.
- **Criterio de Maestría por Tramo**:
  - **90% – 100%**: 🌟 *Ejecución Impecable* (Desbloquea la lección y suma insignia).
  - **75% – 89%**: 👍 *Buena Técnica* (Consejo: "Notas logradas. Realizá una serie de repeticiones x3 para afinar la fluidez").
  - **< 75%**: 💡 *Revisión Requerida* (Sin felicitaciones vacías. Consejo: "Atención con el dedo indicado. Revisá la posición y reintentá").

---

### 6.2. Tarjetas Teóricas Contextuales y Biblioteca Consultable
Para desacoplar la teoría árida de la práctica activa:
1. **Tarjetas Introductivas por Lección (Popups)**:
   - *Lección 1*: ¿Qué es el Pentagrama?, ¿Qué es la Clave de Sol?, Digitación de la Mano Derecha (1 a 5).
   - *Lección 2*: ¿Qué es la Clave de Fa?, Digitación de la Mano Izquierda (5 a 1).
2. **La Biblioteca de la Fragua (Glosario Consultable)**:
   - Panel accesible desde la interfaz principal para releer las tarjetas teóricas y la historia del piano (*De Cristofori al Piano Moderno*).

---

### 6.3. Bitácora del Estudiante (Dashboard de Progreso)
- Panel de visualización de estadísticas individuales por perfil (`UserStats`):
  - Total de notas ejecutadas y porcentaje de precisión acumulada %.
  - Racha de repeticiones completadas y lecciones aprobadas.
  - Ficha personalizada por estudiante.

---

*Documento de diseño pedagógico consolidado y actualizado el 2026-07-21 en el Terroir de Marcelo y NEXO.*


