# src/zzocker/state.py

import math

class Vec2:
    """Represents a 2D vector."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        raise TypeError("Operand must be Vec2")

    def __sub__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x - other.x, self.y - other.y)
        raise TypeError("Operand must be Vec2")

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vec2(self.x * scalar, self.y * scalar)
        raise TypeError("Operand must be a scalar")

    def __rmul__(self, scalar):
        return self.__mul__(scalar) # Allow scalar * Vec2

    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)):
            if scalar == 0:
                # Handle division by zero - return zero vector
                return Vec2(0, 0)
            return Vec2(self.x / scalar, self.y / scalar)
        raise TypeError("Operand must be a scalar")

    def length(self):
        """Calculates the magnitude (length) of the vector."""
        return math.sqrt(self.x**2 + self.y**2)

    def length_sq(self):
        """Calculates the squared magnitude of the vector."""
        return self.x**2 + self.y**2

    def normalize(self):
        """Returns a new vector with the same direction but unit length."""
        len_val = self.length()
        if len_val == 0:
            return Vec2(0, 0)
        return self / len_val

    def dot(self, other):
        """Calculates the dot product with another vector."""
        if isinstance(other, Vec2):
            return self.x * other.x + self.y * other.y
        raise TypeError("Operand must be Vec2")

    def distance_to(self, other_vec):
        """Calculates the distance to another vector (interpreted as a point)."""
        if isinstance(other_vec, Vec2):
            return (self - other_vec).length()
        raise TypeError("Operand must be Vec2")

    def distance_sq_to(self, other_vec):
        """Calculates the squared distance to another vector."""
        if isinstance(other_vec, Vec2):
            return (self - other_vec).length_sq()
        raise TypeError("Operand must be Vec2")

    def __eq__(self, other):
        if isinstance(other, Vec2):
            return self.x == other.x and self.y == other.y
        return False

    def __repr__(self):
        return f"Vec2({self.x:.2f}, {self.y:.2f})"

    def __copy__(self):
        return Vec2(self.x, self.y)

    def copy(self):
        return self.__copy__()


class PlayerState:
    """Represents the state of a single player."""
    def __init__(self, player_id: str, team: str, position: Vec2, velocity: Vec2 = None, score: int = 0):
        self.player_id = player_id
        self.team = team # e.g., 'blue', 'red'
        self.position = position.copy() # Vec2
        self.velocity = velocity.copy() if velocity is not None else Vec2(0, 0) # Vec2
        self.score = score
        self.radius = 0.5 # Example radius (adjust as needed)
        self.max_speed = 5.0 # Example max speed (adjust as needed)
        self.acceleration = 15.0 # Example acceleration (adjust as needed)
        self.friction = 5.0 # Example friction coefficient (adjust as needed)

    def __repr__(self):
        return (f"Player(ID={self.player_id}, Team={self.team}, "
                f"Pos={self.position}, Vel={self.velocity}, Score={self.score})")

    def copy(self):
        return PlayerState(
            player_id=self.player_id,
            team=self.team,
            position=self.position.copy(),
            velocity=self.velocity.copy(),
            score=self.score
        )


class BallState:
    """Represents the state of the ball."""
    def __init__(self, position: Vec2, velocity: Vec2 = None):
        self.position = position.copy() # Vec2
        self.velocity = velocity.copy() if velocity is not None else Vec2(0, 0) # Vec2
        self.radius = 0.3 # Example radius (adjust as needed)
        self.mass = 1.0 # Example mass (adjust as needed)
        self.friction = 0.98 # Example friction factor per second (adjust as needed) - applied in physics
        self.max_speed = 20.0 # Example max speed (adjust as needed)

    def __repr__(self):
        return f"Ball(Pos={self.position}, Vel={self.velocity})"

    def copy(self):
        return BallState(
            position=self.position.copy(),
            velocity=self.velocity.copy()
        )


class GameState:
    """Represents the complete state of the game."""
    def __init__(self, field_width: float, field_height: float):
        self.field_width = field_width
        self.field_height = field_height
        self.players = {} # {player_id: PlayerState}
        self.ball = None # BallState
        self.scores = {'blue': 0, 'red': 0}
        self.time = 0.0
        self.game_over = False
        self.goal_width = 2.0 # Example goal width (adjust as needed)

        # Define goal positions (center of the goal line)
        self.blue_goal_pos = Vec2(0, self.field_height / 2)
        self.red_goal_pos = Vec2(0, -self.field_height / 2)

    def add_player(self, player_id: str, team: str, position: Vec2):
        """Adds a player to the game state."""
        if player_id not in self.players:
            self.players[player_id] = PlayerState(player_id, team, position)
        else:
            print(f"Warning: Player {player_id} already exists.")

    def set_ball(self, position: Vec2):
        """Sets or replaces the ball state."""
        self.ball = BallState(position)

    def get_player(self, player_id: str) -> PlayerState | None:
        """Gets a player by ID."""
        return self.players.get(player_id)

    def get_players_on_team(self, team: str) -> dict[str, PlayerState]:
        """Gets all players belonging to a specific team."""
        return {pid: p for pid, p in self.players.items() if p.team == team}

    def get_all_players(self) -> list[PlayerState]:
        """Gets a list of all players."""
        return list(self.players.values())

    def copy(self):
        """Creates a deep copy of the game state."""
        new_state = GameState(self.field_width, self.field_height)
        new_state.players = {pid: p.copy() for pid, p in self.players.items()}
        new_state.ball = self.ball.copy() if self.ball else None
        new_state.scores = self.scores.copy()
        new_state.time = self.time
        new_state.game_over = self.game_over
        new_state.goal_width = self.goal_width
        new_state.blue_goal_pos = self.blue_goal_pos.copy()
        new_state.red_goal_pos = self.red_goal_pos.copy()
        return new_state


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
    """
    Represents the desired actions for a single player in a time step.
    """
    def __init__(self,
                 move_direction: Vec2 = None, # Desired movement direction (normalized or magnitude <= 1)
                 kick_strength: float = 0.0,  # Strength of the kick (0.0 to 1.0)
                 kick_direction: Vec2 = None  # Desired kick direction (normalized)
                 ):
        # Normalize move_direction if provided
        if move_direction is not None:
            self.move_direction = move_direction.normalize()
        else:
            self.move_direction = Vec2(0, 0)

        # Clamp kick_strength between 0 and 1
        self.kick_strength = max(0.0, min(1.0, kick_strength))

        # Normalize kick_direction if provided and strength > 0
        if kick_direction is not None and self.kick_strength > 0:
            self.kick_direction = kick_direction.normalize()
        else:
            self.kick_direction = Vec2(0, 0) # No kick direction if no kick

    def __repr__(self):
        return (f"PlayerActions(Move={self.move_direction}, "
                f"KickStr={self.kick_strength:.2f}, KickDir={self.kick_direction})")

```
```python
# src/zzocker/physics.py

import math
from src.zzocker.state import GameState, PlayerState, BallState, Vec2
from src.zzocker.actions import PlayerActions

# Physics Constants (can be adjusted)
PLAYER_ACCELERATION = 15.0 # Units per second^2
PLAYER_MAX_SPEED = 5.0     # Units per second
PLAYER_FRICTION = 5.0      # Friction coefficient
BALL_FRICTION_PER_SEC = 0.98 # Factor applied to ball velocity per second
BALL_KICK_FORCE = 30.0     # Base force applied by a kick (scaled by strength)
PLAYER_BALL_KICK_DISTANCE = 0.6 # Max distance for player to kick ball (player_radius + ball_radius + small margin)
PLAYER_PLAYER_COLLISION_ELASTICITY = 0.5 # 0 = inelastic, 1 = elastic
PLAYER_BALL_COLLISION_ELASTICITY = 0.8 # 0 = inelastic, 1 = elastic
WALL_COLLISION_ELASTICITY = 0.7 # 0 = inelastic, 1 = elastic


def update_physics(game_state: GameState, player_actions: dict[str, PlayerActions], dt: float):
    """
    Updates the game state based on physics and player actions over a time delta.

    Args:
        game_state: The current GameState object.
        player_actions: A dictionary mapping player_id to PlayerActions.
        dt: The time delta in seconds.
    """
    # Apply player movement actions and friction
    _apply_player_movement(game_state, player_actions, dt)

    # Apply ball friction
    _apply_ball_friction(game_state.ball, dt)

    # Integrate velocities to update positions
    _integrate_positions(game_state, dt)

    # Handle collisions (order can matter, player-ball first often makes sense for kicks)
    _handle_player_ball_collisions(game_state, player_actions) # Apply kick force here
    _handle_player_player_collisions(game_state)
    _handle_wall_collisions(game_state)

    # Cap speeds
    _cap_speeds(game_state)

    # Check for goals
    _check_goals(game_state)

    # Update game time
    game_state.time += dt


def _apply_player_movement(game_state: GameState, player_actions: dict[str, PlayerActions], dt: float):
    """Applies movement forces and friction to players."""
    for player_id, player in game_state.players.items():
        actions = player_actions.get(player_id, PlayerActions()) # Default to no action if not provided

        # Apply acceleration based on desired move direction
        if actions.move_direction.length_sq() > 0:
             # Apply acceleration up to max speed
             desired_velocity = actions.move_direction.normalize() * PLAYER_MAX_SPEED
             acceleration_vector = (desired_velocity - player.velocity) # Simple steering towards desired vel
             # Limit acceleration magnitude
             if acceleration_vector.length_sq() > PLAYER_ACCELERATION**2:
                 acceleration_vector = acceleration_vector.normalize() * PLAYER_ACCELERATION
             player.velocity += acceleration_vector * dt
        else:
            # Apply deceleration (friction) if no movement command
            if player.velocity.length_sq() > 0:
                friction_force = player.velocity.normalize() * -PLAYER_FRICTION
                player.velocity += friction_force * dt
                # Stop completely if velocity becomes very small due to friction
                if player.velocity.length_sq() < (PLAYER_FRICTION * dt)**2: # Check if friction would reverse velocity
                     player.velocity = Vec2(0, 0)


def _apply_ball_friction(ball: BallState, dt: float):
    """Applies friction to the ball."""
    if ball and ball.velocity.length_sq() > 0:
        # Apply friction factor
        friction_factor = BALL_FRICTION_PER_SEC ** dt # Adjust factor based on dt
        ball.velocity *= friction_factor
        # Stop completely if velocity becomes very small
        if ball.velocity.length_sq() < 0.1**2: # Threshold for stopping
             ball.velocity = Vec2(0, 0)


def _integrate_positions(game_state: GameState, dt: float):
    """Updates positions based on velocities."""
    for player in game_state.players.values():
        player.position += player.velocity * dt

    if game_state.ball:
        game_state.ball.position += game_state.ball.velocity * dt


def _handle_player_ball_collisions(game_state: GameState, player_actions: dict[str, PlayerActions]):
    """Handles collisions and kicks between players and the ball."""
    ball = game_state.ball
    if not ball:
        return

    for player_id, player in game_state.players.items():
        # Check for collision
        combined_radius = player.radius + ball.radius
        distance_sq = player.position.distance_sq_to(ball.position)

        if distance_sq < combined_radius**2:
            # Collision detected
            distance = math.sqrt(distance_sq)
            overlap = combined_radius - distance

            # Resolve overlap - push objects apart
            if distance > 0:
                collision_normal = (ball.position - player.position).normalize()
                # Move them apart slightly based on overlap
                ball.position += collision_normal * (overlap / 2)
                player.position -= collision_normal * (overlap / 2)
            else:
                 # Objects are at the exact same position, push in arbitrary direction
                 collision_normal = Vec2(1, 0) # Or a random direction
                 ball.position += collision_normal * (overlap / 2)
                 player.position -= collision_normal * (overlap / 2)


            # Handle velocities (simple elastic collision response)
            # Relative velocity
            v_rel = ball.velocity - player.velocity
            # Velocity along the normal
            vel_along_normal = v_rel.dot(collision_normal)

            # Do not resolve if velocities are separating
            if vel_along_normal < 0:
                 # Calculate impulse scalar
                 # j = -(1 + e) * vel_along_normal / (1/m_a + 1/m_b)
                 # For player (infinite mass approximation for simplicity) and ball:
                 # j = -(1 + e) * vel_along_normal / (1/m_ball) = -(1 + e) * vel_along_normal * m_ball
                 # Using effective mass for player-ball: m_eff = (m_player * m_ball) / (m_player + m_ball)
                 # If player mass is much larger than ball mass, m_eff ~ m_ball
                 # For simplicity, let's use a simplified impulse based on velocity change
                 # Impulse = change in momentum
                 # Change in velocity along normal = -(1+e) * vel_along_normal
                 # Impulse vector = change in velocity along normal * collision_normal * m_ball
                 impulse_scalar = -(1 + PLAYER_BALL_COLLISION_ELASTICITY) * vel_along_normal
                 impulse = collision_normal * impulse_scalar * ball.mass

                 # Apply impulse
                 ball.velocity += impulse / ball.mass
                 # Player velocity change is smaller (or zero if infinite mass)
                 # For simplicity, let's primarily affect the ball velocity

            # Check for kick action after potential collision resolution
            actions = player_actions.get(player_id, PlayerActions())
            # Check if player is close enough to kick (slightly larger threshold than collision)
            # And if a kick action was requested with sufficient strength
            if player.position.distance_sq_to(ball.position) < PLAYER_BALL_KICK_DISTANCE**2 and actions.kick_strength > 0.01:
                # Apply kick force in the desired direction
                kick_force_vector = actions.kick_direction.normalize() * (BALL_KICK_FORCE * actions.kick_strength)
                # Apply force over a small time step or directly modify velocity
                # Direct velocity change is simpler for arcade physics
                # dv = F * dt / m  ->  v_new = v_old + F * dt / m
                # Let's approximate this as a direct velocity boost
                # The magnitude of the boost could be proportional to force and dt
                # Or simply a fixed impulse scaled by strength
                kick_impulse = kick_force_vector * dt * 10 # Scale force to impulse
                ball.velocity += kick_impulse / ball.mass # Apply impulse to ball velocity

                # Ensure kick doesn't reduce speed if ball was already moving fast in kick direction
                # This part can be complex, simple addition is often sufficient for games.


def _handle_player_player_collisions(game_state: GameState):
    """Handles collisions between players."""
    players = list(game_state.players.values())
    num_players = len(players)

    # Use a simple pairwise check (O(N^2))
    # For performance, consider spatial partitioning (grid, quadtree) for many players
    for i in range(num_players):
        for j in range(i + 1, num_players):
            p1 = players[i]
            p2 = players[j]

            combined_radius = p1.radius + p2.radius
            distance_sq = p1.position.distance_sq_to(p2.position)

            if distance_sq < combined_radius**2:
                # Collision detected
                distance = math.sqrt(distance_sq)
                overlap = combined_radius - distance

                # Resolve overlap - push objects apart
                if distance > 0:
                    collision_normal = (p2.position - p1.position).normalize()
                    # Push apart based on overlap, distributing based on mass (or equally for simplicity)
                    p1.position -= collision_normal * (overlap / 2)
                    p2.position += collision_normal * (overlap / 2)
                else:
                    # Objects are at the exact same position, push in arbitrary direction
                    collision_normal = Vec2(1, 0) # Or a random direction
                    p1.position -= collision_normal * (overlap / 2)
                    p2.position += collision_normal * (overlap / 2)


                # Handle velocities (elastic collision response)
                # Relative velocity
                v_rel = p2.velocity - p1.velocity
                # Velocity along the normal
                vel_along_normal = v_rel.dot(collision_normal)

                # Do not resolve if velocities are separating
                if vel_along_normal < 0:
                    # Calculate impulse scalar
                    # Assuming equal mass for simplicity
                    impulse_scalar = -(1 + PLAYER_PLAYER_COLLISION_ELASTICITY) * vel_along_normal
                    # Impulse vector
                    impulse = collision_normal * impulse_scalar

                    # Apply impulse (assuming equal mass, impulse split equally)
                    p1.velocity -= impulse / 2 # Player mass could be factor here
                    p2.velocity += impulse / 2 # Player mass could be factor here


def _handle_wall_collisions(game_state: GameState):
    """Handles collisions of players and the ball with the field boundaries."""
    field_half_width = game_state.field_width / 2
    field_half_height = game_state.field_height / 2

    # Ball collisions
    ball = game_state.ball
    if ball:
        # Left wall
        if ball.position.x - ball.radius < -field_half_width:
            ball.position.x = -field_half_width + ball.radius # Correct position
            if ball.velocity.x < 0: # Only reflect if moving into the wall
                ball.velocity.x *= -WALL_COLLISION_ELASTICITY # Reverse and dampen velocity

        # Right wall
        if ball.position.x + ball.radius > field_half_width:
            ball.position.x = field_half_width - ball.radius
            if ball.velocity.x > 0:
                ball.velocity.x *= -WALL_COLLISION_ELASTICITY

        # Top wall (excluding goals)
        # Check if ball is outside goal area horizontally
        if abs(ball.position.x) > game_state.goal_width / 2:
            # Top wall (Red's side endline)
            if ball.position.y + ball.radius > field_half_height:
                ball.position.y = field_half_height - ball.radius
                if ball.velocity.y > 0:
                    ball.velocity.y *= -WALL_COLLISION_ELASTICITY

            # Bottom wall (Blue's side endline)
            if ball.position.y - ball.radius < -field_half_height:
                ball.position.y = -field_half_height + ball.radius
                if ball.velocity.y < 0:
                    ball.velocity.y *= -WALL_COLLISION_ELASTICITY

        # Note: Goal collisions are handled by _check_goals which resets the state


    # Player collisions
    for player in game_state.players.values():
        # Left wall
        if player.position.x - player.radius < -field_half_width:
            player.position.x = -field_half_width + player.radius
            if player.velocity.x < 0:
                player.velocity.x *= -WALL_COLLISION_ELASTICITY

        # Right wall
        if player.position.x + player.radius > field_half_width:
            player.position.x = field_half_width - player.radius
            if player.velocity.x > 0:
                player.velocity.x *= -WALL_COLLISION_ELASTICITY

        # Top wall (Red's side endline)
        if player.position.y + player.radius > field_half_height:
            player.position.y = field_half_height - player.radius
            if player.velocity.y > 0:
                player.velocity.y *= -WALL_COLLISION_ELASTICITY

        # Bottom wall (Blue's side endline)
        if player.position.y - player.radius < -field_half_height:
            player.position.y = -field_half_height + player.radius
            if player.velocity.y < 0:
                player.velocity.y *= -WALL_COLLISION_ELASTICITY


def _cap_speeds(game_state: GameState):
    """Limits the maximum speed of players and the ball."""
    for player in game_state.players.values():
        if player.velocity.length_sq() > player.max_speed**2:
            player.velocity = player.velocity.normalize() * player.max_speed

    if game_state.ball:
        if game_state.ball.velocity.length_sq() > game_state.ball.max_speed**2:
            game_state.ball.velocity = game_state.ball.velocity.normalize() * game_state.ball.max_speed


def _check_goals(game_state: GameState):
    """Checks if the ball has entered a goal."""
    ball = game_state.ball
    if not ball:
        return

    field_half_height = game_state.field_height / 2
    goal_half_width = game_state.goal_width / 2

    # Check if ball is beyond the end lines
    if abs(ball.position.y) > field_half_height:
        # Check if ball is within the horizontal bounds of the goal
        if abs(ball.position.x) < goal_half_width:
            # Goal scored!
            if ball.position.y > 0: # Ball is beyond Red's end line (top)
                # Blue scores!
                print("Goal! Blue scores!")
                game_state.scores['blue'] += 1
                _reset_game_state_after_goal(game_state, scoring_team='blue')
            else: # Ball is beyond Blue's end line (bottom)
                # Red scores!
                print("Goal! Red scores!")
                game_state.scores['red'] += 1
                _reset_game_state_after_goal(game_state, scoring_team='red')


def _reset_game_state_after_goal(game_state: GameState, scoring_team: str):
    """Resets player and ball positions after a goal."""
    print(f"Scores: Blue {game_state.scores['blue']} - Red {game_state.scores['red']}")

    # Reset ball to center
    game_state.ball.position = Vec2(0, 0)
    game_state.ball.velocity = Vec2(0, 0)

    # Reset players to starting positions (example - can be customized)
    # This is a simple example, actual starting positions might be needed from config
    player_count = len(game_state.players)
    blue_players = game_state.get_players_on_team('blue')
    red_players = game_state.get_players_on_team('red')

    # Simple reset positions (adjust based on number of players and field size)
    field_half_width = game_state.field_width / 2
    field_half_height = game_state.field_height / 2

    blue_start_y = -field_half_height * 0.7 # Towards their own goal
    red_start_y = field_half_height * 0.7 # Towards their own goal

    # Distribute players horizontally
    blue_player_positions = [Vec2(x, blue_start_y) for x in [-game_state.goal_width*0.5, game_state.goal_width*0.5]] # Example for 2 players
    red_player_positions = [Vec2(x, red_start_y) for x in [-game_state.goal_width*0.5, game_state.goal_width*0.5]] # Example for 2 players


    blue_idx = 0
    red_idx = 0
    for player in game_state.players.values():
        player.velocity = Vec2(0, 0) # Reset velocity

        if player.team == 'blue':
             if blue_idx < len(blue_player_positions):
                 player.position = blue_player_positions[blue_idx].copy()
                 blue_idx += 1
             else:
                 # Handle case where there are more players than defined positions
                 player.position = Vec2(0, blue_start_y) # Default to center
        elif player.team == 'red':
             if red_idx < len(red_player_positions):
                 player.position = red_player_positions[red_idx].copy()
                 red_idx += 1
             else:
                 # Handle case where there are more players than defined positions
                 player.position = Vec2(0, red_start_y) # Default to center

    # TODO: Add logic for game end conditions (e.g., score limit, time limit)

```
```python
# src/zzocker/ai/player_ai.py

from src.zzocker.state import GameState, PlayerState, BallState, Vec2
from src.zzocker.actions import PlayerActions
import math

class PlayerAI:
    """
    Base class for player AI. All custom AIs should inherit from this.
    """
    def __init__(self, player_id: str, team: str):
        self.player_id = player_id
        self.team = team

    def get_actions(self, game_state: GameState) -> PlayerActions:
        """
        Abstract method: Should return the desired actions for the player
        based on the current game state.

        Args:
            game_state: The current GameState object.

        Returns:
            A PlayerActions object.
        """
        raise NotImplementedError("Subclasses must implement get_actions")


class SimpleSeekAI(PlayerAI):
    """
    A simple AI that tries to move towards the