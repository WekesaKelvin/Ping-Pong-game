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
win_sound = pygame.mixer.Sound("Sound/win.wav")

# initializing game scores
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)
label_font = pygame.font.Font("freesansbold.ttf", 32)

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
pygame.display.set_caption("Ping Pong")

# Defining Game elements
ball_size = 30
ball = pygame.Rect(screen_width / 2 - ball_size / 2, screen_height / 2 - ball_size / 2, ball_size, ball_size)

paddle_size= 140
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, paddle_size)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, paddle_size)

# Ball and paddle speeds
original_speed_x = 7
original_speed_y = 7
ball_speed_x = original_speed_x
ball_speed_y = original_speed_y
player_speed = 0
opponent_speed = 0
game_mode = "Score based"  # Match type (can be "score" or "time")
paddle_speed_value = 7
time_limit = 60  # Default to 60 seconds
score_limit = 15


settings = {
    "original_speed_x": original_speed_x,
    "original_speed_y": original_speed_y,
    "paddle_size": paddle_size,
    "paddle_speed_value": paddle_speed_value,
    "game_mode": game_mode,
    "ball_size" : ball_size,
    "time_limit" : time_limit,
    "score_limit" : score_limit
}

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
    "Score Based": {"player": 0, "opponent": 0},
    "Time Based": {"player": 0, "opponent": 0}
}

# Difficulty levels
difficulty_modes = ["Easy", "Medium", "Hard"]

# High scores dictionary
high_scores = {"Easy": 0, "Medium": 0, "Hard": 0}

# File path to store high scores
high_scores_file = "high_scores.json"

def save_settings():
    settings = {
        "paddle_speed_value": paddle_speed_value,
        "original_speed_x": original_speed_x,
        "original_speed_y": original_speed_y,
        "ball_size": ball_size,
        "paddle_size": paddle_size,
        "game_mode": game_mode,
        "time_limit": time_limit,
        "score_limit": score_limit
    }
    with open('settings.json', 'w') as f:
        json.dump(settings, f)

# Function to load settings from a file
def load_settings():
    global paddle_speed_value, opponent_speed, original_speed_x, original_speed_y, ball_size, paddle_size, game_mode, time_limit, score_limit
    try:
        with open('settings.json', 'r') as f:
            settings = json.load(f)
            paddle_speed_value = settings.get("paddle_speed_value", 7)
            original_speed_x = settings.get("original_speed_x", 7)
            original_speed_y = settings.get("original_speed_y", 7)
            ball_size = settings.get("ball_size", 30)
            paddle_size = settings.get("paddle_size", 140)
            game_mode = settings.get("game_mode", "Score Based")
            time_limit = settings.get("time_limit", 60)
            score_limit = settings.get("score_limit", 15)

    except (FileNotFoundError, json.JSONDecodeError):
        # If no file or invalid file, use default values
       paddle_speed_value = 7,
       original_speed_x = 7,
       original_speed_y = 7,
       ball_size = 30,
       paddle_size = 140,
       game_mode = "Score Based",
       time_limit = 60,
       score_limit = 15

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
    global ball_speed_x, ball_speed_y, player, opponent, start_time, time_remaining
    load_settings()
    # Initialize player and opponent with the loaded paddle size
    player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, paddle_size)
    opponent = pygame.Rect(10, screen_height / 2 - 70, 10, paddle_size)
    scores[mode]["player"] = 0
    scores[mode]["opponent"] = 0
    # Initialize timer variables
    start_time = pygame.time.get_ticks()  # Record the start time
    time_remaining = time_limit  # Use the global `time_limit` set earlier
    ball_restart()
# Function to draw the back button
def draw_back_button():
    back_button_rect = pygame.Rect(10, 10, 100, 40)  # Position and size of the button
    pygame.draw.rect(screen, RED, back_button_rect)  # Draw the button
    back_text = font.render("Back", True, WHITE)
    screen.blit(back_text, (back_button_rect.x + 20, back_button_rect.y + 5))  # Center the text

