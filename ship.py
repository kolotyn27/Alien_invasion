import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """Инициализация корябля и задаем начальную позицию"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        """загрузка изображения корабля и получение прямоугольника"""
        self.image = pygame.image.load(
            "/Users/kolotilo/Documents/GitHub/alien_invasion/images/ship-2.bmp"
        )
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # каждый новый корабль появляется внизу экрана
        self.rect.centerx = self.screen_rect.centerx
        self.rect.midbottom = self.screen_rect.midbottom

        # Сохранение вещественной координаты центра корабля
        self.center_x = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)

        # Флаги перемещения
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """перемещения корабля"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center_x += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center_x -= self.ai_settings.ship_speed_factor

        # Обновление атрибута rect на основании self.center
        self.rect.centerx = self.center_x

        if self.moving_up and self.rect.top > 0:
            self.center_y -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.center_y += self.ai_settings.ship_speed_factor

        # Обновление атрибута rect на основании self.center
        self.rect.centery = self.center_y

    def blitme(self):
        """рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Размещает корабль в центре нижней стороны."""
        self.rect.centerx = self.screen_rect.centerx
        self.rect.midbottom = self.screen_rect.midbottom
        self.center_x = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)
