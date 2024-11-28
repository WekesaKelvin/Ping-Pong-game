import pygame
import sys
import time

# initializing pygame module
pygame.init()

clock = pygame.time.Clock()

# initializing game scores
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)

# Level variables
current_level = 1  # Start at Level 1
game_over = False


def ball_animation():
    global ball_speed_x, ball_speed_y, opponent_score, player_score
    # making ball move [speed controls]
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # making the ball bounce back when hitting the top or bottom
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    # scoring logic, when ball passes a paddle
    if ball.right >= screen_width or ball.left <= 0:
        if ball.left <= 0:
            player_score += 1
        elif ball.right >= screen_width:
            opponent_score += 1
        ball_restart()

    # ball collision with paddles
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1


def player_animation():
    # constraining the player's paddle within the screen
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_animation():
    # constraining the opponent's paddle within the screen
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_restart():
    # reset the ball to the center
    ball.center = (screen_width / 2, screen_height / 2)


def switch_to_level_2():
    global player, opponent, current_level
    # Change paddle size to make it shorter
    player.height = 80
    opponent.height = 80
    # Update the level
    current_level = 2
    ball_restart()  # Restart the ball in the center


# setting up the main window
screen_width = 800
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# Defining Game elements
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

# defining ball speed
ball_speed_x = 7
ball_speed_y = 7
# DEFINING PLAYER SPEED
player_speed = 0
opponent_speed = 0

# creating game colors
bg_color = pygame.Color("grey12")
light_grey = (200, 200, 200)
pink = (255, 105, 180)  # Pink color

# starting game loop
while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
            if event.key == pygame.K_s:
                opponent_speed += 7
            if event.key == pygame.K_w:
                opponent_speed -= 7

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7
            if event.key == pygame.K_s:
                opponent_speed -= 7
            if event.key == pygame.K_w:
                opponent_speed += 7

    # Transition to Level 2
    if current_level == 1 and (player_score == 10 or opponent_score == 10):
        switch_to_level_2()

    ball_animation()
    # moving player up or down
    player.y += player_speed
    opponent.y += opponent_speed

    opponent_animation()
    player_animation()

    # setting up background color
    screen.fill(bg_color)

    # Determine paddle and ball colors based on level
    paddle_color = light_grey if current_level == 1 else pink
    ball_color = light_grey if current_level == 1 else pink

    # drawing game elements
    pygame.draw.rect(screen, paddle_color, player)
    pygame.draw.rect(screen, paddle_color, opponent)
    pygame.draw.ellipse(screen, ball_color, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

    # displaying scores
    player_text = game_font.render(f"{player_score}", False, light_grey)
    screen.blit(player_text, (420, 8))

    opponent_text = game_font.render(f"{opponent_score}", False, light_grey)
    screen.blit(opponent_text, (360, 8))

    # Display current level
    level_text = game_font.render(f"Level {current_level}", False, light_grey)
    screen.blit(level_text, (screen_width / 2 - 60, 30))

    # Check if game is over
    if player_score == 20:
        game_over_text = game_font.render("Player Wins!", False, light_grey)
        screen.blit(game_over_text, (screen_width / 2 - 100, screen_height / 2))
        pygame.display.flip()
        time.sleep(2)  # Wait for 2 seconds to show the win message
        pygame.quit()
        sys.exit()

    elif opponent_score == 20:
        game_over_text = game_font.render("Opponent Wins!", False, light_grey)
        screen.blit(game_over_text, (screen_width / 2 - 100, screen_height / 2))
        pygame.display.flip()
        time.sleep(2)  # Wait for 2 seconds to show the win message
        pygame.quit()
        sys.exit()

    # updating the window
    pygame.display.flip()
    clock.tick(60)
