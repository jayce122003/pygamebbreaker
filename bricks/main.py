import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)  # Color used for bonus ball

# Paddle settings
PADDLE_WIDTH = 150
PADDLE_HEIGHT = 10
paddle_x = (WIDTH - PADDLE_WIDTH) // 2
paddle_y = HEIGHT - 50
paddle_speed = 15

# Ball settings
BALL_RADIUS = 8

# Brick settings
BRICK_ROWS = 7  # Starting rows; increases each level
BRICK_COLS = 8
BRICK_WIDTH = WIDTH // BRICK_COLS - 5
BRICK_HEIGHT = 20
BRICK_TOP_MARGIN = 50  # Add margin at the top for the text
bricks = []
brick_colors = [
    (255, 0, 0),    # Red
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (75, 0, 130),   # Indigo
    (238, 130, 238) # Violet
]

def create_bricks(rows):
    new_bricks = []
    for row in range(rows):
        for col in range(BRICK_COLS):
            brick = pygame.Rect(col * (BRICK_WIDTH + 5) + 5,
                                row * (BRICK_HEIGHT + 5) + BRICK_TOP_MARGIN,
                                BRICK_WIDTH,
                                BRICK_HEIGHT)
            new_bricks.append((brick, brick_colors[row % len(brick_colors)]))
    return new_bricks

bricks = create_bricks(BRICK_ROWS)

