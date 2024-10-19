from chess_logic.board import Board
from chess_logic.player import HumanPlayer
class Game:
    def __init__(self, white_player = None, black_player= None):
        self.board = Board()
        self.white_player = white_player or HumanPlayer('white')  # Defaults to a human player if none provided
        self.black_player = black_player or HumanPlayer('black')  # Defaults to a human player if none provided
        self.current_turn = 'white'
        self.game_over = False
        self.move_history = [] # stack

    def switch_turns(self):
        """Switches the turn to the other player."""
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def get_current_player(self):
        """Returns the current player (either white or black)."""
        return self.white_player if self.current_turn == 'white' else self.black_player

    def is_valid_move(self, start_pos, end_pos):
        """Checks if the move is valid."""
        piece = self.board.get_piece_at(start_pos)
        if not piece:
            print("No piece at start position.")
            return False
        if piece.color != self.current_turn:
            print(f"It's {self.current_turn}'s turn, not {piece.color}'s turn.")
            return False
        if not piece.is_valid_move(start_pos, end_pos, self.board):
            print(f"Invalid move for {piece.__class__.__name__}.")
            return False
        return True

    def handle_move(self, start_pos, end_pos):
        """Handles the logic of making a move or quitting the game."""

        if start_pos == "quit" or end_pos == "quit":
            print(f"{self.current_turn.capitalize()} has quit the game.")
            self.game_over = True
            return False
        
        if not self.is_valid_move(start_pos, end_pos):
            return False

        # Make the move on the board
        self.board.move_piece(start_pos, end_pos)

        # Log the move in the history
        move_str = f"{self.current_turn.capitalize()} moves from {self.convert_to_chess_notation(start_pos)} to {self.convert_to_chess_notation(end_pos)}"
        self.move_history.append(move_str)

        # Check for check or checkmate
        if self.board.is_check(self.current_turn):
            print(f"{self.current_turn.capitalize()} is in check!")

        if self.board.is_checkmate(self.current_turn):
            print(f"Checkmate! {self.current_turn.capitalize()} loses.")
            self.game_over = True
            return True

        # Display the updated board and move history
        self.board.display()
        self.display_move_history()

        # Switch turns if the move was valid
        self.switch_turns()
        return True

    def convert_to_chess_notation(self, position):
        """Takes tuple and coverts to a chess position"""
        columns = 'abcdefgh'
        row = 8 - position[0]  # Convert grid row to chess notation
        col = columns[position[1]]  # Get the column from the index
        return f"{col}{row}"
    
    def display_move_history(self):
        print("Move History:")
        for move in self.move_history:
            print(move)

    def play(self):
        """Main loop of the game."""
        print("Starting the chess game!")
        self.board.display()

        while not self.game_over:
            current_player = self.get_current_player()
            start_pos, end_pos = current_player.get_move(self.board)
            if not self.handle_move(start_pos, end_pos):
                if self.game_over:
                    break

        print("Game over!")
