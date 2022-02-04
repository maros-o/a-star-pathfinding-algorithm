import pygame
import os
import random
import queue

pygame.font.init()

X, Y = 30, 21
BLOCK_SIZE = 32
WIDTH, HEIGHT = X * BLOCK_SIZE, Y * BLOCK_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

SNAKE_SPRITE = pygame.image.load(os.path.join('assets', 'snake_sprite.png'))
FONT = pygame.font.SysFont('consolas', 20)

BGCOLOR = (30, 30, 60)
TEXTCOLOR = (255, 255, 255)
PATHCOLOR = (135, 206, 250)
SEARCHCOLOR = (30, 144, 255)
RED = (255, 0, 0)
GOLD = (255, 215, 0)

FPS = 30
STARTING_LEN = 3

def draw_searching(used):
    for coord in used:
        pygame.draw.rect(WIN, SEARCHCOLOR, [coord[0] * BLOCK_SIZE + 6, coord[1] * BLOCK_SIZE + 6, 20, 20])

def draw_path(origin, path, searching):
    if path == None:
        return
    x = origin[0]
    y = origin[1]

    if searching:
        color = SEARCHCOLOR
        size = 6
    else:
        color = PATHCOLOR
        size = 4

    for move in path:
        p_x = x
        p_y = y
        if move == "L":
            x -= 1
        elif move == "R":
            x += 1
        elif move == "U":
            y -= 1
        elif move == "D":
            y += 1
        pygame.draw.circle(WIN, color, [x * BLOCK_SIZE + 16, y * BLOCK_SIZE + 16], size)
        pygame.draw.line(WIN,  color, [x * BLOCK_SIZE + 16, y * BLOCK_SIZE + 16], [p_x * BLOCK_SIZE + 16, p_y * BLOCK_SIZE + 16], size-3)