def show_settings_menu():
    global ball_speed_x, ball_speed_y, player_speed, opponent_speed, paddle_size, game_mode
    while True:
        screen.fill(bg_color)

        # Title text
        title_text = game_font.render("Settings", True, light_grey)
        screen.blit(title_text, (screen_width / 2 - title_text.get_width() / 2, screen_height / 2 - 200))

        # Settings options
        options = [
            ("1. Paddle Speed", screen_height / 2 - 150),
            ("2. Ball Speed", screen_height / 2 - 100),
            ("3. Paddle Size", screen_height / 2 - 50),
            ("4. Ball Size", screen_height / 2),  # Added Ball Size option
            ("5. Match Type", screen_height / 2 + 50),
        ]

        # Create button rectangles and render them
        buttons = []
        for text, y in options:
            button_text = game_font.render(text, True, light_grey)
            button_width = button_text.get_width() + 40  # Add padding
            button_height = 40
            button_rect = pygame.Rect(screen_width / 2 - button_width / 2, y, button_width, button_height)

            # Create the button-like background
            buttons.append((button_rect, button_text))

            # Mouse hover effect
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(screen, (50, 50, 50), button_rect)  # Darker background when hovered
            else:
                pygame.draw.rect(screen, (70, 70, 70), button_rect)  # Normal background

            # Render the text on the button
            screen.blit(button_text, (button_rect.x + (button_width - button_text.get_width()) / 2,
                                      button_rect.y + (button_height - button_text.get_height()) / 2))

        # "Back" button
        back_button_text = game_font.render("Back", True, light_grey)
        back_button_width = back_button_text.get_width() + 20  # Add padding
        back_button_height = 40
        back_button_rect = pygame.Rect(20, 20, back_button_width, back_button_height)
        if back_button_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, (50, 50, 50), back_button_rect)
        else:
            pygame.draw.rect(screen, (70, 70, 70), back_button_rect)
        screen.blit(back_button_text, (back_button_rect.x + (back_button_width - back_button_text.get_width()) / 2,
                                       back_button_rect.y + (back_button_height - back_button_text.get_height()) / 2))

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Back button click
                    if back_button_rect.collidepoint(mouse_x, mouse_y):
                        show_menu()  # Go back to the main menu
                        return

                    # Check each settings button
                    for idx, (button_rect, button_text) in enumerate(buttons):
                        if button_rect.collidepoint(mouse_x, mouse_y):
                            if idx == 0:
                                adjust_paddle_speed()  # Adjust Paddle Speed
                            elif idx == 1:
                                adjust_ball_speed()  # Adjust Ball Speed
                            elif idx == 2:
                                adjust_paddle_size()  # Adjust Paddle Size
                            elif idx == 3:
                                adjust_ball_size()  # Adjust ball Type
                            elif idx == 4:
                                adjust_match_type()  # Adjust Match Type

