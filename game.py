import time
import random
import pygame
from enemie import Enemie, EnemieType
from particle import Particle
from powerup import PowerUp
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


def draw(player, elapsed_time, enemies, balls, score, particles: list[Particle], powerups: list[PowerUp]):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    score_text = FONT.render(f"Score: {score}", 1, "white")
    WIN.blit(score_text, (configs.GAME_WIDTH - score_text.get_width() - 20, 10))

    for enemie in enemies:
        pygame.draw.rect(WIN, enemie.get_color(), enemie)

    for ball in balls:
        pygame.draw.rect(WIN, "green", ball)

    for p in particles:
        p.draw(WIN)

    for p_up in powerups:
        p_up.draw(WIN)

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
    particles = []
    hit = False
    last_ball_time = time.time()

    powerups = []
    current_bonus = None
    bonus_start_time = 0

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
        # Check if bonus expired (e.g., lasts 5 seconds)
        if current_bonus and time.time() - bonus_start_time > 5:
            current_bonus = None

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            cooldown = 0.01 if current_bonus == "RAPID" else 0.15

            if time.time() - last_ball_time > cooldown:
                ball = pygame.Rect(player.x + player.width//2 - 5, player.y, 10, 10)
                balls.append(ball)
                last_ball_time = time.time()
                GUN_SOUND.play()
    
        if keys[pygame.K_LEFT] and player.x - configs.PLAYER_VEL >=0:
            player.x -= configs.PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + configs.PLAYER_VEL + player.width <= configs.GAME_WIDTH:
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
                if enemie.type == EnemieType.HARD and random.random() < 0.2:
                    powerups.append(PowerUp(enemie.x, enemie.y, "RAPID"))
                score += enemie.get_points()
                for _ in range(15):  # Create 15 particles per death
                    particles.append(Particle(enemie.centerx, enemie.centery, enemie.get_color()))
                enemies.remove(enemie)

        for ball in balls[:]:
            ball.y -= configs.BALL_VEL
            #score += 1
            if ball.y < 0:
                balls.remove(ball)

        for particle in particles[:]:
            particle.update()
            if particle.is_dead():
                particles.remove(particle)

        for p_up in powerups[:]:
            p_up.update()
            if p_up.colliderect(player):
                current_bonus = p_up.kind
                bonus_start_time = time.time()
                powerups.remove(p_up)
            elif p_up.y > configs.GAME_HEIGHT:
                powerups.remove(p_up)

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

        if current_bonus:
            rem = max(0, 5 - (time.time() - bonus_start_time))
            bonus_text = FONT.render(f"{current_bonus}: {rem:.1f}s", 1, "yellow")
            WIN.blit(bonus_text, (configs.GAME_WIDTH // 2 - bonus_text.get_width() // 2, 50))

        draw(player, elapsed_time, enemies, balls, score, particles, powerups)

    pygame.quit()


if __name__ == "__main__":
    main()