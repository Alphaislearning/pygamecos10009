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


def load_bg_cover(path, size):
    """Load a background image and scale it to cover the target size without distortion."""
    img = pygame.image.load(path).convert()
    source_width, source_height = img.get_size()
    target_width, target_height = size

    scale = max(target_width / source_width, target_height / source_height)
    scaled_width = int(source_width * scale)
    scaled_height = int(source_height * scale)
    img = pygame.transform.smoothscale(img, (scaled_width, scaled_height))

    crop_x = (scaled_width - target_width) // 2
    crop_y = (scaled_height - target_height) // 2
    return img.subsurface((crop_x, crop_y, target_width, target_height)).copy()


def main():
    """Main game loop"""
    # Initialize pygame
    pygame.init()
    pygame.font.init()
    
    # Setup screen and clock
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Swinburn Runner")
    
    # Load assets
    bg_imgs = {
        1: load_bg_cover("assets/background.png", (WIDTH, HEIGHT)),
        2: load_bg_cover("assets/background_lv2.png", (WIDTH, HEIGHT)),
        3: load_bg_cover("assets/background_lv3.png", (WIDTH, HEIGHT)),
    }
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
            new_state, running, game.game_input = process_events(event, game)
            
            # Handle state transitions
            if new_state == GameState.START and game.state in [GameState.MENU, GameState.LEVEL_SELECT]:
                game.level = game.selected_level
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
        current_bg = bg_imgs.get(game.level, bg_imgs[1])
        game.render_game(font_title, font_ui, current_bg, mountain_img, road_img)
        
        # Update display
        pygame.display.update()
    
    # Cleanup
    pygame.quit()


if __name__ == "__main__":
    main()
