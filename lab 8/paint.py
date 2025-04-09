import pygame
from pygame.locals import *

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [BLACK, RED, GREEN, BLUE]
COLOR_NAMES = ["Black", "Red", "Green", "Blue"]
TOOLBAR_WIDTH = 120  # Width of the toolbar
OFFSET_Y = 50  # Offset to account for the toolbar height

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drawing App")

# Variables
current_tool = "pen"
current_color = BLACK
drawing = False
start_pos = None
canvas = pygame.Surface((WIDTH - TOOLBAR_WIDTH, HEIGHT))
canvas.fill(WHITE)

# Toolbar setup (vertical toolbar on the right)
tool_buttons = {
    "pen": pygame.Rect(WIDTH - 110, 10, 80, 30),
    "rectangle": pygame.Rect(WIDTH - 110, 50, 100, 30),
    "circle": pygame.Rect(WIDTH - 110, 90, 80, 30),
    "eraser": pygame.Rect(WIDTH - 110, 130, 80, 30)
}
color_buttons = {COLORS[i]: pygame.Rect(WIDTH - 90, 170 + i * 40, 40, 30) for i in range(len(COLORS))}

# Font
font = pygame.font.Font(None, 24)

# Function to draw the toolbar
def draw_toolbar():
    # Draw the background of the toolbar
    pygame.draw.rect(screen, (200, 200, 200), (WIDTH - TOOLBAR_WIDTH, 0, TOOLBAR_WIDTH, HEIGHT))
    
    # Draw buttons for each tool (pen, rectangle, circle, eraser)
    for tool, rect in tool_buttons.items():
        pygame.draw.rect(screen, (150, 150, 150), rect)
        text = font.render(tool.capitalize(), True, BLACK)
        screen.blit(text, (rect.x + 10, rect.y + 5))
    
    # Draw color buttons
    for color, rect in color_buttons.items():
        pygame.draw.rect(screen, color, rect)

# Main loop
running = True
while running:
    # Fill the screen with white background
    screen.fill(WHITE)
    
    # Draw the toolbar
    draw_toolbar()
    
    # Display the canvas
    screen.blit(canvas, (0, OFFSET_Y))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if event.pos[0] > WIDTH - TOOLBAR_WIDTH:  # Clicked on toolbar
                    for tool, rect in tool_buttons.items():
                        if rect.collidepoint(event.pos):
                            current_tool = tool
                            drawing = False  # Stop any drawing when tool changes
                    for color, rect in color_buttons.items():
                        if rect.collidepoint(event.pos):
                            current_color = color
                            drawing = False  # Stop drawing when color changes
                else:
                    # Adjust position to account for the toolbar offset
                    start_pos = event.pos[0], event.pos[1] - OFFSET_Y
                    drawing = True
        
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:  # Left click release
                drawing = False
                end_pos = event.pos[0], event.pos[1] - OFFSET_Y
                
                # Draw rectangle if the current tool is rectangle
                if current_tool == "rectangle":
                    pygame.draw.rect(canvas, current_color, (*start_pos, end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]), 2)
                
                # Draw circle if the current tool is circle
                elif current_tool == "circle":
                    radius = int(((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2) ** 0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)
        
        elif event.type == MOUSEMOTION:
            if drawing and current_tool == "pen":
                # Draw line if the current tool is pen
                pygame.draw.line(canvas, current_color, start_pos, (event.pos[0], event.pos[1] - OFFSET_Y), 2)
                start_pos = event.pos[0], event.pos[1] - OFFSET_Y
            
            elif drawing and current_tool == "eraser":
                # Erase with a circle if the current tool is eraser
                pygame.draw.circle(canvas, WHITE, (event.pos[0], event.pos[1] - OFFSET_Y), 10)
    
    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()