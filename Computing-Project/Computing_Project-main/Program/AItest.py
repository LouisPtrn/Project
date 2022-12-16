import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set the width and height of the screen [width, height]
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Set the number of segments the snake will have
NUM_SEGMENTS = 20

# This sets the margin between each segment
SEGMENT_MARGIN = 3

# Create an empty list of segments
segments = []

# Initialize pygame
pygame.init()

# Set the title of the window
pygame.display.set_caption('Snake Game')

# Set the screen size
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Create the snake head
head = pygame.Rect(300, 100, 10, 10)

# Create an empty list of segments
segments.append(head)

# Set the initial speed of the snake
x_change = 10
y_change = 0

# Create the food for the snake
food = pygame.Rect(random.randint(0, SCREEN_WIDTH - 10),
                   random.randint(0, SCREEN_HEIGHT - 10), 10, 10)

# Create a clock object
clock = pygame.time.Clock()

# Set the flag to False so the game will run
game_over = False

# -------- Main Program Loop -----------
while not game_over:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        # Set the speed based on the key pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = (x_change - 10)
                y_change = 0
            if event.key == pygame.K_RIGHT:
                x_change = (x_change + 10)
                y_change = 0
            if event.key == pygame.K_UP:
                x_change = 0
                y_change = (y_change - 10)
            if event.key == pygame.K_DOWN:
                x_change = 0
                y_change = (y_change + 10)

    # --- Game logic
    # Move the snake head
    head.x += x_change
    head.y += y_change

    # Check if the snake has eaten the food
    if head.colliderect(food):
        # Set the food to a random location
        food.x = random.randint(0, SCREEN_WIDTH - 10)
        food.y = random.randint(0, SCREEN_HEIGHT - 10)

        # Append a new segment
        segments.append(pygame.Rect(head.x, head.y, 10, 10))

    # Move the segment
    for index in range(len(segments) - 1, 0, -1):
        segments[index].x = segments[index - 1].x
        segments[index].y = segments[index - 1].y

    # Move the segment 0 to where the head is
    if len(segments) > 0:
        segments[0].x = head.x
        segments[0].y = head.y

    # Check if the snake has collided with itself
    for segment in segments[1:]:
        if head.colliderect(segment):
            game_over = True

    # Check if the snake has reached the edge of the screen
    if head.x < 0 or head.x > SCREEN_WIDTH - 10 or head.y < 0 or head.y > SCREEN_HEIGHT - 10:
        game_over = True

    # --- Draw the screen
    # Set the background color
    screen.fill(BLACK)

    # Draw the food
    pygame.draw.rect(screen, RED, food)

    # Draw the snake
    for segment in segments:
        pygame.draw.rect(screen, WHITE, segment)

    # Update the screen
    pygame.display.flip()

    # Set the frame rate
    clock.tick(200)

# Exit the program
pygame.quit()