import abc
from typing import Tuple, Optional, Dict, Any

# Forward references for type hinting classes defined elsewhere
# (e.g., in game_state.py, player.py)
GameState = 'GameState'
Player = 'Player'

class ActionResult:
    """Represents the outcome of performing an action."""
    def __init__(self, success: bool, message: str = "", data: Dict[str, Any] | None = None):
        """
        Initializes an ActionResult.

        Args:
            success: True if the action was successful in its primary goal.
            message: A descriptive message about the action's outcome.
            data: A dictionary containing relevant data about the outcome
                  (e.g., who passed, who received, tackle success, new position).
        """
        self.success: bool = success
        self.message: str = message
        self.data: Dict[str, Any] = data if data is not None else {}

    def __repr__(self) -> str:
        return f"ActionResult(success={self.success}, message='{self.message}', data={self.data})"

class Action(abc.ABC):
    """Abstract base class for all player actions."""

    @abc.abstractmethod
    def apply(self, game_state: GameState, player: Player) -> ActionResult:
        """
        Applies the action to the game state.

        This method should contain the logic for how the action affects the game,
        update the game_state accordingly, and return an ActionResult detailing
        the outcome, including relevant data for event logging or subsequent logic.

        Args:
            game_state: The current state of the game.
            player: The player performing the action.

        Returns:
            An ActionResult object describing the outcome of the action.
        """
        pass

class MoveAction(Action):
    """Represents a player moving to a new position."""
    def __init__(self, target_position: Tuple[int, int]):
        self.target_position: Tuple[int, int] = target_position

    def __repr__(self) -> str:
        return f"MoveAction(target_position={self.target_position})"

    def apply(self, game_state: GameState, player: Player) -> ActionResult:
        """
        Applies the move action.
        (Placeholder implementation - actual logic would be in GameState)
        """
        # In a real implementation, game_state would handle validity checks,
        # updating player position, potential collisions, etc.
        # For now, simulate a successful move and return data.
        print(f"Player {player.id} attempting to move to {self.target_position}")

        # Example of updating state (would typically call a GameState method)
        # success = game_state.try_move_player(player.id, self.target_position)

        # Simulate outcome
        success = True # Assume move is always successful in this simulation
        message = f"Player {player.id} moved to {self.target_position}"
        data = {
            "player_id": player.id,
            "old_position": player.position, # Need access to player's old position
            "new_position": self.target_position,
            "action_type": "move"
        }

        # If move logic was in GameState:
        # if success:
        #     message = f"Player {player.id} successfully moved to {self.target_position}"
        #     data["new_position"] = self.target_position
        # else:
        #     message = f"Player {player.id} failed to move to {self.target_position}"
        #     data["new_position"] = player.position # Position remains unchanged

        return ActionResult(success=success, message=message, data=data)

class PassAction(Action):
    """Represents a player passing the ball."""
    def __init__(self, target_player_id: Optional[int] = None, target_position: Optional[Tuple[int, int]] = None):
        if target_player_id is None and target_position is None:
            raise ValueError("PassAction requires either target_player_id or target_position")
        self.target_player_id: Optional[int] = target_player_id
        self.target_position: Optional[Tuple[int, int]] = target_position

    def __repr__(self) -> str:
        if self.target_player_id is not None:
            return f"PassAction(target_player_id={self.target_player_id})"
        else:
            return f"PassAction(target_position={self.target_position})"

    def apply(self, game_state: GameState, player: Player) -> ActionResult:
        """
        Applies the pass action.
        (Placeholder implementation - actual logic would be in GameState)
        """
        print(f"Player {player.id} attempting to pass...")

        # In a real implementation, game_state would handle:
        # - Checking if player has the ball
        # - Calculating pass trajectory and success chance
        # - Handling interceptions by opponents
        # - Determining if the pass reaches the target player or position
        # - Transferring ball possession

        # Simulate outcome (e.g., successful pass to target player)
        success = True # Assume success for simulation
        outcome_data = {
            "action_type": "pass",
            "from_player_id": player.id,
            "outcome": "simulated_completion" # or "simulated_incomplete", "simulated_interception"
        }
        message = f"Pass from player {player.id}."

        if self.target_player_id is not None:
            message += f" towards player {self.target_player_id}."
            outcome_data["target_player_id"] = self.target_player_id
            # Simulate passing the ball to the target player if successful
            # if success: game_state.transfer_ball(player.id, self.target_player_id)

        elif self.target_position is not None:
            message += f" towards position {self.target_position}."
            outcome_data["target_position"] = self.target_position
            # Simulate placing the ball at the target position if successful
            # if success: game_state.place_ball(self.target_position)

        # Add more detailed outcome simulation if needed (e.g., who intercepted)
        # outcome_data["intercepted_by"] = None # if applicable

        return ActionResult(success=success, message=message, data=outcome_data)

