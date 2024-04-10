"""
   _____                                         __     _        _    __
  / ____|                                       / _|   | |      (_)  / _|
 | |  __    __ _   _ __ ___     ___      ___   | |_    | |       _  | |_    ___
 | | |_ |  / _` | | '_ ` _ \   / _ \    / _ \  |  _|   | |      | | |  _|  / _ \
 | |__| | | (_| | | | | | | | |  __/   | (_) | | |     | |____  | | | |   |  __/
  \_____|  \__,_| |_| |_| |_|  \___|    \___/  |_|     |______| |_| |_|    \___|


----------

Controls:
left click - place cell
backspace - clear grid
space - toggle play/pause
right arrow - advance one generation
1 ; 2 ; ... ; 9 - select a  pattern
R - rotate the pattern
left click - place the selected pattern
right click - erase
S - toggle select:
    C - copy pattern
    X - cut pattern
    N - save pattern
    backspace - clear selected area
KONAMI CODE - change placement mode

Rules:
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

Pattern library:
https://conwaylife.appspot.com/library
"""

import pygame, sys
import random
import time

pygame.init()

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_GREEN = (150, 255, 150)
DARK_GREEN = (0, 150, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)
ALPHA_BLUE = (0, 0, 255, 127)
RED = (255, 0, 0)
DARK_GREY = (190, 190, 190)
LIGHT_GREY = (80, 80, 80)
# COLOR1 = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
# COLOR2 = (COLOR1[1], COLOR1[2], COLOR1[0])
# COLOR3 = (COLOR2[1], COLOR2[2], COLOR2[0])
# COLORS = [COLOR1, COLOR2, COLOR3]

# PATTERNS
PATTERNS = {
    "from selection": [[]],

    "cell": [[1]],

    "glider": [[1, 1, 1],
               [0, 0, 1],
               [0, 1, 0]],

    "flower": [[1, 1, 1, 1, 1, 1, 1]],

    "gospel's glider gun": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],

    "squid": [[0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
              [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
              [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0]],

    "dick": [[1, 0, 1], # no joke le pattern dick il finit sur 4 oscillators c'est tah swag
             [0, 1, 0],
             [0, 1, 0],
             [0, 1, 0]]
}

# SETTINGS
SLEEP_DURATION = 0.05 # (in seconds) (-1 : pause until right arrow key is pressed)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
GRID_WIDTH = 62
GRID_HEIGHT = 62
SPAWN_RATE = 0 # rate to spawn at start for each cell
PLACEMENT_MODE = 0 # 0 : jpg ; 1 : png
# GRID SETUP
# 0 - dead cell
# 1 - alive cell
GRID = [[(random.randint(0, SPAWN_RATE) >= 1) for i in range(GRID_WIDTH)] for j in range(GRID_HEIGHT)]
GRID_MASK = [[0 for i in range(GRID_WIDTH)] for j in range(GRID_HEIGHT)]

KONAMI_CODE = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_b, pygame.K_a]
lastKeyboardInputs = [0]*len(KONAMI_CODE)
iteration = 0

def rotateTab(tab):
    result = [[] for i in range(len(tab[0]))]
    for i in range(len(tab[0])):
        for j in range(len(tab)-1, -1, -1):
            result[i].append(tab[j][i])

    return result


def applyPattern(pattern, targetGrid, pos, mode):
    """
    Apply pattern on the specified grid
    mode c'est la couleur
    Comme ça vla smart il y a qu'une fonction qui affiche les grids
    """
    x = pos[0]-len(pattern[0])//2
    y = pos[1]-len(pattern)//2
    if len(pattern[0]) < len(GRID[0]):
        if x < 0:
            x = 0
        elif x > len(GRID[0]) - len(pattern[0]):
            x = len(GRID[0]) - len(pattern[0])
    if len(pattern) < len(GRID):
        if y < 0:
            y = 0
        elif y > len(GRID) - len(pattern):
            y = len(GRID) - len(pattern)

    for j in range(len(pattern)):
        for i in range(len(pattern[0])):
            if 0 <= x+i < GRID_WIDTH and 0 <= y+j < GRID_HEIGHT:
                if pattern[j][i] == 1 or PLACEMENT_MODE == 1: # avec : png tier ; sans : jpg tier
                    targetGrid[y+j][x+i] = pattern[j][i]*mode


