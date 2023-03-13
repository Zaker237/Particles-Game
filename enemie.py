import pygame
import configs


class Enemie(pygame.Rect):
    COLORS = {
        1: "white",
        2: "white",
        3: "white",
        4: "white",
        5: "white",
        6: "white",
        7: "white",
        8: "white",
        9: "white",
        10: "white"
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