# src/zzocker/state.py

import math

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vec2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        if scalar == 0:
            return Vec2(0, 0) # Avoid division by zero
        return Vec2(self.x / scalar, self.y / scalar)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        len_val = self.length()
        if len_val == 0:
            return Vec2(0, 0)
        return self / len_val

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def distance_to(self, other_vec):
        return (self - other_vec).length()

    def __repr__(self):
        return f"Vec2({self.x:.2f}, {self.y:.2f})"

class PlayerState:
    def __init__(self, player_id, team, position, velocity=None, score=0):
        self.player_id = player_id
        self.team = team # e.g., 'blue', 'red'
        self.position = position # Vec2
        self.velocity = velocity if velocity is not None else Vec2(0, 0) # Vec2
        self.score = score
        self.radius = 0.5 # Example radius

class BallState:
    def __init__(self, position, velocity=None):
        self.position = position # Vec2
        self.velocity = velocity if velocity is not None else Vec2(0, 0) # Vec2
        self.radius = 0.3 # Example radius

class GameState:
    def __init__(self, field_width, field_height):
        self.field_width = field_width
        self.field_height = field_height
        self.players = {} # {player_id: PlayerState}
        self.ball = None # BallState
        self.scores = {'blue': 0, 'red': 0}
        self.time = 0.0
        self.game_over = False

    def add_player(self, player_id, team, position):
        if player_id not in self.players:
            self.players[player_id] = PlayerState(player_id, team, position)
        else:
            print(f"Warning: Player {player_id} already exists.")

    def set_ball(self, position):
        self.ball = BallState(position)

    def get_player(self, player_id):
        return self.players.get(player_id)

    def get_players_on_team(self, team):
        return {pid: p for pid, p in self.players.items() if p.team == team}

    def __repr__(self):
        player_repr = "\n  ".join([f"{p.player_id}: Pos={p.position}, Vel={p.velocity}" for p in self.players.values()])
        ball_repr = f"Pos={self.ball.position}, Vel={self.ball.velocity}" if self.ball else "None"
        return (f"GameState(Time={self.time:.2f}, Scores={self.scores}, "
                f"Ball={ball_repr}, Players=[\n  {player_repr}\n])")

```
```python
# src/zzocker/actions.py

from src.zzocker.state import Vec2

class PlayerActions:
    def __init__(self, move_direction=None, kick_strength=0.0):
        """
        Represents the actions a single player wants to take in a simulation step.

        Args:
            move_direction (Vec2 or None): The desired direction of movement.
                                           Should be a normalized vector or Vec2(0,0)
                                           if no movement is desired.
            kick_strength (float): The strength of a kick action.
                                   0.0 means no kick. Positive value indicates kick strength.
        """
        self.move_direction = move_direction if move_direction is not None else Vec2(0, 0)
        self.kick_strength = max(0.0, kick_strength) # Ensure non-negative

    def __repr__(self):
        return f"PlayerActions(move_direction={self.move_direction}, kick_strength={self.kick_strength:.2f})"

```
```python
# src/zzocker/physics.py

from src.zzocker.state import GameState, PlayerState, BallState, Vec2
from src.zzocker.actions import PlayerActions
import math

# Constants (example values, should be tuned)
PLAYER_MOVE_SPEED = 5.0 # Units per second
BALL_FRICTION = 0.99 # Multiplier per step
PLAYER_FRICTION = 0.9 # Multiplier per step
KICK_FORCE_MULTIPLIER = 10.0
PLAYER_BALL_INTERACT_DIST = 0.8 # Distance threshold for player-ball interaction

