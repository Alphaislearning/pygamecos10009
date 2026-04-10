import pygame
import random
import math
from settings import *

LABELS = ["HD", "Best"]

class Coin:
    def __init__(self, x):
        self.x = x
        self.label = random.choice(LABELS)

        self.y = random.choice([
            GROUND_Y - 120,
            GROUND_Y - 80,
            GROUND_Y - 160
        ])
        self.w, self.h = 50, 32
        self.base_y = self.y
        self.time = 0

        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        self.surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)

        self.draw_label()  # ✅ giờ gọi OK

        self.mask = pygame.mask.from_surface(self.surface)

    # ✅ ĐÚNG: method phải nằm ngang với __init__
    def draw_label(self):
        self.surface.fill((0, 0, 0, 0))

        if self.label == "HD":
            base_color = (80, 200, 255)   # xanh sáng hơn
            glow_color = (80, 200, 255, 80)
        else:
            base_color = (255, 200, 50)   # vàng đậm hơn
            glow_color = (255, 200, 50, 80)

        # 🔥 Glow (vẽ trước)
        for i in range(3):
            pygame.draw.rect(
                self.surface,
                glow_color,
                (-i, -i, self.w + i*2, self.h + i*2),
                border_radius=14
            )

        # Base
        pygame.draw.rect(self.surface, base_color, (0, 0, self.w, self.h), border_radius=12)

        # Highlight (ánh sáng)
        pygame.draw.rect(
            self.surface,
            (255, 255, 255, 100),
            (4, 2, self.w - 8, self.h // 2),
            border_radius=10
        )

        # Border rõ hơn
        pygame.draw.rect(self.surface, (255, 255, 255), (0, 0, self.w, self.h), 2, border_radius=12)

        # Text rõ hơn
        font = pygame.font.SysFont(None, 20, bold=True)
        text = font.render(self.label, True, (20, 20, 20))  # đậm hơn
        rect = text.get_rect(center=(self.w // 2, self.h // 2))

        self.surface.blit(text, rect)


    def update(self, speed):
        self.x -= speed
        self.rect.x = self.x
        self.time += 0.1
        self.y = self.base_y + math.sin(self.time) * 5  # float lên xuống
        self.rect.y = int(self.y)
        scale = 1 + math.sin(self.time * 2) * 0.05
        self.scaled_surface = pygame.transform.scale(
            self.surface,
            (int(self.w * scale), int(self.h * scale))
        )


    def draw(self, screen):
        surf = getattr(self, "scaled_surface", self.surface)
        rect = surf.get_rect(center=self.rect.center)
        screen.blit(surf, rect)

    def off_screen(self):
        return self.x < -50