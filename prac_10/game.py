import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 4  # 4x4 grid
TILE_SIZE = WIDTH // GRID_SIZE
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CARD_BACK = (100, 100, 255)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Matching Game")
clock = pygame.time.Clock()

# Generate Cards
card_values = list(range(GRID_SIZE * GRID_SIZE // 2)) * 2
random.shuffle(card_values)

# Game state
revealed = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
selected = []
matched = []

def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x, y = col * TILE_SIZE, row * TILE_SIZE
            if revealed[row][col] or (row, col) in matched:
                pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE))
                font = pygame.font.Font(None, 74)
                text = font.render(str(card_values[row * GRID_SIZE + col]), True, BLACK)
                screen.blit(text, (x + TILE_SIZE // 4, y + TILE_SIZE // 4))
            else:
                pygame.draw.rect(screen, CARD_BACK, (x, y, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 3)

def main():
    running = True
    global revealed, selected, matched

    while running:
        screen.fill(WHITE)
        draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col, row = x // TILE_SIZE, y // TILE_SIZE
                if not revealed[row][col] and len(selected) < 2 and (row, col) not in matched:
                    revealed[row][col] = True
                    selected.append((row, col))

        if len(selected) == 2:
            # Check for a match
            r1, c1 = selected[0]
            r2, c2 = selected[1]
            if card_values[r1 * GRID_SIZE + c1] == card_values[r2 * GRID_SIZE + c2]:
                matched.extend(selected)
            else:
                pygame.display.flip()
                time.sleep(1)
                revealed[r1][c1] = False
                revealed[r2][c2] = False
            selected = []

        if len(matched) == GRID_SIZE * GRID_SIZE:
            font = pygame.font.Font(None, 100)
            text = font.render("You Win!", True, BLACK)
            screen.blit(text, (WIDTH // 4, HEIGHT // 2))
            pygame.display.flip()
            time.sleep(3)
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
