"""UI and Screen rendering functions."""
import pygame
from settings import WIDTH, HEIGHT


UI_COLORS = {
    "ink": (248, 236, 214),
    "panel": (114, 58, 42),
    "panel_dark": (76, 35, 24),
    "panel_light": (155, 88, 68),
    "gold": (232, 170, 96),
    "peach": (212, 118, 90),
    "mint": (149, 201, 139),
    "danger": (196, 82, 74),
    "white": (255, 244, 221),
    "shadow": (34, 14, 12),
    "muted": (220, 184, 166),
}


def _font(size, bold=True):
    """Use a blocky system font for a retro-style UI."""
    return pygame.font.SysFont("Courier New", size, bold=bold)


def _draw_overlay(screen, alpha=120, color=(18, 20, 34)):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((*color, alpha))
    screen.blit(overlay, (0, 0))


def _draw_pixel_panel(screen, rect, fill=None, border=None, shadow_offset=6):
    """Draw a chunky panel with square corners and shadow."""
    fill = fill or UI_COLORS["panel"]
    border = border or UI_COLORS["gold"]

    shadow_rect = rect.move(shadow_offset, shadow_offset)
    pygame.draw.rect(screen, UI_COLORS["shadow"], shadow_rect)
    pygame.draw.rect(screen, border, rect)

    inner = rect.inflate(-8, -8)
    pygame.draw.rect(screen, fill, inner)

    top_band = pygame.Rect(inner.x, inner.y, inner.width, 10)
    pygame.draw.rect(screen, UI_COLORS["panel_light"], top_band)

    bottom_band = pygame.Rect(inner.x, inner.bottom - 12, inner.width, 12)
    pygame.draw.rect(screen, UI_COLORS["panel_dark"], bottom_band)


def _draw_text(screen, text, font, color, pos, *, center=False, shadow=True):
    if shadow:
        shadow_surface = font.render(text, False, UI_COLORS["shadow"])
        shadow_rect = shadow_surface.get_rect(center=pos if center else pos)
        shadow_rect.move_ip(1, 1)
        screen.blit(shadow_surface, shadow_rect)

    surface = font.render(text, False, color)
    rect = surface.get_rect(center=pos if center else pos)
    screen.blit(surface, rect)
    return rect


def _fit_text(font, text, max_width):
    if font.size(text)[0] <= max_width:
        return text

    suffix = "..."
    trimmed = text
    while trimmed and font.size(trimmed + suffix)[0] > max_width:
        trimmed = trimmed[:-1]
    return (trimmed + suffix) if trimmed else suffix


def _draw_menu_button(screen, rect, label, selected):
    border = UI_COLORS["gold"] if selected else UI_COLORS["panel_light"]
    fill = (162, 88, 66) if selected else (106, 52, 38)
    _draw_pixel_panel(screen, rect, fill=fill, border=border, shadow_offset=4)
    _draw_text(
        screen,
        label,
        _font(24),
        UI_COLORS["white"] if selected else UI_COLORS["ink"],
        rect.center,
        center=True,
        shadow=selected,
    )


def _draw_leaderboard_rows(screen, rect, top_results, max_rows=5):
    header_font = _font(16)
    row_font = _font(15)
    small_font = _font(12)

    header_y = rect.y + 22
    _draw_text(screen, "RANK", header_font, UI_COLORS["ink"], (rect.x + 20, header_y))
    _draw_text(screen, "NAME", header_font, UI_COLORS["ink"], (rect.x + 88, header_y))
    _draw_text(screen, "SCORE", header_font, UI_COLORS["ink"], (rect.x + 310, header_y))
    _draw_text(screen, "LV", header_font, UI_COLORS["ink"], (rect.x + 430, header_y))
    _draw_text(screen, "TIME", header_font, UI_COLORS["ink"], (rect.x + 485, header_y))

    pygame.draw.line(
        screen,
        UI_COLORS["panel_dark"],
        (rect.x + 16, rect.y + 44),
        (rect.right - 16, rect.y + 44),
        3,
    )

    if not top_results:
        _draw_text(
            screen,
            "NO SCORES SAVED",
            _font(20),
            UI_COLORS["muted"],
            rect.center,
            center=True,
        )
        return

    row_height = 34
    for index, (player_name, score, level, played_at) in enumerate(top_results[:max_rows], start=1):
        row_y = rect.y + 56 + (index - 1) * row_height
        row_rect = pygame.Rect(rect.x + 14, row_y, rect.width - 28, 26)
        pygame.draw.rect(screen, (136, 78, 57) if index % 2 else (116, 63, 45), row_rect)

        rank_text = f"{index:02d}"
        name_text = _fit_text(row_font, player_name.upper(), 195)
        score_text = str(score)
        level_text = str(level)
        time_text = played_at[5:16].replace(" ", "  ") if played_at else "--"

        _draw_text(screen, rank_text, row_font, UI_COLORS["ink"], (rect.x + 22, row_y + 4))
        _draw_text(screen, name_text, row_font, UI_COLORS["ink"], (rect.x + 88, row_y + 4))
        _draw_text(screen, score_text, row_font, UI_COLORS["gold"], (rect.x + 316, row_y + 4))
        _draw_text(screen, level_text, row_font, UI_COLORS["mint"], (rect.x + 438, row_y + 4))
        _draw_text(screen, time_text, small_font, UI_COLORS["muted"], (rect.x + 485, row_y + 7), shadow=False)