def draw_prey(prey):
    pygame.draw.circle(WIN, GOLD, [prey[0] * BLOCK_SIZE + BLOCK_SIZE//2, prey[1] * BLOCK_SIZE + BLOCK_SIZE//2], 13)
    pygame.draw.circle(WIN, RED, [prey[0] * BLOCK_SIZE + BLOCK_SIZE//2, prey[1] * BLOCK_SIZE + BLOCK_SIZE//2], 11)

def draw_snake(snake):
    x = snake[0][0]
    y = snake[0][1]

    for index, coord in enumerate(snake):
        x = coord[0]
        y = coord[1]

        left = False
        right = False
        up = False
        down = False

        substracter = 155
        if (index < substracter):
            snake_color = (0, 255 - index, 0)
        else:
            snake_color = (0, 255 - substracter, 0)

        if (index == 0):
            WIN.blit(SNAKE_SPRITE, (x * BLOCK_SIZE, y * BLOCK_SIZE))
            continue
        
        if (index == len(snake)-1):
            if (snake[index-1] == (x-1, y)): left = True
            if (snake[index-1] == (x+1, y)): right = True
            if (snake[index-1] == (x, y-1)): up = True
            if (snake[index-1] == (x, y+1)): down = True
        else:
            if (snake[index-1] == (x-1, y) or snake[index+1] == (x-1, y)): left = True
            if (snake[index-1] == (x+1, y) or snake[index+1] == (x+1, y)): right = True
            if (snake[index-1] == (x, y-1) or snake[index+1] == (x, y-1)): up = True
            if (snake[index-1] == (x, y+1) or snake[index+1] == (x, y+1)): down = True
                
        if (left and right): pygame.draw.rect(WIN, snake_color, [x * BLOCK_SIZE, y * BLOCK_SIZE + 4, 32, 24])
        elif (left and up): 
            pygame.draw.rect(WIN, snake_color, [x * BLOCK_SIZE, y * BLOCK_SIZE + 4, 28, 24])
            pygame.draw.rect(WIN, snake_color, [x * BLOCK_SIZE + 4, y * BLOCK_SIZE, 24, 4])
        elif (left and down): 
            pygame.draw.rect(WIN, snake_color, [x * BLOCK_SIZE, y * BLOCK_SIZE + 4, 28, 24])
            pygame.draw.rect(WIN, snake_color, [x * BLOCK_SIZE + 4, y * BLOCK_SIZE + 28, 24, 4])
        elif (right and up): 
            pygame.draw.rect(WIN, snake_color, [x * BLOCK_SIZE + 4, y * BLOCK_SIZE + 4, 28, 24])
            pygame.draw.rect(WIN, snake_color, [x * BLOCK_SIZE + 4, y * BLOCK_SIZE, 24, 4])
        elif (right and down): 
            pygame.draw.rect(WIN, snake_color, [x * BLOCK_SIZE + 4, y * BLOCK_SIZE + 4, 28, 24])
            pygame.draw.rect(WIN, snake_color, [x * BLOCK_SIZE + 4, y * BLOCK_SIZE + 28, 24, 4])
        elif (up and down): pygame.draw.rect(WIN, snake_color, [x * BLOCK_SIZE + 4, y * BLOCK_SIZE, 24, 32])
        elif (left): pygame.draw.rect(WIN, snake_color, [x * BLOCK_SIZE, y * BLOCK_SIZE + 4, 28, 24])
        elif (right): pygame.draw.rect(WIN, snake_color, [x * BLOCK_SIZE + 4, y * BLOCK_SIZE + 4, 28, 24])
        elif (up): pygame.draw.rect(WIN, snake_color, [x * BLOCK_SIZE + 4, y * BLOCK_SIZE, 24, 28])
        elif (down): pygame.draw.rect(WIN, snake_color, [x * BLOCK_SIZE + 4, y * BLOCK_SIZE + 4, 24, 28])

def draw_window(snake, prey, path, searching, used):
    WIN.fill(BGCOLOR)

    if searching:
        draw_searching(used)
    else: draw_path(snake[0], path, searching)

    draw_prey(prey)
    draw_snake(snake)
    
    text = FONT.render("score:"+str(len(snake)-STARTING_LEN), 1, TEXTCOLOR)
    WIN.blit(text, (X//3, Y//3))

    pygame.display.update()

def spawn_prey(snake):
    x = -1
    y = -1
    while(x == -1 and y == -1):
        x = random.randint(0, X - 1)
        y = random.randint(0, Y - 1)
        for coord in snake:
            if ((x, y) == coord):
                x = -1
                y = -1
                continue
    return (x, y)

def get_neighbors(point, snake):
    forbidden = snake.copy()
    for x in range(-1, X+1):
        for y in range(-1, Y+1):
            if (x == -1 or y == -1 or x == X or y == Y):
                forbidden.append((x, y))

    neighbors = []
    x = point[0]
    y = point[1]

    if not ((x+1, y) in forbidden): neighbors.append((x+1, y))
    if not ((x-1, y) in forbidden): neighbors.append((x-1, y))
    if not ((x, y+1) in forbidden): neighbors.append((x, y+1))
    if not ((x, y-1) in forbidden): neighbors.append((x, y-1))

    return neighbors

def h(point, end):
    return abs(point[0] - end[0]) + abs(point[1] - end[1])

def reconstruct_path(came_from, current):
    path_coords = [current]
    while current in came_from:
        current = came_from[current]
        path_coords.append(current)
    path_coords.reverse()

    path = ""
    for index, coord in enumerate(path_coords):
        x = coord[0]
        y = coord[1]

        if (index >= len(path_coords)-1):
            break

        if (path_coords[index+1] == (x-1, y)): path = "L" + path
        if (path_coords[index+1] == (x+1, y)): path = "R" + path
        if (path_coords[index+1] == (x, y-1)): path = "U" + path
        if (path_coords[index+1] == (x, y+1)): path = "D" + path

    path = path[::-1]

    return path

def calculate_path(snake, end):
    start = snake[0]
    count = 0
    open_set = queue.PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {(x, y): float("inf") for x in range(0, X) for y in range(0, Y)}
    g_score[start] = 0
    f_score = {(x, y): float("inf") for x in range(0, X) for y in range(0, Y)}
    f_score[start] = h(start, end)

    open_set_hash = {start}

    closed = snake.copy()
    been_there = []

    while not open_set.empty():
        current = open_set.get()[2]
        been_there.append(current)
        draw_window(snake, end, "", True, been_there)
        open_set_hash.remove(current)
        if current == end:
            return reconstruct_path(came_from, end)

        for neighbor in get_neighbors(current, closed):
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor, end)
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

        if current != start:
            closed.append(neighbor)

def movement(snake, prey, curr_path):
    new_x = snake[0][0]
    new_y = snake[0][1]

    if curr_path == None:
        return True, snake, prey, curr_path

    move = curr_path[0]
    if (move == 'U'):
        new_y -= 1
    elif (move == 'D'):
        new_y += 1
    elif (move == 'L'):
        new_x -= 1
    elif (move == 'R'):
        new_x += 1

    for coord in snake:
        if ((new_x, new_y) == coord):
            print("you lose cause of self collision with score", len(snake) - STARTING_LEN)
            return True, snake, prey, curr_path[1:]
    
    if (new_x < 0 or new_x >= X or new_y < 0 or new_y >= Y):
        print("you lose cause of borders with score", len(snake) - STARTING_LEN)
        return True, snake, prey, curr_path[1:]

    snake.insert(0, (new_x, new_y))

    if ((new_x, new_y) == prey):
        prey = spawn_prey(snake)
        curr_path = calculate_path(snake, prey)
        return False, snake, prey, curr_path
    else:
        snake.pop()
        return False, snake, prey, curr_path[1:]

def main():
    pygame.display.set_caption("A*")
    clock = pygame.time.Clock()
    snake = [(0,0), (0,1), (0,2)]
    prey = spawn_prey(snake)
    path = calculate_path(snake, prey)

    lost = False
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if not lost:
            lost, snake, prey, path = movement(snake, prey, path)
            draw_window(snake, prey, path, False, [])

    pygame.quit()

main()