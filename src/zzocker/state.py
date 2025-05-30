import typing

# Define type aliases for clarity
Vector2D = typing.Tuple[float, float]
Vector3D = typing.Tuple[float, float, float]
Position = typing.Union[Vector2D, Vector3D]
Velocity = typing.Union[Vector2D, Vector3D]
Orientation = typing.Union[float, Vector2D, Vector3D] # Angle or vector direction
Attributes = typing.Dict[str, float]

# Define a placeholder type for the AI controller base class.
# Replace typing.Any with the actual type (e.g., AIBasePlayer)
# once the AI module structure is defined and imported.
AIBasePlayer = typing.Any # Placeholder for the base AI controller class type

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
                 mass: float,
                 radius: float,
                 ai_controller: typing.Optional[AIBasePlayer] = None): # Added ai_controller
        """
        Generates a Player object.

        Args:
            id: Unique identifier for the player.
            team: The team the player belongs to (e.g., 'home', 'away').
            position: The current position of the player (2D or 3D vector).
            velocity: The current velocity of the player (2D or 3D vector).
            orientation: The orientation or facing direction of the player (angle or vector).
            is_controlled_by_ai: True if the player is controlled by AI, False if human/other.
                                 This flag indicates if an AI controller is responsible for this player.
            stamina: The current stamina level (e.g., 0.0 to 1.0).
            attributes: Dictionary of player attributes (e.g., {'speed': 0.8, 'shooting': 0.7}).
            mass: The mass of the player (for physics calculations).
            radius: The radius of the player (for collision detection).
            ai_controller: An optional instance of an AI controller class responsible for this player's decisions.
                           Should be None if is_controlled_by_ai is False.
        """
        self.id: int = id
        self.team: str = team
        self.position: Position = position
        self.velocity: Velocity = velocity
        self.orientation: Orientation = orientation
        self.is_controlled_by_ai: bool = is_controlled_by_ai
        self.stamina: float = stamina
        self.attributes: Attributes = attributes
        self.mass: float = mass
        self.radius: float = radius
        self.ai_controller: typing.Optional[AIBasePlayer] = ai_controller # Store the AI controller instance

class Ball:
    """
    Represents the football in the simulation.
    """
    def __init__(self,
                 position: Position,
                 velocity: Velocity,
                 mass: float,
                 radius: float):
        """
        Generates a Ball object.

        Args:
            position: The current position of the ball (2D or 3D vector).
            velocity: The current velocity of the ball (2D or 3D vector).
            mass: The mass of the ball (for physics calculations).
            radius: The radius of the ball (for collision detection).
        """
        self.position: Position = position
        self.velocity: Velocity = velocity
        self.mass: float = mass
        self.radius: float = radius

# Define type aliases for collections within GameState
PlayersList = typing.List[Player]
# Example FieldDimensions: {'length': 105.0, 'width': 68.0, 'goal_size': (7.32, 2.44), 'center_circle_radius': 9.15}
FieldDimensions = typing.Dict[str, typing.Union[float, typing.Tuple[float, float]]]
# Example TeamSides: {'home': 'left', 'away': 'right'}
TeamSides = typing.Dict[str, str]

class GameState:
    """
    Represents the complete state of the football simulation at a given moment.
    """
    def __init__(self,
                 players: PlayersList,
                 ball: Ball,
                 game_time: float = 0.0, # Current time elapsed in the game
                 score: typing.Tuple[int, int] = (0, 0), # Current score (home, away)
                 ball_possession_player_id: typing.Optional[int] = None, # ID of player possessing the ball, or None
                 last_ball_touch_player_id: typing.Optional[int] = None, # ID of player who last touched the ball, or None
                 field_dimensions: typing.Optional[FieldDimensions] = None, # Dimensions of the field
                 team_sides: typing.Optional[TeamSides] = None # Sides of the field for each team
                ):
        """
        Generates a GameState object.

        Args:
            players: A list of all Player objects in the game.
            ball: The Ball object.
            game_time: The current time elapsed in the game (e.g., in seconds).
            score: The current score of the game, as a tuple (home_score, away_score).
            ball_possession_player_id: The ID of the player currently deemed to have possession of the ball, or None.
            last_ball_touch_player_id: The ID of the player who last touched the ball, or None.
            field_dimensions: Dictionary defining the dimensions of the field (e.g., length, width, goal size).
                              Required for context and calculations like offside. Can be None if not initialized yet.
            team_sides: Dictionary mapping team names ('home', 'away') to their side of the field ('left', 'right').
                        Required for context and calculations like offside. Can be None if not initialized yet.
        """
        self.players: PlayersList = players
        self.ball: Ball = ball
        self.game_time: float = game_time
        self.score: typing.Tuple[int, int] = score
        self.ball_possession_player_id: typing.Optional[int] = ball_possession_player_id
        self.last_ball_touch_player_id: typing.Optional[int] = last_ball_touch_player_id
        self.field_dimensions: typing.Optional[FieldDimensions] = field_dimensions
        self.team_sides: typing.Optional[TeamSides] = team_sides

    def get_player_by_id(self, player_id: int) -> typing.Optional[Player]:
        """
        Finds and returns a player by their ID.

        Args:
            player_id: The unique identifier of the player to find.

        Returns:
            The Player object if found, otherwise None.
        """
        for player in self.players:
            if player.id == player_id:
                return player
        return None

    def get_players_by_team(self, team_name: str) -> PlayersList:
        """
        Finds and returns all players belonging to a specific team.

        Args:
            team_name: The name of the team ('home' or 'away').

        Returns:
            A list of Player objects belonging to the specified team.
        """
        return [player for player in self.players if player.team == team_name]

    def get_player_with_possession(self) -> typing.Optional[Player]:
        """
        Returns the Player object currently in possession of the ball.

        Returns:
            The Player object if a player has possession, otherwise None.
        """
        if self.ball_possession_player_id is not None:
            return self.get_player_by_id(self.ball_possession_player_id)
        return None

    def get_player_who_last_touched_ball(self) -> typing.Optional[Player]:
        """
        Returns the Player object who last touched the ball.

        Returns:
            The Player object if a player last touched the ball, otherwise None.
        """
        if self.last_ball_touch_player_id is not None:
            return self.get_player_by_id(self.last_ball_touch_player_id)
        return None

    # Add other utility methods as needed, e.g., for calculating distances, offside, etc.