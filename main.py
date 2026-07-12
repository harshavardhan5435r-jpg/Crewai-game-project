```python
import pygame
import sys
import random

# --- Initialization ---
pygame.init()

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 50
PLAYER_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 150, 0)  # Darker green for ground
RED = (200, 0, 0)    # Darker red for obstacles
YELLOW = (255, 255, 0) # For power-up and invincibility flash
LIGHT_BLUE = (173, 216, 230) # Sky color

# Game Physics
GRAVITY = 0.8
JUMP_STRENGTH = -14

# Game Speed
GAME_SPEED_START = 5
GAME_SPEED_INCREMENT_INTERVAL = 5000 # Increase speed every 5 seconds (milliseconds)
GAME_SPEED_INCREMENT_AMOUNT = 0.5
MAX_GAME_SPEED = 15

# Obstacle Generation
OBSTACLE_WIDTH_MIN = 20
OBSTACLE_WIDTH_MAX = 70
OBSTACLE_HEIGHT_MIN = 30
OBSTACLE_HEIGHT_MAX = 100
# Minimum/Maximum time (in frames, effectively) between obstacle spawns, adjusted by speed
OBSTACLE_GAP_MIN = 200 
OBSTACLE_GAP_MAX = 400 

# Power-Up Generation
POWERUP_SIZE = 15
POWERUP_SPAWN_CHANCE = 0.3 # Chance to spawn a power-up when an obstacle is spawned
POWERUP_SCORE_BONUS = 50
INVINCIBILITY_DURATION_FRAMES = 180 # 3 seconds at 60 FPS

# Scoring
DISTANCE_SCORE_MULTIPLIER = 0.1 # Points per frame based on speed

# --- Setup Screen ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pixel Leap")

# --- Fonts ---
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)
restart_font = pygame.font.Font(None, 48)

# --- Classes ---
class Player(pygame.sprite.Sprite):
    """
    Represents the player character (The Leaper).
    Handles movement, gravity, jumping, and invincibility.
    """
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(BLUE) # Initial color for the player square
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 4, SCREEN_HEIGHT - GROUND_HEIGHT))
        self.y_velocity = 0
        self.on_ground = True
        self.invincible_timer = 0 # Frames of invincibility remaining

    def apply_gravity(self):
        """Applies gravity to the player and handles ground collision."""
        self.y_velocity += GRAVITY
        self.rect.y += self.y_velocity
        if self.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
            self.on_ground = True
            self.y_velocity = 0

    def jump(self):
        """Initiates a jump if the player is on the ground."""
        if self.on_ground:
            self.y_velocity = JUMP_STRENGTH
            self.on_ground = False

    def update(self):
        """Updates player's state, including gravity and invincibility timer."""
        self.apply_gravity()
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        
        # Simple flashing animation for invincibility
        if self.invincible_timer > 0 and (pygame.time.get_ticks() // 100) % 2 == 0:
            self.image.fill(YELLOW) # Flash yellow when invincible
        else:
            self.image.fill(BLUE) # Revert to normal blue color when not flashing or invincible

    def draw(self, surface):
        """Draws the player on the given surface."""
        surface.blit(self.image, self.rect)

class Obstacle(pygame.sprite.Sprite):
    """
    Represents an obstacle that the player must jump over.
    Scrolls from right to left.
    """
    def __init__(self, x_pos, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(bottomleft=(x_pos, SCREEN_HEIGHT - GROUND_HEIGHT))

    def update(self, speed):
        """Moves the obstacle to the left based on game speed."""
        self.rect.x -= speed

    def draw(self, surface):
        """Draws the obstacle on the given surface."""
        surface.blit(self.image, self.rect)

class PowerUp(pygame.sprite.Sprite):
    """
    Represents a collectible power-up (Sparkle Coin).
    Grants points and temporary invincibility.
    """
    def __init__(self, x_pos, y_pos, size, color):
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA) # SRCALPHA for potential transparency/anti-aliasing
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2) # Draw a circle (coin)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    def update(self, speed):
        """Moves the power-up to the left based on game speed."""
        self.rect.x -= speed

    def draw(self, surface):
        """Draws the power-up on the given surface."""
        surface.blit(self.image, self.rect)

# --- Game Variables (will be reset for each game) ---
player = Player()
clock = pygame.time.Clock()

game_active = False
score = 0
current_game_speed = GAME_SPEED_START

obstacles = []
powerups = []

last_obstacle_spawn_time = 0
last_speed_increase_time = 0
ground_x_offset = 0 # For continuous ground scrolling

# --- Game Functions ---
def reset_game():
    """Resets all game variables to their initial state for a new game."""
    global game_active, score, current_game_speed, obstacles, powerups, \
           last_obstacle_spawn_time, last_speed_increase_time, ground_x_offset

    # Reset player state
    player.rect.midbottom = (SCREEN_WIDTH // 4, SCREEN_HEIGHT - GROUND_HEIGHT)
    player.y_velocity = 0
    player.on_ground = True
    player.invincible_timer = 0

    # Clear game elements
    obstacles.clear()
    powerups.clear()

    # Reset game stats
    score = 0
    current_game_speed = GAME_SPEED_START
    
    # Reset timers relative to the current time to avoid immediate spawns/speed up
    now = pygame.time.get_ticks()
    last_obstacle_spawn_time = now
    last_speed_increase_time = now
    
    ground_x_offset = 0

    game_active = True

# --- Main Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if game_active:
                    player.jump()
                else: # Game is not active, so start/restart
                    reset_game()

    if game_active:
        # --- Update Game State ---
        player.update()

        # Update obstacles and remove off-screen ones
        for obstacle in obstacles[:]: # Iterate over a slice to allow modification during iteration
            obstacle.update(current_game_speed)
            if obstacle.rect.right < 0:
                obstacles.remove(obstacle)

        # Update power-ups and remove off-screen ones
        for powerup in powerups[:]:
            powerup.update(current_game_speed)
            if powerup.rect.right < 0:
                powerups.remove(powerup)

        # Obstacle and Power-up Generation
        now = pygame.time.get_ticks()
        # Spawn new obstacle if enough time has passed, adjusted by current speed
        # The divisor makes the effective time gap between obstacles shorter as speed increases
        if now - last_obstacle_spawn_time > random.randint(OBSTACLE_GAP_MIN, OBSTACLE_GAP_MAX) / (current_game_speed / GAME_SPEED_START):
            obstacle_width = random.randint(OBSTACLE_WIDTH_MIN, OBSTACLE_WIDTH_MAX)
            obstacle_height = random.randint(OBSTACLE_HEIGHT_MIN, OBSTACLE_HEIGHT_MAX)
            obstacles.append(Obstacle(SCREEN_WIDTH, obstacle_width, obstacle_height, RED))
            last_obstacle_spawn_time = now

            # Randomly spawn a power-up near the obstacle
            if random.random() < POWERUP_SPAWN_CHANCE:
                # Spawn power-up at a jumpable height, randomly above the obstacle or mid-air
                # The y-position ensures the power-up is always reachable with a jump
                powerup_y_pos = SCREEN_HEIGHT - GROUND_HEIGHT - random.randint(PLAYER_SIZE + 10, PLAYER_SIZE * 3)
                # Position the power-up slightly after the new obstacle to allow player to jump over obstacle first
                powerups.append(PowerUp(SCREEN_WIDTH + random.randint(50, 150), powerup_y_pos, POWERUP_SIZE, YELLOW))

        # Game Speed Increase
        if now - last_speed_increase_time > GAME_SPEED_INCREMENT_INTERVAL:
            if current_game_speed < MAX_GAME_SPEED:
                current_game_speed += GAME_SPEED_INCREMENT_AMOUNT
                last_speed_increase_time = now

        # Collision Detection
        # Player vs Obstacles
        for obstacle in obstacles[:]:
            if player.rect.colliderect(obstacle.rect):
                if player.invincible_timer > 0:
                    obstacles.remove(obstacle) # Invincibility absorbs one hit
                    player.invincible_timer = 0 # Invincibility ends after absorbing a hit
                else:
                    game_active = False # Game Over
                    break # Exit loop as game is over

        # Player vs Power-ups
        for powerup in powerups[:]:
            if player.rect.colliderect(powerup.rect):
                powerups.remove(powerup)
                score += POWERUP_SCORE_BONUS
                player.invincible_timer = INVINCIBILITY_DURATION_FRAMES # Grant invincibility

        # Score Update (based on distance/time and speed)
        score += current_game_speed * DISTANCE_SCORE_MULTIPLIER

        # Update ground offset for continuous scrolling
        ground_x_offset = (ground_x_offset + int(current_game_speed)) % SCREEN_WIDTH

        # --- Drawing ---
        screen.fill(LIGHT_BLUE) # Sky background

        # Draw ground (two rectangles for continuous scroll effect)
        pygame.draw.rect(screen, GREEN, (-ground_x_offset, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
        pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH - ground_x_offset, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

        # Draw all active obstacles and power-ups
        for obstacle in obstacles:
            obstacle.draw(screen)
        for powerup in powerups:
            powerup.draw(screen)
        player.draw(screen) # Draw player last to be on top

        # Display current score
        score_text = font.render(f"Score: {int(score)}", True, BLACK)
        screen.blit(score_text, (10, 10))

    else: # Game Over Screen / Start Screen
        screen.fill(LIGHT_BLUE)

        # Game title / Game Over message
        game_over_text = game_over_font.render("PIXEL LEAP", True, BLACK)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(game_over_text, game_over_rect)

        # Display final score if a game was played
        if score > 0: 
            final_score_text = font.render(f"Final Score: {int(score)}", True, BLACK)
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(final_score_text, final_score_rect)

        # Instructions to start/restart
        restart_text = restart_font.render("Press SPACE or UP Arrow to Start/Restart", True, BLACK)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(restart_text, restart_rect)
        
        # Draw static ground on the start/game over screen
        pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))


    pygame.display.flip() # Update the full display Surface to the screen
    clock.tick(60) # Control the frame rate to 60 FPS

# --- Quit Pygame ---
pygame.quit()
sys.exit()
```

**Instructions on how to play the game:**

1.  **Save the code**: Save the provided code as a Python file (e.g., `pixel_leap.py`).
2.  **Run the game**: Open a terminal or command prompt, navigate to the directory where you saved the file, and run it using:
    ```bash
    python pixel_leap.py
    ```
3.  **Start the game**: Press the `SPACEBAR` or `UP Arrow` key to begin.
4.  **Control the player**: Your character (a blue square) will automatically run from left to right.
5.  **Jump**: Press the `SPACEBAR` or `UP Arrow` key to make your character jump over obstacles.
6.  **Collect Power-Ups**: Collect the yellow "Sparkle Coin" (yellow circle) for bonus points and temporary invincibility. If invincible, you can hit one obstacle without the game ending, but your invincibility will then wear off.
7.  **Avoid Obstacles**: Do not collide with the red blocky obstacles unless you are currently invincible. Hitting an obstacle while not invincible will end the game.
8.  **Score**: Your score increases based on how long you survive and by collecting power-ups. The game speed will gradually increase, making it more challenging.
9.  **Restart**: After the game ends, your final score will be displayed. Press `SPACEBAR` or `UP Arrow` again to restart the game.