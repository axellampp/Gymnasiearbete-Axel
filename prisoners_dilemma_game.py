import pygame
import sys

GREEN = (25, 105, 25)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 480
WINDOW_WIDTH = 840

BUTTON_WIDTH = 180
BUTTON_HEIGHT = BUTTON_WIDTH / 2.5
BUTTON_RADIUS = 8

COOPERATE_COLOR = (0, 140, 255)
DEFECT_COLOR = (255, 140, 0)

def main():
    global SCREEN
    pygame.init()
    pygame.font.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    SCREEN.fill(GREEN)
    
    mouseX = 0
    mouseY = 0

    while True:
        mouseX, mouseY = pygame.mouse.get_pos()

        drawGrid()
        drawButtons()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            
            pass

        pygame.display.update()

def drawButtons():
    button = (pygame.draw.rect(SCREEN, COOPERATE_COLOR, pygame.Rect(30, 100, BUTTON_WIDTH, BUTTON_HEIGHT), 0, border_radius=BUTTON_RADIUS), )
    pygame.draw.rect(SCREEN, DEFECT_COLOR, pygame.Rect(300, 100, BUTTON_WIDTH, BUTTON_HEIGHT), 0, border_radius=BUTTON_RADIUS)

    pass

payoff_matrix = {
    ("Cooperate", "Cooperate"): (3, 3),
    ("Cooperate", "Defect"): (0, 5),
    ("Defect", "Cooperate"): (5, 0),
    ("Defect", "Defect"): (1, 1),
}

# Function for simulating one round.
def simulate_round(A_choice, B_choice):
    return payoff_matrix[(A_choice, B_choice)]

def drawGrid():
    blockSize = 60 #Set the size of the grid block
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)

main()