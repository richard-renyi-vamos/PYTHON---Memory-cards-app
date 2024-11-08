import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 400, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Memory Matrix")

# Colors
white, black, green, light_blue = (255, 255, 255), (0, 0, 0), (0, 255, 0), (173, 216, 230)

# Font settings
font = pygame.font.Font(None, 36)

# Variables for settings
grid_size_options = [3, 4, 5]
difficulty_options = [1, 2, 3]
display_time_options = [1000, 1500, 2000]

# Default settings
grid_size = 4
difficulty = 1
display_time = 1500
score, level = 0, 1

def draw_text(text, y_offset=0):
    """Draws centered text on the screen"""
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + y_offset))
    screen.blit(text_surface, text_rect)

def draw_button(text, x, y, w, h, color, action=None):
    """Draws a button and handles clicks"""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    pygame.draw.rect(screen, color, (x, y, w, h))
    
    text_surf = font.render(text, True, black)
    text_rect = text_surf.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surf, text_rect)

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        if click[0] == 1 and action:
            action()

def show_settings():
    """Display settings menu for customization"""
    global grid_size, difficulty, display_time
    selecting = True
    while selecting:
        screen.fill(white)
        draw_text("Settings", -150)

        draw_button(f"Grid Size: {grid_size}", 100, 120, 200, 40, light_blue, change_grid_size)
        draw_button(f"Difficulty: {difficulty}", 100, 180, 200, 40, light_blue, change_difficulty)
        draw_button(f"Display Time: {display_time}ms", 100, 240, 200, 40, light_blue, change_display_time)
        draw_button("Start Game", 100, 300, 200, 40, green, start_game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                selecting = False
                pygame.quit()
                quit()
        
        pygame.display.flip()

def change_grid_size():
    """Cycle through grid size options"""
    global grid_size
    grid_size = grid_size_options[(grid_size_options.index(grid_size) + 1) % len(grid_size_options)]

def change_difficulty():
    """Cycle through difficulty options"""
    global difficulty
    difficulty = difficulty_options[(difficulty_options.index(difficulty) + 1) % len(difficulty_options)]

def change_display_time():
    """Cycle through display time options"""
    global display_time
    display_time = display_time_options[(display_time_options.index(display_time) + 1) % len(display_time_options)]

def generate_pattern(level):
    """Generate pattern for each level based on difficulty"""
    return [(random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)) for _ in range(level + difficulty)]

def draw_grid(pattern, clicked_cells=[]):
    """Draws the game grid and highlights cells in the pattern"""
    cell_size = screen_width // grid_size
    screen.fill(white)
    for row in range(grid_size):
        for col in range(grid_size):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, black, rect, 1)
            if (row, col) in pattern or (row, col) in clicked_cells:
                pygame.draw.rect(screen, green, rect)

def start_game():
    """Main game loop"""
    global score, level
    score, level = 0, 1
    pattern = generate_pattern(level)
    showing_pattern = True
    clicked_cells = []

    running = True
    while running:
        screen.fill(white)
        draw_grid(pattern if showing_pattern else clicked_cells)
        
        if showing_pattern:
            draw_text(f"Level {level} - Memorize!", -50)
            pygame.display.flip()
            pygame.time.delay(display_time)
            showing_pattern = False
        else:
            draw_text(f"Score: {score}", -50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not showing_pattern:
                x, y = pygame.mouse.get_pos()
                col, row = x // (screen_width // grid_size), y // (screen_height // grid_size)
                if (row, col) not in clicked_cells:
                    clicked_cells.append((row, col))

                if len(clicked_cells) == len(pattern):
                    if clicked_cells == pattern:
                        score += 1
                        level += 1
                        clicked_cells = []
                        pattern = generate_pattern(level)
                        showing_pattern = True
                    else:
                        draw_text("Game Over!", 50)
                        pygame.display.flip()
                        pygame.time.delay(2000)
                        running = False

        pygame.display.flip()

# Display settings first
show_settings()
pygame.quit()
