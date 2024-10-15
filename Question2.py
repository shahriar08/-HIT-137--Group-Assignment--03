import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT - 50)
        self.speed = 5
        self.jump_power = -15
        self.gravity = 1
        self.velocity_y = 0
        self.health = 100
        self.lives = 3
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and self.rect.bottom >= HEIGHT:
            self.velocity_y = self.jump_power

        # Apply gravity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Keep the player on the ground
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity_y = 0

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 8
        self.damage = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(WIDTH + 10, WIDTH + 100), HEIGHT - 50)
        self.speed = random.randint(3, 5)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# Collectible class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, collectible_type):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100))
        self.collectible_type = collectible_type

    def update(self):
        pass

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Square Run")
clock = pygame.time.Clock()

# Groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.rect.bottom >= HEIGHT:
                # Shoot projectile
                projectile = Projectile(player.rect.right, player.rect.centery)
                all_sprites.add(projectile)
                projectiles.add(projectile)

    # Spawn enemies and collectibles
    if random.randint(0, 100) < 2:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
    if random.randint(0, 100) < 1:
        collectible = Collectible(random.choice(["health", "extra_life"]))
        all_sprites.add(collectible)
        collectibles.add(collectible)

    # Update sprites
    all_sprites.update()

    # Check for collisions
    enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
    if enemy_hits:
        player.health -= 10
        if player.health <= 0:
            player.lives -= 1
            player.health = 100

    collectible_hits = pygame.sprite.spritecollide(player, collectibles, True)
    for collectible in collectible_hits:
        if collectible.collectible_type == "health":
            player.health += 20
            if player.health > 100:
                player.health = 100
        elif collectible.collectible_type == "extra_life":
            player.lives += 1

    # Projectile and enemy collisions
    projectile_hits = pygame.sprite.groupcollide(projectiles, enemies, True, True)
    for projectile in projectile_hits:
        for enemy in projectile_hits[projectile]:
            player.score += 10  # Increase score for each defeated enemy

    # Draw everything
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    # Display player health, lives, and score
    font = pygame.font.Font(None, 36)
    health_text = font.render(f"Health: {player.health}", True, WHITE)
    lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
    score_text = font.render(f"Score: {player.score}", True, WHITE)
    screen.blit(health_text, (10, 10))
    screen.blit(lives_text, (10, 50))
    screen.blit(score_text, (10, 90))

    # Check for game over
    if player.lives <= 0:
        # Display game over screen
        game_over_text = font.render("Game Over - Press R to Restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2))
        pygame.display.flip()

        # Wait for player to restart or quit
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_input = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Restart the game
                        player.health = 100
                        player.lives = 3
                        player.score = 0
                        all_sprites.empty()
                        enemies.empty()
                        projectiles.empty()
                        collectibles.empty()
                        player.rect.center = (100, HEIGHT - 50)
                        all_sprites.add(player)
                        waiting_for_input = False

        pygame.display.flip()

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()