"""основной файл игры про космическое """
import sys
import pygame
import json
from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Обрабатывает нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stats.save_high_score()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(
                event, ai_settings, screen, stats, sb, ship, aliens, bullets
            )
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(
                ai_settings,
                screen,
                stats,
                sb,
                play_button,
                ship,
                aliens,
                bullets,
                mouse_x,
                mouse_y,
            )


def check_keydown_event(event, ai_settings, screen, stats, sb, ship, aliens, bullets):
    """обработка нажатой кнопки"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        # создание пули и включение в класс bullets
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
    elif event.key == pygame.K_q:
        stats.save_high_score()
        sys.exit()
    elif event.key == pygame.K_p:
        if not stats.game_active:
            start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_keyup_event(event, ship):
    """обработка отпущенной кнопки"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_play_button(
    ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y
):
    """Запускает новую игру при нажатии кнопки Play или клавиши Р."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)


def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Запускает новую игру при нажатии кнопки Play."""
    stats.reset_stats()
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    ai_settings.initialize_dynamic_settings()
    pygame.mouse.set_visible(False)
    stats.game_active = True
    aliens.empty()
    bullets.empty()
    # создание нового флота и корабля в центре"
    ship.center_ship()
    create_fleet(ai_settings, screen, ship, aliens)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Обновляет изображения на экране и отображает новый экран."""
    # При каждом проходе цикла перерисовывается экран.
    screen.fill(ai_settings.bg_color)
    # Все пули выводятся позади изображений корабля и пришельцев.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    print()
    if not stats.game_active:
        play_button.draw_button()

    # отображение послденего прорисованного экрана
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Обновляет позиции пуль и уничтожает старые пули."""
    # Обновление позиций пуль.
    bullets.update()
    # удаление пуль вышедших за край экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(
    ai_settings, screen, stats, sb, ship, aliens, bullets
):
    """Обработка коллизий пуль с пришельцами."""
    # Удаление пуль и пришельцев, участвующих в коллизиях.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # Уничтожение существующих пуль и создание нового флота.
        bullets.empty()
        ai_settings.increase_speed()
        # Увеличение уровня.
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def get_number_alien_x(ai_settings, alien_width):
    """Вычисляет количество пришельцев в ряду."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Создает пришельца и размещает его в ряду."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Создает флот пришельцев."""
    # Создание пришельца и вычисление количества пришельцев в ряду.
    # Интервал между соседними пришельцами равен одной ширине пришельца.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_alien_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        # создание первого ряда пришельцев
        for alien_number in range(number_aliens_x):
            # создание пришельцев и размещение их в ряду
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_rows(ai_settings, ship_height, alien_height):
    """Определяет количество рядов, помещающихся на экране."""
    available_space_y = ai_settings.screen_hight - 3 * alien_height - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение пришельцем края экрана."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_directions(ai_settings, aliens)
            break


def change_fleet_directions(ai_settings, aliens):
    """Опускает весь флот и меняет направление флота."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.alien_drop_speed
        ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Проверяет, достиг ли флот края экрана,
    после чего обновляет позиции всех пришельцев во флоте"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    check_alien_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)
    # Проверка коллизий "пришелец-корабль".
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Обрабатывает столкновение корабля с пришельцем."""
    # Уменьшение ships_left.
    if stats.ships_left > 0:
        stats.ships_left -= 1
        # Очистка списков пришельцев и пуль.
        aliens.empty()
        bullets.empty()
        # создание нового флота и перемещение корабля в центр
        ship.center_ship()
        sb.prep_ships()
        create_fleet(ai_settings, screen, ship, aliens)
        # пауза
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_alien_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Проверяет, добрались ли пришельцы до нижнего края экрана"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            """происходит тоже, что и при столкновении с кораблем"""
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    """Проверяет, появился ли новый рекорд."""
    if stats.high_score < stats.score:
        stats.high_score = stats.score
        sb.prep_high_score()
