

import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
done = False
is_blue = True

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    is_blue = not is_blue
                    
        if is_blue: 
            color = (0, 128, 255)
        else: 
            color = (255, 100, 0)
        
        pygame.draw.circle(screen, (255, 100, 0), (500, 500), 200, 50)

        pygame.draw.rect(screen, color, pygame.Rect(450, 500, 50, 50))
        
        pygame.draw.rect(screen, color, pygame.Rect(10, 10, 100, 100))
        
        pygame.display.flip()