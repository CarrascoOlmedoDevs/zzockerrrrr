import math
# Assume entity and state definitions exist and are importable
# from .state import State, Entity # Example import structure

# Define simple Entity and State classes for demonstration if not imported
# In a real scenario, these would be defined elsewhere (e.g., src/zzocker/state.py)
class Entity:
    def __init__(self, entity_type, position, velocity, radius=0):
        self.entity_type = entity_type # e.g., 'ball', 'player'
        self.position = list(position) # Use list for mutability
        self.velocity = list(velocity) # Use list for mutability
        self.radius = radius
        self.damping_factor = 0.95 # Default damping

class State:
    def __init__(self):
        self.entities = []
        # Example initialization (replace with actual game setup)
        self.entities.append(Entity('ball', (400, 300), (50, -30), radius=10))
        self.entities.append(Entity('player', (100, 300), (0, 0), radius=15))
        self.entities.append(Entity('player', (700, 300), (0, 0), radius=15))


# --- Constants ---
# Field boundaries (min_x, max_x, min_y, max_y)
FIELD_BOUNDARIES = (0, 800, 0, 600) # Example dimensions

# Damping factors (reduces velocity over time)
BALL_DAMPING = 0.99
PLAYER_DAMPING = 0.97 # Players might have less friction or self-propulsion


# --- Movement Function ---
# This function updates position based on velocity and time delta
# Could be in a separate movement.py, but included here for now
def update_movement(entity, dt):
    """Updates entity position based on its velocity and time delta."""
    entity.position[0] += entity.velocity[0] * dt
    entity.position[1] += entity.velocity[1] * dt

# --- Force Functions ---
def apply_damping(entity, damping_factor):
    """Reduces the entity's velocity by a damping factor."""
    entity.velocity[0] *= damping_factor
    entity.velocity[1] *= damping_factor

# --- Collision Functions ---
def check_boundary_collision(entity, boundaries):
    """Checks if an entity collides with the field boundaries."""
    min_x, max_x, min_y, max_y = boundaries
    collided = False
    if entity.position[0] - entity.radius < min_x or entity.position[0] + entity.radius > max_x:
        collided = True
    if entity.position[1] - entity.radius < min_y or entity.position[1] + entity.radius > max_y:
        collided = True
    return collided

def resolve_boundary_collision(entity, boundaries):
    """Resolves collision with boundaries by reversing velocity and adjusting position."""
    min_x, max_x, min_y, max_y = boundaries

    # Resolve X boundary collision
    if entity.position[0] - entity.radius < min_x:
        entity.position[0] = min_x + entity.radius # Correct position
        entity.velocity[0] *= -1 # Reverse velocity
    elif entity.position[0] + entity.radius > max_x:
        entity.position[0] = max_x - entity.radius # Correct position
        entity.velocity[0] *= -1 # Reverse velocity

    # Resolve Y boundary collision
    if entity.position[1] - entity.radius < min_y:
        entity.position[1] = min_y + entity.radius # Correct position
        entity.velocity[1] *= -1 # Reverse velocity
    elif entity.position[1] + entity.radius > max_y:
        entity.position[1] = max_y - entity.radius # Correct position
        entity.velocity[1] *= -1 # Reverse velocity

# --- Main Physics Update Function ---
def update_physics(state: State, dt: float):
    """
    Updates the physics state for all entities.

    Args:
        state: The current game state object.
        dt: The time delta since the last update.
    """
    for entity in state.entities:
        # Apply forces
        if entity.entity_type == 'ball':
            apply_damping(entity, BALL_DAMPING)
        elif entity.entity_type == 'player':
            apply_damping(entity, PLAYER_DAMPING)
        # Add other forces here (e.g., player kick force, gravity if needed)

        # Update movement based on current velocity
        update_movement(entity, dt)

        # Handle collisions
        if entity.entity_type == 'ball':
            if check_boundary_collision(entity, FIELD_BOUNDARIES):
                resolve_boundary_collision(entity, FIELD_BOUNDARIES)
        # Add other collision checks here (e.g., ball-player, player-player)

# Example of how this might be used in a game loop (not part of the required output)
if __name__ == '__main__':
    game_state = State()
    dt = 1/60.0 # Assume 60 FPS update rate

    print("Initial State:")
    for entity in game_state.entities:
        print(f"{entity.entity_type}: Pos={entity.position}, Vel={entity.velocity}")

    # Simulate a few steps
    for i in range(100):
        update_physics(game_state, dt)
        # print(f"Step {i+1}: Ball Pos={game_state.entities[0].position}, Vel={game_state.entities[0].velocity}")

    print("\nState after 100 steps:")
    for entity in game_state.entities:
        print(f"{entity.entity_type}: Pos={entity.position}, Vel={entity.velocity}")

    # Example: Push the ball towards a wall
    game_state.entities[0].velocity = [200, 50]
    print("\nBall pushed towards wall:")
    print(f"Initial Ball Pos={game_state.entities[0].position}, Vel={game_state.entities[0].velocity}")

    for i in range(100):
         update_physics(game_state, dt)

    print("\nState after 100 steps (after push):")
    for entity in game_state.entities:
        print(f"{entity.entity_type}: Pos={entity.position}, Vel={entity.velocity}")