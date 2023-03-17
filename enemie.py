import pygame
from enum import Enum
import configs

class EnemieType(Enum):
    SIMPLE = 1
    MIDDLE = 2
    HARD = 3


class Enemie(pygame.Rect):
    COLORS = {
        10: pygame.Color(255, 0, 0),
        9: pygame.Color(255, 26, 26),
        8: pygame.Color(255, 51, 51),
        7: pygame.Color(255, 77, 77),
        6: pygame.Color(255, 102, 102),
        5: pygame.Color(255, 128, 128),
        4: pygame.Color(255, 153, 153),
        3: pygame.Color(255, 179, 179),
        2: pygame.Color(255, 204, 204),
        1: pygame.Color(255, 255, 255),
        0: pygame.Color(255, 255, 255),
    }

    COINS = {
        "simple": 1,
        "middle": 5,
        "hard": 10
    }

    def __init__(self, x: int, y: int, width: int, height: int, type: EnemieType) ->None:
        super().__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type
        self.coins = type.value
        self.base_coins = type.value

    def get_color(self) -> str:
        return self.COLORS.get(self.coins)

    def is_alive(self) -> bool:
        return self.coins > 0
    
    def get_points(self):
        if self.type == EnemieType.SIMPLE:
            return 1
        elif self.type == EnemieType.MIDDLE:
            return 10
        elif self.type == EnemieType.HARD:
            return 20
        else:
            return 0