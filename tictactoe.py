import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
GRID_SIZE = 3
CELL_SIZE = 180
GRID_WIDTH = CELL_SIZE * GRID_SIZE
GRID_HEIGHT = CELL_SIZE * GRID_SIZE
GRID_X = (WINDOW_WIDTH - GRID_WIDTH) // 2
GRID_Y = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# Create the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Fonts
title_font = pygame.font.Font(None, 48)
font = pygame.font.Font(None, 120)
button_font = pygame.font.Font(None, 36)
status_font = pygame.font.Font(None, 32)

class TicTacToe:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.player_score = 0
        self.computer_score = 0
        self.ties = 0
        
    def reset_game(self):
        """Reset the game board"""
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
    
    def draw_grid(self, screen):
        """Draw the tic-tac-toe grid"""
        # Draw background
        grid_rect = pygame.Rect(GRID_X, GRID_Y, GRID_WIDTH, GRID_HEIGHT)
        pygame.draw.rect(screen, WHITE, grid_rect)
        
        # Draw grid lines
        for i in range(1, 3):
            # Vertical lines
            start_x = GRID_X + i * CELL_SIZE
            pygame.draw.line(screen, BLACK, (start_x, GRID_Y), 
                           (start_x, GRID_Y + GRID_HEIGHT), 3)
            
            # Horizontal lines
            start_y = GRID_Y + i * CELL_SIZE
            pygame.draw.line(screen, BLACK, (GRID_X, start_y), 
                           (GRID_X + GRID_WIDTH, start_y), 3)
        
        # Draw border
        pygame.draw.rect(screen, BLACK, grid_rect, 3)
    
    def draw_symbols(self, screen):
        """Draw X's and O's on the board"""
        for row in range(3):
            for col in range(3):
                if self.board[row][col]:
                    cell_x = GRID_X + col * CELL_SIZE
                    cell_y = GRID_Y + row * CELL_SIZE
                    
                    symbol = self.board[row][col]
                    color = BLUE if symbol == 'X' else RED
                    
                    text = font.render(symbol, True, color)
                    text_rect = text.get_rect()
                    text_rect.center = (cell_x + CELL_SIZE // 2, cell_y + CELL_SIZE // 2)
                    screen.blit(text, text_rect)
    
    def draw_ui(self, screen):
        """Draw the user interface"""
        # Title
        title_text = title_font.render("Tic Tac Toe", True, BLACK)
        title_rect = title_text.get_rect()
        title_rect.centerx = WINDOW_WIDTH // 2
        title_rect.y = 10
        screen.blit(title_text, title_rect)
        
        # Current player or game status
        if self.game_over:
            if self.winner:
                if self.winner == 'X':
                    status_text = "You Win!"
                    color = GREEN
                else:
                    status_text = "Computer Wins!"
                    color = RED
            else:
                status_text = "It's a Tie!"
                color = GRAY
        else:
            if self.current_player == 'X':
                status_text = "Your Turn (X)"
                color = BLUE
            else:
                status_text = "Computer's Turn (O)"
                color = RED
        
        status_surface = status_font.render(status_text, True, color)
        status_rect = status_surface.get_rect()
        status_rect.centerx = WINDOW_WIDTH // 2
        status_rect.y = GRID_Y + GRID_HEIGHT + 20
        screen.blit(status_surface, status_rect)
        
        # Score
        score_text = f"You: {self.player_score}  Computer: {self.computer_score}  Ties: {self.ties}"
        score_surface = status_font.render(score_text, True, BLACK)
        score_rect = score_surface.get_rect()
        score_rect.centerx = WINDOW_WIDTH // 2
        score_rect.y = GRID_Y + GRID_HEIGHT + 60
        screen.blit(score_surface, score_rect)
        
        # Reset button
        self.reset_button = pygame.Rect(WINDOW_WIDTH // 2 - 75, GRID_Y + GRID_HEIGHT + 100, 150, 40)
        button_color = LIGHT_GRAY if self.game_over else GRAY
        pygame.draw.rect(screen, button_color, self.reset_button)
        pygame.draw.rect(screen, BLACK, self.reset_button, 2)
        
        button_text = button_font.render("New Game", True, BLACK)
        button_rect = button_text.get_rect()
        button_rect.center = self.reset_button.center
        screen.blit(button_text, button_rect)
    
    def get_cell_from_mouse(self, pos):
        """Convert mouse position to board cell"""
        x, y = pos
        if GRID_X <= x < GRID_X + GRID_WIDTH and GRID_Y <= y < GRID_Y + GRID_HEIGHT:
            col = (x - GRID_X) // CELL_SIZE
            row = (y - GRID_Y) // CELL_SIZE
            return (row, col)
        return None
    
    def handle_click(self, pos):
        """Handle mouse click"""
        # Check reset button
        if hasattr(self, 'reset_button') and self.reset_button.collidepoint(pos):
            self.reset_game()
            return
        
        if self.game_over or self.current_player != 'X':
            return
        
        cell = self.get_cell_from_mouse(pos)
        if cell:
            row, col = cell
            if self.board[row][col] == '':
                self.make_move(row, col, 'X')
                
                if not self.game_over:
                    self.current_player = 'O'
                    # Add a small delay before computer move
                    pygame.display.flip()
                    pygame.time.wait(500)
                    self.computer_move()
    
    def make_move(self, row, col, player):
        """Make a move on the board"""
        self.board[row][col] = player
        
        # Check for winner
        if self.check_winner():
            self.game_over = True
            self.winner = player
            if player == 'X':
                self.player_score += 1
            else:
                self.computer_score += 1
        elif self.is_board_full():
            self.game_over = True
            self.winner = None
            self.ties += 1
        else:
            self.current_player = 'X' if player == 'O' else 'O'
    
    def computer_move(self):
        """Make computer move using minimax algorithm"""
        if self.game_over:
            return
        
        best_score = float('-inf')
        best_move = None
        
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    self.board[row][col] = 'O'
                    score = self.minimax(0, False)
                    self.board[row][col] = ''
                    
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        
        if best_move:
            row, col = best_move
            self.make_move(row, col, 'O')
    
    def minimax(self, depth, is_maximizing):
        """Minimax algorithm for computer AI"""
        winner = self.check_winner()
        
        if winner == 'O':
            return 1
        elif winner == 'X':
            return -1
        elif self.is_board_full():
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == '':
                        self.board[row][col] = 'O'
                        score = self.minimax(depth + 1, False)
                        self.board[row][col] = ''
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == '':
                        self.board[row][col] = 'X'
                        score = self.minimax(depth + 1, True)
                        self.board[row][col] = ''
                        best_score = min(score, best_score)
            return best_score
    
    def check_winner(self):
        """Check if there's a winner"""
        # Check rows
        for row in range(3):
            if (self.board[row][0] == self.board[row][1] == self.board[row][2] != ''):
                return self.board[row][0]
        
        # Check columns
        for col in range(3):
            if (self.board[0][col] == self.board[1][col] == self.board[2][col] != ''):
                return self.board[0][col]
        
        # Check diagonals
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] != ''):
            return self.board[0][0]
        
        if (self.board[0][2] == self.board[1][1] == self.board[2][0] != ''):
            return self.board[0][2]
        
        return None
    
    def is_board_full(self):
        """Check if the board is full"""
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    return False
        return True

def main():
    clock = pygame.time.Clock()
    game = TicTacToe()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    game.handle_click(event.pos)
        
        # Clear screen
        screen.fill(WHITE)
        
        # Draw game
        game.draw_grid(screen)
        game.draw_symbols(screen)
        game.draw_ui(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()