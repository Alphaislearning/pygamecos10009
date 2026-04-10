"""
Dreamy Runner - Main Entry Point
"""
import pygame
from settings import WIDTH, HEIGHT, FPS
from game import Game
from events import process_events
from game_state import GameState


def load_img(path, scale=None):
    """Load and process image"""
    img = pygame.image.load(path).convert_alpha()

    # remove white background (tolerant)
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            r, g, b, a = img.get_at((x, y))
            if r > 240 and g > 240 and b > 240:
                img.set_at((x, y), (0, 0, 0, 0))

    if scale:
        img = pygame.transform.scale(img, scale)

    return img


def main():
    """Main game loop"""
    # Initialize pygame
    pygame.init()
    pygame.font.init()
    
    # Setup screen and clock
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Swinburn Runner")
    
    # Load assets
    bg_img = load_img("assets/background.png", (WIDTH, HEIGHT))
    mountain_img = load_img("assets/mountain.png")
    road_img = load_img("assets/road.png")
    
    # Scale images
    mountain_img = pygame.transform.scale(
        mountain_img,
        (int(mountain_img.get_width() * 0.5), int(mountain_img.get_height() * 0.6))
    )
    road_img = pygame.transform.scale(
        road_img,
        (int(road_img.get_width() * 0.5), int(road_img.get_height() * 0.5))
    )
    
    # Setup fonts
    font_title = pygame.font.SysFont("Arial", 40, bold=True)
    font_ui = pygame.font.SysFont("Arial", 26, bold=True)
    
    # Create game instance
    game = Game(screen)
    
    # Store image dimensions for scrolling wrapping
    game.mountain_width = mountain_img.get_width()
    game.road_width = road_img.get_width()
    
    # Game loop
    running = True
    while running:
        game.tick(FPS)
        
        # Handle events
        for event in pygame.event.get():
            new_state, running, game.game_input = process_events(
                event, game.state, game.ui_state, game.settings, game.game_input
            )
            
            # Handle state transitions
            if new_state == GameState.RUNNING and game.state == GameState.START:
                game.reset_game()
            elif new_state == "RETRY" or (new_state == GameState.START and game.state == GameState.GAME_OVER):
                game.reset_game()
                new_state = GameState.START
            
            game.state = new_state
        
        # Update game logic
        game.update_game()
        game.update_scrolling_backgrounds(game.speed)
        
        # Render everything
        game.render_game(font_title, font_ui, bg_img, mountain_img, road_img)
        
        # Update display
        pygame.display.update()
    
    # Cleanup
    pygame.quit()


if __name__ == "__main__":
    main()
