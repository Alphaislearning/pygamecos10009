import pygame
import random

from settings import *
from player import Player
from obstacle import Obstacle
from coin import Coin
from game_state import GameState

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Swinburn Runner")
clock = pygame.time.Clock()

# ================= LOAD IMAGE =================
def load_img(path, scale=None):
    img = pygame.image.load(path).convert_alpha()

    # remove nền trắng (tolerant)
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            r, g, b, a = img.get_at((x, y))
            if r > 240 and g > 240 and b > 240:
                img.set_at((x, y), (0, 0, 0, 0))

    if scale:
        img = pygame.transform.scale(img, scale)

    return img


bg_img = load_img("assets/background.png", (WIDTH, HEIGHT))
mountain_img = load_img("assets/mountain.png")
road_img = load_img("assets/road.png")

# SCALE
mountain_img = pygame.transform.scale(
    mountain_img,
    (int(mountain_img.get_width() * 0.5), int(mountain_img.get_height() * 0.6))
)

road_img = pygame.transform.scale(
    road_img,
    (int(road_img.get_width() * 0.5), int(road_img.get_height() * 0.5))
)

# ================= FONT =================
font_title = pygame.font.SysFont("Arial", 40, bold=True)
font_ui = pygame.font.SysFont("Arial", 26, bold=True)

# ================= GAME OBJECT =================
player = Player()
state = GameState.START

obstacles, coins = [], []
spawn_timer = 0
score = 0
speed = SPEED_START

# ================= SCROLL =================
mountain_x = 0
road_x = 0

# ================= RESET =================
def reset_game():
    global obstacles, coins, score, speed
    obstacles, coins = [], []
    score, speed = 0, SPEED_START
    player.reset()

# ================= DRAW =================
def draw_background(current_speed):
    global mountain_x

    # background
    screen.blit(bg_img, (0, 0))

    # mountain parallax
    if state == GameState.RUNNING:
        mountain_x -= current_speed * 0.3

    w = mountain_img.get_width()
    y = HEIGHT - road_img.get_height() - 100

    screen.blit(mountain_img, (mountain_x, y))
    screen.blit(mountain_img, (mountain_x + w, y))

    if mountain_x <= -w:
        mountain_x += w


def draw_ground(current_speed):
    global road_x

    if state == GameState.RUNNING:
        road_x -= current_speed

    w = road_img.get_width()
    y = HEIGHT - road_img.get_height()

    screen.blit(road_img, (road_x, y))
    screen.blit(road_img, (road_x + w, y))

    if road_x <= -w:
        road_x += w


def draw_ui():
    box_rect = pygame.Rect(WIDTH//2 - 80, 20, 160, 45)
    pygame.draw.rect(screen, (255, 255, 255), box_rect, border_radius=15)
    pygame.draw.rect(screen, (255, 180, 200), box_rect, 3, border_radius=15)

    txt = font_ui.render(f"Score: {int(score)}", True, (70, 75, 95))
    screen.blit(txt, txt.get_rect(center=box_rect.center))


# ================= GAME LOOP =================
running = True
while running:
    clock.tick(FPS)

    jump_pressed = False
    duck_pressed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_w]:
                jump_pressed = True
            if event.key in [pygame.K_DOWN, pygame.K_s]:
                duck_pressed = True
            if event.key == pygame.K_SPACE:
                if state == GameState.START:
                    state = GameState.RUNNING
                elif state == GameState.GAME_OVER:
                    reset_game()
                    state = GameState.RUNNING

    # ===== BACKGROUND + MOUNTAIN =====
    draw_background(speed if state == GameState.RUNNING else 0)

    if state == GameState.RUNNING:
        speed += SPEED_INCREASE
        score += 0.1

        player.update(pygame.key.get_pressed(), jump_pressed, duck_pressed)

        # spawn obstacle
        spawn_timer += 1
        if spawn_timer > 60:
            obstacles.append(Obstacle(speed))
            if random.random() < 0.5:
                coins.append(Coin(obstacles[-1].x + random.randint(180, 280)))
            spawn_timer = 0

        # ===== GROUND (LUÔN DƯỚI) =====
        draw_ground(speed)

        # ===== COIN =====
        for c in coins[:]:
            c.update(speed)
            if player.mask.overlap(c.mask, (c.rect.x-player.rect.x, c.rect.y-player.rect.y)):
                score += 10
                coins.remove(c)
            else:
                c.draw(screen)

        # ===== OBSTACLE =====
        for ob in obstacles[:]:
            ob.update()
            if player.mask.overlap(ob.mask, (ob.rect.x-player.rect.x, ob.rect.y-player.rect.y)):
                state = GameState.GAME_OVER
            else:
                ob.draw(screen)

        obstacles = [o for o in obstacles if not o.off_screen()]
        coins = [c for c in coins if not c.off_screen()]

        # ===== PLAYER (TRÊN CÙNG) =====
        player.draw(screen)

        draw_ui()

    elif state == GameState.START:
        draw_ground(0)
        player.draw(screen)

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 160))
        screen.blit(overlay, (0, 0))

        t1 = font_title.render("Dreamy Runner", True, (70, 75, 95))
        t2 = font_ui.render("Press SPACE to Start", True, (120, 130, 160))

        screen.blit(t1, t1.get_rect(center=(WIDTH//2, HEIGHT//2 - 40)))
        screen.blit(t2, t2.get_rect(center=(WIDTH//2, HEIGHT//2 + 20)))

    elif state == GameState.GAME_OVER:
        draw_ground(0)
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

    pygame.display.update()

pygame.quit()