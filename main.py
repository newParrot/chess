from chess_logic.game import Game
from chess_logic.player import HumanPlayer


if __name__ == "__main__":
    # Start a game with two human players
    game = Game(white_player=HumanPlayer('white'), black_player=HumanPlayer('black'))
    game.play()