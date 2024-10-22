import pygame
import sys
import random

GREEN = (25, 105, 25)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 480
WINDOW_WIDTH = 840

BUTTON_WIDTH = 180
BUTTON_HEIGHT = BUTTON_WIDTH / 2.5
BUTTON_RADIUS = 8

COOPERATE_COLOR = (0, 140, 255)
DEFECT_COLOR = (255, 140, 0)

A_score = 0
B_score = 0

payoff_matrix = {
    ("Cooperate", "Cooperate"): (3, 3),
    ("Cooperate", "Defect"): (0, 5),
    ("Defect", "Cooperate"): (5, 0),
    ("Defect", "Defect"): (1, 1),
}

def main():
    global SCREEN
    pygame.init()
    pygame.font.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    SCREEN.fill(GREEN)

    player_choice = None
    opponent_choice = None

    while True:
        mouseX, mouseY = pygame.mouse.get_pos()
        SCREEN.fill(GREEN)  # Clear the screen with the background color

        drawGrid()
        cooperate_rect, defect_rect = drawButtons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if cooperate_rect.collidepoint(mouseX, mouseY):
                    player_choice = "Cooperate"
                    if random.random() <= 0.5:
                        opponent_choice = "Cooperate"
                    else:
                        opponent_choice = "Defect"

                elif defect_rect.collidepoint(mouseX, mouseY):
                    player_choice = "Defect"
                    if random.random() <= 0.5:
                        opponent_choice = "Cooperate"
                    else:
                        opponent_choice = "Defect"

        # Once a choice is made, simulate the round and display results
        if player_choice and opponent_choice:
            player_score, opponent_score = simulate_round(player_choice, opponent_choice)
            display_result(player_choice, opponent_choice, player_score, opponent_score)

        pygame.display.update()

def drawButtons():
    font = pygame.font.SysFont(None, 36)

    # Cooperate button
    cooperate_rect = pygame.Rect(WINDOW_WIDTH//4 - BUTTON_WIDTH//2, WINDOW_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(SCREEN, COOPERATE_COLOR, cooperate_rect, border_radius=BUTTON_RADIUS)
    cooperate_text = font.render("Cooperate", True, WHITE)
    SCREEN.blit(cooperate_text, (cooperate_rect.x + 20, cooperate_rect.y + 10))

    # Defect button
    defect_rect = pygame.Rect(3 * WINDOW_WIDTH//4 - BUTTON_WIDTH//2, WINDOW_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(SCREEN, DEFECT_COLOR, defect_rect, border_radius=BUTTON_RADIUS)
    defect_text = font.render("Defect", True, WHITE)
    SCREEN.blit(defect_text, (defect_rect.x + 35, defect_rect.y + 10))

    return cooperate_rect, defect_rect


# Function for simulating one round.
def simulate_round(A_choice, B_choice):
    return payoff_matrix[(A_choice, B_choice)]

def drawGrid():
    blockSize = 60 # Grid size
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)

def display_result(player_choice, opponent_choice, player_score, opponent_score):
    font = pygame.font.SysFont(None, 48)

    result_text = f"You chose {player_choice}, Opponent chose {opponent_choice}"
    score_text = f"Your payoff: {player_score}, Opponent payoff: {opponent_score}"

    result_surface = font.render(result_text, True, WHITE)
    score_surface = font.render(score_text, True, WHITE)

    SCREEN.blit(result_surface, (WINDOW_WIDTH//2 - result_surface.get_width()//2, WINDOW_HEIGHT//2 - 100))
    SCREEN.blit(score_surface, (WINDOW_WIDTH//2 - score_surface.get_width()//2, WINDOW_HEIGHT//2))


main()
