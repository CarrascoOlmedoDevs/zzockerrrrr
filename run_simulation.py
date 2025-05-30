import sys
import os

# Add the src directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Import necessary modules from the zzocker package
try:
    from zzocker import simulation
    from zzocker import player_ai
    from zzocker import state
    # Optional imports if needed directly in the runner, otherwise used internally
    # from zzocker import physics
    # from zzocker import actions
except ImportError as e:
    print(f"Error importing zzocker modules: {e}")
    print("Please ensure the 'src/zzocker' directory exists and contains the necessary files.")
    sys.exit(1)


def run_game(num_steps=1000):
    """
    Sets up and runs a simulation of a zzocker game.

    Args:
        num_steps (int): The number of simulation steps to run.
    """
    print("Setting up zzocker simulation...")

    try:
        # Define initial game state (example)
        # This assumes a basic GameState can be initialized or has a default
        # You might need to adjust this based on the actual GameState constructor
        initial_state = state.GameState() # Assuming GameState can be initialized like this

        # Create AI instances for each team
        # Assuming PlayerAI is the base class or a concrete AI implementation
        team1_ai = player_ai.PlayerAI()
        team2_ai = player_ai.PlayerAI()

        # Map team IDs to AI instances
        # Assuming initial_state.teams is a list of team objects with 'id' attribute
        if not initial_state.teams or len(initial_state.teams) < 2:
             print("Error: GameState did not initialize with at least two teams.")
             sys.exit(1)

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
                # Example state info (uncomment if state attributes are accessible)
                # try:
                #     print(f"Ball position: {sim.current_state.ball.position}")
                # except AttributeError:
                #     pass # Ignore if state structure is different

        print("Simulation finished.")
        # Optional: Print final score or state summary
        # try:
        #     print(f"Final Score: Team {initial_state.teams[0].id}: {sim.current_state.teams[0].score}, Team {initial_state.teams[1].id}: {sim.current_state.teams[1].score}")
        # except AttributeError:
        #     pass # Ignore if state structure is different

    except Exception as e:
        print(f"An error occurred during simulation setup or execution: {e}")
        sys.exit(1)


if __name__ == '__main__':
    # You can modify the number of steps here or add command line argument parsing
    default_steps = 5000
    run_game(num_steps=default_steps)