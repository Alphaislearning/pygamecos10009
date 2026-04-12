"""Event handling and input management"""
import pygame
from settings import WIDTH
from game_state import GameState


def _menu_action(selected_index):
    if selected_index == 0:
        return GameState.START
    if selected_index == 1:
        return GameState.LEADERBOARD
    if selected_index == 2:
        return GameState.LEVEL_SELECT
    if selected_index == 3:
        return GameState.SETTINGS
    if selected_index == 4:
        return None
    return GameState.MENU


def handle_menu_input(event, ui_state):
    """Handle input in MENU state"""
    if event.key == pygame.K_UP:
        ui_state["menu_selected"] = (ui_state["menu_selected"] - 1) % 5
    elif event.key == pygame.K_DOWN:
        ui_state["menu_selected"] = (ui_state["menu_selected"] + 1) % 5
    elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
        return _menu_action(ui_state["menu_selected"])
    return GameState.MENU


def handle_menu_click(mouse_pos, ui_state):
    """Handle mouse clicks on main menu buttons."""
    menu_panel = pygame.Rect(WIDTH // 2 - 160, 92, 320, 220)
    for index in range(5):
        button_rect = pygame.Rect(menu_panel.x + 34, menu_panel.y + 22 + index * 38, menu_panel.width - 68, 30)
        if button_rect.collidepoint(mouse_pos):
            ui_state["menu_selected"] = index
            return _menu_action(index)
    return GameState.MENU


def handle_level_select_input(event, game):
    """Handle input in LEVEL_SELECT state"""
    if event.key in [pygame.K_LEFT, pygame.K_UP]:
        game.selected_level = 1 if game.selected_level <= 1 else game.selected_level - 1
    elif event.key in [pygame.K_RIGHT, pygame.K_DOWN]:
        game.selected_level = 3 if game.selected_level >= 3 else game.selected_level + 1
    elif event.key == pygame.K_SPACE:
        return GameState.START
    elif event.key == pygame.K_ESCAPE:
        return GameState.MENU
    return GameState.LEVEL_SELECT


def handle_settings_input(event, ui_state, settings):
    """Handle input in SETTINGS state"""
    if event.key == pygame.K_ESCAPE:
        return GameState.MENU
    elif event.key == pygame.K_UP:
        ui_state["settings_selected"] = (ui_state["settings_selected"] - 1) % 2
    elif event.key == pygame.K_DOWN:
        ui_state["settings_selected"] = (ui_state["settings_selected"] + 1) % 2
    elif event.key == pygame.K_LEFT:
        if ui_state["settings_selected"] == 0:
            settings["volume"] = max(0, settings["volume"] - 10)
        elif ui_state["settings_selected"] == 1:
            settings["difficulty"] = max(1, settings["difficulty"] - 1)
    elif event.key == pygame.K_RIGHT:
        if ui_state["settings_selected"] == 0:
            settings["volume"] = min(100, settings["volume"] + 10)
        elif ui_state["settings_selected"] == 1:
            settings["difficulty"] = min(3, settings["difficulty"] + 1)
    return GameState.SETTINGS


def handle_leaderboard_input(event):
    """Handle input in LEADERBOARD state."""
    if event.key in [pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN]:
        return GameState.MENU
    return GameState.LEADERBOARD


def handle_start_input(event, game):
    """Handle input in START state"""
    if event.key == pygame.K_ESCAPE:
        return GameState.MENU
    elif event.key == pygame.K_BACKSPACE:
        game.player_name = game.player_name[:-1]
    elif event.key == pygame.K_RETURN:
        if game.player_name.strip():
            return GameState.RUNNING
    elif event.unicode and event.unicode.isprintable() and event.key != pygame.K_SPACE:
        if len(game.player_name) < 14:
            game.player_name += event.unicode
    elif event.key == pygame.K_SPACE:
        if game.player_name.strip():
            return GameState.RUNNING
    return GameState.START


def handle_running_input(event, game_input):
    """Handle input in RUNNING state"""
    if event.key in [pygame.K_UP, pygame.K_w]:
        game_input["jump"] = True
    if event.key in [pygame.K_DOWN, pygame.K_s]:
        game_input["duck"] = True
    if event.key == pygame.K_ESCAPE:
        return GameState.MENU
    return GameState.RUNNING


def handle_game_over_input(event):
    """Handle input in GAME_OVER state"""
    if event.key == pygame.K_SPACE:
        return "RETRY"
    elif event.key == pygame.K_ESCAPE:
        return GameState.MENU
    return GameState.GAME_OVER


def process_events(pygame_event, game):
    """Dispatch input to the handler for the current state."""
    running = True
    new_state = game.state
    
    if pygame_event.type == pygame.QUIT:
        running = False
    
    elif pygame_event.type == pygame.KEYDOWN:
        if game.state == GameState.MENU:
            new_state = handle_menu_input(pygame_event, game.ui_state)
            if new_state is None:
                running = False
                new_state = GameState.MENU
            elif new_state == GameState.LEADERBOARD:
                game.refresh_leaderboard()

        elif game.state == GameState.LEADERBOARD:
            new_state = handle_leaderboard_input(pygame_event)

        elif game.state == GameState.LEVEL_SELECT:
            new_state = handle_level_select_input(pygame_event, game)
        
        elif game.state == GameState.SETTINGS:
            new_state = handle_settings_input(pygame_event, game.ui_state, game.settings)
        
        elif game.state == GameState.START:
            new_state = handle_start_input(pygame_event, game)
        
        elif game.state == GameState.RUNNING:
            new_state = handle_running_input(pygame_event, game.game_input)
        
        elif game.state == GameState.GAME_OVER:
            result = handle_game_over_input(pygame_event)
            if result == "RETRY":
                new_state = GameState.START
            else:
                new_state = result

    elif pygame_event.type == pygame.MOUSEBUTTONDOWN and pygame_event.button == 1:
        if game.state == GameState.MENU:
            new_state = handle_menu_click(pygame_event.pos, game.ui_state)
            if new_state is None:
                running = False
                new_state = GameState.MENU
            elif new_state == GameState.LEADERBOARD:
                game.refresh_leaderboard()
    
    game.ui_state["selected_level"] = game.selected_level
    return new_state, running, game.game_input
