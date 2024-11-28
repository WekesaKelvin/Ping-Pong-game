import pygame
import sys
import time
import random
import json
import tkinter as tk
from tkinter import messagebox

# initializing pygame module
pygame.init()
clock = pygame.time.Clock()

# loading sound effects
hit_sound = pygame.mixer.Sound("Sound/hit_sound.wav")
score_sound = pygame.mixer.Sound("Sound/score_sound.wav")

# initializing game scores
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)

# Colors
bg_color = pygame.Color("grey12")
light_grey = (200, 200, 200)
button_color = (50, 150, 255)
text_color = (255, 255, 255)

# Game over flag
game_over = False

# setting up the main window
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# Defining Game elements
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

# Ball and paddle speeds
original_speed_x = 7
original_speed_y = 7
ball_speed_x = original_speed_x
ball_speed_y = original_speed_y
player_speed = 0
opponent_speed = 0

# Difficulty levels
difficulty_speed_map = {
    "Easy": 5,
    "Medium": 6,
    "Hard": 9,
}

scores = {
    "Multiplayer": {"player": 0, "opponent": 0},
    "Singleplayer": {"player": 0, "opponent": 0},
    "Online": {"player": 0, "opponent": 0},
}

# Difficulty levels
difficulty_modes = ["Easy", "Medium", "Hard"]

# High scores dictionary
high_scores = {"Easy": 0, "Medium": 0, "Hard": 0}

# File path to store high scores
high_scores_file = "high_scores.json"

# Game modes
game_mode = "Multiplayer"

# Load high scores from the file
def load_high_scores():
    global high_scores
    try:
        with open(high_scores_file, "r") as file:
            high_scores = json.load(file)
    except FileNotFoundError:
        save_high_scores()

# Save high scores to the file
def save_high_scores(current_difficulty):
    # Save only the high score for the specified difficulty mode
    with open(high_scores_file, "w") as file:
        json.dump(high_scores, file)  # Save the entire high_scores dictionary

# Save  scores to the file
def save_scores():
    with open(high_scores_file, "w") as file:
        json.dump(high_scores, file)

# Function for resetting the game
def reset_game(mode):
    global ball_speed_x, ball_speed_y
    scores[mode]["player"] = 0
    scores[mode]["opponent"] = 0
    ball_restart()
# Function to draw the back button
def draw_back_button():
    back_button_rect = pygame.Rect(10, 10, 100, 40)  # Position and size of the button
    pygame.draw.rect(screen, RED, back_button_rect)  # Draw the button
    back_text = font.render("Back", True, WHITE)
    screen.blit(back_text, (back_button_rect.x + 20, back_button_rect.y + 5))  # Center the text

