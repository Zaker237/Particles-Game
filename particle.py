import pygame
import random

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-4, 4)  # x veolcity
        self.vy = random.uniform(-4, 4)
        self.lifetime = 255  # Used for transparency (alpha)
        self.color = color
        self.size = random.randint(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 7  # How fast the particle fades

    def draw(self, surface):
        if self.lifetime > 0:
            # Create a small surface for the particle to allow transparency
            s = pygame.Surface((self.size, self.size))
            s.set_alpha(self.lifetime)
            s.fill(self.color)
            surface.blit(s, (self.x, self.y))

    def is_dead(self):
        return self.lifetime <= 0