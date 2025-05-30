```markdown
# Arquitectura Modular del Simulador

Este documento describe la arquitectura modular del simulador, detallando los componentes principales y su interacción. La arquitectura se divide en módulos clave para facilitar el desarrollo, mantenimiento y escalabilidad.

## Módulos Principales

El simulador se compone de los siguientes módulos principales:

1.  **Estado del Partido (Game State)**
2.  **Física (Physics)**
3.  **IA (Artificial Intelligence)**
4.  **Simulación (Simulation Core)**

### 1. Estado del Partido (Game State)

*   **Función:** Actúa como la fuente única de verdad para el estado actual de la simulación. Contiene toda la información relevante sobre el partido, los jugadores, el balón, el campo, el marcador, el tiempo, etc. Su estructura y acceso están definidos principalmente en `state.py`.
*   **Clases/Componentes Principales:**
    *   `GameState` (definida en `state.py`): Clase principal que encapsula todo el estado.
    *   `PlayerState`: Información específica de cada jugador (posición, velocidad, estado, estadísticas).
    *   `BallState`: Información del balón (posición, velocidad, rotación).
    *   `FieldState`: Propiedades del campo de juego.
    *   `Scoreboard`: Puntuación y tiempo.
*   **Comunicación:** Es el módulo central. Todos los demás módulos leen de él para obtener la información actual y escriben en él para actualizar el estado según sus cálculos o decisiones.

### 2. Física (Physics)

*   **Función:** Encargado de simular las leyes físicas dentro del entorno del partido. Calcula el movimiento de los objetos (balón, jugadores) basándose en fuerzas, velocidades, colisiones y otras interacciones físicas.
*   **Clases/Componentes Principales:**
    *   `PhysicsEngine`: Motor principal que gestiona las actualizaciones físicas.
    *   `CollisionDetector`: Detecta colisiones entre objetos.
    *   `ForceAccumulator`: Gestiona la aplicación de fuerzas a los objetos.
    *   `Integrator`: Actualiza posiciones y velocidades basándose en fuerzas y tiempo (ej. Euler, Verlet).
*   **Comunicación:**
    *   **Lee de:** Estado del Partido (posiciones, velocidades, propiedades físicas de objetos, fuerzas aplicadas).
    *   **Escribe en:** Estado del Partido (nuevas posiciones, velocidades, estados post-colisión).
    *   Puede recibir *inputs de fuerza/movimiento* del módulo de IA (a través del Estado del Partido o directamente) para aplicar a los jugadores.

### 3. IA (Artificial Intelligence)

*   **Función:** Contiene la lógica para los agentes (jugadores) controlados por la IA. Basándose en el estado actual del partido (obtenido a través de la estructura definida en `state.py`), cada agente toma decisiones. Estas decisiones se expresan como selecciones de un conjunto predefinido de acciones de alto nivel, especificadas en `actions.py`. El framework de IA es responsable de seleccionar la acción adecuada y, si es necesario, traducirla en inputs de bajo nivel (como fuerzas o velocidades deseadas) que el módulo de Física pueda procesar.
*   **Clases/Componentes Principales:**
    *   `AIManager`: Orquesta el ciclo de decisión de la IA para todos los agentes controlados, interactuando con el `GameState`.
    *   `BaseAIAgent`: Clase base abstracta de la cual heredan todas las implementaciones concretas de IA para jugadores. Define la interfaz para la toma de decisiones (ej. un método `decide(game_state)`).
    *   `actions.py`: Archivo que define las posibles acciones de alto nivel que un agente de IA puede intentar realizar (ej. `MoveTo`, `PassBall`, `ShootGoal`, `Tackle`). Estas acciones pueden encapsular lógica compleja pero son la interfaz que la IA utiliza para interactuar con el mundo.
    *   `state.py`: Define la estructura del `GameState` y proporciona métodos para acceder a la información relevante del partido, que es crucial para la toma de decisiones de la IA.
    *   Implementaciones Concretas de IA: Clases específicas que heredan de `BaseAIAgent` e implementan la lógica de decisión particular para diferentes estrategias o roles de jugadores.
*   **Comunicación:**
    *   **Lee de:** Estado del Partido (`GameState` definido en `state.py`). Accede a toda la información necesaria para evaluar la situación del juego.
    *   **Escribe en:** Proporciona la *acción deseada* (definida en `actions.py`) o *inputs de control* (como vectores de movimiento o fuerzas aplicadas) para cada agente controlado. Estos outputs son consumidos por el `Simulation Core` o el `PhysicsEngine` para actualizar el estado del partido en el siguiente paso.

### 4. Simulación (Simulation Core)

*   **Función:** Es el orquestador principal del bucle del simulador. Gestiona el avance del tiempo en la simulación, coordinando la ejecución de los otros módulos en cada paso de tiempo. Recibe los inputs de la IA y los aplica, ejecuta el motor de física para actualizar el estado, y gestiona el estado general del partido (tiempo, marcador, eventos del juego).
*   **Clases/Componentes Principales:**
    *   `SimulationEngine`: Clase principal que contiene el bucle de simulación.
    *   `TimeManager`: Controla el tiempo dentro de la simulación.
    *   `EventManager`: Gestiona eventos del juego (saques, goles, faltas, etc.).
*   **Comunicación:**
    *   **Lee de:** Estado del Partido (estado actual para saber qué procesar).
    *   **Escribe en:** Estado del Partido (actualiza el estado general después de coordinar Física e IA).
    *   **Coordina:** Llama a los módulos de IA (para obtener decisiones/inputs) y Física (para actualizar el estado físico) en el orden correcto para cada paso de simulación.

## Flujo de Ejecución (por paso de simulación)

1.  El `SimulationEngine` avanza el tiempo.
2.  El `SimulationEngine` notifica al `AIManager`.
3.  El `AIManager` lee el `GameState` (vía `state.py`).
4.  Cada `BaseAIAgent` (implementación concreta) lee el `GameState` y decide una `Action` (de `actions.py`) o un set de inputs de control.
5.  El `AIManager` recoge las decisiones/inputs de todos los agentes.
6.  El `SimulationEngine` o un componente intermedio traduce las `Actions` de alto nivel (si aplica) o aplica directamente los inputs de control generados por la IA al `GameState` o los pasa al `PhysicsEngine`.
7.  El `SimulationEngine` notifica al `PhysicsEngine`.
8.  El `PhysicsEngine` lee el `GameState` (incluyendo inputs aplicados) y calcula las nuevas posiciones, velocidades y estados físicos de los objetos para el siguiente paso de tiempo.
9.  El `PhysicsEngine` escribe los resultados de vuelta en el `GameState`.
10. El `SimulationEngine` actualiza cualquier otro aspecto del `GameState` (marcador, tiempo, eventos) basándose en el nuevo estado físico.
11. El bucle se repite.

Esta arquitectura promueve la separación de preocupaciones, permitiendo que los desarrolladores trabajen en la lógica de IA, el motor de física o la gestión del estado de forma relativamente independiente.
```