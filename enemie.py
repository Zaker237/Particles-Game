import pygame
import configs


class Enemie(pygame.Rect):
    COLORS = {
        1: pygame.Color(255, 0, 0),
        2: pygame.Color(255, 26, 26),
        3: pygame.Color(255, 51, 51),
        4: pygame.Color(255, 77, 77),
        5: pygame.Color(255, 102, 102),
        6: pygame.Color(255, 128, 128),
        7: pygame.Color(255, 153, 153),
        8: pygame.Color(255, 179, 179),
        9: pygame.Color(255, 204, 204),
        10: pygame.Color(255, 255, 255)
    }

    COINS = {
        "simple": 1,
        "middle": 5,
        "hard": 10
    }

    def __init__(self, x: int, y: int, width: int, height: int, type: str="simple") ->None:
        super().__init__(x, y, width, height)

        if type not in list(self.COINS.keys()):
            raise ValueError(f"The type should be in [{','.join(list(self.COINS.keys()))}]!")

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type
        self.coins = self.COINS.get(type)

    def get_color(self) -> str:
        return self.COLORS.get(self.COINS.get(self.type))

    def is_alive(self) -> bool:
        return self.coins > 0