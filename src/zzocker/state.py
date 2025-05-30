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
                 attributes: Attributes,
                 mass: float, # Added mass
                 radius: float): # Added radius
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
            mass: The mass of the player (for physics calculations).
            radius: The radius of the player (for collision detection).
        """
        self.id: int = id
        self.team: str = team
        self.position: Position = position
        self.velocity: Velocity = velocity
        self.orientation: Orientation = orientation
        self.is_controlled_by_ai: bool = is_controlled_by_ai
        self.stamina: float = stamina
        self.attributes: Attributes = attributes
        self.mass: float = mass # Added mass attribute
        self.radius: float = radius # Added radius attribute

class Ball:
    """
    Represents the football in the simulation.
    """
    def __init__(self,
                 position: Position,
                 velocity: Velocity,
                 spin: typing.Optional[Vector3D] = None,
                 friction: float = 0.01,
                 mass: float = 0.43, # Added mass with default value (FIFA standard approx)
                 radius: float = 0.11): # Added radius with default value (FIFA standard approx)
        """
        Initializes a Ball object.

        Args:
            position: The current position of the ball (2D or 3D vector).
            velocity: The current velocity of the ball (2D or 3D vector).
            spin: The current spin of the ball (3D vector, optional).
            friction: A factor representing air resistance and surface friction effects.
            mass: The mass of the ball (for physics calculations).
            radius: The radius of the ball (for collision detection).
        """
        self.position: Position = position
        self.velocity: Velocity = velocity
        self.spin: typing.Optional[Vector3D] = spin
        self.friction: float = friction # Combined friction/drag factor
        self.mass: float = mass # Added mass attribute
        self.radius: float = radius # Added radius attribute

class Field:
    """
    Represents the football field and its properties.
    """
    def __init__(self,
                 dimensions: typing.Tuple[float, float], # (width, height)
                 goal_positions: typing.List[Position], # Positions of the centers of the goals
                 boundaries: typing.Any): # Could be a Rect object, list of points, etc.
        """
        Initializes a Field object.

        Args:
            dimensions: The width and height of the playing area.
            goal_positions: A list of positions for the goals.
            boundaries: Representation of the field boundaries.
        """
        self.dimensions: typing.Tuple[float, float] = dimensions
        self.goal_positions: typing.List[Position] = goal_positions
        self.boundaries: typing.Any = boundaries # This type might need refinement later

class GameState:
    """
    Represents the complete state of the football simulation at a given moment.
    """
    def __init__(self,
                 players: typing.List[Player],
                 ball: Ball,
                 field: Field,
                 score: typing.Dict[str, int], # {'home': 0, 'away': 0}
                 time: float, # Current time in the match (e.g., seconds)
                 is_game_over: bool = False):
        """
        Initializes a GameState object.

        Args:
            players: A list of all players in the game.
            ball: The ball object.
            field: The field object.
            score: Dictionary representing the current score for each team.
            time: The current time in the match.
            is_game_over: Flag indicating if the game has ended.
        """
        self.players: typing.List[Player] = players
        self.ball: Ball = ball
        self.field: Field = field
        self.score: typing.Dict[str, int] = score
        self.time: float = time
        self.is_game_over: bool = is_game_over

    def get_player_by_id(self, player_id: int) -> typing.Optional[Player]:
        """
        Retrieves a player by their unique ID.

        Args:
            player_id: The ID of the player to retrieve.

        Returns:
            The Player object if found, otherwise None.
        """
        for player in self.players:
            if player.id == player_id:
                return player
        return None

    def get_players_by_team(self, team_name: str) -> typing.List[Player]:
        """
        Retrieves all players belonging to a specific team.

        Args:
            team_name: The name of the team ('home' or 'away').

        Returns:
            A list of Player objects belonging to the specified team.
        """
        return [player for player in self.players if player.team == team_name]