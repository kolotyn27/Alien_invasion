import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    """Инициализация игры и создание объекта экрана и настроек"""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_hight)
    )
    pygame.display.set_caption("Alien Invasion")

    # Создание кнопки Play.
    play_button = Button(ai_settings, screen, "Play")

    # Создание экземпляров GameStats и Scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # создаем корабль
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # создание флота пршельцев
    gf.create_fleet(ai_settings, screen, ship, aliens)

    """Основной цикл игры"""
    while True:
        gf.check_events(
            ai_settings, screen, stats, sb, ship, aliens, bullets, play_button
        )
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
        gf.update_screen(
            ai_settings, screen, stats, sb, ship, aliens, bullets, play_button
        )


run_game()