def adjust_paddle_speed():
    global paddle_speed_value  # Assuming paddle_speed_value is the shared speed for both paddles.

    # Load settings when entering the settings menu
    load_settings()

    while True:
        screen.fill(bg_color)

        # Title text
        title_text = game_font.render("Adjust Paddle Speed", True, light_grey)
        screen.blit(title_text, (screen_width / 2 - title_text.get_width() / 2, screen_height / 2 - 200))

        # Display current paddle speed
        speed_text = game_font.render(f"Paddle Speed: {paddle_speed_value}", True, light_grey)
        screen.blit(speed_text, (screen_width / 2 - speed_text.get_width() / 2, screen_height / 2 - 100))

        # Create buttons for adjusting speed
        increase_button = pygame.Rect(screen_width / 2 - 150, screen_height / 2, 60, 40)
        decrease_button = pygame.Rect(screen_width / 2 + 90, screen_height / 2, 60, 40)

        pygame.draw.rect(screen, (70, 70, 70), increase_button)
        pygame.draw.rect(screen, (70, 70, 70), decrease_button)

        # Text for the buttons
        increase_text = game_font.render("Increase", True, light_grey)
        decrease_text = game_font.render("Decrease", True, light_grey)

        screen.blit(increase_text, (
        increase_button.x + (increase_button.width - increase_text.get_width()) / 2, increase_button.y + 10))
        screen.blit(decrease_text, (
        decrease_button.x + (decrease_button.width - decrease_text.get_width()) / 2, decrease_button.y + 10))

        # Back button
        back_button_text = game_font.render("Back", True, light_grey)
        back_button_width = back_button_text.get_width() + 20
        back_button_height = 40
        back_button_rect = pygame.Rect(20, screen_height - 60, back_button_width, back_button_height)
        if back_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (50, 50, 50), back_button_rect)
        else:
            pygame.draw.rect(screen, (70, 70, 70), back_button_rect)
        screen.blit(back_button_text, (back_button_rect.x + (back_button_width - back_button_text.get_width()) / 2,
                                       back_button_rect.y + (back_button_height - back_button_text.get_height()) / 2))

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.button == 1:
                    # Adjust paddle speed value
                    if increase_button.collidepoint(mouse_x, mouse_y):
                        paddle_speed_value += 1
                    elif decrease_button.collidepoint(mouse_x, mouse_y):
                        paddle_speed_value -= 1

                    # Back button
                    elif back_button_rect.collidepoint(mouse_x, mouse_y):
                        save_settings()  # Save the updated settings before going back
                        return  # Go back to the previous menu

def adjust_ball_speed():
    global original_speed_x, original_speed_y

    # Load current settings at the start
    load_settings()

    while True:
        screen.fill(bg_color)

        # Title text
        title_text = game_font.render("Adjust Ball Speed", True, light_grey)
        screen.blit(title_text, (screen_width / 2 - title_text.get_width() / 2, screen_height / 2 - 200))

        # Display current ball speed and options to adjust
        speed_text = game_font.render(f"Ball Speed: {original_speed_x}", True, light_grey)
        screen.blit(speed_text, (screen_width / 2 - speed_text.get_width() / 2, screen_height / 2 - 100))

        # Create buttons for adjusting ball speed
        increase_button = pygame.Rect(screen_width / 2 - 150, screen_height / 2, 60, 40)
        decrease_button = pygame.Rect(screen_width / 2 + 90, screen_height / 2, 60, 40)

        pygame.draw.rect(screen, (70, 70, 70), increase_button)
        pygame.draw.rect(screen, (70, 70, 70), decrease_button)

        # Text for the buttons
        increase_text = game_font.render("Increase", True, light_grey)
        decrease_text = game_font.render("Decrease", True, light_grey)

        screen.blit(increase_text, (increase_button.x + (increase_button.width - increase_text.get_width()) / 2, increase_button.y + 10))
        screen.blit(decrease_text, (decrease_button.x + (decrease_button.width - decrease_text.get_width()) / 2, decrease_button.y + 10))

        # Back button
        back_button_text = game_font.render("Back", True, light_grey)
        back_button_width = back_button_text.get_width() + 20
        back_button_height = 40
        back_button_rect = pygame.Rect(20, screen_height - 60, back_button_width, back_button_height)
        if back_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (50, 50, 50), back_button_rect)
        else:
            pygame.draw.rect(screen, (70, 70, 70), back_button_rect)
        screen.blit(back_button_text, (back_button_rect.x + (back_button_width - back_button_text.get_width()) / 2,
                                       back_button_rect.y + (back_button_height - back_button_text.get_height()) / 2))

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.button == 1:
                    # Adjust ball speed based on button clicks
                    if increase_button.collidepoint(mouse_x, mouse_y):
                        original_speed_x += 1  # Increase ball speed horizontally
                        original_speed_y += 1  # Increase ball speed vertically
                    elif decrease_button.collidepoint(mouse_x, mouse_y):
                        original_speed_x -= 1  # Decrease ball speed horizontally
                        original_speed_y -= 1  # Decrease ball speed vertically
                    elif back_button_rect.collidepoint(mouse_x, mouse_y):
                        # Save updated settings before going back
                        save_settings()
                        return  # Go back to the previous menu

