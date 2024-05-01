###initializing###
import random 
import pygame

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

background = (3, 244, 252)
cell_living = (255, 255, 255)
cell_dead = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

run = True

###set up grid###
width = 10
height = 10
margin = 2 #gap between cells

grid = []
for row in range (100):
    grid.append([])
    for column in range (100):
        grid[row].append(False)

clock = pygame.time.Clock()

iteration = 0
setup_done = False
clicked = False
drag_select = False #allows click and drag

living_neighbors = 0

###set screen###
screen.fill(background)

def draw_grid():        
    for row in range (100):
        for column in range (100):
            cell_rect = ((margin + width) * column + margin, (margin + height) * row + margin, width, height)
            if grid[row][column]:
                pygame.draw.rect(screen, cell_living, cell_rect)
            else:
                pygame.draw.rect(screen, cell_dead, cell_rect)
    
    pygame.display.update()
    clock.tick(60)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    while not setup_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                iteration = 10000
                setup_done = True
                run = False
            if event.type == pygame.KEYDOWN:
                #randomize cells
                if event.key == pygame.K_r:
                    grid = [[random.random() < 0.1 for _ in range (100)] for _ in range(100)]
                if event.key == pygame.K_ESCAPE:
                    iteration = 10000
                    setup_done = True
                    run = False
                #exit setup
                if event.key == pygame.K_SPACE:
                    setup_done = True
                #allow drag select
                if event.key == pygame.K_d:
                    drag_select = not drag_select
            #game initial conditions setup
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                column = event.pos[0] // (width + margin)
                row = event.pos[1] // (height + margin)
                #Toggle cell state
                if not setup_done:
                    grid[row][column] = not grid[row][column]
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False
        #drag select
        if clicked and drag_select and not setup_done:
            column = pygame.mouse.get_pos()[0] // (width + margin)
            row = pygame.mouse.get_pos()[1] // (height + margin)
            grid[row][column] = True
            
    ###draw grid###
        draw_grid()

###start simulation###
    while setup_done and iteration < 10000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                iteration = 10000
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    iteration = 10000
                    run = False
        clock.tick(60)
        for row in range (100):
            for column in range (100):
                for i in range(-1, 2):
                    for j in range (-1, 2):
                        if i == 0 and j == 0:
                            continue
                        neighbor_row = row + i
                        neighbor_column = column + j
                        #check if neighbor is within the grid boundary and alive
                        if 0 <= neighbor_row < len(grid) and 0 <= neighbor_column < len(grid[0]) and grid[neighbor_row][neighbor_column]:
                            living_neighbors += 1
                if not grid[row][column] and living_neighbors == 3:
                    grid[row][column] = True #resurrect cell
                elif grid[row][column] and living_neighbors < 2:
                    grid[row][column] = False #kill cell
                elif grid[row][column] and living_neighbors > 3:
                    grid[row][column] = False #kill cell
                living_neighbors = 0
        iteration += 1
        print(iteration)
        draw_grid()


pygame.quit()