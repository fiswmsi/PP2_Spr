import pygame
from pygame.locals import *
import math

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
    "square": pygame.Rect(WIDTH - 110, 130, 80, 30),  # Added square tool
    "triangle": pygame.Rect(WIDTH - 110, 170, 80, 30),  # Added triangle tool
    "equilateral_triangle": pygame.Rect(WIDTH - 110, 210, 80, 30),  # Added equilateral triangle tool
    "rhombus": pygame.Rect(WIDTH - 110, 250, 80, 30),  # Added rhombus tool
    "eraser": pygame.Rect(WIDTH - 110, 290, 80, 30)
}
color_buttons = {COLORS[i]: pygame.Rect(WIDTH - 90, 330 + i * 40, 40, 30) for i in range(len(COLORS))}

# Font
font = pygame.font.Font(None, 24)

# Function to draw the toolbar
def draw_toolbar():
    # Draw the background of the toolbar
    pygame.draw.rect(screen, (200, 200, 200), (WIDTH - TOOLBAR_WIDTH, 0, TOOLBAR_WIDTH, HEIGHT))
    
    # Draw buttons for each tool (pen, rectangle, circle, square, triangle, equilateral triangle, rhombus, eraser)
    for tool, rect in tool_buttons.items():
        pygame.draw.rect(screen, (150, 150, 150), rect)
        text = font.render(tool.replace("_", " ").capitalize(), True, BLACK)
        screen.blit(text, (rect.x + 10, rect.y + 5))
    
    # Draw color buttons
    for color, rect in color_buttons.items():
        pygame.draw.rect(screen, color, rect)

# Function to calculate the vertices of the equilateral triangle
def get_equilateral_triangle_vertices(start, side_length):
    # The angle between the first and second vertex is 60 degrees (in radians)
    angle = math.pi / 3  # 60 degrees in radians
    
    # First vertex is start_pos
    x1, y1 = start
    
    # Second vertex is moving along the x-axis by side_length
    x2, y2 = x1 + side_length, y1
    
    # Third vertex is calculated using rotation (60 degrees from the horizontal line)
    x3 = x1 + side_length * math.cos(angle)
    y3 = y1 + side_length * math.sin(angle)
    
    return [(x1, y1), (x2, y2), (x3, y3)]

# Function to calculate the vertices of the rhombus
def get_rhombus_vertices(start, end):
    # Calculate the half diagonals
    half_width = abs(end[0] - start[0]) / 2
    half_height = abs(end[1] - start[1]) / 2

    # Calculate the center point of the rhombus (midpoint between start and end)
    center_x = (start[0] + end[0]) / 2
    center_y = (start[1] + end[1]) / 2

    # Calculate the four vertices of the rhombus
    top = (center_x, center_y - half_height)
    bottom = (center_x, center_y + half_height)
    left = (center_x - half_width, center_y)
    right = (center_x + half_width, center_y)

    return [top, left, bottom, right]

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
                            drawing = False # Stop any drawing when tool changes
                            current_tool = tool
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

                # Draw square if the current tool is square
                elif current_tool == "square":
                    side_length = max(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))  # Ensure it's a square
                    pygame.draw.rect(canvas, current_color, (*start_pos, side_length, side_length), 2)
                
                # Draw right triangle if the current tool is triangle
                elif current_tool == "triangle":
                    point1 = start_pos
                    point2 = (start_pos[0], end_pos[1])  # Vertical line from start to end_y
                    point3 = (end_pos[0], start_pos[1])  # Horizontal line from start to end_x
                    pygame.draw.polygon(canvas, current_color, [point1, point2, point3], 2)

                # Draw equilateral triangle if the current tool is equilateral_triangle
                elif current_tool == "equilateral_triangle":
                    side_length = math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])  # Calculate the side length
                    vertices = get_equilateral_triangle_vertices(start_pos, side_length)
                    pygame.draw.polygon(canvas, current_color, vertices, 2)
                
                # Draw rhombus if the current tool is rhombus
                elif current_tool == "rhombus":
                    vertices = get_rhombus_vertices(start_pos, end_pos)
                    pygame.draw.polygon(canvas, current_color, vertices, 2)
        
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