import time
import random
import pygame
from enemie import Enemie, EnemieType
pygame.font.init()
pygame.mixer.init()
import configs


WIN = pygame.display.set_mode((configs.GAME_WIDTH, configs.GAME_HEIGHT))
pygame.display.set_caption("Particle Game")

BG = pygame.transform.scale(pygame.image.load(configs.FONT_IMAGE), (configs.GAME_WIDTH, configs.GAME_HEIGHT))
FONT = pygame.font.SysFont("comicsans", 30)

GUN_SOUND = pygame.mixer.Sound(configs.GUN_SONG_PATH)
GRENADE_SOUND = pygame.mixer.Sound(configs.GRENADE_SONG_PATH)

GRENADE_SOUND.play()


def draw(player, elapsed_time, enemies, balls, score):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    score_text = FONT.render(f"Score: {score}", 1, "white")
    WIN.blit(score_text, (configs.GAME_WIDTH - score_text.get_width() - 20, 10))

    for enemie in enemies:
        pygame.draw.rect(WIN, enemie.get_color(), enemie)

    for ball in balls:
        pygame.draw.rect(WIN, "green", ball)

    pygame.draw.rect(WIN, "green", player)

    pygame.display.update()


def main():
    run = True

    player = pygame.Rect(
        (configs.GAME_WIDTH//2 - configs.PLAYER_WIDTH//2),
        (configs.GAME_HEIGHT - configs.PLAYER_HEIGHT),
        configs.PLAYER_WIDTH,
        configs.PLAYER_HEIGHT
    )
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    enemie_add_increment = 2000
    enemie_count = 0
    score = 0

    enemies = []
    balls = []
    hit = False
    last_ball_time = time.time()

    while run:
        enemie_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if enemie_count > enemie_add_increment:
            for _ in range(random.randint(1, 5)):
                enemie_x = random.randint(0, configs.GAME_WIDTH - configs.ENEMIE_WIDTH)
                enemie = Enemie(
                    enemie_x,
                    -configs.ENEMIE_HEIGHT,
                    configs.ENEMIE_WIDTH,
                    configs.ENEMIE_HEIGHT,
                    type=EnemieType.SIMPLE
                )
                enemies.append(enemie)

            enemie_add_increment = max(200, enemie_add_increment - 50)
            enemie_count = 0

        if random.randint(1, 100) == 17:
            enemie_x = random.randint(0, configs.GAME_WIDTH - configs.ENEMIE_WIDTH)
            enemie = Enemie(
                enemie_x,
                -configs.ENEMIE_HEIGHT,
                configs.ENEMIE_WIDTH + 5,
                configs.ENEMIE_HEIGHT + 5,
                type=EnemieType.MIDDLE
            )
            enemies.append(enemie)
        
        if random.randint(1, 500) == 59:
            enemie_x = random.randint(0, configs.GAME_WIDTH - configs.ENEMIE_WIDTH)
            enemie = Enemie(
                enemie_x,
                -configs.ENEMIE_HEIGHT,
                configs.ENEMIE_WIDTH + 10,
                configs.ENEMIE_HEIGHT + 10,
                type=EnemieType.HARD
            )
            enemies.append(enemie)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if time.time() - last_ball_time > 0.05:
                ball = pygame.Rect(player.x + player.width//2 - 5, player.y, 10, 10)
                balls.append(ball)
                last_ball_time = time.time()
                GUN_SOUND.play()
    
        if keys[pygame.K_a] and player.x - configs.PLAYER_VEL >=0:
            player.x -= configs.PLAYER_VEL
        if keys[pygame.K_d] and player.x + configs.PLAYER_VEL + player.width <= configs.GAME_WIDTH:
            player.x += configs.PLAYER_VEL

        for enemie in enemies[:]:
            enemie.y += configs.ENEMIE_VEL
            if enemie.y > configs.GAME_HEIGHT:
                enemies.remove(enemie)
                # score += 1
            elif enemie.y + enemie.height >= player.y and enemie.colliderect(player):
                enemies.remove(enemie)
                hit = True
                GRENADE_SOUND.play(2)
                # score += 1
                break
            for ball in balls[:]:
                if enemie.colliderect(ball) and enemie in enemies:
                    balls.remove(ball)
                    enemie.coins -= 1
                    #enemies.remove(enemie)
                    #score += 1

            if not enemie.is_alive():
                score += enemie.get_points()
                enemies.remove(enemie)

        for ball in balls[:]:
            ball.y -= configs.BALL_VEL
            #score += 1
            if ball.y < 0:
                balls.remove(ball)

        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(
                lost_text,
                (configs.GAME_WIDTH//2-lost_text.get_width()//2,
                configs.GAME_HEIGHT//2 - lost_text.get_height()//2)
            )
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, enemies, balls, score)

    pygame.quit()


if __name__ == "__main__":
    main()