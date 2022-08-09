import json


class GameStats:
    """отслеживание статистики для игры"""

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        # Игра Alien Invasion запускается в неактивном состоянии.
        self.game_active = False
        # Рекорд не должен сбрасываться.
        with open(
            "/Users/kolotilo/Documents/GitHub/alien_invasion/high_score.json"
        ) as file:
            self.high_score = int(json.load(file))

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def save_high_score(self):
        """Сохранение лучшего результата в файл"""
        with open(
            "/Users/kolotilo/Documents/GitHub/alien_invasion/high_score.json", "w"
        ) as file:
            json.dump(self.high_score, file)
