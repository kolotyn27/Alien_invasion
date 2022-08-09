import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_settings, screen):
        """инициализация корабля пришельцев и задание начальной позиции"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        """загрузка изображения корабля пришельцев и получение прямоугольника"""
        self.image = pygame.image.load(
            "/Users/kolotilo/Documents/GitHub/alien_invasion/images/alien_ship-2.bmp"
        )
        self.rect = self.image.get_rect()

        # каждый новый корабль появляется левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение вещественной координаты центра корабля
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        """рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Перемещает пришельца вправо/влево"""
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """Возвращает True, если пришелец находится у края экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        if self.rect.left <= 0:
            return True
