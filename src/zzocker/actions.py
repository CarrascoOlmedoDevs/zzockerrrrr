import enum

class PlayerAction(enum.Enum):
    MOVE = "mover"
    PASS = "pasar"
    SHOOT = "disparar"
    TACKLE = "placar"

# Example usage (optional, not required by the prompt, but good for context)
# action = PlayerAction.MOVE
# print(action.value)
# print(PlayerAction("mover"))