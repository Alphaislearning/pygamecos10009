"""UI and Screen rendering functions"""
import pygame
from settings import WIDTH, HEIGHT, GROUND_Y


def draw_background(screen, bg_img, mountain_img, road_img, mountain_x):
    """Draw background with parallax scrolling - position updated in game.py"""
    screen.blit(bg_img, (0, 0))

    w = mountain_img.get_width()
    y = HEIGHT - road_img.get_height() - 100

    screen.blit(mountain_img, (mountain_x, y))
    screen.blit(mountain_img, (mountain_x + w, y))


def draw_ground(screen, road_img, road_x):
    """Draw scrolling ground - position updated in game.py"""
    w = road_img.get_width()
    y = HEIGHT - road_img.get_height()

    screen.blit(road_img, (road_x, y))
    screen.blit(road_img, (road_x + w, y))


def draw_ui(screen, score, font_ui, WIDTH, HEIGHT):
    """Draw score UI"""
    box_rect = pygame.Rect(WIDTH//2 - 80, 20, 160, 45)
    pygame.draw.rect(screen, (255, 255, 255), box_rect, border_radius=15)
    pygame.draw.rect(screen, (255, 180, 200), box_rect, 3, border_radius=15)

    txt = font_ui.render(f"Score: {int(score)}", True, (70, 75, 95))
    screen.blit(txt, txt.get_rect(center=box_rect.center))


def draw_level(screen, level, font_ui, WIDTH):
    """Draw level indicator"""
    # Level colors
    level_colors = {
        1: (100, 200, 100),  # Green
        2: (255, 200, 100),  # Orange
        3: (255, 100, 100)   # Red
    }
    
    color = level_colors.get(level, (200, 200, 200))
    level_txt = font_ui.render(f"Level {level}", True, color)
    screen.blit(level_txt, (20, 20))


def draw_level_select(screen, selected_level, WIDTH, HEIGHT):
    """Draw stage selection screen."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    screen.blit(overlay, (0, 0))

    title = pygame.font.SysFont("Arial", 38, bold=True).render("SELECT LEVEL", True, (255, 200, 100))
    hint = pygame.font.SysFont("Arial", 20).render("Use LEFT/RIGHT and press SPACE to confirm", True, (230, 230, 230))
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 35)))
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 70)))

    card_w = 170
    card_h = 150
    gap = 20
    start_x = (WIDTH - (card_w * 3 + gap * 2)) // 2
    top_y = 120

    card_data = [
        (1, "Level 1", "Easy start", (100, 200, 100)),
        (2, "Level 2", "Faster spawn", (255, 200, 100)),
        (3, "Level 3", "Hard mode", (255, 100, 100)),
    ]

    font_title = pygame.font.SysFont("Arial", 26, bold=True)
    font_body = pygame.font.SysFont("Arial", 18, bold=True)

    for index, (level_id, label, desc, accent) in enumerate(card_data):
        x = start_x + index * (card_w + gap)
        selected = level_id == selected_level
        rect = pygame.Rect(x, top_y, card_w, card_h)
        bg_color = (255, 245, 225) if selected else (245, 245, 245)
        border_color = accent if selected else (140, 140, 140)

        pygame.draw.rect(screen, bg_color, rect, border_radius=16)
        pygame.draw.rect(screen, border_color, rect, 4, border_radius=16)

        label_txt = font_title.render(label, True, border_color)
        desc_txt = font_body.render(desc, True, (70, 75, 95))
        press_txt = font_body.render("Press SPACE", True, (90, 90, 90))

        screen.blit(label_txt, label_txt.get_rect(center=(rect.centerx, rect.y + 40)))
        screen.blit(desc_txt, desc_txt.get_rect(center=(rect.centerx, rect.y + 78)))
        screen.blit(press_txt, press_txt.get_rect(center=(rect.centerx, rect.y + 112)))

        if selected:
            pygame.draw.rect(screen, accent, rect.inflate(10, 10), 2, border_radius=18)


def _draw_pixel_heart(screen, x, y, scale, filled):
    """Draw a pixel-style heart similar to the provided reference image."""
    heart_map = [
        "..BBBB..BBBB..",
        ".BRRRRBBRRRRB.",
        "BRRWWRRRRRRRRB",
        "BRRWWRRRRRRRRB",
        ".BRRRRRRRRRRB.",
        "..BRRRRRRRRB..",
        "...BRRRRRRB...",
        "....BRRRRB....",
        ".....BRRB.....",
        "......BB......",
    ]

    if filled:
        color_map = {
            "B": (5, 10, 20),
            "R": (200, 20, 50),
            "W": (245, 245, 245),
        }
    else:
        color_map = {
            "B": (70, 70, 70),
            "R": (120, 120, 120),
            "W": (190, 190, 190),
        }

    for row_idx, row in enumerate(heart_map):
        for col_idx, cell in enumerate(row):
            if cell == ".":
                continue
            color = color_map[cell]
            rect = pygame.Rect(x + col_idx * scale, y + row_idx * scale, scale, scale)
            pygame.draw.rect(screen, color, rect)


def draw_hearts(screen, lives):
    """Draw 3 hearts to represent player lives."""
    max_lives = 3
    scale = 2
    heart_w = 14 * scale
    spacing = 6
    start_x = WIDTH - (heart_w * max_lives + spacing * (max_lives - 1)) - 14
    y = 14

    for i in range(max_lives):
        x = start_x + i * (heart_w + spacing)
        filled = i < lives
        _draw_pixel_heart(screen, x, y, scale, filled)


def draw_menu(screen, ui_state, bg_img, road_img, player, WIDTH, HEIGHT):
    """Draw main menu screen"""
    screen.blit(bg_img, (0, 0))
    # Simple ground draw
    y = HEIGHT - road_img.get_height()
    screen.blit(road_img, (0, y))
    player.draw(screen)

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    screen.blit(overlay, (0, 0))

    # Title
    t1 = pygame.font.SysFont("Arial", 50, bold=True).render("Dreamy Runner", True, (255, 200, 100))
    screen.blit(t1, t1.get_rect(center=(WIDTH//2, 50)))

    # Menu items
    font_menu = pygame.font.SysFont("Arial", 30, bold=True)
    items = ["PLAY", "SELECT LEVEL", "SETTINGS", "QUIT"]
    colors = [(70, 75, 95), (70, 75, 95), (70, 75, 95), (70, 75, 95)]
    colors[ui_state["menu_selected"]] = (255, 200, 100)  # Highlight selected

    for i, item in enumerate(items):
        txt = font_menu.render(item, True, colors[i])
        y = 150 + i * 60
        screen.blit(txt, txt.get_rect(center=(WIDTH//2, y)))

        # Draw selection box
        if i == ui_state["menu_selected"]:
            rect = pygame.Rect(WIDTH//2 - 100, y - 25, 200, 50)
            pygame.draw.rect(screen, (255, 200, 100), rect, 3, border_radius=10)

    selected_level = ui_state.get("selected_level", 1)
    level_hint = pygame.font.SysFont("Arial", 20, bold=True).render(
        f"Selected Level: {selected_level}", True, (255, 255, 255)
    )
    screen.blit(level_hint, level_hint.get_rect(center=(WIDTH // 2, HEIGHT - 36)))


def draw_settings(screen, ui_state, settings, bg_img, WIDTH, HEIGHT):
    """Draw settings screen"""
    screen.blit(bg_img, (0, 0))

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    screen.blit(overlay, (0, 0))

    # Title
    t1 = pygame.font.SysFont("Arial", 40, bold=True).render("SETTINGS", True, (255, 200, 100))
    screen.blit(t1, t1.get_rect(center=(WIDTH//2, 30)))

    font_menu = pygame.font.SysFont("Arial", 26, bold=True)
    font_info = pygame.font.SysFont("Arial", 20)

    # Volume setting
    vol_color = (255, 200, 100) if ui_state["settings_selected"] == 0 else (200, 200, 200)
    vol_txt = font_menu.render("Volume:", True, vol_color)
    screen.blit(vol_txt, (80, 120))
    vol_bar = pygame.Rect(300, 125, 200, 20)
    pygame.draw.rect(screen, (100, 100, 100), vol_bar)
    vol_fill = pygame.Rect(300, 125, (settings["volume"] / 100) * 200, 20)
    pygame.draw.rect(screen, (255, 200, 100), vol_fill)
    pygame.draw.rect(screen, vol_color, vol_bar, 2)

    vol_val = font_info.render(f"{settings['volume']}%", True, (255, 255, 255))
    screen.blit(vol_val, (520, 125))

    # Difficulty setting
    diff_color = (255, 200, 100) if ui_state["settings_selected"] == 1 else (200, 200, 200)
    diff_txt = font_menu.render("Difficulty:", True, diff_color)
    screen.blit(diff_txt, (60, 200))
    
    difficulties = ["Easy", "Normal", "Hard"]
    diff_val_txt = font_menu.render(difficulties[settings["difficulty"] - 1], True, (255, 200, 100))
    screen.blit(diff_val_txt, (300, 195))

    # Back instruction
    back_txt = font_info.render("Press ESC to Back | UP/DOWN to Select | LEFT/RIGHT to Change", True, (200, 200, 200))
    screen.blit(back_txt, (30, HEIGHT - 50))


def draw_start_screen(screen, player, road_img, font_title, font_ui, WIDTH, HEIGHT, level, player_name=""):
    """Draw pre-game start screen"""
    y = HEIGHT - road_img.get_height()
    screen.blit(road_img, (0, y))
    player.draw(screen)

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 160))
    screen.blit(overlay, (0, 0))

    t1 = font_title.render("Dreamy Runner", True, (70, 75, 95))
    t2 = font_ui.render("Press SPACE to Start", True, (120, 130, 160))
    t3 = font_ui.render("(ESC for Menu)", True, (100, 120, 150))
    t4 = font_ui.render(f"Current Stage: Level {level}", True, (255, 140, 120))
    t5 = font_ui.render(f"Name: {player_name or 'Type your name'}", True, (70, 75, 95))

    screen.blit(t1, t1.get_rect(center=(WIDTH//2, HEIGHT//2 - 40)))
    screen.blit(t2, t2.get_rect(center=(WIDTH//2, HEIGHT//2 + 20)))
    screen.blit(t3, t3.get_rect(center=(WIDTH//2, HEIGHT//2 + 60)))
    screen.blit(t4, t4.get_rect(center=(WIDTH//2, HEIGHT//2 - 90)))
    screen.blit(t5, t5.get_rect(center=(WIDTH//2, HEIGHT//2 - 10)))


def draw_game_over(screen, player, road_img, font_title, font_ui, score, WIDTH, HEIGHT):
    """Draw game over screen"""
    y = HEIGHT - road_img.get_height()
    screen.blit(road_img, (0, y))
    player.draw(screen)

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((100, 110, 140, 180))
    screen.blit(overlay, (0, 0))

    t1 = font_title.render("Game Over", True, (255, 255, 255))
    t2 = font_ui.render(f"Final Score: {int(score)}", True, (255, 180, 200))
    t3 = font_ui.render("Press SPACE to Try Again", True, (255, 255, 255))

    screen.blit(t1, t1.get_rect(center=(WIDTH//2, HEIGHT//2 - 60)))
    screen.blit(t2, t2.get_rect(center=(WIDTH//2, HEIGHT//2)))
    screen.blit(t3, t3.get_rect(center=(WIDTH//2, HEIGHT//2 + 60)))
