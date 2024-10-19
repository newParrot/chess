class Player:
    def __init__(self, color):
        self.color = color  # "white" or "black"

    def get_move(self, board):
        """Abstract method to get a move. Should be overridden by derived classes."""
        raise NotImplementedError("This method should be implemented by subclasses.")


class HumanPlayer(Player):
    def __init__(self, color):
        super().__init__(color)

    def get_move(self, board):
        """Prompt the player for a move or quit the game."""
        while True:
            move_input = input(f"{self.color.capitalize()} to move (e.g., e2 e4) or type 'quit' to exit: ").lower().strip()
            if move_input == "quit":
                return "quit", "quit"
            try:
                start, end = move_input.split()
                start_pos = self.convert_to_position(start)
                end_pos = self.convert_to_position(end)
                
                # Debugging outputs to check values
                print(f"Start Position: {start_pos}, End Position: {end_pos}")
                return start_pos, end_pos
            except ValueError as e:
                print("Invalid input. Please enter a move like 'e2 e4' or 'quit' to exit.")
                print(f"Error details: {e}")
            except IndexError as e:
                print("Invalid board position. Ensure your input is correct.")
                print(f"Error details: {e}")

    def convert_to_position(self, position_str):
        """Convert board coordinates from chess notation (e.g., 'e2') to grid indices."""
        columns = 'abcdefgh'
        
        # Check if the input format is valid
        if len(position_str) != 2 or position_str[0] not in columns or position_str[1] not in '12345678':
            raise ValueError("Invalid chess notation.")

        row = 8 - int(position_str[1])  # Convert the rank (1-8) to grid row (7-0)
        col = columns.index(position_str[0])  # Convert the file (a-h) to grid column (0-7)
        return row, col


class AIPlayer(Player):
    def __init__(self, color):
        super().__init__(color)

    def get_move(self, board):
        """AI logic for generating a move would go here."""
        # For now, this is a placeholder for an AI player.
        print(f"{self.color.capitalize()} AI is thinking...")
        # Implement AI logic (e.g., minimax or other algorithms)
        pass


# Example usage in the Game class

# In the Game class, we would instantiate Player objects like so:
# self.white_player = HumanPlayer('white')
# self.black_player = HumanPlayer('black')  # Or AIPlayer for a computer player

# During the game loop, we would use:
# current_player.get_move(self.board)