def savePattern(pattern):
    with open("pattern.txt", "w") as f:
        f.write("[")
        for i in pattern:
            f.write(str(i) + ",\n")
        f.write("]")


def evolveLife(grid):
    global iteration
    iteration += 1
    updatedGrid = [[0 for i in range(len(grid[0]))] for j in range(len(grid))]
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            neighbours = 0
            # neighbours calculation
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= y + i < len(GRID) and 0 <= x + j < len(GRID[0]):
                        if (not (j == 0 and i == 0)) and grid[y + i][x + j] == 1 or grid[y + i][x + j] == 3:
                            neighbours += 1
            if grid[y][x] == 1 or grid[y][x] == 3: # if alive
                if 2 <= neighbours <= 3:
                    updatedGrid[y][x] = 1
                else:
                    updatedGrid[y][x] = 0
            elif grid[y][x] == 0 or grid[y][x] == 2: # if dead
                if neighbours == 3:
                    updatedGrid[y][x] = 1
                else:
                    updatedGrid[y][x] = 0

    return updatedGrid


def displayGrid(grid, screen: pygame.surface):
    cellWidth = screen.get_width() // len(grid[0])
    cellHeight = screen.get_height() // len(grid)

    # draw cells
    for j in range(len(grid)):
        for i in range(len(grid[0])):
            if grid[j][i] == 1: # alive cell
                #pygame.draw.rect(screen, random.choice(COLORS), (i*cellWidth, j*cellHeight, cellWidth, cellHeight))
                pygame.draw.rect(screen, GREEN, (i * cellWidth, j * cellHeight, cellWidth, cellHeight))
            elif grid[j][i] == 2: # mouse cursor
                pygame.draw.rect(screen, LIGHT_GREEN, (i * cellWidth, j * cellHeight, cellWidth, cellHeight))
            elif grid[j][i] == 3: # selection rect border
                pygame.draw.rect(screen, LIGHT_BLUE, (i * cellWidth, j * cellHeight, cellWidth, cellHeight))
            elif grid[j][i] == 4: # selection filled rect
                # How to get a cancer very quickly:
                # 1. Touch grass, look at the sun during 5 minutes
                # 2. Talk to a feminist
                # 3. Read the code down below ↓↓
                rect = pygame.Rect(i * cellWidth, j * cellHeight, cellWidth, cellHeight)
                s = pygame.Surface(rect.size)
                s.set_alpha(127)
                pygame.draw.rect(s, (200, 200, 255), s.get_rect())
                screen.blit(s, rect.topleft)
            elif grid[j][i] == 5: # debug color
                pygame.draw.rect(screen, RED, (i * cellWidth, j * cellHeight, cellWidth, cellHeight))


screen = pygame.display.set_mode((GRID_WIDTH * round(WINDOW_WIDTH / GRID_WIDTH), GRID_HEIGHT * round(WINDOW_HEIGHT / GRID_HEIGHT)))
pygame.display.set_caption('Game of Life')
print(screen.get_size())
font = pygame.font.Font("freesansbold.ttf", 15)

# first render #
screen.fill(BLACK)
displayGrid(GRID, screen)
screen.blit(font.render(f"Grid w: {len(GRID)} ; h: {len(GRID[0])}", False, RED), (5, 5))
screen.blit(font.render(f"Iteration: {iteration}", False, RED), (5, 25))
pygame.display.update()
# ------------ #

