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