def adjust_ball_size():
    global ball_size

    while True:
        screen.fill(bg_color)

        # Title text
        title_text = game_font.render("Adjust Ball Size", True, light_grey)
        screen.blit(title_text, (screen_width / 2 - title_text.get_width() / 2, screen_height / 2 - 200))

        # Display current ball size
        size_text = game_font.render(f"Ball Size: {ball_size}x{ball_size}", True, light_grey)
        screen.blit(size_text, (screen_width / 2 - size_text.get_width() / 2, screen_height / 2 - 100))

        # Create buttons for adjusting ball size
        increase_button = pygame.Rect(screen_width / 2 - 150, screen_height / 2, 60, 40)
        decrease_button = pygame.Rect(screen_width / 2 + 90, screen_height / 2, 60, 40)

        pygame.draw.rect(screen, (70, 70, 70), increase_button)
        pygame.draw.rect(screen, (70, 70, 70), decrease_button)

        # Text for the buttons
        increase_text = game_font.render("Increase", True, light_grey)
        decrease_text = game_font.render("Decrease", True, light_grey)

        screen.blit(increase_text, (increase_button.x + (increase_button.width - increase_text.get_width()) / 2, increase_button.y + 10))
        screen.blit(decrease_text, (decrease_button.x + (decrease_button.width - decrease_text.get_width()) / 2, decrease_button.y + 10))

        # Back button
        back_button_text = game_font.render("Back", True, light_grey)
        back_button_width = back_button_text.get_width() + 20
        back_button_height = 40
        back_button_rect = pygame.Rect(20, screen_height - 60, back_button_width, back_button_height)
        if back_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (50, 50, 50), back_button_rect)
        else:
            pygame.draw.rect(screen, (70, 70, 70), back_button_rect)
        screen.blit(back_button_text, (back_button_rect.x + (back_button_width - back_button_text.get_width()) / 2,
                                       back_button_rect.y + (back_button_height - back_button_text.get_height()) / 2))

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position when the click happens
                if event.button == 1:
                    if increase_button.collidepoint(mouse_x, mouse_y):
                        # Increase ball size
                        ball_size += 5  # Adjust the size increment as needed
                    elif decrease_button.collidepoint(mouse_x, mouse_y):
                        # Decrease ball size
                        if ball_size > 10:  # Prevent making the ball too small
                            ball_size -= 5
                    elif back_button_rect.collidepoint(mouse_x, mouse_y):
                        # Save updated settings before going back
                        save_settings()  # Assuming you have this function implemented
                        return  # Go back to the previous menu

def adjust_paddle_size():
    global paddle_size
    while True:
        screen.fill(bg_color)

        # Title text
        title_text = game_font.render("Adjust Paddle Size", True, light_grey)
        screen.blit(title_text, (screen_width / 2 - title_text.get_width() / 2, screen_height / 2 - 200))

        # Display current paddle size and increase/decrease options
        size_text = game_font.render(f"Paddle Size: {paddle_size}", True, light_grey)
        screen.blit(size_text, (screen_width / 2 - size_text.get_width() / 2, screen_height / 2 - 100))

        increase_button = pygame.Rect(screen_width / 2 - 150, screen_height / 2, 60, 40)
        decrease_button = pygame.Rect(screen_width / 2 + 90, screen_height / 2, 60, 40)

        pygame.draw.rect(screen, (70, 70, 70), increase_button)
        pygame.draw.rect(screen, (70, 70, 70), decrease_button)

        increase_text = game_font.render("Increase", True, light_grey)
        decrease_text = game_font.render("Decrease", True, light_grey)

        screen.blit(increase_text, (increase_button.x + (increase_button.width - increase_text.get_width()) / 2, increase_button.y + 10))
        screen.blit(decrease_text, (decrease_button.x + (decrease_button.width - decrease_text.get_width()) / 2, decrease_button.y + 10))

        # Back button
        back_button_text = game_font.render("Back", True, light_grey)
        back_button_width = back_button_text.get_width() + 20
        back_button_height = 40
        back_button_rect = pygame.Rect(20, screen_height - 60, back_button_width, back_button_height)
        if back_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (50, 50, 50), back_button_rect)
        else:
            pygame.draw.rect(screen, (70, 70, 70), back_button_rect)
        screen.blit(back_button_text, (back_button_rect.x + (back_button_width - back_button_text.get_width()) / 2,
                                       back_button_rect.y + (back_button_height - back_button_text.get_height()) / 2))

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.button == 1:
                    if increase_button.collidepoint(mouse_x, mouse_y):
                        paddle_size += 10  # Adjust the value as needed
                        save_settings()  # Save settings immediately after changing paddle size
                    elif decrease_button.collidepoint(mouse_x, mouse_y):
                        paddle_size -= 10  # Adjust the value as needed
                        save_settings()  # Save settings immediately after changing paddle size
                    elif back_button_rect.collidepoint(mouse_x, mouse_y):
                        save_settings()  # Save settings when exiting the menu
                        return  # Go back to the main game loop

