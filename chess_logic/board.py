from chess_logic.pieces import Pawn, King, Queen, Bishop, Rook, Knight

class Board:
    def __init__(self):
        #self.board = self.create_initial_board()
        # Initialize an 8x8 board with None values or pieces.
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_pieces()  # Call the method to set up pieces at the start.
    
    def setup_pieces(self):
        """Set up the pieces in their initial positions."""
        # Map columns to indices
        columns = 'abcdefgh'

        # Set up the white pieces on row 0 (back rank)
        for col, piece_class in zip(columns, [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]):
            col_index = columns.index(col)
            self.grid[0][col_index] = piece_class('white', (0, col_index))  # Use tuple (row, col)

        # Set up the white pawns on row 1
        for col in columns:
            col_index = columns.index(col)
            self.grid[1][col_index] = Pawn('white', (1, col_index))  # Use tuple (row, col)

        # Set up the black pieces on row 7 (back rank)
        for col, piece_class in zip(columns, [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]):
            col_index = columns.index(col)
            self.grid[7][col_index] = piece_class('black', (7, col_index))  # Use tuple (row, col)

        # Set up the black pawns on row 6
        for col in columns:
            col_index = columns.index(col)
            self.grid[6][col_index] = Pawn('black', (6, col_index))  # Use tuple (row, col)
    
    def display(self):
        """Display the board with row and column labels."""
        print("    a  b  c  d  e  f  g  h")  # Column labels
        print("  +------------------------+")

        for i, row in enumerate(self.grid):
            row_str = f"{8 - i} |"  # Row label (reversed, as row 8 is at the top in chess)
            for piece in row:
                row_str += f" {piece.symbol if piece else '.'} "  # Display piece or empty square
            row_str += f"| {8 - i}"  # Row label again for symmetry
            print(row_str)

        print("  +------------------------+")
        print("    a  b  c  d  e  f  g  h")  # Column labels again for symmetry

    def piece_symbol(self, piece):
        """Returns a shorthand symbol for each piece based on its type and color."""
        if isinstance(piece, King):
            return "K" if piece.color == 'white' else "k"
        elif isinstance(piece, Queen):
            return "Q" if piece.color == 'white' else "q"
        elif isinstance(piece, Rook):
            return "R" if piece.color == 'white' else "r"
        elif isinstance(piece, Bishop):
            return "B" if piece.color == 'white' else "b"
        elif isinstance(piece, Knight):
            return "N" if piece.color == 'white' else "n"
        elif isinstance(piece, Pawn):
            return "P" if piece.color == 'white' else "p"
        return "?"
    
    def get_piece_at(self, position):
        """Returns the piece at the given position or None if no piece is there."""
        row, col = position
        return self.grid[row][col]
    
    def move_piece(self, start_pos, end_pos):
        """Moves a piece from start_pos to end_pos, updating the board."""
        piece = self.get_piece_at(start_pos)
        
        if not piece:
            raise ValueError(f"No piece at position {start_pos}")
        
        if not piece.is_valid_move(start_pos, end_pos, self):
            raise ValueError(f"Invalid move for {piece.__class__.__name__} from {start_pos} to {end_pos}")
        
        self.update_position(start_pos, end_pos)
    
    def update_position(self, start_pos, end_pos):
        """Updates the board by moving a piece from start_pos to end_pos."""
        piece = self.get_piece_at(start_pos)
        self.grid[end_pos[0]][end_pos[1]] = piece  # Place piece at new position
        piece.position = end_pos  # Update the piece's position
        self.grid[start_pos[0]][start_pos[1]] = None  # Clear the old position
    
    def is_check(self, color):
        """Checks if the current player's king is in check."""
        king_pos = self.find_king(color)
        # Check if any opponent's piece can move to the king's position
        for row in self.grid:
            for piece in row:
                if piece and piece.color != color and piece.is_valid_move(piece.position, king_pos, self):
                    return True
        return False
    
    def find_king(self, color):
        """Finds the king's position for the given color."""
        for row in self.grid:
            for piece in row:
                if isinstance(piece, King) and piece.color == color:
                    return piece.position
        raise ValueError(f"King for {color} not found on the board.")
    
    def is_checkmate(self, color):
        """Determines if the current player is in checkmate."""
        if not self.is_check(color):
            return False
        
        # Check if any move can save the king
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color == color:
                    for r in range(8):
                        for c in range(8):
                            if piece.is_valid_move((row, col), (r, c), self):
                                saved_board = self.clone_board()  # Make a copy of the board
                                saved_board.move_piece((row, col), (r, c))
                                if not saved_board.is_check(color):
                                    return False
        return True
    
    def clone_board(self):
        """Creates a deep copy of the current board (for simulating moves)."""
        new_board = Board()
        new_board.grid = [[piece for piece in row] for row in self.grid]
        return new_board
