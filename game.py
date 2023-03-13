import time
import random
import pygame
pygame.font.init()

WIDTH = 1000
HEIGHT = 800
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 8
STAR_WIDTH = 15
STAR_HEIGHT = 30
STAR_VEL = 5
BALL_VEL = 15

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Game")

BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (WIDTH, HEIGHT))
FONT = pygame.font.SysFont("comicsans", 30)


def draw(player, elapsed_time, stars, balls, score):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    score_text = FONT.render(f"Score: {score}", 1, "white")
    WIN.blit(score_text, (WIDTH - score_text.get_width() - 20, 10))

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    for ball in balls:
        pygame.draw.rect(WIN, "red", ball)

    pygame.draw.rect(WIN, "red", player)

    pygame.display.update()


def main():
    run = True

    player = pygame.Rect((WIDTH//2 - PLAYER_WIDTH//2), (HEIGHT - PLAYER_HEIGHT), PLAYER_WIDTH, PLAYER_HEIGHT)
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
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
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
    
        if keys[pygame.K_a] and player.x - PLAYER_VEL >=0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_d] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
                # score += 1
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                # score += 1
                break
            for ball in balls[:]:
                if star.colliderect(ball) and star in stars:
                    balls.remove(ball)
                    stars.remove(star)
                    score += 1

        for ball in balls[:]:
            ball.y -= BALL_VEL
            #score += 1
            if ball.y < 0:
                balls.remove(ball)

        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH//2-lost_text.get_width()//2, HEIGHT//2 - lost_text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, stars, balls, score)

    pygame.quit()


if __name__ == "__main__":
    main()