def adjust_match_type():
    global game_mode, time_limit, score_limit
    selecting_time_limit = False
    selecting_score_limit = False
    load_settings()

    while True:
        screen.fill(bg_color)

        # Title text
        title_text = game_font.render("Select Match Type", True, light_grey)
        screen.blit(title_text, (screen_width / 2 - title_text.get_width() / 2, screen_height / 2 - 150))

        # Current match type display
        current_type_text = game_font.render(f"Current: {game_mode}", True, light_grey)
        screen.blit(current_type_text, (screen_width / 2 - current_type_text.get_width() / 2, screen_height / 2 - 110))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Score-based button
        score_button = pygame.Rect(screen_width / 2 - 150, screen_height / 2 - 60, 300, 40)
        score_button_color = (50, 50, 50) if score_button.collidepoint(mouse_x, mouse_y) else (70, 70, 70)
        pygame.draw.rect(screen, score_button_color, score_button)
        score_text = game_font.render("Score Based", True, light_grey)
        screen.blit(score_text,
                    (score_button.x + (score_button.width - score_text.get_width()) / 2, score_button.y + 10))

        # Time-based button
        time_button = pygame.Rect(screen_width / 2 - 150, screen_height / 2, 300, 40)
        time_button_color = (50, 50, 50) if time_button.collidepoint(mouse_x, mouse_y) else (70, 70, 70)
        pygame.draw.rect(screen, time_button_color, time_button)
        time_text = game_font.render("Time Based", True, light_grey)
        screen.blit(time_text,
                    (time_button.x + (time_button.width - time_text.get_width()) / 2, time_button.y + 10))

        # Back button
        back_button_text = game_font.render("Back", True, light_grey)
        back_button_width = back_button_text.get_width() + 20
        back_button_height = 40
        back_button_rect = pygame.Rect(20, screen_height - 60, back_button_width, back_button_height)
        back_button_color = (50, 50, 50) if back_button_rect.collidepoint(mouse_x, mouse_y) else (70, 70, 70)
        pygame.draw.rect(screen, back_button_color, back_button_rect)
        screen.blit(back_button_text, (back_button_rect.x + (back_button_width - back_button_text.get_width()) / 2,
                                       back_button_rect.y + (back_button_height - back_button_text.get_height()) / 2))

        # Time limit selection (if active)
        if selecting_time_limit:
            time_limit_text = game_font.render(f"Select Time Limit: {time_limit} seconds", True, light_grey)
            screen.blit(time_limit_text, (screen_width / 2 - time_limit_text.get_width() / 2, screen_height / 2 + 80))

            # Decrease button
            decrease_button = pygame.Rect(screen_width / 2 - 100, screen_height / 2 + 120, 80, 40)
            decrease_button_color = (50, 50, 50) if decrease_button.collidepoint(mouse_x, mouse_y) else (70, 70, 70)
            pygame.draw.rect(screen, decrease_button_color, decrease_button)
            decrease_text = game_font.render("-", True, light_grey)
            screen.blit(decrease_text,
                        (decrease_button.x + (decrease_button.width - decrease_text.get_width()) / 2,
                         decrease_button.y + 10))

            # Increase button
            increase_button = pygame.Rect(screen_width / 2 + 20, screen_height / 2 + 120, 80, 40)
            increase_button_color = (50, 50, 50) if increase_button.collidepoint(mouse_x, mouse_y) else (70, 70, 70)
            pygame.draw.rect(screen, increase_button_color, increase_button)
            increase_text = game_font.render("+", True, light_grey)
            screen.blit(increase_text,
                        (increase_button.x + (increase_button.width - increase_text.get_width()) / 2,
                         increase_button.y + 10))

        # Score limit selection (if active)
        if selecting_score_limit:
            score_limit_text = game_font.render(f"Select Score Limit: {score_limit}", True, light_grey)
            screen.blit(score_limit_text,
                        (screen_width / 2 - score_limit_text.get_width() / 2, screen_height / 2 + 80))

            # Decrease button
            decrease_button = pygame.Rect(screen_width / 2 - 100, screen_height / 2 + 120, 80, 40)
            decrease_button_color = (50, 50, 50) if decrease_button.collidepoint(mouse_x, mouse_y) else (70, 70, 70)
            pygame.draw.rect(screen, decrease_button_color, decrease_button)
            decrease_text = game_font.render("-", True, light_grey)
            screen.blit(decrease_text,
                        (decrease_button.x + (decrease_button.width - decrease_text.get_width()) / 2,
                         decrease_button.y + 10))

            # Increase button
            increase_button = pygame.Rect(screen_width / 2 + 20, screen_height / 2 + 120, 80, 40)
            increase_button_color = (50, 50, 50) if increase_button.collidepoint(mouse_x, mouse_y) else (70, 70, 70)
            pygame.draw.rect(screen, increase_button_color, increase_button)
            increase_text = game_font.render("+", True, light_grey)
            screen.blit(increase_text,
                        (increase_button.x + (increase_button.width - increase_text.get_width()) / 2,
                         increase_button.y + 10))

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if score_button.collidepoint(mouse_x, mouse_y):
                    game_mode = "Score Based"
                    selecting_score_limit = True
                    selecting_time_limit = False  # Hide time limit settings
                    save_settings()
                elif time_button.collidepoint(mouse_x, mouse_y):
                    game_mode = "Time Based"
                    selecting_time_limit = True
                    selecting_score_limit = False  # Hide score limit settings
                elif back_button_rect.collidepoint(mouse_x, mouse_y):
                    return
                elif selecting_time_limit:
                    if decrease_button.collidepoint(mouse_x, mouse_y) and time_limit > 10:
                        time_limit -= 10  # Decrease time by 10 seconds
                    elif increase_button.collidepoint(mouse_x, mouse_y):
                        time_limit += 10  # Increase time by 10 seconds
                elif selecting_score_limit:
                    if decrease_button.collidepoint(mouse_x, mouse_y) and score_limit > 5:
                        score_limit -= 1  # Decrease score by 1
                    elif increase_button.collidepoint(mouse_x, mouse_y):
                        score_limit += 1  # Increase score by 1
                    save_settings()

