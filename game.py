import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 800
PLAY_AREA = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FLOWER_COLORS = [
    (255, 255, 0),   # Yellow
    (0, 255, 0),     # Green
    (0, 0, 255),     # Blue
    (255, 0, 255),   # Magenta
    (0, 255, 255),   # Cyan
    (255, 165, 0),   # Orange
    (255, 100, 100), # Light Red
    (100, 100, 255), # Light Blue
    (200, 200, 100), # Light Yellow
    (150, 255, 150)  # Light Green
]

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Butterfly Garden")

# Function to initialize game
def init_game(level=1):
    # Butterfly properties
    butterfly_x = SCREEN_WIDTH // 2
    butterfly_y = SCREEN_HEIGHT // 2
    
    # Number of flowers based on level
    num_flowers = min(6 + (level - 1) * 2, len(FLOWER_COLORS))
    
    # Create flowers at random positions
    flowers = []
    for i in range(num_flowers):
        valid_position = False
        while not valid_position:
            x = random.randint(30, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            
            # Check if position is far enough from other flowers and player start position
            valid_position = True
            for flower in flowers:
                if ((x - flower.x) ** 2 + (y - flower.y) ** 2) ** 0.5 < 70:
                    valid_position = False
                    break
            
            # Check distance from player start position
            if ((x - SCREEN_WIDTH // 2) ** 2 + (y - SCREEN_HEIGHT // 2) ** 2) ** 0.5 < 100:
                valid_position = False
        
        flowers.append(Flower(x, y, FLOWER_COLORS[i % len(FLOWER_COLORS)], level))
    
    # Adjust time based on level (more time for higher levels with more flowers)
    time_limit = 60 + (level - 1) * 10
    
    return butterfly_x, butterfly_y, flowers, 0, time_limit, False, level

# Butterfly properties
butterfly_size = 30
butterfly_speed = 5

# Flower properties
class Flower:
    def __init__(self, x, y, color, level=1):
        self.x = x
        self.y = y
        self.color = color
        self.captured = False
        self.move_angle = random.uniform(0, 2 * math.pi)
        self.move_speed = random.uniform(0.5, 1.5) * (1 + (level - 1) * 0.2)  # Faster movement at higher levels
        self.move_range = random.randint(20, 40)
        self.original_x = x
        self.original_y = y
        self.time_offset = random.uniform(0, 2 * math.pi)
    
    def update(self):
        if not self.captured:
            # Create a gentle swaying motion
            time_factor = pygame.time.get_ticks() / 1000 + self.time_offset
            self.x = self.original_x + math.sin(time_factor * self.move_speed) * self.move_range / 2
            self.y = self.original_y + math.cos(time_factor * 0.7 * self.move_speed) * self.move_range / 3
    
    def draw(self):
        if not self.captured:
            # Draw stem
            pygame.draw.rect(screen, (0, 100, 0), (self.x, self.y, 3, 30))
            
            # Draw flower petals
            petal_radius = 10
            pygame.draw.circle(screen, self.color, (int(self.x + 1), int(self.y - 5)), petal_radius)
            pygame.draw.circle(screen, self.color, (int(self.x + 10), int(self.y - 10)), petal_radius)
            pygame.draw.circle(screen, self.color, (int(self.x - 8), int(self.y - 10)), petal_radius)
            pygame.draw.circle(screen, self.color, (int(self.x + 5), int(self.y - 18)), petal_radius)
            pygame.draw.circle(screen, self.color, (int(self.x - 3), int(self.y - 18)), petal_radius)
            
            # Draw flower center
            pygame.draw.circle(screen, (255, 255, 100), (int(self.x + 1), int(self.y - 12)), 7)
    
    def check_capture(self, player_x, player_y, size):
        if not self.captured:
            # Check if butterfly overlaps with flower
            distance = ((player_x - self.x) ** 2 + (player_y - self.y + 12) ** 2) ** 0.5
            if distance < size + 15:
                self.captured = True
                return True
        return False

# Function to draw butterfly
def draw_butterfly(x, y, size):
    # Body
    pygame.draw.ellipse(screen, (70, 30, 10), (x - size//4, y - size//2, size//2, size))
    
    # Wings
    wing_color = (200, 100, 255)
    
    # Left wings
    pygame.draw.ellipse(screen, wing_color, (x - size, y - size//2, size, size//1.5))
    pygame.draw.ellipse(screen, wing_color, (x - size, y, size, size//1.5))
    
    # Right wings
    pygame.draw.ellipse(screen, wing_color, (x, y - size//2, size, size//1.5))
    pygame.draw.ellipse(screen, wing_color, (x, y, size, size//1.5))
    
    # Wing patterns
    pattern_color = (150, 50, 200)
    pygame.draw.arc(screen, pattern_color, (x - size, y - size//2, size, size//1.5), 0, math.pi, 2)
    pygame.draw.arc(screen, pattern_color, (x, y - size//2, size, size//1.5), 0, math.pi, 2)
    pygame.draw.arc(screen, pattern_color, (x - size, y, size, size//1.5), math.pi, 2*math.pi, 2)
    pygame.draw.arc(screen, pattern_color, (x, y, size, size//1.5), math.pi, 2*math.pi, 2)
    
    # Antennae
    pygame.draw.line(screen, (0, 0, 0), (x - size//8, y - size//2), (x - size//4, y - size), 2)
    pygame.draw.line(screen, (0, 0, 0), (x + size//8, y - size//2), (x + size//4, y - size), 2)
    pygame.draw.circle(screen, (0, 0, 0), (x - size//4, y - size), 3)
    pygame.draw.circle(screen, (0, 0, 0), (x + size//4, y - size), 3)

# Initialize game variables
level = 1
butterfly_x, butterfly_y, flowers, score, time_left, game_over, level = init_game(level)
font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 72)

# Game loop
clock = pygame.time.Clock()
running = True
start_ticks = pygame.time.get_ticks()
level_complete = False
level_transition_time = 0

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                # Reset the game to level 1
                level = 1
                butterfly_x, butterfly_y, flowers, score, time_left, game_over, level = init_game(level)
                start_ticks = pygame.time.get_ticks()
            elif game_over and event.key == pygame.K_ESCAPE:
                running = False
            elif level_complete and event.key == pygame.K_SPACE:
                # Start next level
                level += 1
                butterfly_x, butterfly_y, flowers, score, time_left, game_over, level = init_game(level)
                start_ticks = pygame.time.get_ticks()
                level_complete = False
    
    # Update timer if game is not over and not in level transition
    if not game_over and not level_complete:
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        time_left = max(0, 60 + (level - 1) * 10 - seconds)
        
        # Check if time is up
        if time_left <= 0:
            game_over = True
    
    if not game_over and not level_complete:
        # Get keyboard input
        keys = pygame.key.get_pressed()
        
        # Move the butterfly based on arrow key presses
        if keys[pygame.K_LEFT] and butterfly_x - butterfly_size > 0:
            butterfly_x -= butterfly_speed
        if keys[pygame.K_RIGHT] and butterfly_x + butterfly_size < SCREEN_WIDTH:
            butterfly_x += butterfly_speed
        if keys[pygame.K_UP] and butterfly_y - butterfly_size > 0:
            butterfly_y -= butterfly_speed
        if keys[pygame.K_DOWN] and butterfly_y + butterfly_size < SCREEN_HEIGHT:
            butterfly_y += butterfly_speed
    
    # Fill the screen with black
    screen.fill(BLACK)
    
    # Update and draw flowers
    for flower in flowers:
        flower.update()
        flower.draw()
    
    # Draw the butterfly
    draw_butterfly(butterfly_x, butterfly_y, butterfly_size)
    
    # Check for flower captures
    for flower in flowers:
        if not game_over and not level_complete and flower.check_capture(butterfly_x, butterfly_y, butterfly_size):
            score += 50
    
    # Check if all flowers are captured
    if all(flower.captured for flower in flowers) and not game_over and not level_complete:
        level_complete = True
        level_transition_time = pygame.time.get_ticks()
    
    # Display score, timer and level
    score_text = font.render(f"Score: {score}", True, WHITE)
    timer_text = font.render(f"Time: {time_left}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (20, 20))
    screen.blit(timer_text, (SCREEN_WIDTH - 120, 20))
    screen.blit(level_text, (SCREEN_WIDTH // 2 - 50, 20))
    
    # Display level complete message
    if level_complete:
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, 200))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, SCREEN_HEIGHT // 2 - 100))
        
        # Level complete message
        level_complete_text = large_font.render(f"Level {level} Complete!", True, WHITE)
        next_level_text = font.render("Press SPACE for next level", True, WHITE)
        
        # Position and display text
        screen.blit(level_complete_text, (SCREEN_WIDTH // 2 - level_complete_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(next_level_text, (SCREEN_WIDTH // 2 - next_level_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
    
    # Display game over banner and final score
    if game_over:
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, 200))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, SCREEN_HEIGHT // 2 - 100))
        
        # Game over message
        if all(flower.captured for flower in flowers):
            game_over_text = large_font.render("All Flowers Collected!", True, WHITE)
        else:
            game_over_text = large_font.render("Time's Up!", True, WHITE)
        
        # Final score and instructions
        final_score_text = font.render(f"Final Score: {score} | Level: {level}", True, WHITE)
        restart_text = font.render("Press R to Restart or ESC to Exit", True, WHITE)
        
        # Position and display text
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 70))
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 10))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()