import pygame
import os

# Initialise the pygame processes to handle the text and the sound effects
pygame.font.init()
pygame.mixer.init()

# Assign window dimensions to variables for reuse
WINDOW_WIDTH, WINDOW_HEIGHT = 900, 500
# Set pygame window with declared dimensions
WINDOW = pygame.display.set_mode(
    (
        WINDOW_WIDTH,
        WINDOW_HEIGHT
    )
)
# Set pygame window title
pygame.display.set_caption("Spaceship Fight!")

# Assign colours to variables in order to make the code more readable
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Instantiate object representing the uncrossable divider between the two
# spaceships
BORDER_THICKNESS = 10
BORDER = pygame.Rect(
    WINDOW_WIDTH // 2 - BORDER_THICKNESS // 2,
    0,
    BORDER_THICKNESS,
    WINDOW_HEIGHT
)

# Instantiate objects containing the game sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(
    os.path.join(
        "GameAssets",
        "Grenade+1.mp3"
    )
)
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join(
        "GameAssets",
        "Gun+Silencer.mp3"
    )
)

# Instantiate objects containing font information
HEALTH_FONT = pygame.font.SysFont(
    "comicsans",
    30
)
WINNER_FONT = pygame.font.SysFont(
    "comicsans",
    100
)

# Initialise game variables
FRAMES = 60
SPACESHIP_VELOCITY = 5
BULLET_VELOCITY = 7
MAX_ON_SCREEN_BULLETS = 3
INITIAL_SPACESHIP_HEALTH = 10
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
BULLET_WIDTH, BULLET_HEIGHT = 10, 5

# Define custom events for spaceships getting hit by a bullet
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Instantiate objects containing the spaceship images
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(
    # Rotate the image 90 degrees to the right to make it face the other
    # spaceship
    pygame.transform.scale(
        # Scale down the image from its original size, otherwise it
        # would take up the whole screen
        pygame.image.load(
            # Load the actual image from the GameAssets folder
            os.path.join(
                "GameAssets",
                "spaceship_yellow.png"
            )
        ),
        (
            SPACESHIP_WIDTH,
            SPACESHIP_HEIGHT
        )
    ),
    90)

RED_SPACESHIP_IMAGE = pygame.transform.rotate(
    # Rotate the image 90 degrees to the left to make it face the other
    # spaceship
    pygame.transform.scale(
        # Scale down the image from its original size, otherwise it
        # would take up the whole screen
        pygame.image.load(
            # Load the actual image from the GameAssets folder
            os.path.join(
                "GameAssets",
                "spaceship_red.png"
            )
        ),
        (
            SPACESHIP_WIDTH,
            SPACESHIP_HEIGHT
        )
    ),
    270)

# Load the image to put as background, scaled to the pygame window size
BACKGROUND_IMAGE = pygame.transform.scale(
    pygame.image.load(
        os.path.join(
            "GameAssets",
            "space.png"
        )
    ),
    (
        WINDOW_WIDTH,
        WINDOW_HEIGHT
    )
)


def draw_window(
        yellow_spaceship,
        red_spaceship,
        on_screen_yellow_bullets,
        on_screen_red_bullets,
        yellow_spaceship_health,
        red_spaceship_health
):
    """Function containing the logic to draw the game window at each frame."""
    # Draw the background
    WINDOW.blit(
        BACKGROUND_IMAGE,
        (0, 0)
    )
    
    # Draw the divider
    pygame.draw.rect(WINDOW, BLACK, BORDER)
    
    # Instantiate the objects representing the spaceship health points
    yellow_spaceship_health_text = HEALTH_FONT.render(
        f"Yellow Spaceship Health: {yellow_spaceship_health}",
        1,
        WHITE
    )
    red_spaceship_health_text = HEALTH_FONT.render(
        f"Red Spaceship Health: {red_spaceship_health}",
        1,
        WHITE
    )
    
    # Display the spaceship health points on the screen
    WINDOW.blit(
        yellow_spaceship_health_text,
        (
            10,
            10
        )
    )
    WINDOW.blit(
        red_spaceship_health_text,
        (
            WINDOW_WIDTH - red_spaceship_health_text.get_width() - 10,
            10
        )
    )
    
    # Draw the spaceships on the screen at their current positions
    WINDOW.blit(
        YELLOW_SPACESHIP_IMAGE,
        (
            yellow_spaceship.x,
            yellow_spaceship.y
        )
    )
    WINDOW.blit(
        RED_SPACESHIP_IMAGE,
        (
            red_spaceship.x,
            red_spaceship.y
        )
    )
    
    # Draw each bullet object that has been fired and hasn't "disappeared"
    # yet on the screen
    for bullet in on_screen_yellow_bullets:
        pygame.draw.rect(
            WINDOW,
            YELLOW,
            bullet
        )
    for bullet in on_screen_red_bullets:
        pygame.draw.rect(
            WINDOW,
            RED,
            bullet
        )
    
    # Update the window image with the new information
    pygame.display.update()


