"""Game logic and main game loop"""
import pygame
import random
from settings import *
from player import Player
from obstacle import Obstacle
from coin import Coin
from game_state import GameState


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        # Game state
        self.state = GameState.MENU
        self.player = Player()
        self.obstacles = []
        self.coins = []
        self.spawn_timer = 0
        self.score = 0
        self.speed = SPEED_START
        self.level = 1  # Current level
        self.lives = START_LIVES
        self.hit_cooldown = 0
        
        # Scrolling backgrounds
        self.mountain_x = 0
        self.road_x = 0
        
        # Settings and UI state
        self.settings = {
            "volume": 50,
            "difficulty": 1  # 1: Easy, 2: Normal, 3: Hard
        }
        
        self.ui_state = {
            "menu_selected": 0,  # 0: Play, 1: Settings, 2: Quit
            "settings_selected": 0  # 0: Volume, 1: Difficulty
        }
        
        self.game_input = {
            "jump": False,
            "duck": False
        }
    
    def get_current_level(self):
        """Determine current level based on score"""
        if self.score >= LEVEL_THRESHOLDS[3]:
            return 3
        elif self.score >= LEVEL_THRESHOLDS[2]:
            return 2
        else:
            return 1
    
    def update_level(self):
        """Update level based on score"""
        new_level = self.get_current_level()
        if new_level != self.level:
            self.level = new_level
    
    def reset_game(self):
        """Reset game for new play session"""
        self.obstacles = []
        self.coins = []
        self.score = 0
        self.speed = SPEED_START
        self.spawn_timer = 0
        self.level = 1
        self.lives = START_LIVES
        self.hit_cooldown = 0
        self.player.reset()
        self.mountain_x = 0
        self.road_x = 0
    
    def update_scrolling_backgrounds(self, current_speed):
        """Update mountain and road scrolling positions"""
        if self.state == GameState.RUNNING:
            self.mountain_x -= current_speed * 0.3
            self.road_x -= current_speed
        
        # Wrap mountain (width stored in game startup)
        if hasattr(self, 'mountain_width'):
            if self.mountain_x <= -self.mountain_width:
                self.mountain_x += self.mountain_width
        
        # Wrap road (width stored in game startup)
        if hasattr(self, 'road_width'):
            if self.road_x <= -self.road_width:
                self.road_x += self.road_width
    
    def update_game(self):
        """Update game state during RUNNING"""
        if self.state != GameState.RUNNING:
            return
        
        # Get level multiplier
        level_mult = LEVEL_MULTIPLIERS[self.level]
        
        # Speed increase with level multiplier
        self.speed += SPEED_INCREASE * level_mult["speed_increase"]
        self.score += 0.1
        
        # Update level
        self.update_level()

        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1
        
        # Update player
        self.player.update(
            pygame.key.get_pressed(),
            self.game_input["jump"],
            self.game_input["duck"]
        )
        self.game_input["jump"] = False
        self.game_input["duck"] = False
        
        # Spawn obstacles with level-based rate
        spawn_rate = level_mult["spawn_rate"]
        self.spawn_timer += 1
        if self.spawn_timer > spawn_rate:
            self.obstacles.append(Obstacle(self.speed))
            if random.random() < 0.5:
                self.coins.append(
                    Coin(self.obstacles[-1].x + random.randint(180, 280))
                )
            self.spawn_timer = 0
        
        # Update and draw coins
        for c in self.coins[:]:
            c.update(self.speed)
            if self.player.mask.overlap(c.mask, (c.rect.x - self.player.rect.x, c.rect.y - self.player.rect.y)):
                self.score += 10
                self.coins.remove(c)
        
        # Update obstacles and check collision
        for ob in self.obstacles[:]:
            ob.update()
            if self.hit_cooldown == 0 and self.player.mask.overlap(
                ob.mask, (ob.rect.x - self.player.rect.x, ob.rect.y - self.player.rect.y)
            ):
                self.lives -= 1
                self.hit_cooldown = HIT_INVINCIBILITY_FRAMES
                self.obstacles.remove(ob)
                if self.lives <= 0:
                    self.state = GameState.GAME_OVER
                break
        
        # Remove off-screen objects
        self.obstacles = [o for o in self.obstacles if not o.off_screen()]
        self.coins = [c for c in self.coins if not c.off_screen()]
    
    def render_game(self, font_title, font_ui, bg_img, mountain_img, road_img):
        """Render current game state to screen"""
        from screens import (
            draw_menu, draw_settings, draw_start_screen, draw_game_over,
            draw_background, draw_ground, draw_ui, draw_level, draw_hearts
        )
        
        if self.state == GameState.MENU:
            draw_menu(self.screen, self.ui_state, bg_img, road_img, self.player, WIDTH, HEIGHT)
        
        elif self.state == GameState.SETTINGS:
            draw_settings(self.screen, self.ui_state, self.settings, bg_img, WIDTH, HEIGHT)
        
        else:
            # Draw background for non-menu states
            if self.state != GameState.MENU and self.state != GameState.SETTINGS:
                draw_background(
                    self.screen, bg_img, mountain_img, road_img, self.mountain_x
                )
            
            if self.state == GameState.RUNNING:
                # Draw game elements
                draw_ground(self.screen, road_img, self.road_x)
                
                # Draw coins
                for c in self.coins:
                    c.draw(self.screen)
                
                # Draw obstacles
                for ob in self.obstacles:
                    ob.draw(self.screen)
                
                # Draw player
                self.player.draw(self.screen)
                
                # Draw UI
                draw_ui(self.screen, self.score, font_ui, WIDTH, HEIGHT)
                draw_level(self.screen, self.level, font_ui, WIDTH)
                draw_hearts(self.screen, self.lives)
            
            elif self.state == GameState.START:
                draw_start_screen(self.screen, self.player, road_img, font_title, font_ui, WIDTH, HEIGHT)
            
            elif self.state == GameState.GAME_OVER:
                draw_game_over(self.screen, self.player, road_img, font_title, font_ui, self.score, WIDTH, HEIGHT)
    
    def tick(self, fps):
        """Advance game by one frame"""
        self.clock.tick(fps)
