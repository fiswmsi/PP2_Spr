import pygame
import os

pygame.init()
pygame.mixer.init()

MUSIC_FOLDER = '/Users/sarsenbaisarbinaz/Desktop/pp2/githowto/repositories/w3school/lab 7 /music'  
music_files = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith(('.mp3'))]
current_track = 0

screen = pygame.display.set_mode((1000, 400))
pygame.display.set_caption("Music Player")
font = pygame.font.Font(None, 36)

def draw_text(text, x, y):
    render = font.render(text, True, (255, 255, 255))
    screen.blit(render, (x, y))

def play_music(index):
    if music_files:
        pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, music_files[index]))
        pygame.mixer.music.play()
        print(f"Playing: {music_files[index]}")

if music_files:
    play_music(current_track)
else:
    print("No music files found in the folder.")
   
running = True
while running:
    screen.fill((0, 0, 0)) 
    draw_text("Music Player", 120, 20)
    
    if music_files:
        draw_text(f"Now Playing: {music_files[current_track]}", 250, 100)
    else:
        draw_text("No music files found", 50, 100)
    
    draw_text("SPACE: Play/Pause", 100, 150)
    draw_text("S: Stop", 100, 180)
    draw_text("N: Next", 100, 210)
    draw_text("P: Previous", 100, 240)
    draw_text("ESC: Exit", 100, 270)
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: 
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                    print("Paused")
                else:
                    pygame.mixer.music.unpause()
                    print("Resumed")
            elif event.key == pygame.K_s:  
                pygame.mixer.music.stop()
                print("Stopped")
            elif event.key == pygame.K_n:  
                current_track = (current_track + 1) % len(music_files)
                play_music(current_track)
            elif event.key == pygame.K_p: 
                current_track = (current_track - 1) % len(music_files)
                play_music(current_track)
            elif event.key == pygame.K_ESCAPE:  
                running = False

pygame.quit()