def update_state(state: GameState, all_player_actions: dict[str, PlayerActions], dt: float):
    """
    Updates the game state based on physics, player actions, and time delta.

    Args:
        state (GameState): The current state of the game. This object will be modified.
        all_player_actions (dict[str, PlayerActions]): A dictionary mapping player_id to PlayerActions.
        dt (float): The time delta for this simulation step (e.g., seconds per frame).
    """
    # Apply player actions and movement
    for player_id, player in state.players.items():
        actions = all_player_actions.get(player_id, PlayerActions()) # Get actions or default
        
        # Apply movement based on desired direction (simple model)
        desired_velocity = actions.move_direction.normalize() * PLAYER_MOVE_SPEED
        player.velocity = desired_velocity # Instantaneous change for simplicity

        # Apply player friction (slow down if no action or limited action)
        # A more complex model would blend desired velocity with current velocity
        player.velocity = player.velocity * PLAYER_FRICTION # Simple friction

        # Update player position
        player.position += player.velocity * dt

        # Handle player-ball interaction (kick)
        if state.ball and actions.kick_strength > 0:
            dist_to_ball = player.position.distance_to(state.ball.position)
            if dist_to_ball < player.radius + state.ball.radius + PLAYER_BALL_INTERACT_DIST:
                # Calculate kick direction (from player to ball)
                kick_direction = (state.ball.position - player.position).normalize()
                # Apply force to the ball
                kick_force = kick_direction * (actions.kick_strength * KICK_FORCE_MULTIPLIER)
                state.ball.velocity += kick_force * dt # Apply as impulse/force over dt

    # Update ball physics
    if state.ball:
        # Apply ball friction
        state.ball.velocity *= BALL_FRICTION

        # Update ball position
        state.ball.position += state.ball.velocity * dt

        # Handle wall collisions for ball (simple reflection)
        if state.ball.position.x < state.ball.radius:
            state.ball.position.x = state.ball.radius
            state.ball.velocity.x *= -1
        elif state.ball.position.x > state.field_width - state.ball.radius:
            state.ball.position.x = state.field_width - state.ball.radius
            state.ball.velocity.x *= -1

        if state.ball.position.y < state.ball.radius:
            state.ball.position.y = state.ball.radius
            state.ball.velocity.y *= -1
        elif state.ball.position.y > state.field_height - state.ball.radius:
            state.ball.position.y = state.field_height - state.ball.radius
            state.ball.velocity.y *= -1

        # Handle scoring (simplified: check if ball is behind goal line)
        # Assume goals are centered on the ends (x=0 and x=field_width)
        # and have a certain width (e.g., 20% of field height, centered)
        goal_width = state.field_height * 0.2
        goal_y_min = (state.field_height - goal_width) / 2.0
        goal_y_max = (state.field_height + goal_width) / 2.0

        scored = False
        if state.ball.position.x < 0 and goal_y_min < state.ball.position.y < goal_y_max:
            # Ball crossed left goal line (score for red team if blue attacked left)
            # Assuming blue attacks right, red attacks left
            state.scores['red'] += 1
            print(f"Score! Red team scores. Current scores: {state.scores}")
            scored = True
        elif state.ball.position.x > state.field_width and goal_y_min < state.ball.position.y < goal_y_max:
            # Ball crossed right goal line (score for blue team)
            state.scores['blue'] += 1
            print(f"Score! Blue team scores. Current scores: {state.scores}")
            scored = True

        if scored:
            # Reset ball and player positions after score
            reset_positions(state)


    # Update game time
    state.time += dt

    # Check for game over condition (example: first team to 5 goals)
    if state.scores['blue'] >= 5 or state.scores['red'] >= 5:
        state.game_over = True
        print("Game Over!")

def reset_positions(state: GameState):
    """Resets ball and player positions after a score."""
    state.ball.position = Vec2(state.field_width / 2, state.field_height / 2)
    state.ball.velocity = Vec2(0, 0)

    # Example: Reset players to center line
    blue_start_x = state.field_width * 0.25
    red_start_x = state.field_width * 0.75
    player_y_spacing = state.field_height / (len(state.players) / 2 + 1) # Simple spacing

    blue_count = 0
    red_count = 0
    for player in state.players.values():
        player.velocity = Vec2(0, 0)
        if player.team == 'blue':
            blue_count += 1
            player.position = Vec2(blue_start_x, blue_count * player_y_spacing)
        else: # red team
            red_count += 1
            player.position = Vec2(red_start_x, red_count * player_y_spacing)

```
```python
# src/zzocker/ai/player_ai.py

from src.zzocker.state import GameState, PlayerState, Vec2
from src.zzocker.actions import PlayerActions

