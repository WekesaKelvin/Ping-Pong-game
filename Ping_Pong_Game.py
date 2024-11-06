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

# Display scores on screen
def display_scores():
    player_text = game_font.render(f"{player_score}", False, light_grey)
    opponent_text = game_font.render(f"{opponent_score}", False, light_grey)
    screen.blit(player_text, (420, 8))
    screen.blit(opponent_text, (360, 8))

# Handle keyboard inputs
def handle_input():
    global player_speed, opponent_speed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
            if event.key == pygame.K_w:
                opponent_speed += 7
            if event.key == pygame.K_s:
                opponent_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7
            if event.key == pygame.K_w:
                opponent_speed -= 7
            if event.key == pygame.K_s:
                opponent_speed += 7
                
# Main game loop
while True:
    handle_input()
    ball_animation()
    player.y += player_speed
    opponent.y += opponent_speed
    player_animation()
    opponent_animation()

    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))
    
    display_scores()

    if player_score == 10:
        game_over_text = game_font.render("Player Wins!", False, light_grey)
        screen.blit(game_over_text, (screen_width / 2 - 100, screen_height / 2))
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    elif opponent_score == 10:
        game_over_text = game_font.render("Opponent Wins!", False, light_grey)
        screen.blit(game_over_text, (screen_width / 2 - 100, screen_height / 2))
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    clock.tick(60)