def show_menu():
    load_high_scores()
    global game_mode, computer_difficulty

    while True:
        screen.fill(bg_color)

        # Title text
        title_text = game_font.render("Main Menu", True, light_grey)
        screen.blit(title_text, (screen_width / 2 - title_text.get_width() / 2, screen_height / 2 - 200))

        # Menu options
        options = [
            ("1. Settings", screen_height / 2 - 150),
            ("2. Online", screen_height / 2 - 100),
            ("3. Multiplayer", screen_height / 2 - 50),
            ("4. Single-player vs Computer", screen_height / 2),
        ]

        # Display high scores (adjusted position)
        high_score_text = game_font.render("High Scores:", True, light_grey)
        screen.blit(high_score_text, (screen_width / 2 - high_score_text.get_width() / 2, screen_height / 2 + 50))

        # Start high score display
        y_offset = 40
        for difficulty in difficulty_modes:
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
        if back_button_rect.collidepoint(mouse_x, mouse_y):  # Hover effect
            pygame.draw.rect(screen, (50, 50, 50), back_button_rect)  # Darker background when hovered
        else:
            pygame.draw.rect(screen, (70, 70, 70), back_button_rect)  # Normal background

        # Render the "Back" button text
        screen.blit(back_button_text, (back_button_rect.x + (back_button_width - back_button_text.get_width()) / 2,
                                       back_button_rect.y + (back_button_height - back_button_text.get_height()) / 2))

        pygame.display.flip()

        # Event handling
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

                    # Check if mouse is over the 'Settings' button
                    if options[0][1] <= mouse_y <= options[0][
                        1] + 40 and screen_width / 2 - 150 <= mouse_x <= screen_width / 2 + 150:
                        show_settings_menu()

                    # Check if mouse is over the 'Online' button
                    elif options[1][1] <= mouse_y <= options[1][1] + 40:
                        game_mode = "Online"
                        reset_game(game_mode)
                        return

                    # Check if mouse is over the 'Multiplayer' button
                    elif options[2][1] <= mouse_y <= options[2][1] + 40:
                        game_mode = "Multiplayer"
                        reset_game(game_mode)
                        return

                    # Check if mouse is over the 'Single-player vs Computer' button
                    elif options[3][1] <= mouse_y <= options[3][1] + 40:
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

