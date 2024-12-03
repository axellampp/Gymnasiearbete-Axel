from ast import Pass
from turtle import window_height, window_width
import pygame
import sys
import random

### Constants
FPS = 60

WHITE = (240, 240, 240)
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
BLACK = (20, 20, 20)

START_RECT_COLOR = (60, 179, 113)
COOPERATE_COLOR = (0, 140, 255)
DEFECT_COLOR = (255, 140, 0)

BUTTON_WIDTH = 180
BUTTON_HEIGHT = BUTTON_WIDTH / 2.5
BUTTON_RADIUS = 8

# Class for switching states
class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.gameStateManager = GameStateManager('intro')
        self.splashScreen = SplashScreen(self.screen, self.gameStateManager)
        self.intro = Intro(self.screen, self.gameStateManager)
        self.game = Game(self.screen, self.gameStateManager)

        self.states = {'splashScreen':self.splashScreen, 'intro':self.intro, 'game':self.game}

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.states[self.gameStateManager.get_state()].run()

            pygame.display.update()
            pygame.font.init()
            self.clock.tick(FPS)

class Intro:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.header_font = pygame.font.SysFont('freesansbold.ttf', 84)
        self.subheader_font = pygame.font.SysFont('freesansbold.ttf', 30)
        self.start_font = pygame.font.SysFont('freesansbold.ttf', 50)

    def run(self):
        self.display.fill(BLACK)

        # Texts
        self.header_surface = self.header_font.render('Fångarnas Dilemma', True, WHITE)
        self.subheader_surface = self.subheader_font.render('Det mest klassiska problemet inom spelteori', True, WHITE)
        self.start_button_text = self.start_font.render('STARTA', True, WHITE)
        self.start_surface = self.subheader_font.render('Rör STARTA för att börja!', True, WHITE)

        self.display.blit(self.header_surface, (WINDOW_WIDTH // 2 - self.header_surface.get_width() // 2, 50))
        self.display.blit(self.subheader_surface, (WINDOW_WIDTH // 2 - self.subheader_surface.get_width() // 2, 150))
        self.display.blit(self.start_surface, (WINDOW_WIDTH // 2 - self.start_surface.get_width() // 2, 2.8 * WINDOW_HEIGHT // 4))

        # Start button
        # Define the buttons positions and size
        start_rect = pygame.Rect((WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2), 3 * WINDOW_HEIGHT // 4, BUTTON_WIDTH, BUTTON_HEIGHT)

        # Give colour
        pygame.draw.rect(self.display, START_RECT_COLOR, start_rect)
        pygame.draw.rect(self.display, START_RECT_COLOR, start_rect, border_radius=BUTTON_RADIUS)
       
        # Center the text on the button
        self.text_rect = self.start_button_text.get_rect(center=(start_rect.centerx, start_rect.centery))
        self.display.blit(self.start_button_text, self.text_rect)

        mouse_pos = pygame.mouse.get_pos()
        if start_rect.collidepoint(mouse_pos):
            pygame.time.wait(500)
            self.gameStateManager.set_state('splashScreen')

class SplashScreen:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.header_font = pygame.font.SysFont('freesansbold.ttf', 60)
        self.body_font = pygame.font.SysFont('freesansbold.ttf', 30)

    def render_text(self, text, font, y_pos, color):
        surface = font.render(text, True, color)
        x_pos = WINDOW_WIDTH // 2 - surface.get_width() // 2
        self.display.blit(surface, (x_pos, y_pos))

    def run(self):
        self.display.fill(BLACK)

        # Header
        self.render_text('Innan du kör', self.header_font, 50, WHITE)

        # List of body text strings and their corresponding vertical positions
        self.body_texts = [
            ('Du och en annan fånge är misstänkta för att ha begått brott och ska straffas.', 120),
            ('Du och medbrottslingen kan välja att antingen vittna eller tiga, ', 150),
            ('men ni vet inte den andres val. Hur väljer du att agera?', 180),
            ('Straffen kan ritas som följande baserat på ditt val:', 220),
            ('Tryck på mellanslag för att fortsätta', WINDOW_HEIGHT - 50)
        ]

        # Render each line of body text
        for text, y_pos in self.body_texts:
            self.render_text(text, self.body_font, y_pos, WHITE)

        matrix_width, matrix_height = 400 * 1182/1080, 400 # 1182 is the width and 1080 is the height, thus the specific numbers
        self.imp = pygame.image.load("payoffmatrix1.png")
        self.imp = pygame.transform.scale(self.imp, (matrix_width, matrix_height))
        self.display.blit(self.imp, (WINDOW_WIDTH // 2 - self.imp.get_width() // 2, 240))  

        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_SPACE]:
            self.gameStateManager.set_state('game')     

class Game():
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.payoff_matrix = {
            ("tiga", "tiga"): (1, 1),
            ("tiga", "vittna"): (5, 0),
            ("vittna", "tiga"): (0, 5),
            ("vittna", "vittna"): (3, 3),
        }
        self.header_font = pygame.font.SysFont('freesansbold.ttf', 60)
        self.body_font = pygame.font.SysFont('freesansbold.ttf', 30)
        self.result_font = pygame.font.SysFont('freesansbold.ttf', 50)
        self.player_choice = None
        self.opponent_choice = None
        self.result = None

    # Helper method to render and blit text centered on the screen
    def render_text(self, text, font, y_pos, color):
        surface = font.render(text, True, color)
        x_pos = self.display.get_width() // 2 - surface.get_width() // 2
        self.display.blit(surface, (x_pos, y_pos))

    # Helper method to get the opponents choice
    def get_opponent_choice(self):
        return random.choice(["tiga", "vittna"])

    def calculate_result(self):
        self.result = self.payoff_matrix[(self.player_choice, self.opponent_choice)]

    # Display the choices
    def draw_choices(self):
        self.render_text('Vad väljer du att göra?:', self.header_font, WINDOW_HEIGHT // 8, WHITE)

        # Define the buttons positions and size
        self.cooperate_rect = pygame.Rect((WINDOW_WIDTH // 2) - (BUTTON_WIDTH * 1.5), WINDOW_HEIGHT // 4, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.defect_rect = pygame.Rect((WINDOW_WIDTH // 2) + (BUTTON_WIDTH * 0.5), WINDOW_HEIGHT // 4, BUTTON_WIDTH, BUTTON_HEIGHT)

        # Give colour
        pygame.draw.rect(self.display, COOPERATE_COLOR, self.cooperate_rect)
        pygame.draw.rect(self.display, DEFECT_COLOR, self.defect_rect)

        pygame.draw.rect(self.display, COOPERATE_COLOR, self.cooperate_rect, border_radius=BUTTON_RADIUS)
        pygame.draw.rect(self.display, DEFECT_COLOR, self.defect_rect, border_radius=BUTTON_RADIUS)
        self.cooperate_text = self.body_font.render("TIGA", True, BLACK)
        self.defect_text = self.body_font.render("VITTNA", True, BLACK)

       
        # Center the texts on the buttons
        self.text_rect = self.cooperate_text.get_rect(center=(self.cooperate_rect.centerx, self.cooperate_rect.centery))
        self.display.blit(self.cooperate_text, self.text_rect)

        text_rect = self.defect_text.get_rect(center=(self.defect_rect.centerx, self.defect_rect.centery))
        self.display.blit(self.defect_text, text_rect)

        # Help the user with a payoff matrix
        matrix_width, matrix_height = 400 * 1182/1080, 400
        self.imp = pygame.image.load("payoffmatrix1.png")
        self.imp = pygame.transform.scale(self.imp, (matrix_width, matrix_height))
        self.display.blit(self.imp, (WINDOW_WIDTH // 2 - self.imp.get_width() // 2,  2 * WINDOW_HEIGHT // 5))


        return self.cooperate_rect, self.defect_rect

    def draw_result(self):
        self.render_text(f'Du valde att {self.player_choice}', self.result_font, 100, WHITE)
        self.render_text(f'Andra fången valde att {self.opponent_choice}', self.result_font, 150, WHITE)
        self.render_text(f'Resultat: ', self.result_font, 250, WHITE)
        self.render_text(f'Du fick {self.result[0]} år i fängelse.', self.body_font, 300, WHITE)
        self.render_text(f'Andra fången fick {self.result[1]} år i fängelse.', self.body_font, 330, WHITE)
        self.render_text(f'Tryck på \'R\' för att starta om.', self.body_font, 540, WHITE)
    
    def restart_game(self):
        self.player_choice = None
        self.opponent_choice = None
        self.result = None

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            self.display.fill(BLACK)

            if self.player_choice is None:
                cooperate_rect, defect_rect = self.draw_choices()
            else:
                if self.result is None:
                    self.opponent_choice = self.get_opponent_choice()
                    self.calculate_result()
                self.draw_result()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and self.player_choice is None:
                    mouse_pos = pygame.mouse.get_pos()
                    if cooperate_rect.collidepoint(mouse_pos):
                        self.player_choice = "tiga"
                    elif defect_rect.collidepoint(mouse_pos):
                        self.player_choice = "vittna" 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart_game()
            

            clock.tick(FPS)

class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState
    def get_state(self):
        return self.currentState
    def set_state(self, state):
        self.currentState = state

if __name__ == '__main__':
    game = Main()
    game.run()