class PlayerAI:
    def __init__(self, player_id, team):
        self.player_id = player_id
        self.team = team

    def get_actions(self, game_state: GameState) -> PlayerActions:
        """
        Calculates and returns the actions for this player based on the current game state.

        Args:
            game_state (GameState): The current state of the game.

        Returns:
            PlayerActions: The actions the AI wants the player to perform this step.
        """
        player = game_state.get_player(self.player_id)
        if not player or not game_state.ball:
            return PlayerActions(move_direction=Vec2(0, 0), kick_strength=0.0) # No actions if player/ball missing

        # Simple AI: Move towards the ball and try to kick if close
        ball_position = game_state.ball.position
        player_position = player.position

        # Calculate direction towards the ball
        direction_to_ball = ball_position - player_position
        move_direction = direction_to_ball.normalize()

        # Determine if close enough to kick
        distance_to_ball = direction_to_ball.length()
        kick_strength = 0.0
        # Use a slightly larger threshold than physics interaction distance
        # to give the AI a chance to initiate the kick action
        if distance_to_ball < player.radius + game_state.ball.radius + 1.0: # Example threshold
             # Simple kick strength: max strength if close
             kick_strength = 1.0 # Example max strength

        return PlayerActions(move_direction=move_direction, kick_strength=kick_strength)

```
```python
# src/zzocker/simulation.py

from src.zzocker.state import GameState, Vec2
from src.zzocker.actions import PlayerActions
from src.zzocker import physics
from src.zzocker.ai.player_ai import PlayerAI
import time

class SimulationManager:
    def __init__(self, field_width=100, field_height=60, dt=1/60.0):
        """
        Initializes the simulation manager.

        Args:
            field_width (int): Width of the game field.
            field_height (int): Height of the game field.
            dt (float): Time step for each simulation frame (seconds).
        """
        self.field_width = field_width
        self.field_height = field_height
        self.dt = dt
        self.game_state = GameState(field_width, field_height)
        self.ais = {} # {player_id: PlayerAI instance}

        # Setup initial state (example)
        self._setup_initial_state()

    def _setup_initial_state(self):
        """Sets up the initial players, ball, and positions."""
        # Add players
        # Team Blue (attacks right)
        self.game_state.add_player("blue_p1", "blue", Vec2(self.field_width * 0.25, self.field_height * 0.5))
        # Team Red (attacks left)
        self.game_state.add_player("red_p1", "red", Vec2(self.field_width * 0.75, self.field_height * 0.5))

        # Set ball position
        self.game_state.set_ball(Vec2(self.field_width / 2, self.field_height / 2))

        # Initialize AIs for all players
        for player_id, player in self.game_state.players.items():
            self.ais[player_id] = PlayerAI(player_id, player.team)
            print(f"Initialized AI for {player_id} ({player.team})")

    def step(self):
        """
        Executes one step of the simulation.

        Returns:
            bool: True if the simulation is ongoing, False if game is over.
        """
        if self.game_state.game_over:
            return False

        # 1. Get actions from all AIs
        all_player_actions = {}
        for player_id, ai in self.ais.items():
            # Pass the current game state to each AI
            actions = ai.get_actions(self.game_state)
            all_player_actions[player_id] = actions
            # print(f"AI {player_id} actions: {actions}") # Optional: log actions

        # 2. Update game state based on physics and actions
        # The physics module modifies the game_state object directly
        physics.update_state(self.game_state, all_player_actions, self.dt)

        # 3. Check for game over (handled within physics.update_state for scoring)
        # The game_state.game_over flag is updated there.

        return not self.game_state.game_over

    def run(self, max_steps=10000):
        """Runs the simulation for a maximum number of steps."""
        print("Starting simulation...")
        step_count = 0
        while step_count < max_steps and self.step():
            # Optional: print state periodically or visualize
            # if step_count % 100 == 0:
            #     print(f"Step {step_count}: {self.game_state}")
            step_count += 1
            # Optional: add a small delay to slow down simulation for viewing
            # time.sleep(self.dt)

        print(f"Simulation finished after {step_count} steps.")
        print(f"Final Scores: {self.game_state.scores}")

# Example usage (optional, could be in a separate run script)
# if __name__ == "__main__":
#     sim = SimulationManager()
#     sim.run(max_steps=5000) # Run for up to 5000 steps