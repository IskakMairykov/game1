import pygame
import random

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Shooter")

# звуктары
shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
pygame.mixer.music.load("sounds/music.mp3")
pygame.mixer.music.play(-1)  # бесконечно

# сурот
player_img = pygame.image.load("images/player.png").convert_alpha()
enemy_img = pygame.image.load("images/enemy.png").convert_alpha()
bullet_img = pygame.image.load("images/bullet.png").convert_alpha()

player_img = pygame.transform.scale(player_img, (70, 70))
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
bullet_img = pygame.transform.scale(bullet_img, (12, 24))
bullet_img = pygame.transform.rotate(bullet_img, 90)

clock = pygame.time.Clock()
WHITE = (255, 255, 255)
RED = (255, 0, 0)

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

def reset_game():
    global player, bullets, enemies, score, game_over
    player = player_img.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))
    bullets = []
    enemies = []
    score = 0
    game_over = False

# башталышы
player = player_img.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))
player_speed = 5
bullets = []
bullet_speed = 7
enemies = []
enemy_timer = 0
enemy_speed = 3
score = 0
game_over = False

running = True
while running:
    clock.tick(60)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over and event.key == pygame.K_SPACE:
                bullet = bullet_img.get_rect(midbottom=player.midtop)
                bullets.append(bullet)
                shoot_sound.play()

            if game_over and event.key == pygame.K_r:
                reset_game()

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_a] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_d] and player.right < WIDTH:
            player.x += player_speed

        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.bottom < 0:
                bullets.remove(bullet)

        enemy_timer += 1
        if enemy_timer >= 40:
            enemy_timer = 0
            enemy = enemy_img.get_rect(
                midtop=(random.randint(25, WIDTH - 25), 0)
            )
            enemies.append(enemy)

        for enemy in enemies[:]:
            enemy.y += enemy_speed
            if enemy.top > HEIGHT:
                enemies.remove(enemy)

            if enemy.colliderect(player):
                game_over = True

        for enemy in enemies[:]:
            for bullet in bullets[:]:
                if enemy.colliderect(bullet):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 1
                    break

    screen.blit(player_img, player)

    for bullet in bullets:
        screen.blit(bullet_img, bullet)

    for enemy in enemies:
        screen.blit(enemy_img, enemy)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    if game_over:
        text = big_font.render("GAME OVER", True, RED)
        restart = font.render("R ди бас кайра ойно  ", True, WHITE)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 20))

    pygame.display.flip()

pygame.quit()
