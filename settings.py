class Settings:
    """Класс для хранения настроек игры"""

    def __init__(self):
        """Инициализирует статические настройки игры."""
        # параметры экрана
        self.screen_width = 1200
        self.screen_hight = 800
        self.bg_color = (255, 255, 255)
        # настройки корабля
        self.ship_limit = 3
        # настройки пришельцев
        self.alien_drop_speed = 10
        # Темп ускорения игры
        self.speedup_scale = 1.5
        # параметры пули
        self.bullet_height = 15
        self.bullet_width = 400
        self.bullet_color = 60, 60, 60
        # Темп роста стоимости пришельцев
        self.score_scale = 2
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 3.5
        self.alien_speed_factor = 1
        self.bullet_speed_factor = 5
        # fleet_direction = 1 обозначает движение вправо; а -1 - влево.
        self.fleet_direction = 1
        # Подсчет очков
        self.alien_points = 10

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
