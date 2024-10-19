class Piece:
    def __init__(self, color, position):
        self.color = color  # 'white' or 'black'
        self.position = position  # (row, col), e.g., (0, 4) for a king starting at e1
        self.symbol = ''

    def is_valid_move(self, start_pos, end_pos, board):
        raise NotImplementedError("This method should be overridden by subclasses")
    
    def is_within_bounds(self, pos):
        """Check if the position is within the 8x8 chess board."""
        row, col = pos
        return 0 <= row < 8 and 0 <= col < 8

    def is_enemy_piece(self, pos, board):
        """Return True if there's an enemy piece at the given position."""
        piece = board.get_piece_at(pos)
        return piece is not None and piece.color != self.color
    
    def is_path_clear(self, start_pos, end_pos, board):
        """Checks if the path between start_pos and end_pos is clear for sliding pieces."""
        row_step = (end_pos[0] - start_pos[0]) // max(1, abs(end_pos[0] - start_pos[0]))
        col_step = (end_pos[1] - start_pos[1]) // max(1, abs(end_pos[1] - start_pos[1]))

        current_pos = (start_pos[0] + row_step, start_pos[1] + col_step)

        while current_pos != end_pos:
            if board.get_piece_at(current_pos) is not None:
                return False
            current_pos = (current_pos[0] + row_step, current_pos[1] + col_step)

        return True

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'K' if color == 'white' else 'k'

    def is_valid_move(self, start_pos, end_pos, board):
        row_diff = abs(start_pos[0] - end_pos[0])
        col_diff = abs(start_pos[1] - end_pos[1])

        # The King can move one square in any direction
        if max(row_diff, col_diff) == 1 and self.is_within_bounds(end_pos):
            return not self.is_enemy_piece(end_pos, board) or self.is_enemy_piece(end_pos, board)

        return False

class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'Q' if color == 'white' else 'q'

    def is_valid_move(self, start_pos, end_pos, board):
        row_diff = abs(start_pos[0] - end_pos[0])
        col_diff = abs(start_pos[1] - end_pos[1])

        # Queen moves diagonally, vertically, or horizontally
        if row_diff == col_diff or row_diff == 0 or col_diff == 0:
            return self.is_path_clear(start_pos, end_pos, board) and self.is_within_bounds(end_pos)

        return False
    

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'R' if color == 'white' else 'r'

    def is_valid_move(self, start_pos, end_pos, board):
        row_diff = abs(start_pos[0] - end_pos[0])
        col_diff = abs(start_pos[1] - end_pos[1])

        # Rook moves either horizontally or vertically
        if row_diff == 0 or col_diff == 0:
            return self.is_path_clear(start_pos, end_pos, board) and self.is_within_bounds(end_pos)

        return False
    

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'B' if color == 'white' else 'b'

    def is_valid_move(self, start_pos, end_pos, board):
        row_diff = abs(start_pos[0] - end_pos[0])
        col_diff = abs(start_pos[1] - end_pos[1])

        # Bishop moves diagonally
        if row_diff == col_diff:
            return self.is_path_clear(start_pos, end_pos, board) and self.is_within_bounds(end_pos)

        return False


class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'N' if color == 'white' else 'n'

    def is_valid_move(self, start_pos, end_pos, board):
        row_diff = abs(start_pos[0] - end_pos[0])
        col_diff = abs(start_pos[1] - end_pos[1])

        # The Knight moves in an "L" shape (2,1) or (1,2)
        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            return self.is_within_bounds(end_pos)

        return False
    

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = 'P' if color == 'white' else 'p'

    def is_valid_move(self, start_pos, end_pos, board):

        row_diff = end_pos[0] - start_pos[0]
        col_diff = abs(end_pos[1] - start_pos[1])

        direction = 1 if self.color == 'white' else -1

        # Normal move (forward 1 square)
        if col_diff == 0 and row_diff == direction:
            return board.get_piece_at(end_pos) is None

        # First move (can move 2 squares)
        if col_diff == 0 and row_diff == 2 * direction and self.is_first_move():
            return self.is_path_clear(start_pos, end_pos, board) and board.get_piece_at(end_pos) is None

        # Capturing diagonally
        if col_diff == 1 and row_diff == direction:
            return self.is_enemy_piece(end_pos, board)

        return False

    def is_first_move(self):
        """Check if it's the pawn's first move (either from row 1 or 6)."""
        return (self.color == 'white' and self.position[0] == 6) or (self.color == 'black' and self.position[0] == 1)