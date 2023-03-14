import time
import random
import pygame
from enemie import Enemie
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


def draw(player, elapsed_time, stars, balls, score):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    score_text = FONT.render(f"Score: {score}", 1, "white")
    WIN.blit(score_text, (configs.GAME_WIDTH - score_text.get_width() - 20, 10))

    for star in stars:
        pygame.draw.rect(WIN, star.get_color(), star)

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

    star_add_increment = 2000
    star_count = 0
    score = 0

    stars = []
    balls = []
    hit = False
    last_ball_time = time.time()

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(random.randint(1, 5)):
                star_x = random.randint(0, configs.GAME_WIDTH - configs.STAR_WIDTH)
                star = Enemie(
                    star_x,
                    -configs.STAR_HEIGHT,
                    configs.STAR_WIDTH,
                    configs.STAR_HEIGHT,
                    type="middle"
                )
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

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

        for star in stars[:]:
            star.y += configs.STAR_VEL
            if star.y > configs.GAME_HEIGHT:
                stars.remove(star)
                # score += 1
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                GRENADE_SOUND.play(2)
                # score += 1
                break
            for ball in balls[:]:
                if star.colliderect(ball) and star in stars:
                    balls.remove(ball)
                    star.coins -= 1
                    #stars.remove(star)
                    #score += 1

            if not star.is_alive():
                score += star.get_points()
                stars.remove(star)

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

        draw(player, elapsed_time, stars, balls, score)

    pygame.quit()


if __name__ == "__main__":
    main()