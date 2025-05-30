```markdown
# Arquitectura Modular del Simulador

Este documento describe la arquitectura modular del simulador, detallando los componentes principales y su interacción. La arquitectura se divide en módulos clave para facilitar el desarrollo, mantenimiento y escalabilidad.

## Módulos Principales

El simulador se compone de los siguientes módulos principales:

1.  **Estado del Partido (Game State)**
2.  **Física (Physics)**
3.  **IA (Artificial Intelligence)**
4.  **Simulación (Simulation Core)**
5.  **Acciones (Actions)**

### 1. Estado del Partido (Game State)

*   **Función:** Actúa como la fuente única de verdad para el estado actual de la simulación. Contiene toda la información relevante sobre el partido, los jugadores, el balón, el campo, el marcador, el tiempo, etc. Su estructura y acceso están definidos principalmente en `src/zzocker/state.py`.
*   **Clases/Componentes Principales:**
    *   `GameState` (definida en `src/zzocker/state.py`): Clase principal que encapsula todo el estado.
    *   `PlayerState`: Información específica de cada jugador (posición, velocidad, estado, estadísticas).
    *   `BallState`: Información del balón (posición, velocidad, rotación).
    *   `FieldState`: Propiedades del campo de juego.
    *   `Scoreboard`: Puntuación y tiempo.
*   **Comunicación:** Es el módulo central. Todos los demás módulos leen de él para obtener la información actual y escriben en él para actualizar el estado según sus cálculos o decisiones.

### 2. Física (Physics)

*   **Función:** Encargado de simular las leyes físicas dentro del entorno del partido. Calcula el movimiento de los objetos (balón, jugadores) basándose en fuerzas, velocidades, colisiones y otras interacciones físicas.
*   **Clases/Componentes Principales:**
    *   `PhysicsEngine` (definida en `src/zzocker/physics.py`): Motor principal que gestiona las actualizaciones físicas.
    *   `CollisionDetector`: Detecta colisiones entre objetos.
    *   `ForceAccumulator`: Gestiona la aplicación de fuerzas a los objetos.
    *   `Integrator`: Actualiza posiciones y velocidades basándose en fuerzas y tiempo (ej. Euler, Verlet).
*   **Comunicación:**
    *   **Lee de:** Estado del Partido (posiciones, velocidades, propiedades físicas de objetos, fuerzas aplicadas).
    *   **Escribe en:** Estado del Partido (nuevas posiciones, velocidades, estados post-colisión).
    *   Recibe *inputs de fuerza/movimiento* que se derivan de las acciones de la IA (gestionado por el módulo de Simulación).

### 3. IA (Artificial Intelligence)

*   **Función:** Contiene la lógica para los agentes (jugadores) controlados por la IA. Basándose en el estado actual del partido (obtenido a través de la estructura definida en `src/zzocker/state.py`), cada agente toma decisiones. Estas decisiones se expresan como selecciones de un conjunto predefinido de acciones de alto nivel, especificadas en `src/zzocker/actions.py`. El framework de IA (ej. `src/zzocker/ai/player_ai.py`) es responsable de seleccionar la acción adecuada para cada jugador.
*   **Clases/Componentes Principales:**
    *   `PlayerAI` (definida en `src/zzocker/ai/player_ai.py`): Clase base o interfaz para los controladores de IA de los jugadores.
    *   Implementaciones específicas de `PlayerAI` (ej. IA ofensiva, IA defensiva).
    *   Lógica de toma de decisiones (evaluación de estado, selección de objetivo, planificación de acción).
*   **Comunicación:**
    *   **Lee de:** Estado del Partido (para entender la situación actual).
    *   **Escribe en:** Devuelve la acción de alto nivel deseada para cada jugador controlado por IA. Esta acción es procesada por el módulo de Simulación.

### 4. Simulación (Simulation Core)

*   **Función:** Es el orquestador principal del simulador. Gestiona el bucle de simulación, coordina las interacciones entre los otros módulos y mantiene el flujo de tiempo. Es responsable de avanzar el estado del partido paso a paso.
*   **Clases/Componentes Principales:**
    *   `Simulator` (o clase similar): Clase principal que contiene el bucle de simulación.
    *   Mecanismos para cargar y configurar partidos (equipos, IA, reglas).
    *   Componentes para gestionar el tiempo de simulación.
*   **Comunicación:**
    *   Coordina las llamadas a los módulos de IA y Física.
    *   Actualiza el Estado del Partido basándose en los resultados de Física y las acciones procesadas.

### 5. Acciones (Actions)

*   **Función:** Define el conjunto de acciones de alto nivel que un jugador controlado por IA puede intentar realizar. Este módulo proporciona una abstracción entre la decisión de la IA (ej. "pasar el balón", "mover a posición X") y la implementación física de esa acción (ej. aplicar fuerza, establecer velocidad deseada). Las acciones están definidas en `src/zzocker/actions.py`.
*   **Clases/Componentes Principales:**
    *   Clases o enumeraciones que representan diferentes tipos de acciones (ej. `MoveToAction`, `ShootAction`, `PassAction`).
    *   Mecanismos para parametrizar acciones (ej. destino de pase, potencia de tiro).
*   **Comunicación:**
    *   Utilizado por el módulo de IA para expresar sus decisiones.
    *   Procesado por el módulo de Simulación para traducirlo en inputs de bajo nivel para el módulo de Física.

## Bucle de Simulación (Simulation Loop)

El corazón del simulador es el bucle principal que avanza el estado del partido en incrementos de tiempo discretos. La simulación utiliza un **timestep fijo** (`dt`), lo que significa que el tiempo avanza en pasos constantes (por ejemplo, 60 veces por segundo, correspondiendo a un `dt` de 1/60 segundos). Esto asegura una simulación determinista y simplifica la integración física.

Dentro de cada paso del bucle de simulación (`dt`), las operaciones se ejecutan en un orden específico:

1.  **Lectura del Estado Actual:** El `Simulator` obtiene el `GameState` actual (`src/zzocker/state.py`). Este estado es la base para las decisiones de la IA y los cálculos físicos del paso actual.
2.  **Obtención de Inputs de IA:** Para cada jugador controlado por IA, el `Simulator` llama al método correspondiente en su `PlayerAI` (`src/zzocker/ai/player_ai.py`), pasándole el `GameState` actual. Cada `PlayerAI` evalúa el estado y devuelve la `Action` de alto nivel deseada para ese jugador (`src/zzocker/actions.py`).
3.  **Procesamiento de Acciones:** El `Simulator` toma las `Action`s devueltas por las IAs (y posiblemente inputs de jugadores humanos, si aplica) y las traduce en inputs de bajo nivel para el motor de física. Por ejemplo, una `MoveToAction` podría traducirse en una fuerza a aplicar o una velocidad deseada para el jugador.
4.  **Actualización Física:** El `Simulator` invoca al `PhysicsEngine` (`src/zzocker/physics.py`), pasándole el `GameState` actual y los inputs de bajo nivel generados en el paso anterior. El `PhysicsEngine` calcula las nuevas posiciones, velocidades y estados de los objetos (jugadores, balón) después de un intervalo de tiempo `dt`, considerando fuerzas, colisiones, etc.
5.  **Actualización del Estado del Partido:** El `Simulator` actualiza el `GameState` con los resultados calculados por el `PhysicsEngine`. Esto incluye nuevas posiciones, velocidades, cambios de estado (ej. posesión del balón), actualizaciones del marcador, y el avance del tiempo del partido.

Este ciclo se repite para cada timestep, haciendo avanzar la simulación en el tiempo hasta que se cumpla una condición de fin de partido.

## Interacción entre Módulos

La interacción principal ocurre a través del `GameState`. El módulo de Simulación orquesta el flujo, leyendo el estado, consultando a la IA, preparando inputs para la física, ejecutando la física y actualizando el estado. Este diseño centrado en el estado facilita la depuración y asegura que todos los módulos operen sobre la misma instantánea del partido en cada paso de simulación.

```
```