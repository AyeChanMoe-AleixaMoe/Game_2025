import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Matching Game")
font = pygame.font.Font(None, 74)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Card settings
CARD_SIZE = 100
MARGIN = 20

# Create card positions
def create_card_positions():
    positions = []
    for i in range(4):
        for j in range(4):
            x = MARGIN + j * (CARD_SIZE + MARGIN)
            y = MARGIN + i * (CARD_SIZE + MARGIN)
            positions.append((x, y))
    return positions

positions = create_card_positions()

# Generate pairs
def generate_pairs():
    symbols = list(range(8)) * 2
    random.shuffle(symbols)
    return symbols

pairs = generate_pairs()

# Card class
class Card:
    def __init__(self, symbol, position):
        self.symbol = symbol
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], CARD_SIZE, CARD_SIZE)
        self.revealed = False
        self.matched = False

    def draw(self, screen):
        if self.revealed or self.matched:
            pygame.draw.rect(screen, WHITE, self.rect)
            text = font.render(str(self.symbol), True, BLACK)
            screen.blit(text, (self.position[0] + 35, self.position[1] + 25))
        else:
            pygame.draw.rect(screen, GREEN, self.rect)

# Create card objects
cards = [Card(pairs[i], positions[i]) for i in range(16)]

# Game variables
revealed_cards = []  # Store the two revealed cards
matches = 0
attempts = 0
running = True
clock = pygame.time.Clock()

# Show all cards at the start
screen.fill(BLACK)
for card in cards:
    card.revealed = True
    card.draw(screen)
screen.blit(font.render("Memorize the pairs ", True, WHITE), (10, 500))
pygame.display.flip()

# Wait for 5 seconds
time.sleep(5)

# Hide all cards after the initial reveal
for card in cards:
    card.revealed = False

# Main game loop
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if len(revealed_cards) < 2:
                for card in cards:
                    if card.rect.collidepoint(event.pos) and not card.revealed and not card.matched:
                        card.revealed = True
                        revealed_cards.append(card)
                        if len(revealed_cards) == 2:
                            attempts += 1

    # Check for match after two cards are revealed
    if len(revealed_cards) == 2:
        pygame.time.wait(500)
        if revealed_cards[0].symbol == revealed_cards[1].symbol:
            revealed_cards[0].matched = True
            revealed_cards[1].matched = True
            matches += 1
        else:
            revealed_cards[0].revealed = False
            revealed_cards[1].revealed = False
        revealed_cards = []  # Reset revealed cards

    # Draw cards
    for card in cards:
        card.draw(screen)

    # Display match count
    font = pygame.font.Font(None, 36)
    text = font.render(f"Matches: {matches}  Attempts: {attempts}", True, WHITE)
    screen.blit(text, (10, 500))

    # Check for win
    if matches == 8:
        font = pygame.font.Font(None, 74)
        win_text = font.render("You Win!", True, RED)
        screen.blit(win_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