def draw_background(screen, bg_img, mountain_img, road_img, mountain_x):
    """Draw background with parallax scrolling."""
    screen.blit(bg_img, (0, 0))

    width = mountain_img.get_width()
    y = HEIGHT - road_img.get_height() - 100

    screen.blit(mountain_img, (mountain_x, y))
    screen.blit(mountain_img, (mountain_x + width, y))


def draw_ground(screen, road_img, road_x):
    """Draw scrolling ground."""
    width = road_img.get_width()
    y = HEIGHT - road_img.get_height()

    screen.blit(road_img, (road_x, y))
    screen.blit(road_img, (road_x + width, y))


def draw_ui(screen, score, font_ui, WIDTH, HEIGHT):
    """Draw score UI."""
    del font_ui
    box_rect = pygame.Rect(WIDTH // 2 - 95, 16, 190, 42)
    _draw_pixel_panel(screen, box_rect, fill=(103, 50, 38), border=UI_COLORS["gold"], shadow_offset=4)
    _draw_text(screen, f"SCORE {int(score):04d}", _font(20), UI_COLORS["white"], box_rect.center, center=True)


def draw_level(screen, level, font_ui, WIDTH):
    """Draw level indicator."""
    del font_ui, WIDTH
    level_colors = {
        1: UI_COLORS["mint"],
        2: UI_COLORS["gold"],
        3: UI_COLORS["danger"],
    }

    rect = pygame.Rect(14, 14, 130, 40)
    _draw_pixel_panel(screen, rect, fill=(103, 50, 38), border=level_colors.get(level, UI_COLORS["gold"]), shadow_offset=4)
    _draw_text(screen, f"LEVEL {level}", _font(18), UI_COLORS["white"], rect.center, center=True)


def draw_level_select(screen, selected_level, WIDTH, HEIGHT):
    """Draw stage selection screen."""
    _draw_overlay(screen, alpha=90, color=(29, 24, 49))

    _draw_text(screen, "SELECT LEVEL", _font(34), UI_COLORS["gold"], (WIDTH // 2, 34), center=True)
    _draw_text(
        screen,
        "LEFT RIGHT TO PICK  |  SPACE TO CONFIRM",
        _font(16),
        UI_COLORS["white"],
        (WIDTH // 2, 66),
        center=True,
    )

    card_w = 190
    card_h = 160
    gap = 22
    start_x = (WIDTH - (card_w * 3 + gap * 2)) // 2
    top_y = 118

    card_data = [
        (1, "LEVEL 1", "CALM START", UI_COLORS["mint"]),
        (2, "LEVEL 2", "MORE SPAWN", UI_COLORS["gold"]),
        (3, "LEVEL 3", "DANGER MODE", UI_COLORS["danger"]),
    ]

    for index, (level_id, label, desc, accent) in enumerate(card_data):
        x = start_x + index * (card_w + gap)
        selected = level_id == selected_level
        rect = pygame.Rect(x, top_y, card_w, card_h)
        _draw_pixel_panel(
            screen,
            rect,
            fill=(140, 76, 58) if selected else (103, 50, 38),
            border=accent if selected else UI_COLORS["panel_light"],
            shadow_offset=5,
        )

        _draw_text(screen, label, _font(24), UI_COLORS["white"], (rect.centerx, rect.y + 28), center=True)
        _draw_text(screen, desc, _font(16), UI_COLORS["muted"], (rect.centerx, rect.y + 68), center=True, shadow=False)

        hint_rect = pygame.Rect(rect.x + 28, rect.bottom - 50, rect.width - 56, 30)
        _draw_pixel_panel(
            screen,
            hint_rect,
            fill=(162, 88, 66) if selected else (103, 50, 38),
            border=accent if selected else UI_COLORS["panel_light"],
            shadow_offset=3,
        )
        _draw_text(screen, "PRESS SPACE", _font(15), UI_COLORS["white"], hint_rect.center, center=True)


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
            pixel = pygame.Rect(x + col_idx * scale, y + row_idx * scale, scale, scale)
            pygame.draw.rect(screen, color, pixel)


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
        _draw_pixel_heart(screen, x, y, scale, i < lives)


def draw_menu(screen, ui_state, bg_img, road_img, player, WIDTH, HEIGHT):
    """Draw main menu screen."""
    screen.blit(bg_img, (0, 0))
    ground_y = HEIGHT - road_img.get_height()
    screen.blit(road_img, (0, ground_y))
    player.draw(screen)

    _draw_overlay(screen, alpha=24, color=(44, 18, 14))
    _draw_text(screen, "SWINBURN RUNNER", _font(42), UI_COLORS["gold"], (WIDTH // 2, 48), center=True)

    menu_panel = pygame.Rect(WIDTH // 2 - 160, 92, 320, 220)
    _draw_pixel_panel(screen, menu_panel, fill=(111, 54, 39), border=UI_COLORS["gold"])

    items = ["PLAY", "LEADERBOARD", "SELECT LEVEL", "SETTINGS", "QUIT"]
    for index, item in enumerate(items):
        button_rect = pygame.Rect(menu_panel.x + 34, menu_panel.y + 22 + index * 38, menu_panel.width - 68, 30)
        _draw_menu_button(screen, button_rect, item, index == ui_state["menu_selected"])

    footer_panel = pygame.Rect(WIDTH // 2 - 138, HEIGHT - 58, 276, 30)
    _draw_pixel_panel(screen, footer_panel, fill=(111, 54, 39), border=UI_COLORS["panel_light"], shadow_offset=3)
    selected_level = ui_state.get("selected_level", 1)
    _draw_text(screen, f"CURRENT LEVEL {selected_level}", _font(15), UI_COLORS["white"], footer_panel.center, center=True, shadow=False)


def draw_leaderboard(screen, bg_img, WIDTH, HEIGHT, top_results):
    """Draw leaderboard screen accessible from the main menu."""
    screen.blit(bg_img, (0, 0))
    _draw_overlay(screen, alpha=52, color=(52, 20, 18))

    _draw_text(screen, "LEADERBOARD", _font(42), UI_COLORS["gold"], (WIDTH // 2, 42), center=True)

    panel = pygame.Rect(112, 82, 576, 244)
    _draw_pixel_panel(screen, panel, fill=(111, 54, 39), border=UI_COLORS["gold"], shadow_offset=7)

    score_rect = pygame.Rect(panel.x + 18, panel.y + 18, panel.width - 36, panel.height - 36)
    pygame.draw.rect(screen, (92, 44, 34), score_rect)
    _draw_leaderboard_rows(screen, score_rect, top_results, max_rows=5)

    hint_rect = pygame.Rect(WIDTH // 2 - 170, HEIGHT - 44, 340, 24)
    _draw_pixel_panel(screen, hint_rect, fill=(111, 54, 39), border=UI_COLORS["panel_light"], shadow_offset=3)
    _draw_text(screen, "ESC  SPACE  ENTER  TO GO BACK", _font(13), UI_COLORS["white"], hint_rect.center, center=True, shadow=False)


def draw_settings(screen, ui_state, settings, bg_img, WIDTH, HEIGHT):
    """Draw settings screen."""
    screen.blit(bg_img, (0, 0))
    _draw_overlay(screen, alpha=52, color=(52, 20, 18))

    _draw_text(screen, "SETTINGS", _font(38), UI_COLORS["gold"], (WIDTH // 2, 34), center=True)

    panel = pygame.Rect(150, 86, 500, 220)
    _draw_pixel_panel(screen, panel, fill=(111, 54, 39), border=UI_COLORS["gold"])

    font_menu = _font(22)
    font_info = _font(16)

    vol_color = UI_COLORS["gold"] if ui_state["settings_selected"] == 0 else UI_COLORS["muted"]
    diff_color = UI_COLORS["gold"] if ui_state["settings_selected"] == 1 else UI_COLORS["muted"]

    _draw_text(screen, "VOLUME", font_menu, vol_color, (panel.x + 36, panel.y + 42))
    bar_rect = pygame.Rect(panel.x + 170, panel.y + 34, 220, 26)
    _draw_pixel_panel(screen, bar_rect, fill=(84, 40, 30), border=vol_color if ui_state["settings_selected"] == 0 else UI_COLORS["panel_light"], shadow_offset=3)
    fill_rect = pygame.Rect(bar_rect.x + 6, bar_rect.y + 6, int((settings["volume"] / 100) * (bar_rect.width - 12)), bar_rect.height - 12)
    pygame.draw.rect(screen, UI_COLORS["peach"], fill_rect)
    _draw_text(screen, f"{settings['volume']}%", font_info, UI_COLORS["white"], (bar_rect.right + 20, bar_rect.y + 4))

    _draw_text(screen, "DIFFICULTY", font_menu, diff_color, (panel.x + 36, panel.y + 116))
    difficulty_rect = pygame.Rect(panel.x + 220, panel.y + 108, 150, 32)
    _draw_pixel_panel(screen, difficulty_rect, fill=(84, 40, 30), border=diff_color if ui_state["settings_selected"] == 1 else UI_COLORS["panel_light"], shadow_offset=3)
    difficulties = ["EASY", "NORMAL", "HARD"]
    _draw_text(screen, difficulties[settings["difficulty"] - 1], _font(18), UI_COLORS["white"], difficulty_rect.center, center=True)

    hint_rect = pygame.Rect(panel.x + 28, panel.bottom - 46, panel.width - 56, 26)
    _draw_pixel_panel(screen, hint_rect, fill=(111, 54, 39), border=UI_COLORS["panel_light"], shadow_offset=3)
    _draw_text(screen, "ESC BACK  |  UP DOWN SELECT  |  LEFT RIGHT CHANGE", _font(12), UI_COLORS["white"], hint_rect.center, center=True, shadow=False)


def draw_start_screen(screen, player, road_img, font_title, font_ui, WIDTH, HEIGHT, level, player_name=""):
    """Draw pre-game start screen."""
    del font_title, font_ui
    ground_y = HEIGHT - road_img.get_height()
    screen.blit(road_img, (0, ground_y))
    player.draw(screen)

    _draw_overlay(screen, alpha=36, color=(52, 20, 18))

    panel = pygame.Rect(166, 74, 468, 220)
    _draw_pixel_panel(screen, panel, fill=(111, 54, 39), border=UI_COLORS["gold"])

    _draw_text(screen, "READY TO RUN", _font(34), UI_COLORS["gold"], (panel.centerx, panel.y + 34), center=True)

    level_badge = pygame.Rect(panel.centerx - 84, panel.y + 68, 168, 30)
    _draw_pixel_panel(screen, level_badge, fill=(155, 78, 60), border=UI_COLORS["peach"], shadow_offset=3)
    _draw_text(screen, f"LEVEL {level}", _font(16), UI_COLORS["white"], level_badge.center, center=True)

    name_box = pygame.Rect(panel.x + 46, panel.y + 118, panel.width - 92, 34)
    _draw_pixel_panel(screen, name_box, fill=(84, 40, 30), border=UI_COLORS["panel_light"], shadow_offset=3)
    name_text = _fit_text(_font(18), (player_name or "TYPE YOUR NAME").upper(), name_box.width - 24)
    _draw_text(screen, name_text, _font(18), UI_COLORS["white"], name_box.center, center=True, shadow=False)

    hint_box = pygame.Rect(panel.x + 68, panel.bottom - 50, panel.width - 136, 28)
    _draw_pixel_panel(screen, hint_box, fill=(111, 54, 39), border=UI_COLORS["gold"], shadow_offset=3)
    _draw_text(screen, "PRESS SPACE TO START  |  ESC TO MENU", _font(12), UI_COLORS["white"], hint_box.center, center=True, shadow=False)


def draw_game_over(screen, player, road_img, font_title, font_ui, score, WIDTH, HEIGHT, top_results):
    """Draw game over screen."""
    del font_title, font_ui
    ground_y = HEIGHT - road_img.get_height()
    screen.blit(road_img, (0, ground_y))
    player.draw(screen)

    _draw_overlay(screen, alpha=68, color=(60, 14, 18))

    panel = pygame.Rect(126, 54, 548, 278)
    _draw_pixel_panel(screen, panel, fill=(101, 46, 38), border=UI_COLORS["danger"])

    _draw_text(screen, "GAME OVER", _font(38), UI_COLORS["danger"], (panel.centerx, panel.y + 28), center=True)

    score_box = pygame.Rect(panel.centerx - 100, panel.y + 54, 200, 30)
    _draw_pixel_panel(screen, score_box, fill=(155, 78, 60), border=UI_COLORS["peach"], shadow_offset=3)
    _draw_text(screen, f"FINAL SCORE {int(score):04d}", _font(16), UI_COLORS["white"], score_box.center, center=True)

    board_rect = pygame.Rect(panel.x + 24, panel.y + 100, panel.width - 48, 124)
    pygame.draw.rect(screen, (88, 36, 34), board_rect)
    _draw_leaderboard_rows(screen, board_rect, top_results, max_rows=3)

    retry_box = pygame.Rect(panel.centerx - 132, panel.bottom - 42, 264, 26)
    _draw_pixel_panel(screen, retry_box, fill=(101, 46, 38), border=UI_COLORS["danger"], shadow_offset=3)
    _draw_text(screen, "PRESS SPACE TO TRY AGAIN", _font(13), UI_COLORS["white"], retry_box.center, center=True, shadow=False)
