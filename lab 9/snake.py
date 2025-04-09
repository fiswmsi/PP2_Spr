import pygame
import random
import time

pygame.init()

# game variables
width = 500
height = 400
screen = pygame.display.set_mode((width, height))  # создаем окно
pygame.display.set_caption("Snake Game with Levels")  # заголовок окна
clock = pygame.time.Clock()
done = False  
score = 0  # начальный счёт
level = 1  # начальный уровень

# head variable
coor_head = [100, 100]  # координаты головы змеи

# body variable
coor_body = [  # начальные координаты тела змеи
    [30, 100],
    [40, 100],
    [50, 100],
    [60, 100],
    [70, 100],
    [80, 100],
    [90, 100],
    [100, 100]
]

# apple
def generate_apple():
    while True:
        apple_x = random.randrange(0, width // 10) * 10  # координата X кратна 10
        apple_y = random.randrange(0, height // 10) * 10  # координата Y кратна 10
        new_apple = [apple_x, apple_y]
        if new_apple not in coor_body and new_apple != coor_head:
            weight = random.choice([10, 20, 30])  # выбираем вес еды
            color = {10: (0, 255, 0), 20: (255, 165, 0), 30: (255, 0, 0)}[weight]  # цвет зависит от веса
            timer = random.randint(10, 15)  # таймер от 5 до 10 сек
            return {"pos": new_apple, "weight": weight, "color": color, "spawn_time": time.time(), "timer": timer}


coor_apple = generate_apple()
eaten = False

# direction
next_dir = "r"  # следующая команда направления
direc = "r"  # текущее направление

def score_update(font, size, color, level):
    global score
    score_font = pygame.font.SysFont(font, size)
    score_render = score_font.render(f"Score: {score}  Level: {level}", True, color)
    score_rect = score_render.get_rect()
    screen.blit(score_render, score_rect)  # выводим текст счёта на экран
    pygame.display.update()

def game_over_message(font, size, color):
    global score
    global done
    game_over_font = pygame.font.SysFont(font, size)
    game_over_surface = game_over_font.render("Game Over, your final score: " + str(score), True, color)
    game_over_rect = pygame.Rect(100, 100, 400, 400)
    screen.blit(game_over_surface, game_over_rect) # выводим текст проигрыша 
    pygame.display.update()
    pygame.time.delay(3000)  # пауза перед выходом
    done = True

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:  # обработка управления
            if event.key == pygame.K_RIGHT:
                next_dir = "r"
            if event.key == pygame.K_LEFT:
                next_dir = "l"
            if event.key == pygame.K_UP:
                next_dir = "u"
            if event.key == pygame.K_DOWN:
                next_dir = "d"

    for seg in coor_body[:-1]:  # проверка на столкновение с телом
        if coor_head[0] == seg[0] and coor_head[1] == seg[1]:
            game_over_message("times new roman", 20, (255, 0, 0))

    screen.fill((0, 0, 0))  # очистка экрана

    # direction logic
    if next_dir == "r" and direc != "l":
        direc = "r"
    if next_dir == "l" and direc != "r":
        direc = "l"
    if next_dir == "u" and direc != "d":
        direc = "u"
    if next_dir == "d" and direc != "u":
        direc = "d"

    # move head
    if direc == "r":
        coor_head[0] += 10
    if direc == "l":
        coor_head[0] -= 10
    if direc == "u":
        coor_head[1] -= 10
    if direc == "d":
        coor_head[1] += 10

    # wall collision
    if coor_head[0] < 0 or coor_head[0] >= width or coor_head[1] < 0 or coor_head[1] >= height:
        game_over_message("times new roman", 20, (255, 0, 0))

    # update body
    new_coor = [coor_head[0], coor_head[1]]
    coor_body.append(new_coor)  # добавляем новую голову
    coor_body.pop(0)  # удаляем последний сегмент

    # check apple timer
    current_time = time.time()
    if current_time - coor_apple["spawn_time"] >= coor_apple["timer"]:
        coor_apple = generate_apple()

    # apple collision
    if coor_head[0] == coor_apple["pos"][0] and coor_head[1] == coor_apple["pos"][1]:
        eaten = True
        score += coor_apple["weight"]  # прибавляем очки в зависимости от веса еды

    if eaten:
        coor_body.insert(0, coor_body[0])  # увеличиваем змею
        coor_apple = generate_apple()  # создаем новое яблоко
        eaten = False

    # update level and speed
    level = score // 30 + 1  # каждые 30 очков — новый уровень
    speed = 5 + (level - 1)  # с каждым уровнем скорость увеличивается

    # drawing section
    pygame.draw.rect(screen, coor_apple["color"], pygame.Rect(coor_apple["pos"][0], coor_apple["pos"][1], 10, 10))  # рисуем яблоко

    for el in coor_body:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(el[0], el[1], 10, 10))  # рисуем тело змеи

    pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(coor_head[0], coor_head[1], 10, 10))  # рисуем голову

    score_update("times new roman", 20, (128, 128, 128), level)

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()