import sys
import os

# Add the src directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from zzocker import simulation
from zzocker import player_ai
from zzocker import state
from zzocker import physics # May not be directly used here, but good practice to import if part of the core
from zzocker import actions # May not be directly used here, but good practice to import if part of the core

def run_game(num_steps=1000):
    """
    Sets up and runs a simulation of a zzocker game.

    Args:
        num_steps (int): The number of simulation steps to run.
    """
    print("Setting up zzocker simulation...")

    # Define initial game state (example)
    # This assumes a basic GameState can be initialized or has a default
    # You might need to adjust this based on the actual GameState constructor
    initial_state = state.GameState() # Assuming GameState can be initialized like this

    # Create AI instances for each team
    team1_ai = player_ai.PlayerAI()
    team2_ai = player_ai.PlayerAI()

    # Map team IDs to AI instances
    # Assuming team IDs are 'team1' and 'team2' or similar
    # Adjust if your GameState or Simulation uses different IDs
    team_ais = {
        initial_state.teams[0].id: team1_ai,
        initial_state.teams[1].id: team2_ai,
    }

    # Create the simulation instance
    sim = simulation.Simulation(initial_state, team_ais)

    print(f"Running simulation for {num_steps} steps...")

    # Run the simulation for the specified number of steps
    for step in range(num_steps):
        # The simulation.step() method should internally call the AIs
        # to get actions and update the state based on physics.
        sim.step()

        # Optional: Print state or progress indicator
        if step % 100 == 0:
            print(f"Step {step}/{num_steps} complete.")
            # print(f"Ball position: {sim.current_state.ball.position}") # Example state info

    print("Simulation finished.")
    # Optional: Print final score or state summary
    # print(f"Final Score: Team {initial_state.teams[0].id}: {sim.current_state.teams[0].score}, Team {initial_state.teams[1].id}: {sim.current_state.teams[1].score}")


if __name__ == '__main__':
    # You can modify the number of steps here
    run_game(num_steps=5000)