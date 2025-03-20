import pygame

pygame.init()

WIDTH, HEIGHT = 500, 500   
STEP = 20 

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move the Ball")

ball_x = WIDTH // 2
ball_y = HEIGHT // 2

running = True
while running:
    pygame.time.delay(50) 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ball_x - 25 - STEP >= 0:
        ball_x -= STEP
    if keys[pygame.K_RIGHT] and ball_x + 25 + STEP <= WIDTH:
        ball_x += STEP
    if keys[pygame.K_UP] and ball_y - 25 - STEP >= 0:
        ball_y -= STEP
    if keys[pygame.K_DOWN] and ball_y + 25 + STEP <= HEIGHT:
        ball_y += STEP
    
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0)  , (ball_x, ball_y), 25)
    pygame.display.update()
    
pygame.quit()
