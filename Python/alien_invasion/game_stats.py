"""A module for GameStats class to keep track of game stats"""
import json

class GameStats():
    """Track statistics for alien invader game."""

    def __init__(self, game_settings):
        """Initialize statistics."""

        self.settings = game_settings
        self.reset_stats()
        self.highscore_file = "hall_of_fame.json"
        self.hall_of_fame = [0]
        self.fetch_highscore_from_file()

        # Start game in an inactive state.
        self.game_active = False

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.game_active = True
        self.score = 0
        self.level = 1

    def fetch_highscore_from_file(self):
        try:
            with open(self.highscore_file) as hof:
                highscores = json.load(hof)

                if highscores:
                    # Save the list of top 5 highscores
                    self.hall_of_fame = highscores
                    # In the hall of fame record the first entry is the highest score.
                    self.high_score = highscores[0]
                
        except FileNotFoundError:
            # High score doesn't exist, start from zero.
            self.high_score = 0

        except json.JSONDecodeError:
            # High score file is not readable or empty, start from zero.
            self.high_score = 0

    def update_hall_of_fame(self):
        with open(self.highscore_file, 'w') as hs_file:
            # First add the current high score in the hall of fame.
            self.hall_of_fame.append(self.score)
            # Next sort the hall of fame list highest score first.
            self.hall_of_fame.sort(reverse=True)
            # Next slice the list if it is larger than 5.
            if len(self.hall_of_fame) > 5:
                self.hall_of_fame = self.hall_of_fame[:5]
            # Finally write the updated hall of fame in the file.
            json.dump(self.hall_of_fame, hs_file)
            # Also print hall of fame
            print(f"Hall of fame: {self.hall_of_fame}")
