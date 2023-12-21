from .player import Player
from .choices import Rock, Paper, Scissors, Spock, Lizard

class Game:
    def __init__(self):
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        self.choices = {
            "rock": Rock(),
            "paper": Paper(),
            "scissors": Scissors(),
            "spock": Spock(),
            "lizard": Lizard()
        }

    def start_game(self):
        pass  # TODO: Implement start game logic

    def get_player_choice(self, player):
        pass  # TODO: Implement get player choice logic

    def determine_winner(self):
        pass  # TODO: Implement determine winner logic

    def end_game(self):
        pass  # TODO: Implement end game logic