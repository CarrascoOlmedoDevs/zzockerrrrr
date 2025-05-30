import typing

# Define type aliases for clarity
Vector2D = typing.Tuple[float, float]
Vector3D = typing.Tuple[float, float, float]
Position = typing.Union[Vector2D, Vector3D]
Velocity = typing.Union[Vector2D, Vector3D]
Orientation = typing.Union[float, Vector2D, Vector3D] # Angle or vector direction
Attributes = typing.Dict[str, float]

class Player:
    """
    Represents a single football player in the simulation.
    """
    def __init__(self,
                 id: int,
                 team: str,
                 position: Position,
                 velocity: Velocity,
                 orientation: Orientation,
                 is_controlled_by_ai: bool,
                 stamina: float,
                 attributes: Attributes):
        """
        Initializes a Player object.

        Args:
            id: Unique identifier for the player.
            team: The team the player belongs to (e.g., 'home', 'away').
            position: The current position of the player (2D or 3D vector).
            velocity: The current velocity of the player (2D or 3D vector).
            orientation: The orientation or facing direction of the player (angle or vector).
            is_controlled_by_ai: True if the player is controlled by AI, False if human/other.
            stamina: The current stamina level (e.g., 0.0 to 1.0).
            attributes: Dictionary of player attributes (e.g., {'speed': 0.8, 'shooting': 0.7}).
        """
        self.id: int = id
        self.team: str = team
        self.position: Position = position
        self.velocity: Velocity = velocity
        self.orientation: Orientation = orientation
        self.is_controlled_by_ai: bool = is_controlled_by_ai
        self.stamina: float = stamina
        self.attributes: Attributes = attributes

class Ball:
    """
    Represents the football in the simulation.
    """
    def __init__(self,
                 position: Position,
                 velocity: Velocity,
                 spin: typing.Optional[Vector3D] = None,
                 friction: float = 0.01):
        """
        Initializes a Ball object.

        Args:
            position: The current position of the ball (2D or 3D vector).
            velocity: The current velocity of the ball (2D or 3D vector).
            spin: The current spin of the ball (3D vector, optional).
            friction: A factor representing air resistance and surface friction effects.
        """
        self.position: Position = position
        self.velocity: Velocity = velocity
        self.spin: typing.Optional[Vector3D] = spin
        self.friction: float = friction # Combined friction/drag factor

class Field:
    """
    Represents the football field and its properties.
    """
    def __init__(self,
                 dimensions: typing.Tuple[float, float], # (width, height)
                 goal_positions: typing.List[Position], # Positions of the centers of the goals
                 boundaries: typing.Any, # Could be a Rect object, list of points, etc.
                 surface_friction: float = 0.05):
        """
        Initializes a Field object.

        Args:
            dimensions: The size of the playable area (width, height).
            goal_positions: A list containing the positions of the goals.
            boundaries: Definition of the field limits (e.g., a rectangle object).
            surface_friction: A factor representing the friction of the grass surface.
        """
        self.dimensions: typing.Tuple[float, float] = dimensions
        self.goal_positions: typing.List[Position] = goal_positions
        self.boundaries: typing.Any = boundaries # Placeholder for a more specific type if needed
        self.surface_friction: float = surface_friction

class TimeState:
    """
    Represents the current time state of the match.
    """
    def __init__(self,
                 current_time_seconds: float = 0.0,
                 half_length_seconds: float = 2700.0, # 45 minutes
                 is_half_time: bool = False,
                 is_full_time: bool = False):
        """
        Initializes a TimeState object.

        Args:
            current_time_seconds: The elapsed time in the current half/period.
            half_length_seconds: The standard duration of a half in seconds.
            is_half_time: True if the match is currently at half-time break.
            is_full_time: True if the match has concluded.
        """
        self.current_time_seconds: float = current_time_seconds
        self.half_length_seconds: float = half_length_seconds
        self.is_half_time: bool = is_half_time
        self.is_full_time: bool = is_full_time

class ScoreState:
    """
    Represents the current score of the match.
    """
    def __init__(self,
                 home_score: int = 0,
                 away_score: int = 0):
        """
        Initializes a ScoreState object.

        Args:
            home_score: The current score for the home team.
            away_score: The current score for the away team.
        """
        self.home_score: int = home_score
        self.away_score: int = away_score

# Example usage (optional, for demonstration, not part of the final file content)
if __name__ == '__main__':
    # Example Player
    player1 = Player(
        id=1,
        team='home',
        position=(0.0, 10.0),
        velocity=(0.0, 0.0),
        orientation=90.0, # Degrees
        is_controlled_by_ai=True,
        stamina=1.0,
        attributes={'speed': 0.85, 'shooting': 0.7, 'passing': 0.75}
    )
    print(f"Player 1: ID={player1.id}, Team={player1.team}, Pos={player1.position}, Stamina={player1.stamina}")

    # Example Ball
    ball = Ball(position=(0.0, 0.0), velocity=(0.0, 0.0), friction=0.005)
    print(f"Ball: Pos={ball.position}, Vel={ball.velocity}")

    # Example Field
    field = Field(
        dimensions=(105.0, 68.0), # Standard FIFA dimensions
        goal_positions=[(-52.5, 0.0), (52.5, 0.0)], # Assuming center of field is (0,0)
        boundaries=(-52.5, -34.0, 52.5, 34.0), # (min_x, min_y, max_x, max_y)
        surface_friction=0.06
    )
    print(f"Field: Dimensions={field.dimensions}, Goal Positions={field.goal_positions}")

    # Example TimeState
    time_state = TimeState(current_time_seconds=1500.0)
    print(f"Time: Current={time_state.current_time_seconds}s, Half Length={time_state.half_length_seconds}s")

    # Example ScoreState
    score_state = ScoreState(home_score=2, away_score=1)
    print(f"Score: Home={score_state.home_score}, Away={score_state.away_score}")