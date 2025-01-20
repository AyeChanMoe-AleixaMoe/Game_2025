import tkinter as tk
import random
import pygame


class Game2048:
    def __init__(self):
        # Initialize Pygame for music and sound effects
        pygame.mixer.init()
        pygame.mixer.music.load("Memories-of-Spring(chosic.com).mp3")  # Background music file
        pygame.mixer.music.play(-1, 0.0)  # Loop the music infinitely

        self.game_over_sound = pygame.mixer.Sound("game_over_sound.mp3")  # Game Over sound effect
        self.window = tk.Tk()
        self.window.title("2048 Game")
        self.board = [[0] * 4 for _ in range(4)]
        self.grid_cells = []
        self.score = 0
        self.high_score = 0  # Store the high score from previous rounds
        self.game_over_label = None  # Store the Game Over label reference
        self.retry_button = None  # Store the Retry button reference

        self.initialize_ui()
        self.add_new_tile()
        self.add_new_tile()
        self.update_ui()

        self.window.bind("<Key>", self.handle_keypress)
        self.window.mainloop()

    def initialize_ui(self):
        # Main frame for the game
        self.main_frame = tk.Frame(self.window, bg="black", bd=5)
        self.main_frame.grid(row=0, column=0, pady=10, padx=10)

        # Game grid cells
        for r in range(4):
            row_cells = []
            for c in range(4):
                cell = tk.Label(self.main_frame, text="", bg="lightgrey", font=("Helvetica", 24), width=4, height=2,
                                borderwidth=2, relief="groove")
                cell.grid(row=r, column=c, padx=5, pady=5)
                row_cells.append(cell)
            self.grid_cells.append(row_cells)

        # Score label
        self.score_label = tk.Label(self.window, text=f"Score: {self.score}", font=("Helvetica", 16))
        self.score_label.grid(row=1, column=0, pady=10)

        # High score label
        self.high_score_label = tk.Label(self.window, text=f"High Score: {self.high_score}", font=("Helvetica", 16))
        self.high_score_label.grid(row=2, column=0, pady=10)

    def add_new_tile(self):
        empty_cells = [(r, c) for r in range(4) for c in range(4) if self.board[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.board[r][c] = 2 if random.random() < 0.9 else 4

    def update_ui(self):
        for r in range(4):
            for c in range(4):
                value = self.board[r][c]
                self.grid_cells[r][c].config(text=f"{value}" if value != 0 else "", bg=self.get_cell_color(value))
        self.score_label.config(text=f"Score: {self.score}")
        self.high_score_label.config(text=f"High Score: {self.high_score}")

    def get_cell_color(self, value):
        colors = {
            0: "lightgrey",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e",
        }
        return colors.get(value, "#3c3a32")

    def handle_keypress(self, event):
        direction = event.keysym
        if direction in ("Up", "Down", "Left", "Right"):
            if self.move(direction):
                self.add_new_tile()
                self.update_ui()
                if not self.can_move():
                    self.end_game()

    def move(self, direction):
        moved = False

        def merge_line(line):
            new_line = [num for num in line if num != 0]
            for i in range(len(new_line) - 1):
                if new_line[i] == new_line[i + 1]:
                    new_line[i] *= 2
                    self.score += new_line[i]
                    new_line[i + 1] = 0
            new_line = [num for num in new_line if num != 0]
            return new_line + [0] * (4 - len(new_line))

        if direction in ("Up", "Down"):
            for c in range(4):
                line = [self.board[r][c] for r in range(4)]
                if direction == "Down":
                    line.reverse()
                merged = merge_line(line)
                if direction == "Down":
                    merged.reverse()
                for r in range(4):
                    if self.board[r][c] != merged[r]:
                        moved = True
                    self.board[r][c] = merged[r]
        elif direction in ("Left", "Right"):
            for r in range(4):
                line = self.board[r][:]
                if direction == "Right":
                    line.reverse()
                merged = merge_line(line)
                if direction == "Right":
                    merged.reverse()
                if self.board[r] != merged:
                    moved = True
                self.board[r] = merged
        return moved

    def can_move(self):
        for r in range(4):
            for c in range(4):
                if self.board[r][c] == 0:
                    return True
                if c < 3 and self.board[r][c] == self.board[r][c + 1]:
                    return True
                if r < 3 and self.board[r][c] == self.board[r + 1][c]:
                    return True
        return False

    def end_game(self):
        # Stop the background music and play the game over sound
        pygame.mixer.music.stop()
        self.game_over_sound.play()  # Play the game over sound effect

        # Update high score if the current score is higher than the stored high score
        if self.score > self.high_score:
            self.high_score = self.score

        self.game_over_label = tk.Label(self.main_frame, text="Game Over!", font=("Helvetica", 24), fg="red", bg="black")
        self.game_over_label.grid(row=4, column=0, columnspan=4)

        # Create and display the Retry button only if the game is over
        if not self.retry_button:
            self.retry_button = tk.Button(self.main_frame, text="Retry", font=("Helvetica", 16), command=self.retry_game)
            self.retry_button.grid(row=5, column=0, columnspan=4, pady=10)

        self.window.unbind("<Key>")

    def retry_game(self):
        # Remove the "Game Over" label and Retry button before restarting
        if self.game_over_label:
            self.game_over_label.grid_forget()
            self.game_over_label = None  # Reset the reference to the label

        if self.retry_button:
            self.retry_button.grid_forget()  # Hide the Retry button
            self.retry_button = None  # Reset the reference to the button

        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()
        self.update_ui()

        # Restart the background music when retrying
        pygame.mixer.music.play(-1, 0.0)  # Loop the music infinitely
        self.window.bind("<Key>", self.handle_keypress)


if __name__ == "__main__":
    Game2048()
