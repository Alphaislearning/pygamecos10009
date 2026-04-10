import pygame
from settings import *

class Player:
    def __init__(self):
        self.load_images()
        self.reset()

    def load_images(self):
        def load(path):
            img = pygame.image.load(path).convert()
            img.set_colorkey((255, 255, 255))
            return pygame.transform.scale(img, (PLAYER_SCALE, PLAYER_SCALE))

        self.idle = load("assets/idle.png")
        self.jump_img = load("assets/jump.png")
        self.duck_img = load("assets/duck.png")

        self.run_frames = [
            load("assets/run_1.png"),
            load("assets/run_2.png")
        ]

    def reset(self):
        self.x = 100
        self.y = GROUND_Y
        self.vel_y = 0
        self.on_ground = True

        self.ducking = False
        self.duck_timer = 0

        self.jump_timer = 0

        self.frame_index = 0
        self.frame_timer = 0

    def update(self, keys, jump_pressed, duck_pressed):

        if jump_pressed and self.on_ground:
            self.vel_y = JUMP_FORCE
            self.on_ground = False
            self.ducking = False
            self.jump_timer = 15 

        if duck_pressed:
            if not self.ducking:
                self.ducking = True
                self.duck_timer = 40

            if not self.on_ground:
                self.vel_y += 3

        if self.ducking:
            self.duck_timer -= 1
            if self.duck_timer <= 0:
                self.ducking = False

        if self.jump_timer > 0:
            self.vel_y += GRAVITY * 0.6 
            self.jump_timer -= 1
        else:
            self.vel_y += GRAVITY

        self.y += self.vel_y

        if self.y >= GROUND_Y:
            self.y = GROUND_Y
            self.vel_y = 0
            self.on_ground = True
            self.jump_timer = 0

        if self.on_ground and not self.ducking:
            self.frame_timer += 1
            if self.frame_timer > 10:
                self.frame_index = (self.frame_index + 1) % len(self.run_frames)
                self.frame_timer = 0
        else:
            self.frame_index = 0

    def get_image(self):
        if not self.on_ground:
            return self.jump_img
        if self.ducking:
            return self.duck_img
        return self.run_frames[self.frame_index]

    def draw(self, screen):
        img = self.get_image()
        rect = img.get_rect(midbottom=(self.x, self.y))
        screen.blit(img, rect)

        self.rect = rect
        self.mask = pygame.mask.from_surface(img)