"""Game logic and main game loop"""
import pygame
import random
from settings import *
from player import Player
from obstacle import Obstacle
from coin import Coin
from database import GameDatabase
from game_state import GameState


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.state = GameState.MENU
        self.player = Player()
        self.obstacles = []
        self.coins = []
        self.spawn_timer = 0
        self.score = 0
        self.speed = SPEED_START
        self.selected_level = 1
        self.level = 1  # Current stage
        self.lives = START_LIVES
        self.hit_cooldown = 0
        self.player_name = ""
        self.result_saved = False
        self.database = GameDatabase()
        self.top_results = self.database.get_top_results()

        self.mountain_x = 0
        self.road_x = 0

        self.settings = {
            "volume": int(MUSIC_VOLUME * 100),
            "difficulty": 1,
        }

        self.ui_state = {
            "menu_selected": 0,
            "selected_level": 1,
            "settings_selected": 0,
        }

        self.game_input = {
            "jump": False,
            "duck": False
        }
    
    def reset_game(self):
        """Reset game for new play session"""
        self.obstacles = []
        self.coins = []
        self.score = 0
        self.speed = SPEED_START
        self.spawn_timer = 0
        self.level = self.selected_level
        self.lives = START_LIVES
        self.hit_cooldown = 0
        self.player.reset()
        self.mountain_x = 0
        self.road_x = 0
        self.result_saved = False
    
    def update_scrolling_backgrounds(self, current_speed):
        """Update mountain and road scrolling positions"""
        if self.state == GameState.RUNNING:
            self.mountain_x -= current_speed * 0.3
            self.road_x -= current_speed

        if hasattr(self, 'mountain_width'):
            if self.mountain_x <= -self.mountain_width:
                self.mountain_x += self.mountain_width

        if hasattr(self, 'road_width'):
            if self.road_x <= -self.road_width:
                self.road_x += self.road_width
    
    def update_game(self):
        """Update game state during RUNNING"""
        if self.state != GameState.RUNNING:
            return

        level_mult = LEVEL_CONFIGS[self.level]

        self.speed += SPEED_INCREASE * level_mult["speed_increase"]
        self.score += 0.1 * level_mult["score_multiplier"]

        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

        self.player.update(
            pygame.key.get_pressed(),
            self.game_input["jump"],
            self.game_input["duck"]
        )
        self.game_input["jump"] = False
        self.game_input["duck"] = False

        spawn_rate = level_mult["spawn_rate"]
        self.spawn_timer += 1
        if self.spawn_timer > spawn_rate:
            self.obstacles.append(Obstacle(self.speed))
            if random.random() < 0.5:
                self.coins.append(
                    Coin(self.obstacles[-1].x + random.randint(180, 280))
                )
            self.spawn_timer = 0

        for c in self.coins[:]:
            c.update(self.speed)
            if self.player.mask.overlap(c.mask, (c.rect.x - self.player.rect.x, c.rect.y - self.player.rect.y)):
                self.score += 10
                self.coins.remove(c)

        for ob in self.obstacles[:]:
            ob.update()
            if self.hit_cooldown == 0 and self.player.mask.overlap(
                ob.mask, (ob.rect.x - self.player.rect.x, ob.rect.y - self.player.rect.y)
            ):
                self.lives -= 1
                self.hit_cooldown = HIT_INVINCIBILITY_FRAMES
                self.obstacles.remove(ob)
                if self.lives <= 0:
                    self.save_current_result()
                    self.state = GameState.GAME_OVER
                break

        self.obstacles = [o for o in self.obstacles if not o.off_screen()]
        self.coins = [c for c in self.coins if not c.off_screen()]
    
    def render_game(self, font_title, font_ui, bg_img, mountain_img, road_img):
        """Render current game state to screen"""
        from screens import (
            draw_menu, draw_settings, draw_start_screen, draw_game_over,
            draw_level_select, draw_background, draw_ground, draw_ui, draw_level,
            draw_hearts, draw_leaderboard
        )
        
        if self.state == GameState.MENU:
            draw_menu(self.screen, self.ui_state, bg_img, road_img, self.player, WIDTH, HEIGHT)

        elif self.state == GameState.LEADERBOARD:
            draw_leaderboard(self.screen, bg_img, WIDTH, HEIGHT, self.top_results)

        elif self.state == GameState.LEVEL_SELECT:
            draw_level_select(self.screen, self.selected_level, WIDTH, HEIGHT)
        
        elif self.state == GameState.SETTINGS:
            draw_settings(self.screen, self.ui_state, self.settings, bg_img, WIDTH, HEIGHT)

        else:
            if self.state != GameState.MENU and self.state != GameState.SETTINGS:
                draw_background(
                    self.screen, bg_img, mountain_img, road_img, self.mountain_x
                )

            if self.state == GameState.RUNNING:
                draw_ground(self.screen, road_img, self.road_x)

                for c in self.coins:
                    c.draw(self.screen)

                for ob in self.obstacles:
                    ob.draw(self.screen)

                self.player.draw(self.screen)

                if self.player_name:
                    name_surface = font_ui.render(self.player_name, True, (255, 255, 255))
                    name_box = pygame.Rect(0, 0, name_surface.get_width() + 16, name_surface.get_height() + 8)
                    name_box.midbottom = (self.player.rect.centerx, self.player.rect.top - 8)
                    pygame.draw.rect(self.screen, (0, 0, 0), name_box, border_radius=8)
                    pygame.draw.rect(self.screen, (255, 200, 100), name_box, 2, border_radius=8)
                    self.screen.blit(name_surface, name_surface.get_rect(center=name_box.center))

                draw_ui(self.screen, self.score, font_ui, WIDTH, HEIGHT)
                draw_level(self.screen, self.level, font_ui, WIDTH)
                draw_hearts(self.screen, self.lives)

            elif self.state == GameState.START:
                draw_start_screen(
                    self.screen,
                    self.player,
                    bg_img,
                    font_title,
                    font_ui,
                    WIDTH,
                    HEIGHT,
                    self.level,
                    self.player_name,
                )

            elif self.state == GameState.GAME_OVER:
                draw_game_over(
                    self.screen,
                    self.player,
                    road_img,
                    font_title,
                    font_ui,
                    self.score,
                    WIDTH,
                    HEIGHT,
                    self.top_results,
                )

    def tick(self, fps):
        """Advance game by one frame"""
        self.clock.tick(fps)

    def save_current_result(self):
        """Persist the current run once when the player loses."""
        if self.result_saved:
            return

        self.database.save_result(self.player_name, self.score, self.level)
        self.top_results = self.database.get_top_results()
        self.result_saved = True

    def refresh_leaderboard(self):
        """Reload leaderboard data from the database."""
        self.top_results = self.database.get_top_results()
