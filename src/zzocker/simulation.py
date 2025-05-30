import time
from . import state
from . import physics
from . import player_ai
from . import actions # Assuming actions structure is defined here

class SimulationManager:
    """
    Manages the main simulation loop of a game.
    """
    def __init__(self, team1_ai: player_ai.BaseAI, team2_ai: player_ai.BaseAI, timestep: float = 1/60):
        """
        Initializes the simulation manager.

        Args:
            team1_ai: The AI object for team 1.
            team2_ai: The AI object for team 2.
            timestep: The time step for each simulation step in seconds.
        """
        # 1. Initialize the game state
        self.game_state = state.GameState()
        self.team1_ai = team1_ai
        self.team2_ai = team2_ai
        self.timestep = timestep
        self._is_running = False

        # Optional: Initialize AIs with the game state or relevant info if needed
        # self.team1_ai.initialize(self.game_state, team_id=1) # Example
        # self.team2_ai.initialize(self.game_state, team_id=2) # Example


    def run(self):
        """
        Runs the main simulation loop until the game is over or stopped.
        """
        self._is_running = True
        print("Simulation started.")

        # Optional: Add initial state setup/broadcast if needed
        # self.game_state.setup_initial_state() # Example

        # 2. Iterate through the game time
        while self._is_running and not self.game_state.is_game_over():
            # Advance time
            self.game_state.current_time += self.timestep

            # 3. Get the current state
            current_state = self.game_state

            # 4. Call AI logic to determine actions
            # AIs receive the current state and return actions for their players
            # Actions should be a dictionary mapping player_id to action data (using actions.py structure)
            try:
                team1_actions = self.team1_ai.get_actions(current_state, team_id=1)
                team2_actions = self.team2_ai.get_actions(current_state, team_id=2)
            except Exception as e:
                print(f"Error getting AI actions: {e}")
                self.stop() # Stop simulation on AI error
                break

            # Combine actions from both teams
            all_actions = {}
            all_actions.update(team1_actions)
            all_actions.update(team2_actions)

            # Optional: Validate actions against allowed actions for the state/player

            # 5. Pass state and actions to the physics engine to calculate the next state
            # The physics module updates positions, velocities, etc., based on current state, actions, and timestep
            try:
                # Assuming physics modifies game_state in place
                physics.update_physics(self.game_state, all_actions, self.timestep)
            except Exception as e:
                print(f"Error during physics update: {e}")
                self.stop() # Stop simulation on physics error
                break

            # 6. Update the game state with the result of the physics calculation
            # This is implicitly done if physics.update_physics modifies self.game_state in place.
            # 7. Include logic for handling game events (score, fouls, etc.)
            try:
                # Assuming GameState has a method to update non-physical state and handle events
                self.game_state.update_game_state()
            except Exception as e:
                print(f"Error during game state update: {e}")
                self.stop() # Stop simulation on state update error
                break

            # Check for game end conditions is done by the loop condition

            # Optional: Add a small delay if simulating in real-time for visualization
            # time.sleep(self.timestep)

            # Optional: Add logging or state visualization hooks here
            # print(f"Time: {self.game_state.current_time:.2f}, Score: {self.game_state.score}") # Example logging

        print("Simulation ended.")
        # Optional: Print final score or game summary
        # print(f"Final Score: Team 1 - {self.game_state.score[1]}, Team 2 - {self.game_state.score[2]}") # Example

    def stop(self):
        """
        Stops the simulation loop.
        """
        self._is_running = False
        print("Simulation stopping...")