selecting = False
origin = (0, 0) # origin coords of the selection rect
patternID = 1
pattern = PATTERNS["cell"]
FPS = 0
lastMousePos = (0, 0)
paused = 0
# Game States:
# 0 : running
# 1 : semi-paused
# 2 : paused
cellWidth = screen.get_width() // len(GRID[0])
cellHeight = screen.get_height() // len(GRID)
while True:
    # mouse position
    x = int(pygame.mouse.get_pos()[0] / cellWidth)
    y = int(pygame.mouse.get_pos()[1] / cellHeight)

    if not paused:
        if SLEEP_DURATION < 0:
            paused = 2
        else:
            time.sleep(SLEEP_DURATION)

    t1 = time.time()

    # -- Events --
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # User inputs
        elif event.type == pygame.KEYDOWN:
            lastKeyboardInputs.append(event.key)
            del lastKeyboardInputs[0]
            if lastKeyboardInputs == KONAMI_CODE:
                PLACEMENT_MODE = int(not PLACEMENT_MODE)
                print("KONAMI CODE : placement mode switched")

            # Only evolve one generation (only if the user isn't entering konami code)
            if event.key == pygame.K_RIGHT and not (lastKeyboardInputs[len(KONAMI_CODE)-6:] == KONAMI_CODE[:6] or lastKeyboardInputs[len(KONAMI_CODE)-8:] == KONAMI_CODE[:8]):
                GRID = evolveLife(GRID)

            # Increase and decrease the game speed
            elif event.key == pygame.K_UP and SLEEP_DURATION:
                SLEEP_DURATION -= 0.005

            elif event.key == pygame.K_DOWN and SLEEP_DURATION <= 5:
                SLEEP_DURATION += 0.005

            # Pause the game
            if event.key == pygame.K_SPACE:
                paused = (not paused) * 2
                selecting = False

            # Clear the grid
            elif event.key == pygame.K_BACKSPACE and not selecting:
                GRID = [[0 for i in range(GRID_WIDTH)] for j in range(GRID_HEIGHT)]

            # Toggle select
            elif event.key == pygame.K_s and paused == 2:
                selecting = not selecting
                origin = (x, y)
                selection = []

            # Cancel select
            elif event.key == pygame.K_ESCAPE and selecting:
                selecting = False

            # Select the pattern
            elif pygame.K_0 <= event.key <= pygame.K_9 and paused == 2:
                selecting = False
                patternID = event.key - pygame.K_0
                try:
                    pattern = PATTERNS[list(PATTERNS.keys())[patternID]]
                except IndexError: # occur if there is not enough pattern in PATTERNS
                    print(f"Pattern nb {patternID} doesn't exist yet")
                    pass

            # Rotate the pattern
            elif event.key == pygame.K_r:
                pattern = rotateTab(pattern)

        elif event.type == pygame.MOUSEBUTTONDOWN and not paused:
            paused = 1
            patternID = 1
            pattern = PATTERNS["cell"]

        elif event.type == pygame.MOUSEBUTTONUP and paused == 1:
            paused = 0

    # clear grid mask
    GRID_MASK = [[0 for i in range(GRID_WIDTH)] for j in range(GRID_HEIGHT)] # running this every frame is cancer
    if paused:
        if not selecting:
            # --- Patterns ---
            if pygame.mouse.get_pressed()[0] == True:
                applyPattern(pattern, GRID, (x, y), 1)
            elif pygame.mouse.get_pressed()[2] == True:
                applyPattern(pattern, GRID, (x, y), 0)
            applyPattern(pattern, GRID_MASK, (x, y), 2)
        else:
            # --- Selection ---
            # draw selection rect
            rectWidth = abs(x - origin[0])
            rectHeight = abs(y - origin[1])
            if rectWidth > 0 and rectHeight > 0:
                rectWidth += (rectWidth//(x - origin[0]) == 1)
                rectHeight += (rectHeight//(y - origin[1]) == 1)
                filledRect = [[1 for i in range(rectWidth)] for j in range(rectHeight)]
                borderRect = [[0 for i in range(rectWidth)] for j in range(rectHeight)]
                for j in range(rectHeight):
                    for i in range(rectWidth):
                        if (j == 0 or j == rectHeight-1) or (i == 0 or i == rectWidth-1):
                            borderRect[j][i] = 1
                if x > origin[0]:
                    rectX = origin[0]+rectWidth//2
                else:
                    rectX = origin[0]-(rectWidth+1)//2
                if y > origin[1]:
                    rectY = origin[1]+rectHeight//2
                else:
                    rectY = origin[1]-(rectHeight+1)//2

                applyPattern(filledRect, GRID_MASK, (rectX, rectY), 4)
                applyPattern(borderRect, GRID_MASK, (rectX, rectY), 3)
                # applyPattern([[1]], GRID_MASK, (rectX, rectY), 5) # display grid center

            # Handle user inputs
            # All ranges are from 0 to x-2 in order to don't consider rectangle edges
            if pygame.key.get_pressed()[pygame.K_BACKSPACE] == True:
                # clear selected area
                rectX -= rectWidth//2
                rectY -= rectHeight//2
                for j in range(1, rectHeight-1):
                    for i in range(1, rectWidth-1):
                        GRID[rectY+j][rectX+i] = 0
                selecting = False

            if pygame.key.get_pressed()[pygame.K_c] == True or pygame.key.get_pressed()[pygame.K_x] == True:
                # copy / cut selected area
                rectX -= rectWidth//2
                rectY -= rectHeight//2
                selectedArea = [[0 for i in range(rectWidth-2)] for j in range(rectHeight-2)]
                for j in range(rectHeight-2):
                    for i in range(rectWidth-2):
                        selectedArea[j][i] = GRID[rectY+j+1][rectX+i+1]
                        if pygame.key.get_pressed()[pygame.K_x] == True:
                            GRID[rectY+j+1][rectX+i+1] = 0
                PATTERNS["from selection"] = selectedArea
                pattern = PATTERNS["from selection"]
                patternID = 0
                selecting = False

            if pygame.key.get_pressed()[pygame.K_n] == True:
                # save selected area
                rectX -= rectWidth//2
                rectY -= rectHeight//2
                selectedArea = [[0 for i in range(rectWidth-2)] for j in range(rectHeight-2)]
                for j in range(1, rectHeight-1):
                    for i in range(1, rectWidth-1):
                        selectedArea[j][i] = GRID[rectY+j][rectX+i]
                savePattern(selectedArea)
                selecting = False

    # -- Rendering --
    screen.fill(BLACK)
    # game logic
    if not paused:
        GRID = evolveLife(GRID)
    # draw game and UI
    displayGrid(GRID, screen)
    displayGrid(GRID_MASK, screen)
    # draw text
    screen.blit(font.render(f"Grid w: {len(GRID)} ; h: {len(GRID[0])}", False, RED), (5, 5))
    screen.blit(font.render(f"Iteration: {iteration}", False, RED), (5, 25))
    if FPS < 0:
        screen.blit(font.render("FPS: INFINITY", False, RED), (5, 45))
    else:
        screen.blit(font.render(f"FPS: {FPS:.1f}", False, RED), (5, 45))
    screen.blit(font.render("State: " + "pause"*(paused > 0) + "playing"*(not paused), False, RED), (5, 65))
    screen.blit(font.render("Speed "+ str(1 // SLEEP_DURATION), False, RED), (5, 85))
    try:
        screen.blit(font.render("Pattern: "*(paused > 0) + str(list(PATTERNS.keys())[patternID])*(paused > 0), False, RED), (5, 105))
    except IndexError:
        pass
    screen.blit(font.render("Selecting"*(selecting > 0), False, RED), (5, 125))
    pygame.display.update()
    # -- FPS Calculation --
    try:
        FPS = 1 / (time.time() - t1)
    except ZeroDivisionError: # this error may occur on PCs with too much RGB running the game too fast
        FPS = -1
