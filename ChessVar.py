class Piece:
    def __init__(self, name, color):
        self.name = name
        self.color = color


class King(Piece):
    def __init__(self, color):
        super().__init__('king', color)

    def is_valid_move(self, from_square, to_square):
        # Kings can move one square in any direction
        return max(abs(from_square[0] - to_square[0]), abs(from_square[1] - to_square[1])) == 1


class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color)

    def is_valid_move(self, from_square, to_square):
        # Queens can move any number of squares along a rank, file, or diagonal
        return from_square[0] == to_square[0] or \
            from_square[1] == to_square[1] or abs(from_square[0] - to_square[0]) == abs(from_square[1] - to_square[1])

class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color)

    def is_valid_move(self, from_square, to_square):
        # Rooks can move any number of squares along a rank or file
        return from_square[0] == to_square[0] or from_square[1] == to_square[1]


class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color)

    def is_valid_move(self, from_square, to_square):
        # Knights can move to any square not on the same rank, file, or diagonal
        return abs(from_square[0] - to_square[0]) == 2 and abs(from_square[1] - to_square[1]) \
            == 1 or abs(from_square[0] - to_square[0]) \
            == 1 and abs(from_square[1] - to_square[1]) == 2

class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color)

    def is_valid_move(self, from_square, to_square):
        # Bishops can move any number of squares diagonally
        return abs(from_square[0] - to_square[0]) == abs(from_square[1] - to_square[1])

class Pawn(Piece):
    def __init__(self, color):
        super().__init__('pawn', color)

    def is_valid_move(self, from_square, to_square):
        # Pawns can move forward one square, two squares from their initial position, and capture diagonally
        if self.color == 'white':
            return from_square[0] - to_square[0] == 1 and abs(from_square[1] - to_square[1]) <= 1 or from_square[0] \
                == 6 and from_square[1] == to_square[1] and from_square[0] - to_square[0] == 2
        else:
            return to_square[0] - from_square[0] == 1 and abs(from_square[1] - to_square[1]) <= 1 or from_square[0]\
                == 1 and from_square[1] == to_square[1] and to_square[0] - from_square[0] == 2


class ChessVar:
    def __init__(self):
        # Initialize the game board
        self.game_board = [
            [Rook('white'), Knight('white'), Bishop('white'), Queen('white'), King('white'), Bishop('white'),
             Knight('white'), Rook('white')],
            [Pawn('white') for _ in range(8)],
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [Pawn('black') for _ in range(8)],
            [Rook('black'), Knight('black'), Bishop('black'), Queen('black'), King('black'), Bishop('black'),
             Knight('black'), Rook('black')]
        ]

        self.current_player = 'white'
        self.game_state = 'UNFINISHED'
        self.captured_pieces = {'white': {}, 'black': {}}

    def get_game_state(self):
        return self.game_state

    def make_move(self, from_square, to_square):
        # Convert algebraic notation to array indices
        from_col = ord(from_square[0]) - ord('a')
        from_row = 8 - int(from_square[1])
        to_col = ord(to_square[0]) - ord('a')
        to_row = 8 - int(to_square[1])

        # Get the piece to move
        piece = self.game_board[from_row][from_col]

        # Check if the square is empty
        if piece is None:
            print("No piece at the given square")
            return False

        # Check if there's a piece at the destination square
        captured_piece = self.game_board[to_row][to_col]
        if captured_piece is not None:
            # Update the captured pieces dictionary
            if captured_piece.name not in self.captured_pieces[self.current_player]:
                self.captured_pieces[self.current_player][captured_piece.name] = 0
            self.captured_pieces[self.current_player][captured_piece.name] += 1

            # Check if the current player has won
            if (captured_piece.name in ['knight', 'rook', 'bishop'] and
                self.captured_pieces[self.current_player][captured_piece.name] >= 2) or \
               (captured_piece.name ==
                'pawn' and self.captured_pieces[self.current_player][captured_piece.name] >= 8) or \
               captured_piece.name in ['queen', 'king']:
                self.game_state = 'FINISHED'
                print(f"{self.current_player} wins!")
                return True

        # Move the piece
        self.game_board[to_row][to_col] = piece
        self.game_board[from_row][from_col] = None

        # Switch the current player
        self.current_player = 'black' if self.current_player == 'white' else 'white'

        return True

    def display_board(self):
        for row in self.game_board:
            for square in row:
                if square is None:
                    print("  -  ", end=" ")
                else:
                    print(f"{square.name[0].upper()}_{square.color[0].upper()}", end=" ")
            print()


if __name__ == "__main__":
# Example of usage:
    game = ChessVar()
    move_result = game.make_move('a2', 'a4')

    game.make_move('b7', 'b5')
    game.make_move('a4', 'b5')
    game.make_move('b8', 'b6')
    state = game.get_game_state()
    # Display the board after the moves
    game.display_board()

