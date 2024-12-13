# snake_game.py

import pygame
import time
import random
from snake_db import create_db, get_user_details, save_user_score, save_user

# Initialize the pygame library
pygame.init()

# Game window size
window_x = 720
window_y = 480

# Define colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
green = pygame.Color(0, 255, 0)

# Initialize the game window
pygame.display.set_caption('Snake Game with Database')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# Function to prompt user for their username and load their data
def prompt_for_username():
    username = input("Enter your username: ")
    
    # Check if the user exists in the DB
    user = get_user_details(username)
    
    if user:
        print(f"Welcome back {username}! Your current level is {user[2]} and your highest score is {user[3]}")
        level = user[2]
        high_score = user[3]
    else:
        print(f"Welcome {username}! It seems you're new to the game!")
        level = 1  # Default starting level
        high_score = 0  # No score yet
    
    return username, level, high_score

# Function to adjust snake speed based on the level
def update_game_level(level):
    if level == 1:
        return 15  # Speed for level 1
    elif level == 2:
        return 20  # Speed for level 2
    elif level == 3:
        return 25  # Speed for level 3
    else:
        return 15  # Default speed

# Function to display the score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

# Function to handle game over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Game Over! Your Score is: ' + str(score), True, pygame.Color(255, 0, 0))
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

# Main game function
def game():
    global score, snake_speed

    # Prompt for username and get their level and high score
    username, level, high_score = prompt_for_username()
    snake_speed = update_game_level(level)

    # Initialize game variables
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

    # Game loop
    while True:
        # Handle key events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                if event.key == pygame.K_p:  # Pause and save the game state
                    print("Game Paused. Saving progress...")
                    save_user_score(user_id, score, level)
                    save_user(username, level, score)
                    time.sleep(2)
                    return  # Pause and exit or return to main menu

        # Avoid snake from moving in opposite directions
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        # Snake body growing
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 10
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
        fruit_spawn = True

        # Filling the background with black
        game_window.fill(black)

        # Drawing the snake
        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Drawing the fruit
        pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

        # Checking if the snake hits the wall
        if snake_position[0] < 0 or snake_position[0] > window_x - 10 or snake_position[1] < 0 or snake_position[1] > window_y - 10:
            game_over()

        # Checking if the snake collides with itself
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over()

        # Displaying the score
        show_score(1, white, 'times new roman', 20)

        # Updating the game screen
        pygame.display.update()

        # Setting the game speed
        fps.tick(snake_speed)

        # Save the score to the database if the score is higher than the high_score
        if score > high_score:
            high_score = score
        save_user_score(user_id, score, level)
        save_user(username, level, high_score)

# Create the database and tables
create_db()

# Start the game
game()
