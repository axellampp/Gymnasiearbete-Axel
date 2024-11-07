import pygame
import sys
import random

# Color and window configurations
GREEN = (25, 105, 25)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1000
GRAY = (227, 227, 227)
BLACK = (20, 20, 20)

BUTTON_WIDTH = 180
BUTTON_HEIGHT = BUTTON_WIDTH / 2.5
BUTTON_RADIUS = 8

COOPERATE_COLOR = (0, 140, 255)
DEFECT_COLOR = (255, 140, 0)

# Payoff matrix for Prisoner's Dilemma
payoff_matrix = {
    ("Cooperate", "Cooperate"): (3, 3),
    ("Cooperate", "Defect"): (0, 5),
    ("Defect", "Cooperate"): (5, 0),
    ("Defect", "Defect"): (1, 1),
}

def introScreen():
    global INTRO_SCREEN
    pygame.init()
    pygame.font.init()
    INTRO_SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Main game function
def main():
    global SCREEN
    pygame.init()
    pygame.font.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    player_total_score = 0
    opponent_total_score = 0
    rounds = 1
    max_rounds = 5
    round_complete = False  # Flag to detect if a round is completed

    player_choice = None
    opponent_choice = None


    while True:
        mouseX, mouseY = pygame.mouse.get_pos()
        SCREEN.fill(GRAY)
        display_scores(player_total_score, opponent_total_score, rounds)

        
        cooperate_rect, defect_rect = drawButtons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not round_complete:
                if cooperate_rect.collidepoint(mouseX, mouseY):
                    player_choice = "Cooperate"
                    opponent_choice = random.choice(["Cooperate", "Defect"])
                elif defect_rect.collidepoint(mouseX, mouseY):
                    player_choice = "Defect"
                    opponent_choice = random.choice(["Cooperate", "Defect"])

        # Once a choice is made, simulate the round and display results
        if player_choice and opponent_choice and not round_complete:
            player_score, opponent_score = simulate_round(player_choice, opponent_choice)
            player_total_score += player_score
            opponent_total_score += opponent_score
            rounds += 1

            # Display result and score
            display_result(player_choice, opponent_choice, player_score, opponent_score)
            #display_scores(player_total_score, opponent_total_score, rounds)

            pygame.display.update()  # Update the display to show the result

            # Wait 5 seconds so the player can see the result before next round
            pygame.time.wait(5000)

            # Mark round as complete
            round_complete = True
            player_choice = None
            opponent_choice = None

        # Reset for next round
        if round_complete:
            round_complete = False  # Reset flag to indicate the next round can begin

        pygame.display.update()

        # Check if max rounds are reached
        if rounds >= max_rounds:
            SCREEN.fill(GRAY)  # Clear the screen just before displaying the results

            show_final_score(player_total_score, opponent_total_score)
            pygame.time.wait(6000)  # Wait for 6 seconds before resetting
            player_total_score, opponent_total_score, rounds = reset_game()




# Functions for the intro
def startButtons():
    font = pygame.font.SysFont(None, 40)

    start_rect = pygame.Rect(WINDOW_WIDTH // 4 - BUTTON_WIDTH // 2, WINDOW_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)

    intro_text = f"Welcome to the Prisoner's Dilemma. Here you will play against an opponent and both will be given the option to defect or cooperate."

    INTRO_SCREEN.blit()
### Functions for the main program
# Draws buttons for cooperating and defecting
def drawButtons():
    font = pygame.font.SysFont(None, 36)

    # Cooperate button
    cooperate_rect = pygame.Rect(WINDOW_WIDTH // 4 - BUTTON_WIDTH // 2, WINDOW_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(SCREEN, COOPERATE_COLOR, cooperate_rect, border_radius=BUTTON_RADIUS)
    pygame.draw.rect(SCREEN, BLACK, cooperate_rect, 3, border_radius=BUTTON_RADIUS)
    cooperate_text = font.render("Cooperate", True, BLACK)
    
    # Center the text on the button
    text_rect = cooperate_text.get_rect(center=(cooperate_rect.centerx, cooperate_rect.centery))
    SCREEN.blit(cooperate_text, text_rect)

    # Defect button
    defect_rect = pygame.Rect(3 * WINDOW_WIDTH // 4 - BUTTON_WIDTH // 2, WINDOW_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(SCREEN, DEFECT_COLOR, defect_rect, border_radius=BUTTON_RADIUS)
    pygame.draw.rect(SCREEN, BLACK, defect_rect, 3, border_radius=BUTTON_RADIUS)
    defect_text = font.render("Defect", True, BLACK)
    
    # Center the text on the button
    text_rect = defect_text.get_rect(center=(defect_rect.centerx, defect_rect.centery))
    SCREEN.blit(defect_text, text_rect)

    return cooperate_rect, defect_rect


# Function for simulating one round
def simulate_round(A_choice, B_choice):
    return payoff_matrix[(A_choice, B_choice)]

# Displays the result for a single round
def display_result(player_choice, opponent_choice, player_score, opponent_score):
    font = pygame.font.SysFont(None, 48)
    result_text = f"You chose {player_choice}, Opponent chose {opponent_choice}"
    score_text = f"You got: {player_score} points, Opponent got: {opponent_score} points"

    result_surface = font.render(result_text, True, BLACK)
    score_surface = font.render(score_text, True, BLACK)

    SCREEN.blit(result_surface, (WINDOW_WIDTH // 2 - result_surface.get_width() // 2, WINDOW_HEIGHT // 2 - 100))
    SCREEN.blit(score_surface, (WINDOW_WIDTH // 2 - score_surface.get_width() // 2, WINDOW_HEIGHT // 2))

# Displays the cumulative scores and rounds
def display_scores(player_total_score, opponent_total_score, rounds):
    font = pygame.font.SysFont(None, 36)
    score_text = f"Round: {rounds} | Your Total Score: {player_total_score} | Opponent's Total Score: {opponent_total_score}"
    score_surface = font.render(score_text, True, BLACK)
    SCREEN.blit(score_surface, (WINDOW_WIDTH // 2 - score_surface.get_width() // 2, 50))

# Shows the final score after all rounds
def show_final_score(player_total_score, opponent_total_score):
    font = pygame.font.SysFont(None, 40)
    final_text = f"Game Over! Final Score: You got {player_total_score} points - Opponent got {opponent_total_score} points"
    final_surface = font.render(final_text, True, BLACK)

    SCREEN.blit(final_surface, (WINDOW_WIDTH // 2 - final_surface.get_width() // 2, WINDOW_HEIGHT // 2 - 50))
    pygame.display.update()

# Resets the game state for a new game
def reset_game():
    return 0, 0, 0  # Reset player score, opponent score, and round count to zero

#introScreen()

#main()

FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.gameStateManager = GameStateManager('intro')
        self.start = Start(self.screen, self.gameStateManager)
        self.intro = Intro(self.screen, self.gameStateManager)

        self.states = {'start':self.start, 'intro':self.intro}

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.states[self.gameStateManager.get_state()].run()

            pygame.display.update()
            self.clock.tick(FPS)

class Intro:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    def run(self):
        self.display.fill('blue')

class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    def run(self):
        self.display.fill('red')

class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState
    def get_state(self):
        return self.currentState
    def set_state(self, state):
        self.currentState = state

if __name__ == '__main__':
    game = Game()
    game.run()