def show_menu():
    load_high_scores()
    global game_mode, computer_difficulty
    while True:
        screen.fill(bg_color)

        # Title text
        title_text = game_font.render("Ping Pong Menu", True, light_grey)
        screen.blit(title_text, (screen_width / 2 - title_text.get_width() / 2, screen_height / 2 - 200))

        # Menu options
        options = [
            ("1. Online", screen_height / 2 - 100),
            ("2. Multiplayer", screen_height / 2 - 50),
            ("3. Single-player vs Computer", screen_height / 2),
        ]

        # Display high scores (adjusted position)
        high_score_text = game_font.render(f"High Scores:", True, light_grey)
        screen.blit(high_score_text, (screen_width / 2 - high_score_text.get_width() / 2, screen_height / 2 + 50))

        # Start high score display
        y_offset = 40
        for difficulty in difficulty_modes:
            # Fetch score for each difficulty from high_scores
            score = high_scores.get(difficulty, 0)  # Default to 0 if no score exists
            score_text = game_font.render(f"{difficulty}: {score}", True, light_grey)
            screen.blit(score_text, (screen_width / 2 - score_text.get_width() / 2, screen_height / 2 + 50 + y_offset))
            y_offset += 40

        # "Reset High Scores" button below the high scores
        reset_button_text = game_font.render("Reset High Scores", True, light_grey)
        reset_button_width = reset_button_text.get_width() + 40  # Add padding
        reset_button_height = 40
        reset_button_rect = pygame.Rect(screen_width / 2 - reset_button_width / 2, screen_height / 2 + 50 + y_offset,
                                        reset_button_width, reset_button_height)

        # Create the button-like background for "Reset High Scores"
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if reset_button_rect.collidepoint(mouse_x, mouse_y):  # Hover effect
            pygame.draw.rect(screen, (50, 50, 50), reset_button_rect)  # Darker background when hovered
        else:
            pygame.draw.rect(screen, (70, 70, 70), reset_button_rect)  # Normal background

        # Render the text on the button
        screen.blit(reset_button_text, (reset_button_rect.x + (reset_button_width - reset_button_text.get_width()) / 2,
                                        reset_button_rect.y + (
                                                    reset_button_height - reset_button_text.get_height()) / 2))

        # Render the menu options
        for text, y in options:
            button_text = game_font.render(text, True, light_grey)
            button_width = button_text.get_width() + 40  # Add padding
            button_height = 40
            button_rect = pygame.Rect(screen_width / 2 - button_width / 2, y, button_width, button_height)

            # Create the button-like background
            if button_rect.collidepoint(mouse_x, mouse_y):  # Hover effect
                pygame.draw.rect(screen, (50, 50, 50), button_rect)  # Darker background when hovered
            else:
                pygame.draw.rect(screen, (70, 70, 70), button_rect)  # Normal background

            # Render the text on the button
            screen.blit(button_text, (button_rect.x + (button_width - button_text.get_width()) / 2,
                                      button_rect.y + (button_height - button_text.get_height()) / 2))


        # "Back" button at the top left
        back_button_text = game_font.render("Back", True, light_grey)
        back_button_width = back_button_text.get_width() + 20  # Add padding
        back_button_height = 40
        back_button_rect = pygame.Rect(20, 20, back_button_width, back_button_height)

        # Create the button-like background for "Back"
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if back_button_rect.collidepoint(mouse_x, mouse_y):  # Hover effect
            pygame.draw.rect(screen, (50, 50, 50), back_button_rect)  # Darker background when hovered
        else:
            pygame.draw.rect(screen, (70, 70, 70), back_button_rect)  # Normal background

        # Render the "Back" button text
        screen.blit(back_button_text, (back_button_rect.x + (back_button_width - back_button_text.get_width()) / 2,
                                       back_button_rect.y + (back_button_height - back_button_text.get_height()) / 2))



        # Draw the option buttons
        for text, y in options:
            button_text = game_font.render(text, True, light_grey)
            button_width = button_text.get_width() + 40  # Add padding
            button_height = 40
            button_rect = pygame.Rect(screen_width / 2 - button_width / 2, y, button_width, button_height)

            # Create the button-like background
            if button_rect.collidepoint(mouse_x, mouse_y):  # Hover effect
                pygame.draw.rect(screen, (50, 50, 50), button_rect)  # Darker background when hovered
            else:
                pygame.draw.rect(screen, (70, 70, 70), button_rect)  # Normal background

            # Render the text on the button
            screen.blit(button_text, (button_rect.x + (button_width - button_text.get_width()) / 2,
                                     button_rect.y + (button_height - button_text.get_height()) / 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Check if mouse is over the 'Back' button
                    if back_button_rect.collidepoint(mouse_x, mouse_y):
                        pygame.quit()
                        sys.exit()  # Go back to the previous menu

                    # Check if mouse is over the 'Reset High Scores' button
                    if reset_button_rect.collidepoint(mouse_x, mouse_y):
                        reset_high_scores()

                    # Check if mouse is over the 'Online' button
                    if options[0][1] <= mouse_y <= options[0][1] + 40 and button_rect.collidepoint(mouse_x, mouse_y):
                        game_mode = "Online"
                        reset_game(game_mode)
                        return
                    # Check if mouse is over the 'Multiplayer' button
                    elif screen_width / 2 - 150 <= mouse_x <= screen_width / 2 + 100 and screen_height / 2 - 50 <= mouse_y <= screen_height / 2:
                        game_mode = "Multiplayer"
                        reset_game(game_mode)
                        return
                    # Check if mouse is over the 'Single-player vs Computer' button
                    elif options[2][1] <= mouse_y <= options[2][1] + 40 and button_rect.collidepoint(mouse_x, mouse_y):
                        select_difficulty()
                        game_mode = "Singleplayer"
                        reset_game(game_mode)
                        return

def reset_high_scores():
    global high_scores
    # Reset all high scores to 0 for each difficulty
    high_scores = {
        "Easy": 0,
        "Medium": 0,
        "Hard": 0
    }
    save_scores()

def update_high_scores(current_difficulty):
    global high_scores
    # Ensure the difficulty exists in high_scores, initialize if missing
    if current_difficulty not in high_scores:
        high_scores[current_difficulty] = 0  # Default value in case of missing key

    if scores["Singleplayer"]["player"] > high_scores[current_difficulty]:
        high_scores[current_difficulty] = scores["Singleplayer"]["player"]
        save_high_scores(current_difficulty)  # Save high score for the current difficulty

def select_difficulty():
    global computer_difficulty
    while True:
        screen.fill(bg_color)

        # Title text for difficulty selection
        title_text = game_font.render("Select Difficulty", True, light_grey)
        screen.blit(title_text, (screen_width / 2 - title_text.get_width() / 2, screen_height / 2 - 200))

        # "Back" button at the top left
        back_button_text = game_font.render("Back", True, light_grey)
        back_button_width = back_button_text.get_width() + 20  # Add padding
        back_button_height = 40
        back_button_rect = pygame.Rect(20, 20, back_button_width, back_button_height)

        # Create the button-like background for "Back"
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if back_button_rect.collidepoint(mouse_x, mouse_y):  # Hover effect
            pygame.draw.rect(screen, (50, 50, 50), back_button_rect)  # Darker background when hovered
        else:
            pygame.draw.rect(screen, (70, 70, 70), back_button_rect)  # Normal background

        # Render the "Back" button text
        screen.blit(back_button_text, (back_button_rect.x + (back_button_width - back_button_text.get_width()) / 2,
                                       back_button_rect.y + (back_button_height - back_button_text.get_height()) / 2))

        # Difficulty options
        options = [
            ("1. Easy", screen_height / 2 - 100),
            ("2. Medium", screen_height / 2 - 50),
            ("3. Hard", screen_height / 2),
        ]

        # Draw the option buttons
        for text, y in options:
            button_text = game_font.render(text, True, light_grey)
            button_width = button_text.get_width() + 40  # Add padding
            button_height = 40
            button_rect = pygame.Rect(screen_width / 2 - button_width / 2, y, button_width, button_height)

            # Create the button-like background
            if button_rect.collidepoint(mouse_x, mouse_y):  # Hover effect
                pygame.draw.rect(screen, (50, 50, 50), button_rect)  # Darker background when hovered
            else:
                pygame.draw.rect(screen, (70, 70, 70), button_rect)  # Normal background

            # Render the text on the button
            screen.blit(button_text, (button_rect.x + (button_width - button_text.get_width()) / 2,
                                     button_rect.y + (button_height - button_text.get_height()) / 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Check if mouse is over the 'Back' button
                    if back_button_rect.collidepoint(mouse_x, mouse_y):
                        show_menu()
                        return

                    # Check if mouse is over the 'Easy' button
                    if screen_width / 2 - 150 <= mouse_x <= screen_width / 2 + 100 and screen_height / 2 - 100 <= mouse_y <= screen_height / 2 - 50:
                        computer_difficulty = "Easy"
                        return
                    # Check if mouse is over the 'Medium' button
                    elif screen_width / 2 - 150 <= mouse_x <= screen_width / 2 + 100 and screen_height / 2 - 50 <= mouse_y <= screen_height / 2:
                        computer_difficulty = "Medium"
                        return
                    # Check if mouse is over the 'Hard' button
                    elif options[2][1] <= mouse_y <= options[2][1] + 40 and button_rect.collidepoint(mouse_x, mouse_y):
                        computer_difficulty = "Hard"
                        return

def ball_animation():
    global ball_speed_x, ball_speed_y, opponent_score, player_score
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.right >= screen_width:  # Player scores
        scores[game_mode]["opponent"] += 1
        score_sound.play()
        ball_restart()
    elif ball.left <= 0:  # Opponent scores
        scores[game_mode]["player"] += 1
        score_sound.play()
        ball_restart()
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1
        hit_sound.play()
        increase_difficulty()

def player_animation():
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_animation():
    update_high_scores(computer_difficulty)  # Check and update high scores if needed
    if game_mode == "Singleplayer":
        # The computer tracks the ball based on the difficulty level
        reaction_speed = difficulty_speed_map[computer_difficulty]

        # Define a distance threshold where the AI will start reacting
        reaction_threshold = 100  # AI starts tracking when the ball is this far away from it

        # Set the miss chance based on difficulty
        if computer_difficulty == "Easy":
            miss_chance = 0.05  # 10% chance of missing (very low)
        elif computer_difficulty == "Medium":
            miss_chance = 0.2  # 30% chance of missing (moderate)
        elif computer_difficulty == "Hard":
            miss_chance = 0.5  # 50% chance of missing (higher chance)

        # Check if the ball is within the reaction threshold (AI will only track the ball when close enough)
        if abs(ball.centery - opponent.centery) < reaction_threshold:
            # AI reacts but with human-like imperfections
            random_factor = random.uniform(0.8, 1.2)  # Random factor for human-like reaction speed

            # AI adjusts its position to align with the ball (but imperfectly)
            if opponent.centery < ball.centery:
                opponent.y += reaction_speed * random_factor
            elif opponent.centery > ball.centery:
                opponent.y -= reaction_speed * random_factor

            # Occasionally simulate human-like mistakes (AI misses or overshoots)
            if random.random() < miss_chance:  # Adjust based on difficulty
                opponent.y += random.randint(-20, 20)  # Overshoot or undershoot

        # If the ball is far away, the AI stops moving
        else:
            # The AI doesn't move unless the ball is within range
            pass

        # Prevent the opponent from moving out of bounds
        if opponent.top < 0:
            opponent.top = 0
        if opponent.bottom > screen_height:
            opponent.bottom = screen_height

        # Save the high score for the current difficulty
        save_high_scores(computer_difficulty)
    else:
        # Multiplayer logic: Opponent paddle is player-controlled
        if opponent.top <= 0:
            opponent.top = 0
        if opponent.bottom >= screen_height:
            opponent.bottom = screen_height

def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_x, ball_speed_y = original_speed_x, original_speed_y

def increase_difficulty():
    global ball_speed_x, ball_speed_y
    ball_speed_x *= 1.05
    ball_speed_y *= 1.05

# Display menu at the start
show_menu()

# Main game loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Check for mouse button click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_button_rect.collidepoint(event.pos):
                if back_button_rect.collidepoint(event.pos):
                    show_menu()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
            if game_mode == "Multiplayer":
                if event.key == pygame.K_s:
                    opponent_speed += 7
                if event.key == pygame.K_w:
                    opponent_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7
            if game_mode == "Multiplayer":
                if event.key == pygame.K_s:
                    opponent_speed -= 7
                if event.key == pygame.K_w:
                    opponent_speed += 7

    ball_animation()
    player.y += player_speed
    if game_mode == "Multiplayer":
        opponent.y += opponent_speed
    opponent_animation()
    player_animation()
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))
    current_scores = scores[game_mode]
    player_text = game_font.render(f"{current_scores['player']}", False, light_grey)
    opponent_text = game_font.render(f"{current_scores['opponent']}", False, light_grey)
    screen.blit(player_text, (420, 8))
    screen.blit(opponent_text, (360, 8))

    # "Back" button at the top left
    back_button_text = game_font.render("Back", True, light_grey)
    back_button_width = back_button_text.get_width() + 20  # Add padding
    back_button_height = 40
    back_button_rect = pygame.Rect(20, 20, back_button_width, back_button_height)
    # Create the button-like background for "Back"
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if back_button_rect.collidepoint(mouse_x, mouse_y):  # Hover effect
        pygame.draw.rect(screen, (50, 50, 50), back_button_rect)  # Darker background when hovered
    else:
        pygame.draw.rect(screen, (70, 70, 70), back_button_rect)  # Normal background

    # Render the "Back" button text
    screen.blit(back_button_text, (back_button_rect.x + (back_button_width - back_button_text.get_width()) / 2,
                                   back_button_rect.y + (back_button_height - back_button_text.get_height()) / 2))

    if current_scores["player"] == 15 or current_scores["opponent"] == 15:
        winner_text = "Player 1 Wins!" if current_scores["player"] == 15 else "Player 2 wins!"
        game_over_text = game_font.render(winner_text, False, light_grey)
        screen.fill(bg_color)  # Clear the screen before displaying the text
        screen.blit(game_over_text, (screen_width / 2 - game_over_text.get_width() / 2, screen_height / 2))
        pygame.display.flip()
        pygame.time.delay(5000)  # Pause for 5 seconds
        reset_game(game_mode)  # Reset the game for the current mode

    pygame.display.flip()
    clock.tick(60)