def draw_labels():
    player1_label = label_font.render("Player 1", True, light_grey)
    player2_label = label_font.render("Player 2", True, light_grey)

    # Draw labels for Player 1 (Left side)
    screen.blit(player1_label, (screen_width / 4 - player1_label.get_width() / 2, 10))  # Top of the left side

    # Draw labels for Player 2 (Right side)
    screen.blit(player2_label, (3 * screen_width / 4 - player2_label.get_width() / 2, 10))  # Top of the right side

def ball_animation():
    global ball_speed_x, ball_speed_y, opponent_score, player_score

    load_settings()

    # Update ball position based on current speed
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball bouncing off top and bottom walls
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1  # Reverse direction on vertical collision

    # Ball scoring conditions
    if ball.right >= screen_width:  # Player scores
        scores[game_mode]["opponent"] += 1
        score_sound.play()
        ball_restart()
    elif ball.left <= 0:  # Opponent scores
        scores[game_mode]["player"] += 1
        score_sound.play()
        ball_restart()

    # Ball collision with player or opponent paddles
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1  # Reverse direction on paddle collision
        hit_sound.play()
        increase_difficulty()

def player_animation():
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_animation():

    if game_mode == "Singleplayer":
        update_high_scores(computer_difficulty)  # Check and update high scores if needed
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
    global ball_speed_x, ball_speed_y,ball, start_time, time_remaining

    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_x, ball_speed_y = original_speed_x, original_speed_y
    ball = pygame.Rect(screen_width / 2 - ball_size / 2, screen_height / 2 - ball_size / 2, ball_size, ball_size)



def increase_difficulty():
    global ball_speed_x, ball_speed_y
    ball_speed_x *= 1.05
    ball_speed_y *= 1.05


# Display menu at the start
show_menu()
load_settings()

