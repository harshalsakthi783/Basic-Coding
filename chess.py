import pygame
import sys
import random
import copy

# Initialize Pygame
pygame.init()

# Constants
BOARD_SIZE = 640
SQUARE_SIZE = BOARD_SIZE // 8
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
HIGHLIGHT = (255, 255, 0, 128)
SELECTED = (0, 255, 0, 128)
POSSIBLE_MOVE = (0, 0, 255, 128)

# Create the display
screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE + 100))
pygame.display.set_caption("Chess Game")

# Font for text
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

class ChessGame:
    def __init__(self):
        self.board = self.create_initial_board()
        self.current_player = 'white'
        self.selected_square = None
        self.possible_moves = []
        self.game_over = False
        self.winner = None
        self.move_history = []
        
        # Letter chess pieces
        self.piece_symbols = {
            'K': 'K', 'Q': 'Q', 'R': 'R', 'B': 'B', 'N': 'N', 'P': 'P',
            'k': 'k', 'q': 'q', 'r': 'r', 'b': 'b', 'n': 'n', 'p': 'p'
        }
        
    def create_initial_board(self):
        """Create the initial chess board setup"""
        board = [[None for _ in range(8)] for _ in range(8)]
        
        # Place white pieces
        board[7] = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        board[6] = ['P'] * 8
        
        # Place black pieces
        board[0] = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        board[1] = ['p'] * 8
        
        return board
    
    def draw_board(self, screen):
        """Draw the chess board"""
        for row in range(8):
            for col in range(8):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, color, rect)
                
                # Draw pieces
                piece = self.board[row][col]
                if piece:
                    piece_color = (255, 255, 255) if piece.isupper() else (0, 0, 0)
                    piece_text = font.render(self.piece_symbols[piece], True, piece_color)
                    piece_rect = piece_text.get_rect()
                    piece_rect.center = rect.center
                    screen.blit(piece_text, piece_rect)
        
        # Highlight selected square
        if self.selected_square:
            row, col = self.selected_square
            highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            highlight_surface.fill(SELECTED)
            screen.blit(highlight_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))
        
        # Highlight possible moves
        for row, col in self.possible_moves:
            highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            highlight_surface.fill(POSSIBLE_MOVE)
            screen.blit(highlight_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))
    
    def draw_ui(self, screen):
        """Draw game UI"""
        ui_rect = pygame.Rect(0, BOARD_SIZE, BOARD_SIZE, 100)
        pygame.draw.rect(screen, (50, 50, 50), ui_rect)
        
        # Current player
        player_text = f"Current Player: {self.current_player.capitalize()}"
        text_surface = small_font.render(player_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, BOARD_SIZE + 10))
        
        # Game status
        if self.game_over:
            status_text = f"Game Over! Winner: {self.winner}" if self.winner else "Game Over! Stalemate"
            status_surface = small_font.render(status_text, True, (255, 255, 0))
            screen.blit(status_surface, (10, BOARD_SIZE + 40))
        elif self.is_in_check(self.current_player):
            check_text = "Check!"
            check_surface = small_font.render(check_text, True, (255, 0, 0))
            screen.blit(check_surface, (10, BOARD_SIZE + 40))
        
        # Instructions
        instr_text = "Click to select piece, click again to move"
        instr_surface = small_font.render(instr_text, True, (200, 200, 200))
        screen.blit(instr_surface, (10, BOARD_SIZE + 70))
    
    def get_square_from_mouse(self, pos):
        """Convert mouse position to board square"""
        x, y = pos
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            col = x // SQUARE_SIZE
            row = y // SQUARE_SIZE
            return (row, col)
        return None
    
    def handle_click(self, pos):
        """Handle mouse click on the board"""
        if self.game_over:
            return
        
        square = self.get_square_from_mouse(pos)
        if not square:
            return
        
        row, col = square
        
        # If no square is selected, select this square if it has player's piece
        if self.selected_square is None:
            piece = self.board[row][col]
            if piece and self.is_own_piece(piece, self.current_player):
                self.selected_square = (row, col)
                self.possible_moves = self.get_piece_moves(row, col, self.current_player)
        else:
            # If clicking on the same square, deselect
            if self.selected_square == (row, col):
                self.selected_square = None
                self.possible_moves = []
            # If clicking on a possible move, make the move
            elif (row, col) in self.possible_moves:
                self.make_move(self.selected_square[0], self.selected_square[1], row, col)
                self.selected_square = None
                self.possible_moves = []
                
                # Switch to computer's turn
                if not self.game_over:
                    self.current_player = 'black'
                    pygame.display.flip()
                    pygame.time.wait(500)  # Brief pause before computer move
                    self.computer_move()
            # If clicking on another own piece, select it
            else:
                piece = self.board[row][col]
                if piece and self.is_own_piece(piece, self.current_player):
                    self.selected_square = (row, col)
                    self.possible_moves = self.get_piece_moves(row, col, self.current_player)
                else:
                    self.selected_square = None
                    self.possible_moves = []
    
    def make_move(self, from_row, from_col, to_row, to_col):
        """Make a move on the board"""
        # Record the move
        piece = self.board[from_row][from_col]
        captured = self.board[to_row][to_col]
        
        # Make the move
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        
        # Pawn promotion (simple - always promote to queen)
        if piece and piece.lower() == 'p':
            if (piece.isupper() and to_row == 0) or (piece.islower() and to_row == 7):
                self.board[to_row][to_col] = 'Q' if piece.isupper() else 'q'
        
        # Switch players and check game state
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        self.check_game_over()
    
    def computer_move(self):
        """Make a computer move"""
        if self.game_over:
            return
        
        # Get all possible moves for computer (black)
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and self.is_own_piece(piece, 'black'):
                    moves = self.get_piece_moves(row, col, 'black')
                    for move in moves:
                        all_moves.append((row, col, move[0], move[1]))
        
        if all_moves:
            # Simple AI - prioritize captures, then random moves
            capture_moves = []
            for move in all_moves:
                from_row, from_col, to_row, to_col = move
                if self.board[to_row][to_col] is not None:
                    capture_moves.append(move)
            
            chosen_move = random.choice(capture_moves if capture_moves else all_moves)
            from_row, from_col, to_row, to_col = chosen_move
            self.make_move(from_row, from_col, to_row, to_col)
    
    def is_own_piece(self, piece, player):
        """Check if piece belongs to current player"""
        if player == 'white':
            return piece.isupper()
        else:
            return piece.islower()
    
    def is_enemy_piece(self, piece, player):
        """Check if piece belongs to opponent"""
        if player == 'white':
            return piece.islower()
        else:
            return piece.isupper()
    
    def is_valid_position(self, row, col):
        """Check if position is within board bounds"""
        return 0 <= row < 8 and 0 <= col < 8
    
    def get_piece_moves(self, row, col, player):
        """Get all possible moves for a piece"""
        piece = self.board[row][col]
        if not piece or not self.is_own_piece(piece, player):
            return []
        
        piece_type = piece.lower()
        moves = []
        
        if piece_type == 'p':
            moves = self.get_pawn_moves(row, col, player)
        elif piece_type == 'r':
            moves = self.get_rook_moves(row, col, player)
        elif piece_type == 'n':
            moves = self.get_knight_moves(row, col, player)
        elif piece_type == 'b':
            moves = self.get_bishop_moves(row, col, player)
        elif piece_type == 'q':
            moves = self.get_queen_moves(row, col, player)
        elif piece_type == 'k':
            moves = self.get_king_moves(row, col, player)
        
        # Filter out moves that would put own king in check
        valid_moves = []
        for move in moves:
            if not self.would_be_in_check_after_move(row, col, move[0], move[1], player):
                valid_moves.append(move)
        
        return valid_moves
    
    def get_pawn_moves(self, row, col, player):
        """Get possible pawn moves"""
        moves = []
        direction = -1 if player == 'white' else 1
        start_row = 6 if player == 'white' else 1
        
        # Move forward one square
        new_row = row + direction
        if self.is_valid_position(new_row, col) and self.board[new_row][col] is None:
            moves.append((new_row, col))
            
            # Move forward two squares from starting position
            if row == start_row and self.board[new_row + direction][col] is None:
                moves.append((new_row + direction, col))
        
        # Capture diagonally
        for dc in [-1, 1]:
            new_row, new_col = row + direction, col + dc
            if self.is_valid_position(new_row, new_col):
                target = self.board[new_row][new_col]
                if target and self.is_enemy_piece(target, player):
                    moves.append((new_row, new_col))
        
        return moves
    
    def get_rook_moves(self, row, col, player):
        """Get possible rook moves"""
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + i * dr, col + i * dc
                if not self.is_valid_position(new_row, new_col):
                    break
                
                target = self.board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                elif self.is_enemy_piece(target, player):
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves
    
    def get_knight_moves(self, row, col, player):
        """Get possible knight moves"""
        moves = []
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), 
                       (1, -2), (1, 2), (2, -1), (2, 1)]
        
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_position(new_row, new_col):
                target = self.board[new_row][new_col]
                if target is None or self.is_enemy_piece(target, player):
                    moves.append((new_row, new_col))
        
        return moves
    
    def get_bishop_moves(self, row, col, player):
        """Get possible bishop moves"""
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + i * dr, col + i * dc
                if not self.is_valid_position(new_row, new_col):
                    break
                
                target = self.board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                elif self.is_enemy_piece(target, player):
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves
    
    def get_queen_moves(self, row, col, player):
        """Get possible queen moves (combination of rook and bishop)"""
        return self.get_rook_moves(row, col, player) + self.get_bishop_moves(row, col, player)
    
    def get_king_moves(self, row, col, player):
        """Get possible king moves"""
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), 
                     (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_position(new_row, new_col):
                target = self.board[new_row][new_col]
                if target is None or self.is_enemy_piece(target, player):
                    moves.append((new_row, new_col))
        
        return moves
    
    def find_king(self, player):
        """Find the king's position for the given player"""
        king_piece = 'K' if player == 'white' else 'k'
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == king_piece:
                    return (i, j)
        return None
    
    def is_in_check(self, player):
        """Check if the player's king is in check"""
        king_pos = self.find_king(player)
        if not king_pos:
            return False
        
        opponent = 'black' if player == 'white' else 'white'
        
        # Check if any opponent piece can attack the king
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece and self.is_own_piece(piece, opponent):
                    moves = self.get_piece_moves_raw(i, j, opponent)
                    if king_pos in moves:
                        return True
        
        return False
    
    def get_piece_moves_raw(self, row, col, player):
        """Get piece moves without check validation to avoid recursion"""
        piece = self.board[row][col]
        if not piece or not self.is_own_piece(piece, player):
            return []
        
        piece_type = piece.lower()
        
        if piece_type == 'p':
            return self.get_pawn_moves(row, col, player)
        elif piece_type == 'r':
            return self.get_rook_moves(row, col, player)
        elif piece_type == 'n':
            return self.get_knight_moves(row, col, player)
        elif piece_type == 'b':
            return self.get_bishop_moves(row, col, player)
        elif piece_type == 'q':
            return self.get_queen_moves(row, col, player)
        elif piece_type == 'k':
            return self.get_king_moves(row, col, player)
        
        return []
    
    def would_be_in_check_after_move(self, from_row, from_col, to_row, to_col, player):
        """Check if player would be in check after making a move"""
        # Make the move temporarily
        original_piece = self.board[to_row][to_col]
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = None
        
        # Check if in check
        in_check = self.is_in_check(player)
        
        # Undo the move
        self.board[from_row][from_col] = self.board[to_row][to_col]
        self.board[to_row][to_col] = original_piece
        
        return in_check
    
    def get_all_possible_moves(self, player):
        """Get all possible moves for a player"""
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and self.is_own_piece(piece, player):
                    moves = self.get_piece_moves(row, col, player)
                    for move in moves:
                        all_moves.append((row, col, move[0], move[1]))
        return all_moves
    
    def check_game_over(self):
        """Check if the game is over"""
        # Check if current player has any legal moves
        possible_moves = self.get_all_possible_moves(self.current_player)
        
        if not possible_moves:
            if self.is_in_check(self.current_player):
                # Checkmate
                self.game_over = True
                self.winner = 'black' if self.current_player == 'white' else 'white'
            else:
                # Stalemate
                self.game_over = True
                self.winner = None

def main():
    clock = pygame.time.Clock()
    game = ChessGame()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    game.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game.game_over:
                    # Reset game
                    game = ChessGame()
        
        # Clear screen
        screen.fill((0, 0, 0))
        
        # Draw game
        game.draw_board(screen)
        game.draw_ui(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()