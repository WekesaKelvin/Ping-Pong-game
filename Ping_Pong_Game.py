import pygame
import sys
import time

# initializing pygame module
pygame.init()

# Set screen dimensions and initialize display
screen_width = 800
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# Create clock and game font
clock = pygame.time.Clock()
game_font = pygame.font.Font("freesansbold.ttf", 32)

# Set initial scores and game colors
player_score = 0
opponent_score = 0
bg_color = pygame.Color("grey12")
light_grey = (200, 200, 200)
game_over = False
# Define game elements
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

# Define ball speed
ball_speed_x = 7
ball_speed_y = 7
player_speed = 0
opponent_speed = 0

# Ball movement and collision logic
def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    if ball.right >= screen_width:
        opponent_score += 1
        ball_restart()
    elif ball.left <= 0:
        player_score += 1
        ball_restart()

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1
        # Player paddle movement restriction
def player_animation():
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

# Opponent paddle movement restriction
def opponent_animation():
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

# Reset ball to center
def ball_restart():
    ball.center = (screen_width / 2, screen_height / 2)
