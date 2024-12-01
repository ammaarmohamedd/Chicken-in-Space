import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flying Chickens in Space")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Load assets
spaceship_img = pygame.image.load("spaceship.png")  # Replace with your image
chicken_img = pygame.image.load("chicken.png")  # Replace with your image
egg_img = pygame.image.load("egg.png")  # Replace with your image
background_img = pygame.image.load("space_background.jpg")  # Replace with your image

# Sound effects
shoot_sound = pygame.mixer.Sound("shoot.mp3")
hit_sound = pygame.mixer.Sound("hit.mp3")
game_over_sound = pygame.mixer.Sound("game_over.mp3")

# Game variables
spaceship_x, spaceship_y = 370, 480
spaceship_speed = 5
lives = 3
shield = False

bullets = []
bullet_speed = -7

chickens = []
chicken_speed = 2
chicken_spawn_timer = 30

eggs = []
egg_speed = 4

score = 0
level = 1
font = pygame.font.Font(None, 36)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.blit(background_img, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and spaceship_x > 0:
        spaceship_x -= spaceship_speed
    if keys[pygame.K_RIGHT] and spaceship_x < SCREEN_WIDTH - 64:
        spaceship_x += spaceship_speed
    if keys[pygame.K_SPACE]:
        bullets.append([spaceship_x + 16, spaceship_y])
        shoot_sound.play()

    # Update bullets
    for bullet in bullets:
        bullet[1] += bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Spawn chickens
    chicken_spawn_timer -= 1
    if chicken_spawn_timer == 0:
        chicken_spawn_timer = max(10, 30 - level * 2)  # Chickens spawn faster at higher levels
        chickens.append([random.randint(0, SCREEN_WIDTH - 64), 0])

    # Update chickens
    for chicken in chickens:
        chicken[1] += chicken_speed
        if random.randint(0, 100) < 2:  # 2% chance of dropping an egg
            eggs.append([chicken[0] + 16, chicken[1] + 40])
        if chicken[1] > SCREEN_HEIGHT:
            chickens.remove(chicken)

    # Update eggs
    for egg in eggs:
        egg[1] += egg_speed
        if egg[1] > SCREEN_HEIGHT:
            eggs.remove(egg)

    # Check for collisions
    for chicken in chickens:
        for bullet in bullets:
            if bullet[0] in range(chicken[0], chicken[0] + 64) and bullet[1] in range(chicken[1], chicken[1] + 64):
                bullets.remove(bullet)
                chickens.remove(chicken)
                hit_sound.play()
                score += 1
                if score % 10 == 0:  # Increase level every 10 points
                    level += 1
                    chicken_speed += 0.5

    for egg in eggs:
        if egg[0] in range(spaceship_x, spaceship_x + 64) and egg[1] in range(spaceship_y, spaceship_y + 64):
            eggs.remove(egg)
            if not shield:
                lives -= 1
                game_over_sound.play()
            shield = False

    # Draw elements
    screen.blit(spaceship_img, (spaceship_x, spaceship_y))
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, (*bullet, 5, 10))
    for chicken in chickens:
        screen.blit(chicken_img, tuple(chicken))
    for egg in eggs:
        screen.blit(egg_img, tuple(egg))

    # Draw score and lives
    score_text = font.render(f"Score: {score} | Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    lives_text = font.render(f"Lives: {lives}", True, RED)
    screen.blit(lives_text, (SCREEN_WIDTH - 150, 10))

    # Check game over
    if lives <= 0:
        game_over_text = font.render("GAME OVER! Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        game_over_sound.play()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Reset the game
                        score, lives, level = 0, 3, 1
                        chickens.clear()
                        bullets.clear()
                        eggs.clear()
                        chicken_speed = 2
                        waiting = False
                    elif event.key == pygame.K_q:
                        running = False
                        waiting = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