def handle_yellow_spaceship_movement(
        keys_pressed,
        yellow_spaceship
):
    """Function containing the logic to handle the movement of the yellow
    spaceship. Using the WASD keys, the yellow spaceship can be moved
    anywhere on the screen, while staying in the left half of the screen and
    on-screen. To make it look better, I also imposed the condition that the
    health text area is off-limits as well."""
    if keys_pressed[pygame.K_a] and yellow_spaceship.x - SPACESHIP_VELOCITY > 0:
        yellow_spaceship.x -= SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_s] \
            and yellow_spaceship.y + SPACESHIP_HEIGHT + SPACESHIP_VELOCITY \
            < WINDOW_HEIGHT - 15:
        yellow_spaceship.y += SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_d] \
            and yellow_spaceship.x + SPACESHIP_VELOCITY + SPACESHIP_WIDTH \
            < BORDER.x + 15:
        yellow_spaceship.x += SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_w] \
            and yellow_spaceship.y - SPACESHIP_VELOCITY > 55:
        yellow_spaceship.y -= SPACESHIP_VELOCITY


def handle_red_spaceship_movement(
        keys_pressed,
        red_spaceship
):
    """Function containing the logic to handle the movement of the red
    spaceship. Using the arrow keys, the yellow spaceship can be moved
    anywhere on the screen, while staying in the right half of the screen and
    on-screen. To make it look better, I also imposed the condition that the
    health text area is off-limits as well."""
    if keys_pressed[pygame.K_LEFT] and red_spaceship.x - SPACESHIP_VELOCITY \
            > BORDER.x + BORDER_THICKNESS:
        # Move spaceship to the LEFT
        red_spaceship.x -= SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_DOWN] \
            and red_spaceship.y + SPACESHIP_HEIGHT + SPACESHIP_VELOCITY \
            < WINDOW_HEIGHT - 15:
        # Move spaceship towards the bottom of the screen
        red_spaceship.y += SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_RIGHT] \
            and red_spaceship.x + SPACESHIP_VELOCITY + SPACESHIP_WIDTH < \
            WINDOW_WIDTH + 15:
        # Move spaceship to the RIGHT
        red_spaceship.x += SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_UP] \
            and red_spaceship.y - SPACESHIP_VELOCITY > 55:
        # Move spaceship towards the top of the screen
        red_spaceship.y -= SPACESHIP_VELOCITY


def handle_bullet_movement(
        on_screen_yellow_bullets,
        on_screen_red_bullets,
        yellow_spaceship,
        red_spaceship
):
    """Function that contains the logic to handle bullet movement. Bullets
    fired from each spaceship are added to the on-screen bullet lists and
    removed if they either hit the other spaceship or go off-screen.
    The bullet-spaceship collisions are handled using the collideRect method
    as they both are pygame rectangles."""
    for bullet in on_screen_yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red_spaceship.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            on_screen_yellow_bullets.remove(bullet)
        elif bullet.x > WINDOW_WIDTH:
            on_screen_yellow_bullets.remove(bullet)
    
    for bullet in on_screen_red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow_spaceship.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            on_screen_red_bullets.remove(bullet)
        elif bullet.x < 0:
            on_screen_red_bullets.remove(bullet)


def declare_winner(
        text
):
    """ Function containing the logic to print on the centre of the screen
    'Yellow/Red Player wins!' according to which one who managed to reduce
    the opponent's health points to zero. The message is displayed for five
    seconds."""
    winner_text = WINNER_FONT.render(
        text,
        1,
        WHITE
    )
    WINDOW.blit(
        winner_text,
        (
            WINDOW_WIDTH // 2 - winner_text.get_width() // 2,
            WINDOW_HEIGHT // 2 - winner_text.get_height() // 2
        )
    )
    pygame.display.update()
    pygame.time.delay(5000)


