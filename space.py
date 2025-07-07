import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_START_X = 370
PLAYER_START_Y = 480

# Game settings
ENEMY_COUNT = 7
ENEMY_SPEED_X = 2
ENEMY_SPEED_Y = 40
BULLET_SPEED = 10
PLAYER_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load images
try:
    background = pygame.image.load("background.png").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    player_img = pygame.image.load("player.png").convert_alpha()
    enemy_img = pygame.image.load("enemy.png").convert_alpha()
    bullet_img = pygame.image.load("bullet.png").convert_alpha()
    icon = pygame.image.load("ufo.png").convert_alpha()
    pygame.display.set_icon(icon)
except:
    print("Warning: Some image files not found. Using placeholders.")
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill(BLACK)
    player_img = pygame.Surface((50, 50))
    player_img.fill(WHITE)
    enemy_img = pygame.Surface((40, 40))
    enemy_img.fill(WHITE)
    bullet_img = pygame.Surface((10, 20))
    bullet_img.fill(WHITE)

# Load sounds
try:
    shoot_sound = pygame.mixer.Sound("shoot.wav")
    explosion_sound = pygame.mixer.Sound("explosion.wav")
    background_music = pygame.mixer.Sound("background.wav")
    pygame.mixer.Sound.play(background_music, loops=-1)
except:
    print("Warning: Sound files not found. Game will continue without sounds.")

# Player setup
player_rect = player_img.get_rect()
player_rect.x = PLAYER_START_X
player_rect.y = PLAYER_START_Y
player_speed = PLAYER_SPEED

# Enemies setup
enemies = []
for _ in range(ENEMY_COUNT):
    enemy_rect = enemy_img.get_rect()
    enemy_rect.x = random.randint(0, SCREEN_WIDTH - enemy_rect.width)
    enemy_rect.y = random.randint(50, 200)
    enemies.append({
        'rect': enemy_rect,
        'speed_x': ENEMY_SPEED_X * random.choice([-1, 1]),
        'speed_y': ENEMY_SPEED_Y
    })

# Bullet setup
bullet_rect = bullet_img.get_rect()
bullet_state = "ready"  # "ready" - not fired, "fire" - bullet moving
bullet_speed = BULLET_SPEED

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Keyboard controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_rect.x -= player_speed
            if event.key == pygame.K_RIGHT:
                player_rect.x += player_speed
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_state = "fire"
                bullet_rect.x = player_rect.x + player_rect.width // 2 - bullet_rect.width // 2
                bullet_rect.y = player_rect.y
                try:
                    pygame.mixer.Sound.play(shoot_sound)
                except:
                    pass
    
    # Keep player on screen
    player_rect.x = max(0, min(player_rect.x, SCREEN_WIDTH - player_rect.width))
    
    # Enemy movement
    for enemy in enemies:
        enemy['rect'].x += enemy['speed_x']
        
        # Change direction if hitting screen edge
        if enemy['rect'].x <= 0 or enemy['rect'].x >= SCREEN_WIDTH - enemy['rect'].width:
            enemy['speed_x'] *= -1
            enemy['rect'].y += enemy['speed_y']
    
    # Bullet movement
    if bullet_state == "fire":
        bullet_rect.y -= bullet_speed
        screen.blit(bullet_img, bullet_rect)
        
        if bullet_rect.y <= 0:
            bullet_state = "ready"
    
    # Collision detection
    if bullet_state == "fire":
        for enemy in enemies[:]:
            if bullet_rect.colliderect(enemy['rect']):
                try:
                    pygame.mixer.Sound.play(explosion_sound)
                except:
                    pass
                enemies.remove(enemy)
                bullet_state = "ready"
                score += 1
                
                # Add new enemy
                if len(enemies) < ENEMY_COUNT:
                    new_enemy = {
                        'rect': enemy_img.get_rect(),
                        'speed_x': ENEMY_SPEED_X * random.choice([-1, 1]),
                        'speed_y': ENEMY_SPEED_Y
                    }
                    new_enemy['rect'].x = random.randint(0, SCREEN_WIDTH - new_enemy['rect'].width)
                    new_enemy['rect'].y = random.randint(50, 200)
                    enemies.append(new_enemy)
                break
    
    # Draw everything
    screen.blit(player_img, player_rect)
    for enemy in enemies:
        screen.blit(enemy_img, enemy['rect'])
    
    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()


