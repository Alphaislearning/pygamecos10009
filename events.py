"""Event handling and input management"""
import pygame
from game_state import GameState


def handle_menu_input(event, ui_state):
    """Handle input in MENU state"""
    if event.key == pygame.K_UP:
        ui_state["menu_selected"] = (ui_state["menu_selected"] - 1) % 3
    elif event.key == pygame.K_DOWN:
        ui_state["menu_selected"] = (ui_state["menu_selected"] + 1) % 3
    elif event.key == pygame.K_SPACE:
        if ui_state["menu_selected"] == 0:  # Play
            return GameState.START
        elif ui_state["menu_selected"] == 1:  # Settings
            return GameState.SETTINGS
        elif ui_state["menu_selected"] == 2:  # Quit
            return None  # Signal to quit
    return GameState.MENU


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


def handle_start_input(event):
    """Handle input in START state"""
    if event.key == pygame.K_SPACE:
        return GameState.RUNNING
    elif event.key == pygame.K_ESCAPE:
        return GameState.MENU
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
        return "RETRY"  # Signal to retry
    elif event.key == pygame.K_ESCAPE:
        return GameState.MENU
    return GameState.GAME_OVER


def process_events(pygame_event, game_state, ui_state, settings, game_input):
    """
    Main event processor that dispatches to appropriate handler
    
    Returns:
        - New game state or command
        - running flag (True/False)
    """
    running = True
    new_state = game_state
    
    if pygame_event.type == pygame.QUIT:
        running = False
    
    elif pygame_event.type == pygame.KEYDOWN:
        if game_state == GameState.MENU:
            new_state = handle_menu_input(pygame_event, ui_state)
            if new_state is None:  # Quit selected
                running = False
                new_state = GameState.MENU
        
        elif game_state == GameState.SETTINGS:
            new_state = handle_settings_input(pygame_event, ui_state, settings)
        
        elif game_state == GameState.START:
            new_state = handle_start_input(pygame_event)
        
        elif game_state == GameState.RUNNING:
            new_state = handle_running_input(pygame_event, game_input)
        
        elif game_state == GameState.GAME_OVER:
            result = handle_game_over_input(pygame_event)
            if result == "RETRY":
                new_state = GameState.START
            else:
                new_state = result
    
    return new_state, running, game_input
