import pygame
import random
import sys
import time # Added for debugging pauses, good for Pygame too

# --- Pygame Initialization ---
pygame.init()

# --- Screen Dimensions ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cricket Game")

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0) # For background
RED = (200, 0, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)
GREY = (100, 100, 100)

# --- Fonts ---
font_large = pygame.font.Font(None, 74) # For major scores
font_medium = pygame.font.Font(None, 50) # For messages
font_small = pygame.font.Font(None, 36) # For details

# --- Game Variables ---
team1_name = "CSK"
team2_name = "RCB"

team1_letter = "CSK"
team2_letter = "RCB"

total_overs = 5 # Default overs

# Game State Management
GAME_STATE_INTRO = 0
GAME_STATE_PLAYING_INNING1 = 1
GAME_STATE_TRANSITION_INNINGS = 2 # New state for transition message
GAME_STATE_PLAYING_INNING2 = 3
GAME_STATE_GAME_OVER = 4
current_game_state = GAME_STATE_INTRO

# Cricket Game Variables (will be reset for each match)
current_batting_team_name = ""
current_bowling_team_name = ""
current_batting_letter = ""
current_bowling_letter = ""

team1_score = {'runs': 0, 'wickets': 0}
team2_score = {'runs': 0, 'wickets': 0}

current_runs = 0
current_wickets = 0
current_balls_bowled = 0
current_over_balls = 0
current_over_number = 0
first_inning_score = 0
target_score = 0
match_result_message = ""

# Game control flags
ball_outcome_displayed = False
waiting_for_ball = True
inning_transition_timer_active = False # For the new transition state

# --- Functions ---

def reset_inning_variables():
    """Resets variables specific to an inning."""
    global current_runs, current_wickets, current_balls_bowled, current_over_balls, current_over_number
    global ball_outcome_displayed, waiting_for_ball, match_result_message

    current_runs = 0
    current_wickets = 0
    current_balls_bowled = 0
    current_over_balls = 0
    current_over_number = 0
    ball_outcome_displayed = False
    waiting_for_ball = True
    match_result_message = "" # Clear message for new inning