class ShootAction(Action):
    """Represents a player shooting the ball towards a goal."""
    def __init__(self, target_goal_id: Optional[int] = None, target_position: Optional[Tuple[int, int]] = None):
         if target_goal_id is None and target_position is None:
            raise ValueError("ShootAction requires either target_goal_id or target_position")
         self.target_goal_id: Optional[int] = target_goal_id
         self.target_position: Optional[Tuple[int, int]] = target_position # Could be specific spot in goal or general area

    def __repr__(self) -> str:
        if self.target_goal_id is not None:
            return f"ShootAction(target_goal_id={self.target_goal_id})"
        else:
            return f"ShootAction(target_position={self.target_position})"

    def apply(self, game_state: GameState, player: Player) -> ActionResult:
        """
        Applies the shoot action.
        (Placeholder implementation - actual logic would be in GameState)
        """
        print(f"Player {player.id} attempting to shoot...")

        # In a real implementation, game_state would handle:
        # - Checking if player has the ball
        # - Calculating shot trajectory, power, accuracy
        # - Goalie save chance
        # - Hitting post, missing, going in (GOAL!)
        # - Updating score if goal

        # Simulate outcome
        import random
        possible_outcomes = ["goal", "save", "miss"]
        simulated_outcome = random.choice(possible_outcomes)
        success = simulated_outcome == "goal" # Primary success is scoring a goal

        outcome_data = {
            "action_type": "shoot",
            "shooter_id": player.id,
            "outcome": simulated_outcome
        }
        message = f"Shot by player {player.id}. Outcome: {simulated_outcome}."

        if self.target_goal_id is not None:
             outcome_data["target_goal_id"] = self.target_goal_id
             message = f"Shot by {player.id} towards goal {self.target_goal_id}. Outcome: {simulated_outcome}."
        elif self.target_position is not None:
             outcome_data["target_position"] = self.target_position
             message = f"Shot by {player.id} towards position {self.target_position}. Outcome: {simulated_outcome}."

        # If outcome was "goal", game_state would update the score
        # if simulated_outcome == "goal":
        #     game_state.score_goal(player.team_id) # Assuming player has team_id

        return ActionResult(success=success, message=message, data=outcome_data)

class TackleAction(Action):
    """Represents a player attempting to tackle an opponent."""
    def __init__(self, target_player_id: int):
        self.target_player_id: int = target_player_id

    def __repr__(self) -> str:
        return f"TackleAction(target_player_id={self.target_player_id})"

    def apply(self, game_state: GameState, player: Player) -> ActionResult:
        """
        Applies the tackle action.
        (Placeholder implementation - actual logic would be in GameState)
        """
        print(f"Player {player.id} attempting to tackle player {self.target_player_id}")

        # In a real implementation, game_state would handle:
        # - Checking if target is an opponent and is near
        # - Calculating tackle success based on player stats
        # - Handling ball possession change on success
        # - Handling fouls, injuries on failure/specific outcomes

        # Simulate outcome
        import random
        possible_outcomes = ["success", "failure", "foul"]
        simulated_outcome = random.choice(possible_outcomes)
        success = simulated_outcome == "success" # Primary success is winning the ball

        outcome_data = {
            "action_type": "tackle",
            "tackler_id": player.id,
            "tackled_id": self.target_player_id,
            "outcome": simulated_outcome
        }
        message = f"Tackle attempt by {player.id} on {self.target_player_id}. Outcome: {simulated_outcome}."

        # If outcome was "success", game_state would transfer ball possession
        # if simulated_outcome == "success":
        #    game_state.transfer_ball(self.target_player_id, player.id)
        # If outcome was "foul", game_state might record a foul, award a free kick, etc.
        # elif simulated_outcome == "foul":
        #    game_state.handle_foul(...)

        return ActionResult(success=success, message=message, data=outcome_data)

# Example of how an action might be created and applied (for illustration, not part of the file content)
# from .game_state import GameState # Assuming GameState is in .game_state
# from .player import Player # Assuming Player is in .player
#
# # Create dummy objects for demonstration
# class MockPlayer:
#     def __init__(self, id, position, team_id):
#         self.id = id
#         self.position = position
#         self.team_id = team_id
#
# class MockGameState:
#      def __init__(self):
#          self.players = {1: MockPlayer(1, (10, 20), 1), 2: MockPlayer(2, (30, 40), 2)}
#          # Add other state attributes like ball_position, score, etc.
#
#      def get_player(self, player_id):
#          return self.players.get(player_id)
#
#      # Add methods like try_move_player, transfer_ball, simulate_shot, simulate_tackle etc.
#      # These methods would contain the core game logic and modify the state.
#      # They would be called by the action's apply method.
#      pass # Placeholder
#
# if __name__ == "__main__":
#     # This block is for testing/demonstration purposes and should not be in the final file content
#     game_state = MockGameState()
#     player1 = game_state.get_player(1)
#     player2 = game_state.get_player(2)
#
#     # Example Move Action
#     move_action = MoveAction(target_position=(15, 25))
#     move_result = move_action.apply(game_state, player1)
#     print(move_result)
#
#     # Example Pass Action
#     pass_action = PassAction(target_player_id=2)
#     pass_result = pass_action.apply(game_state, player1)
#     print(pass_result)
#
#     # Example Shoot Action
#     shoot_action = ShootAction(target_goal_id=2)
#     shoot_result = shoot_action.apply(game_state, player1)
#     print(shoot_result)
#
#     # Example Tackle Action
#     tackle_action = TackleAction(target_player_id=2)
#     tackle_result = tackle_action.apply(game_state, player1)
#     print(tackle_result)