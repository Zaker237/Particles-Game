import pygame


class PowerUp(pygame.Rect):
    def __init__(self, x, y, kind):
        super().__init__(x, y, 20, 20)
        self.kind = kind  # "RAPID", "SPREAD", or "NUKE"
        self.vel = 3

    def update(self):
        self.y += self.vel

    def draw(self, surface):
        color = "yellow" if self.kind == "RAPID" else "cyan"
        pygame.draw.rect(surface, color, self)