# Add a function for the welcome screen
def show_welcome_screen():
    # Load and display the background image
    bg_image = pygame.image.load("brick.jpg")
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    screen.blit(bg_image, (0, 0))
    
    # Create and blit a semi-transparent black overlay to darken the background
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(100)  # Adjust alpha as needed (0-255)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
   
    # Load fonts (ensure Monogram.ttf is in the same directory)
    font_title = pygame.font.Font("Monogram.ttf", 74)
    font_subtext = pygame.font.Font("Monogram.ttf", 36)
    # Increase button font size to make the buttons larger
    font_buttons = pygame.font.Font("Monogram.ttf", 40)

    # Title text (bold effect by rendering multiple times with slight offsets)
    text = font_title.render("Brick Breaker", True, WHITE)
    for offset in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        screen.blit(font_title.render("Brick Breaker", True, WHITE),
                    (WIDTH // 2 - text.get_width() // 2 + offset[0],
                     HEIGHT // 2 - 200 + offset[1]))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 200))

    # Subtext
    subtext = font_subtext.render("Select Difficulty", True, WHITE)
    screen.blit(subtext, (WIDTH // 2 - subtext.get_width() // 2, HEIGHT // 2 - 100))

    # Prepare button texts (default strings)
    base_easy = "Easy"
    base_medium = "Medium"
    base_hard = "Hard"
    
    # Render static buttons once to get their positions
    temp_easy = font_buttons.render(base_easy, True, WHITE)
    temp_medium = font_buttons.render(base_medium, True, WHITE)
    temp_hard = font_buttons.render(base_hard, True, WHITE)
    easy_rect = temp_easy.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    medium_rect = temp_medium.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    hard_rect = temp_hard.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    
    pygame.display.flip()  # Show the initial screen
    
    waiting = True
    clock = pygame.time.Clock()
    while waiting:
        # Redraw the background and overlay every frame
        screen.blit(bg_image, (0, 0))
        screen.blit(overlay, (0, 0))
        # Redraw title and subtext
        for offset in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            screen.blit(font_title.render("Brick Breaker", True, WHITE),
                        (WIDTH // 2 - text.get_width() // 2 + offset[0],
                         HEIGHT // 2 - 200 + offset[1]))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 200))
        screen.blit(subtext, (WIDTH // 2 - subtext.get_width() // 2, HEIGHT // 2 - 100))
        
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        # For the transparent (fading) effect, calculate the alpha based on a sine wave
        # This will oscillate between 128 and 255 when hovered.
        time_factor = pygame.time.get_ticks() * 0.005  # Adjust speed of oscillation here
        
        # Easy button
        if easy_rect.collidepoint(mouse_pos):
            alpha = 128 + 127 * (math.sin(time_factor) + 1) / 2  # Range 128 to 255
            easy_button = font_buttons.render(base_easy, True, WHITE).convert_alpha()
            easy_button.set_alpha(int(alpha))
        else:
            easy_button = font_buttons.render(base_easy, True, WHITE)
        
        # Medium button
        if medium_rect.collidepoint(mouse_pos):
            alpha = 128 + 127 * (math.sin(time_factor) + 1) / 2
            medium_button = font_buttons.render(base_medium, True, WHITE).convert_alpha()
            medium_button.set_alpha(int(alpha))
        else:
            medium_button = font_buttons.render(base_medium, True, WHITE)
            
        # Hard button
        if hard_rect.collidepoint(mouse_pos):
            alpha = 128 + 127 * (math.sin(time_factor) + 1) / 2
            hard_button = font_buttons.render(base_hard, True, WHITE).convert_alpha()
            hard_button.set_alpha(int(alpha))
        else:
            hard_button = font_buttons.render(base_hard, True, WHITE)
        
        # Blit buttons at their respective positions
        screen.blit(easy_button, easy_rect)
        screen.blit(medium_button, medium_rect)
        screen.blit(hard_button, hard_rect)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos):
                    return "easy"
                elif medium_rect.collidepoint(event.pos):
                    return "medium"
                elif hard_rect.collidepoint(event.pos):
                    return "hard"
        clock.tick(60)

# Function for the "Next Level" screen with a button
def show_next_level_screen():
    font_button = pygame.font.Font("Monogram.ttf", 36)
    button_text = font_button.render("Next Level", True, BLACK)
    button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    button_bg = pygame.Rect(button_rect.x - 10, button_rect.y - 10,
                            button_rect.width + 20, button_rect.height + 20)
    waiting = True
    while waiting:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        pygame.draw.rect(screen, WHITE, button_bg, border_radius=5)
        screen.blit(button_text, button_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_bg.collidepoint(event.pos):
                    waiting = False

# Function to display a Game Over screen
def show_game_over_screen():
    font_game_over = pygame.font.Font("Monogram.ttf", 74)
    font_score = pygame.font.Font("Monogram.ttf", 36)
    game_over_text = font_game_over.render("GAME OVER", True, RED)
    score_text = font_score.render(f"Final Score: {score}", True, WHITE)
    screen.fill(BLACK)
    # Position the texts centered and one below the other
    go_x = WIDTH // 2 - game_over_text.get_width() // 2
    go_y = HEIGHT // 2 - game_over_text.get_height() // 2 - 40
    sc_x = WIDTH // 2 - score_text.get_width() // 2
    sc_y = HEIGHT // 2 - score_text.get_height() // 2 + 40
    screen.blit(game_over_text, (go_x, go_y))
    screen.blit(score_text, (sc_x, sc_y))
    pygame.display.flip()
    pygame.time.delay(3000)

# Call the welcome screen and set difficulty
difficulty = show_welcome_screen()

if difficulty == "easy":
    initial_dx = random.choice([-4, 4])
    initial_dy = -4
elif difficulty == "medium":
    initial_dx = random.choice([-5, 5])
    initial_dy = -5
elif difficulty == "hard":
    initial_dx = random.choice([-7, 7])
    initial_dy = -7

# Initialize level and score
level = 1
score = 0

# Load font for level and score display
font_hud = pygame.font.Font("Monogram.ttf", 36)  # Ensure Monogram.ttf is in the same directory

# Use lists to support multiple balls:
# normal_balls are active balls in play; bonus_balls are falling rewards
normal_balls = [{
    'x': WIDTH // 2,
    'y': HEIGHT // 2,
    'dx': initial_dx,
    'dy': initial_dy
}]
bonus_balls = []

# Add before the game loop (after other settings)
TOP_WALL_HEIGHT = 40

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 5:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
        paddle_x += paddle_speed

    # Update normal balls
    balls_to_remove = []
    for ball in normal_balls:
        ball['x'] += ball['dx']
        ball['y'] += ball['dy']

        if ball['x'] - BALL_RADIUS <= 0 or ball['x'] + BALL_RADIUS >= WIDTH:
            ball['dx'] *= -1
        # Bounce off the top wall instead of y=0
        if ball['y'] - BALL_RADIUS <= TOP_WALL_HEIGHT:
            ball['dy'] *= -1

        paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        # Only bounce if the ball is moving downward
        if paddle_rect.collidepoint(ball['x'], ball['y'] + BALL_RADIUS) and ball['dy'] > 0:
            ball['dy'] *= -1
            ball['y'] = paddle_y - BALL_RADIUS  # Move ball just above the paddle

        # Ball collision with bricks
        for i, (brick, color) in enumerate(bricks[:]):
            if brick.collidepoint(ball['x'], ball['y'] - BALL_RADIUS) or \
               brick.collidepoint(ball['x'], ball['y'] + BALL_RADIUS):
                ball['dy'] *= -1
                bricks.pop(i)
                score += 10

                # 20% chance to spawn a bonus ball at the brick position
                if random.random() < 0.2:
                    bonus_balls.append({
                        'x': brick.centerx,
                        'y': brick.centery,
                        'dy': 3  # Falling speed for bonus ball
                    })
                break

        if ball['y'] - BALL_RADIUS > HEIGHT:
            balls_to_remove.append(ball)

    for ball in balls_to_remove:
        normal_balls.remove(ball)

    # Update bonus balls
    bonus_to_remove = []
    for bonus in bonus_balls:
        bonus['y'] += bonus['dy']
        paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        bonus_rect = pygame.Rect(bonus['x'] - BALL_RADIUS, bonus['y'] - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)
        if paddle_rect.colliderect(bonus_rect):
            normal_balls.append({
                'x': bonus['x'],
                'y': bonus['y'],
                'dx': initial_dx,
                'dy': initial_dy
            })
            bonus_to_remove.append(bonus)
        elif bonus['y'] - BALL_RADIUS > HEIGHT:
            bonus_to_remove.append(bonus)

    for bonus in bonus_to_remove:
        bonus_balls.remove(bonus)

    # When all bricks are broken, show the "Next Level" button and reset the game state
    if not bricks:
        show_next_level_screen()
        level += 1
        BRICK_ROWS += 1

        # Calculate a new speed factor (increases 20% per level above 1)
        speed_factor = 1 + (level - 1) * 0.2

        # Reset ball to the center with increased speed based on the level
        normal_balls = [{
            'x': WIDTH // 2,
            'y': HEIGHT // 2,
            'dx': initial_dx * speed_factor,
            'dy': initial_dy * speed_factor
        }]
        # Reset paddle position
        paddle_x = (WIDTH - PADDLE_WIDTH) // 2
        # Create more bricks with an additional row
        bricks = create_bricks(BRICK_ROWS)

    # Check game over: if there are no normal balls in play, show GAME OVER screen
    if not normal_balls:
        show_game_over_screen()
        running = False

    # Draw paddle
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT), border_radius=5)

    # Draw normal balls
    for ball in normal_balls:
        pygame.draw.circle(screen, WHITE, (int(ball['x']), int(ball['y'])), BALL_RADIUS)

    # Draw bonus balls
    for bonus in bonus_balls:
        pygame.draw.circle(screen, YELLOW, (int(bonus['x']), int(bonus['y'])), BALL_RADIUS)

    # Draw bricks
    for brick, color in bricks:
        pygame.draw.rect(screen, color, brick, border_radius=5)

    # Draw top wall
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, TOP_WALL_HEIGHT))

    # Render level and score
    level_text = font_hud.render(f"Level: {level}", True, WHITE)
    score_text = font_hud.render(f"Score: {score}", True, WHITE)
    screen.blit(level_text, (10, 10))
    screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()