def game_loop():
    """Main game loop."""
    # Instantiate the objects representing the spaceships.
    yellow_spaceship = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_spaceship = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    # Initialise the lists that will contain the on-screen bullets fired by
    # each spaceship.
    on_screen_yellow_bullets = []
    on_screen_red_bullets = []
    
    # Initialise the spaceship health values.
    yellow_spaceship_health = INITIAL_SPACESHIP_HEALTH
    red_spaceship_health = INITIAL_SPACESHIP_HEALTH
    
    # Initialise the pygame clock object that will dictate the speed of the
    # game.
    clock = pygame.time.Clock()
    
    # Initialise a variable declaring whether the game has yet to be
    # terminated by the user by closing the game window.
    running = True
    
    while running:
        clock.tick(FRAMES)
        # Handling breaking the game loop and terminating the process when the
        # pygame window is closed.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                break
            
            # Handling firing bullets when either the left control or the
            # right control button have been pressed. Using the KEYDOWN
            # event each key press fires one bullet and cannot be held down
            # to create continuous fire.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(
                        on_screen_yellow_bullets) < MAX_ON_SCREEN_BULLETS:
                    # Draw the bullet in front of the spaceship.
                    bullet = pygame.Rect(
                        yellow_spaceship.x + SPACESHIP_WIDTH - 15,
                        yellow_spaceship.y + SPACESHIP_HEIGHT // 2 +
                        BULLET_HEIGHT,
                        BULLET_WIDTH,
                        BULLET_HEIGHT
                    )
                    # Add the bullet to the list of on-screen bullets and
                    # limit the amount of on-screen bullets to prevent
                    # continuous firing.
                    on_screen_yellow_bullets.append(bullet)
                    # Play bullet sound.
                    BULLET_FIRE_SOUND.play()
                
                if event.key == pygame.K_RCTRL and len(
                        on_screen_red_bullets) < MAX_ON_SCREEN_BULLETS:
                    # Draw the bullet in front of the spaceship.
                    bullet = pygame.Rect(
                        red_spaceship.x,
                        red_spaceship.y + SPACESHIP_HEIGHT // 2 +
                        BULLET_HEIGHT,
                        BULLET_WIDTH,
                        BULLET_HEIGHT
                    )
                    # Add the bullet to the list of on-screen bullets and
                    # limit the amount of on-screen bullets to prevent
                    # continuous firing.
                    on_screen_red_bullets.append(bullet)
                    # Play bullet sound.
                    BULLET_FIRE_SOUND.play()
            
            # Reduce spaceship health and play a sound every time a spaceship
            # is hit by an opponent's bullet.
            if event.type == RED_HIT:
                red_spaceship_health -= 1
                BULLET_HIT_SOUND.play()
            
            if event.type == YELLOW_HIT:
                yellow_spaceship_health -= 1
                BULLET_HIT_SOUND.play()
        
        # Break the main loop if the game window has been closed.
        if not running:
            break
        
        # Capture keyboard key presses and pass those to the functions
        # handling spaceship movement.
        keys_pressed = pygame.key.get_pressed()
        handle_yellow_spaceship_movement(keys_pressed, yellow_spaceship)
        handle_red_spaceship_movement(keys_pressed, red_spaceship)
        handle_bullet_movement(on_screen_yellow_bullets,
                               on_screen_red_bullets,
                               yellow_spaceship,
                               red_spaceship)
        # Redraw the game window at each iteration of the game loop to cover
        # previous game windows.
        draw_window(
            yellow_spaceship,
            red_spaceship,
            on_screen_yellow_bullets,
            on_screen_red_bullets,
            yellow_spaceship_health,
            red_spaceship_health
        )

        # Call the declare_winner function if the winning condition is
        # triggered.
        winner_text = ""
        if red_spaceship_health <= 0:
            winner_text = "Yellow Player Wins!"
        if yellow_spaceship_health <= 0:
            winner_text = "Red Player Wins!"
        if winner_text != "":
            declare_winner(winner_text)
            break
    # Restart the game if the main game loop has been broken because of a
    # win and not because of the window closing.
    if running:
        game_loop()


if __name__ == "__main__":
    game_loop()
