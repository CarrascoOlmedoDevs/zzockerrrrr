# Arquitectura Modular del Simulador

Este documento describe la arquitectura modular del simulador, detallando los componentes principales y su interacción. La arquitectura se divide en módulos clave para facilitar el desarrollo, mantenimiento y escalabilidad.

## Módulos Principales

El simulador se compone de los siguientes módulos principales:

1.  **Estado del Partido (Game State)**
2.  **Física (Physics)**
3.  **IA (Artificial Intelligence)**
4.  **Simulación (Simulation Core)**

### 1. Estado del Partido (Game State)

*   **Función:** Actúa como la fuente única de verdad para el estado actual de la simulación. Contiene toda la información relevante sobre el partido, los jugadores, el balón, el campo, el marcador, el tiempo, etc.
*   **Clases/Componentes Principales:**
    *   `GameState`: Clase principal que encapsula todo el estado.
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

*   **Función:** Toma decisiones para los agentes (jugadores) controlados por la IA. Basándose en el estado actual del partido, determina las acciones deseadas por cada jugador (moverse a una posición, intentar un pase, un tiro, etc.) y las traduce en inputs para el módulo de Física (ej. fuerzas deseadas, velocidades objetivo).
*   **Clases/Componentes Principales:**
    *   `AIManager`: Orquesta la toma de decisiones para todos los agentes de IA.
    *   `AgentController`: Lógica de IA para un agente individual (ej. un jugador).
    *   `DecisionTree` / `BehaviorTree` / `GoalOrientedAgent`: Implementaciones de lógicas de decisión.
    *   `Pathfinding`: Algoritmos para encontrar rutas por el campo.
*   **Comunicación:**
    *   **Lee de:** Estado del Partido (posiciones de todos los objetos, estado del juego, tácticas).
    *   **Escribe en:** Estado del Partido (decisiones de los agentes, objetivos, fuerzas/velocidades deseadas que serán leídas por Física). No modifica directamente las propiedades físicas finales (posición, velocidad) que son responsabilidad de Física.

### 4. Simulación (Simulation Core)

*   **Función:** Es el orquestador principal. Controla el bucle de simulación, inicializa el estado, gestiona el paso del tiempo y coordina la ejecución de los otros módulos en el orden correcto para cada "tick" de simulación.
*   **Clases/Componentes Principales:**
    *   `Simulator`: Clase principal que contiene el bucle (`run()`).
    *   `ConfigLoader`: Carga la configuración inicial del partido.
    *   `EventProcessor`: Maneja eventos del juego (ej. gol, falta).
*   **Comunicación:**
    *   **Coordina:** Llama secuencialmente a los métodos de actualización de los módulos IA y Física en cada paso del tiempo.
    *   **Inicializa:** Crea la instancia del Estado del Partido y la inicializa.
    *   **Controla:** El flujo general y el avance del tiempo.

## Flujo de Comunicación y Ejecución (Bucle Principal)

El bucle de simulación sigue generalmente este patrón en cada "tick":

1.  **Inicio Tick:** El `Simulator` inicia un nuevo paso de tiempo.
2.  **Lectura Estado:** Los módulos (IA, Física) leen el estado actual del `GameState`.
3.  **Toma de Decisiones (IA):** El `AIManager` ejecuta la lógica de IA para cada agente, basándose en el estado leído. La IA escribe sus *intenciones* o *inputs físicos deseados* (ej. fuerza a aplicar, velocidad objetivo) en el `GameState` o los pasa como inputs al módulo de Física.
4.  **Cálculos Físicos (Física):** El `PhysicsEngine` toma el estado actual (incluyendo los inputs de la IA) y calcula las nuevas posiciones, velocidades y maneja las interacciones (colisiones) para el siguiente instante de tiempo.
5.  **Actualización Estado:** El `PhysicsEngine` escribe los resultados de sus cálculos (nuevas posiciones, velocidades, etc.) en el `GameState`.
6.  **Procesamiento Eventos:** El `Simulator` o un `EventProcessor` verifica el `GameState` para detectar eventos significativos (gol, fuera de banda, fin de tiempo) y actualiza el `GameState` o dispara acciones correspondientes.
7.  **Fin Tick:** El `Simulator` avanza el tiempo de simulación y prepara para el siguiente tick o termina si las condiciones de fin de partido se cumplen.

## Diagrama Conceptual

```mermaid
graph TD
    A[Simulación (Bucle Principal)] --> B(Lee Configuración);
    B --> C[Inicializa Estado del Partido];
    C --> D{Bucle por Tick};
    D --> E[Estado del Partido (Lectura)];
    E -- Lee Estado --> F[Módulo IA];
    F -- Escribe Intenciones/Inputs --> E;
    E -- Lee Estado e Inputs --> G[Módulo Física];
    G -- Escribe Nuevas Posiciones/Velocidades --> E;
    E -- Estado Actualizado --> H[Procesamiento de Eventos];
    H -- Actualiza Estado --> E;
    H --> I{¿Fin de Simulación?};
    I -- No --> D;
    I -- Sí --> J[Fin Simulación];

    subgraph Módulos
        F
        G
        E
    end
```

Este diagrama ilustra cómo la `Simulación` orquesta el bucle, cómo la `IA` y la `Física` leen y escriben en el `Estado del Partido`, que actúa como el centro de datos, y cómo el bucle continúa hasta que las condiciones de fin de simulación se cumplen.