def draw_text(surface, text, font, color, x, y, center=False):
    """Helper to draw text on the screen."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def draw_button(surface, text, font, rect, color, hover_color):
    """Helper to draw a button and check for hover."""
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = rect.collidepoint(mouse_pos)
    current_color = hover_color if is_hovered else color

    pygame.draw.rect(surface, current_color, rect, border_radius=10)
    pygame.draw.rect(surface, BLACK, rect, 2, border_radius=10) # Border

    draw_text(surface, text, font, WHITE, rect.centerx, rect.centery, center=True)
    return is_hovered

def play_ball():
    """Simulates one ball being bowled."""
    global current_runs, current_wickets, current_balls_bowled, current_over_balls, ball_outcome_displayed, current_over_number, match_result_message

    if current_wickets >= 10: # Should ideally be checked before calling play_ball
        match_result_message = f"{current_batting_team_name} All Out!"
        return

    outcome = random.randint(0, 7) # 0-6 runs, 7 for wicket
    current_balls_bowled += 1
    current_over_balls += 1

    if outcome == 7:
        current_wickets += 1
        match_result_message = f"OUT! {current_wickets} wicket(s) down."
    else:
        runs_on_ball = outcome
        current_runs += runs_on_ball
        match_result_message = f"{runs_on_ball} runs!"

    if current_over_balls == 6:
        current_over_number += 1
        current_over_balls = 0
        if current_over_number < total_overs:
            match_result_message += f" | Over {current_over_number} Complete."
        else:
            match_result_message += f" | Innings End!"

    ball_outcome_displayed = True


# --- Game Loop ---
running = True
clock = pygame.time.Clock()

# Buttons for start screen
start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 70)
quit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90, 200, 70)

# Button for bowling
bowl_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 100, 150, 60)

# Button for next inning/game over (re-used)
continue_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 100, 300, 60)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left mouse button
                if current_game_state == GAME_STATE_INTRO:
                    if start_button_rect.collidepoint(event.pos):
                        # Reset scores for new match
                        team1_score = {'runs': 0, 'wickets': 0}
                        team2_score = {'runs': 0, 'wickets': 0}
                        reset_inning_variables() # Reset inning-specific variables

                        # Simulate toss
                        if random.choice([True, False]):
                            current_batting_team_name = team1_name
                            current_bowling_team_name = team2_name
                            current_batting_letter = team1_letter
                            current_bowling_letter = team2_letter
                        else:
                            current_batting_team_name = team2_name
                            current_bowling_team_name = team1_name
                            current_batting_letter = team2_letter
                            current_bowling_letter = team1_letter

                        match_result_message = f"{current_batting_team_name} won the toss and will bat first!"
                        current_game_state = GAME_STATE_PLAYING_INNING1
                        waiting_for_ball = True # Ensure ready for first ball
                        pygame.time.set_timer(pygame.USEREVENT + 1, 3000) # Show toss message for 3 secs
                    elif quit_button_rect.collidepoint(event.pos):
                        running = False
                elif current_game_state in [GAME_STATE_PLAYING_INNING1, GAME_STATE_PLAYING_INNING2]:
                    # Check if allowed to bowl (inning not over, waiting for click, button clicked)
                    can_bowl = waiting_for_ball and current_wickets < 10 and current_over_number < total_overs
                    if can_bowl and bowl_button_rect.collidepoint(event.pos):
                        play_ball()
                        waiting_for_ball = False # Prevent multiple bowls per click
                        pygame.time.set_timer(pygame.USEREVENT + 1, 1500) # Set timer to reset outcome display after 1.5 seconds
                elif current_game_state == GAME_STATE_TRANSITION_INNINGS:
                    if continue_button_rect.collidepoint(event.pos):
                        pygame.time.set_timer(pygame.USEREVENT + 2, 0) # Stop transition timer
                        inning_transition_timer_active = False # Deactivate flag
                        reset_inning_variables() # Reset for second inning
                        current_game_state = GAME_STATE_PLAYING_INNING2 # Switch to second inning state
                elif current_game_state == GAME_STATE_GAME_OVER:
                    if continue_button_rect.collidepoint(event.pos):
                        current_game_state = GAME_STATE_INTRO # Go back to main menu

        # Timer events for controlling message display
        if event.type == pygame.USEREVENT + 1: # Custom event for ball outcome display timer
            ball_outcome_displayed = False
            match_result_message = "" # Clear temporary ball outcome message
            waiting_for_ball = True # Allow next ball to be bowled
            pygame.time.set_timer(pygame.USEREVENT + 1, 0) # Stop the timer

        if event.type == pygame.USEREVENT + 2: # Custom event for inning transition timer
            if current_game_state == GAME_STATE_TRANSITION_INNINGS:
                inning_transition_timer_active = False
                reset_inning_variables() # Reset for second inning
                current_game_state = GAME_STATE_PLAYING_INNING2 # Switch to second inning state
            pygame.time.set_timer(pygame.USEREVENT + 2, 0) # Stop the timer


    # --- Drawing ---
    screen.fill(GREEN) # Fill background

    if current_game_state == GAME_STATE_INTRO:
        draw_text(screen, "Pygame Cricket Game", font_large, YELLOW, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, center=True)
        draw_text(screen, f"Teams: {team1_name} vs {team2_name}", font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 70, center=True)
        draw_text(screen, f"Overs: {total_overs}", font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 120, center=True)

        draw_button(screen, "Start Game", font_medium, start_button_rect, BLUE, (0, 0, 255))
        draw_button(screen, "Quit", font_medium, quit_button_rect, RED, (255, 0, 0))

    elif current_game_state in [GAME_STATE_PLAYING_INNING1, GAME_STATE_PLAYING_INNING2]:
        # --- Display Players (Letters) ---
        draw_text(screen, current_batting_letter, font_large, YELLOW, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 50, center=True)
        draw_text(screen, "BATSMAN", font_small, WHITE, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 100, center=True)

        draw_text(screen, current_bowling_letter, font_large, BLUE, SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT // 2 + 50, center=True)
        draw_text(screen, "BOWLER", font_small, WHITE, SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT // 2 + 100, center=True)

        # Draw a simple pitch line
        pygame.draw.line(screen, GREY, (SCREEN_WIDTH // 4 + 50, SCREEN_HEIGHT // 2 + 150),
                                      (SCREEN_WIDTH * 3 // 4 - 50, SCREEN_HEIGHT // 2 + 150), 5)


        # Display Current Score
        inning_display_text = "1st Inning" if current_game_state == GAME_STATE_PLAYING_INNING1 else "2nd Inning"
        draw_text(screen, f"{inning_display_text}: {current_batting_team_name} Batting", font_medium, YELLOW, SCREEN_WIDTH // 2, 50, center=True)
        draw_text(screen, f"Score: {current_runs}/{current_wickets}", font_large, WHITE, SCREEN_WIDTH // 2, 150, center=True)
        draw_text(screen, f"Overs: {current_over_number}.{current_over_balls} / {total_overs}", font_medium, WHITE, SCREEN_WIDTH // 2, 220, center=True)

        if current_game_state == GAME_STATE_PLAYING_INNING2:
            draw_text(screen, f"Target: {target_score}", font_medium, YELLOW, SCREEN_WIDTH // 2, 280, center=True)

        # Display last ball outcome or general message
        if match_result_message and ball_outcome_displayed:
            draw_text(screen, match_result_message, font_medium, YELLOW, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, center=True)
        elif waiting_for_ball:
            draw_text(screen, "Click 'Bowl Ball'!", font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, center=True)

        # Bowl Button logic
        can_bowl_now = waiting_for_ball and current_wickets < 10 and current_over_number < total_overs
        if can_bowl_now:
            draw_button(screen, "Bowl Ball", font_medium, bowl_button_rect, BLUE, (0, 0, 255))
        else:
            # Display 'Inning Over' if conditions met
            pygame.draw.rect(screen, GREY, bowl_button_rect, border_radius=10) # Greyed out
            draw_text(screen, "Inning Over", font_medium, BLACK, bowl_button_rect.centerx, bowl_button_rect.centery, center=True)


        # --- Inning End / Game Over Checks ---
        inning_over_condition = (current_wickets >= 10) or (current_over_number == total_overs and current_over_balls == 0 and not waiting_for_ball)

        if current_game_state == GAME_STATE_PLAYING_INNING1 and inning_over_condition:
            # Save first inning score
            if current_batting_team_name == team1_name:
                team1_score['runs'] = current_runs
                team1_score['wickets'] = current_wickets
            else:
                team2_score['runs'] = current_runs
                team2_score['wickets'] = current_wickets

            first_inning_score = current_runs
            target_score = first_inning_score + 1

            # Prepare for second inning: switch teams
            if current_batting_team_name == team1_name:
                current_batting_team_name = team2_name
                current_bowling_team_name = team1_name
                current_batting_letter = team2_letter
                current_bowling_letter = team1_letter
            else:
                current_batting_team_name = team1_name
                current_bowling_team_name = team2_name
                current_batting_letter = team1_letter
                current_bowling_letter = team2_letter

            match_result_message = f"{current_bowling_team_name} set a target of {target_score} for {current_batting_team_name}"
            current_game_state = GAME_STATE_TRANSITION_INNINGS
            pygame.time.set_timer(pygame.USEREVENT + 2, 3000) # Show transition message for 3 secs
            inning_transition_timer_active = True

        elif current_game_state == GAME_STATE_PLAYING_INNING2 and (current_runs >= target_score or inning_over_condition):
            # Save second inning score
            if current_batting_team_name == team1_name:
                team1_score['runs'] = current_runs
                team1_score['wickets'] = current_wickets
            else:
                team2_score['runs'] = current_runs
                team2_score['wickets'] = current_wickets

            # Determine winner
            if team1_score['runs'] > team2_score['runs']:
                if first_inning_score == team1_score['runs']: # Team 1 batted first
                    match_result_message = f"{team1_name} wins by {team1_score['runs'] - team2_score['runs']} runs!"
                else: # Team 1 batted second and chased
                    match_result_message = f"{team1_name} wins by {10 - team1_score['wickets']} wickets!"
            elif team2_score['runs'] > team1_score['runs']:
                if first_inning_score == team2_score['runs']: # Team 2 batted first
                    match_result_message = f"{team2_name} wins by {team2_score['runs'] - team1_score['runs']} runs!"
                else: # Team 2 batted second and chased
                    match_result_message = f"{team2_name} wins by {10 - team2_score['wickets']} wickets!"
            else:
                match_result_message = "It's a TIE!" # Scores are equal

            current_game_state = GAME_STATE_GAME_OVER

    elif current_game_state == GAME_STATE_TRANSITION_INNINGS:
        draw_text(screen, "Inning Break", font_large, YELLOW, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, center=True)
        draw_text(screen, f"Previous Score: {first_inning_score} runs", font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 70, center=True)
        draw_text(screen, match_result_message, font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
        if not inning_transition_timer_active: # Allow manual skip if timer not active
            draw_button(screen, "Continue to 2nd Inning", font_medium, continue_button_rect, BLUE, (0, 0, 255))

    elif current_game_state == GAME_STATE_GAME_OVER:
        draw_text(screen, "Game Over!", font_large, YELLOW, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, center=True)
        draw_text(screen, match_result_message, font_medium, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
        draw_button(screen, "Play Again / Main Menu", font_medium, continue_button_rect, BLUE, (0, 0, 255))


    pygame.display.flip()
    clock.tick(60) # Limit frame rate to 60 FPS

pygame.quit()
sys.exit()