# Initialize timer variables
start_time = pygame.time.get_ticks()  # Record the start time
time_remaining = time_limit  # Use the global `time_limit` set earlier

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Check for mouse button click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_button_rect.collidepoint(event.pos):
                show_menu()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += paddle_speed_value
            if event.key == pygame.K_UP:
                player_speed -= paddle_speed_value
            if game_mode == "Multiplayer":
                if event.key == pygame.K_s:
                    opponent_speed += paddle_speed_value
                if event.key == pygame.K_w:
                    opponent_speed -= paddle_speed_value
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= paddle_speed_value
            if event.key == pygame.K_UP:
                player_speed += paddle_speed_value
            if game_mode == "Multiplayer":
                if event.key == pygame.K_s:
                    opponent_speed -= paddle_speed_value
                if event.key == pygame.K_w:
                    opponent_speed += paddle_speed_value

    # Game logic
    ball_animation()
    player.y += player_speed
    if game_mode == "Multiplayer":
        opponent.y += opponent_speed
    opponent_animation()
    player_animation()

    # Draw game elements
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

    current_scores = scores[game_mode]

    # Timer-based game mode logic
    if game_mode == "Time Based":
        # Calculate remaining time
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Elapsed time in seconds
        time_remaining = time_limit - elapsed_time

        # Display timer
        timer_text = game_font.render(f"Time: {time_remaining}s", False, light_grey)
        screen.blit(timer_text, (screen_width / 2 - timer_text.get_width() / 2, 8))

        # Display scores below the timer
        player_score_text = game_font.render(f"Player 1: {scores['Time Based']['player']}", True, light_grey)
        opponent_score_text = game_font.render(f"Player 2: {scores['Time Based']['opponent']}", True, light_grey)
        screen.blit(opponent_score_text, (screen_width / 2 - opponent_score_text.get_width() - 10, 50))
        screen.blit(player_score_text, (screen_width / 2 + 10, 50))

        # End the game when the timer reaches 0
        if time_remaining <= 0:
            if current_scores["player"] > current_scores["opponent"]:
                winner_text = "Player 2 Wins!"
            elif current_scores["opponent"] > current_scores["player"]:
                winner_text = "Player 2 Wins!"
            else:
                winner_text = "It's a Draw!"

            # Display winner and reset the game
            win_sound.play()
            game_over_text = game_font.render(winner_text, False, light_grey)
            screen.fill(bg_color)
            screen.blit(game_over_text, (screen_width / 2 - game_over_text.get_width() / 2, screen_height / 2))
            pygame.display.flip()
            pygame.time.delay(5000)
            reset_game(game_mode)

    # Score-based game mode logic
    else:  # "Score Based"
        # Assuming 'score_limit' is the variable holding the current score limit.
        player_text = game_font.render(f"{current_scores['player']}", False, light_grey)
        opponent_text = game_font.render(f"{current_scores['opponent']}", False, light_grey)
        score_limit_text = game_font.render(f"Score Limit: {score_limit}", False, light_grey)  # Render score limit

        # Position the player and opponent scores
        screen.blit(player_text, (420, 8))
        screen.blit(opponent_text, (360, 8))

       
        # Position the score limit at the bottom of the screen
        screen.blit(score_limit_text,
                    (screen_width / 2 - score_limit_text.get_width() / 2, screen_height - 40))  # Center at the bottom

        # Check for the winner
        if current_scores["player"] == score_limit or current_scores["opponent"] == score_limit:
            if current_scores["player"] == score_limit:
                winner_text = "Player 2 Wins!"
            else:
                winner_text = "Player 1 Wins!"

            # Display winner and reset the game
            win_sound.play()
            game_over_text = game_font.render(winner_text, False, light_grey)
            screen.fill(bg_color)
            screen.blit(game_over_text, (screen_width / 2 - game_over_text.get_width() / 2, screen_height / 2))
            pygame.display.flip()
            pygame.time.delay(5000)
            reset_game(game_mode)

    # Draw the "Back" button
    back_button_text = game_font.render("Back", True, light_grey)
    back_button_width = back_button_text.get_width() + 20
    back_button_height = 40
    back_button_rect = pygame.Rect(20, 20, back_button_width, back_button_height)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if back_button_rect.collidepoint(mouse_x, mouse_y):  # Hover effect
        pygame.draw.rect(screen, (50, 50, 50), back_button_rect)
    else:
        pygame.draw.rect(screen, (70, 70, 70), back_button_rect)
    screen.blit(back_button_text, (back_button_rect.x + (back_button_width - back_button_text.get_width()) / 2,
                                   back_button_rect.y + (back_button_height - back_button_text.get_height()) / 2))

    pygame.display.flip()
    clock.tick(60)
