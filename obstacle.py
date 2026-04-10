import pygame
import random
from settings import *

WORDS = ["Assignment", "Vovinam", "Research", "GC", "DL"]

class Obstacle:
    def __init__(self, speed):
        self.word = random.choice(WORDS)
        self.x = WIDTH + 50
        self.speed = speed

        self.w = 95
        self.h = 44

        if self.word in ["Assignment", "Research"]:
            self.y = GROUND_Y
        else:
            self.y = GROUND_Y - 100

        self.rect = pygame.Rect(self.x, self.y - self.h, self.w, self.h)

        self.surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)

        self.draw_text_box()

        self.mask = pygame.mask.from_surface(self.surface)

    def draw_text_box(self):
        self.surface.fill((0, 0, 0, 0))

      
        base_color = (160, 50, 50)

     
        pygame.draw.rect(
            self.surface,
            base_color,
            (0, 0, self.w, self.h),
            border_radius=2
        )

        pygame.draw.rect(
            self.surface,
            (255, 255, 255),
            (0, 0, self.w, self.h),
            2,
            border_radius=2
        )

 
        spike_width = 10
        spike_height = 10


        if self.y == GROUND_Y:
            for i in range(0, self.w, spike_width):
                pygame.draw.polygon(
                    self.surface,
                    (255, 255, 255),
                    [
                        (i, 0),
                        (i + spike_width // 2, -spike_height),
                        (i + spike_width, 0)
                    ]
                )

        else:
            for i in range(0, self.w, spike_width):
                pygame.draw.polygon(
                    self.surface,
                    (255, 255, 255),
                    [
                        (i, self.h),
                        (i + spike_width // 2, self.h + spike_height),
                        (i + spike_width, self.h)
                    ]
                )

        for i in range(0, self.w, 12):
            pygame.draw.line(
                self.surface,
                (0, 0, 0, 80),
                (i, 0),
                (i + 12, self.h),
                2
            )

  
        font = pygame.font.SysFont(None, 22, bold=True)

        text = font.render(self.word, True, (255, 255, 255))
        outline = font.render(self.word, True, (0, 0, 0))

        cx = self.w // 2
        cy = self.h // 2

        for dx in [-1, 1]:
            for dy in [-1, 1]:
                rect = outline.get_rect(center=(cx + dx, cy + dy))
                self.surface.blit(outline, rect)

        rect = text.get_rect(center=(cx, cy))
        self.surface.blit(text, rect)

    def update(self):
        self.x -= self.speed
        self.rect.x = self.x

    def draw(self, screen):
        screen.blit(self.surface, (self.rect.x, self.rect.y))

    def off_screen(self):
        return self.x < -50