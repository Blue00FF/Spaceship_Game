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
        "Assets",
        "Grenade+1.mp3"
    )
)
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join(
        "Assets",
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
                "Assets",
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
                "Assets",
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
            "Assets",
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
        red_spaceship_health,
        yellow_spaceship_health
):
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
    # Using the WASD keys, the yellow spaceship can be moved, with the only
    # condition that it stays in the left half of the screen and doesn't go
    # off-screen.
    if keys_pressed[pygame.K_a] and yellow_spaceship.x - SPACESHIP_HEIGHT // \
            2 \
            - SPACESHIP_VELOCITY > 0:
        yellow_spaceship.x -= SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_s] \
            and yellow_spaceship.y + SPACESHIP_HEIGHT // 2 + \
            SPACESHIP_VELOCITY \
            < WINDOW_HEIGHT:
        yellow_spaceship.y += SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_d] \
            and yellow_spaceship.x + SPACESHIP_VELOCITY + SPACESHIP_WIDTH // \
            2 \
            < BORDER.x:
        yellow_spaceship.x += SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_w] \
            and yellow_spaceship.y - SPACESHIP_VELOCITY - SPACESHIP_HEIGHT \
            // 2 \
            > 0:
        yellow_spaceship.y -= SPACESHIP_VELOCITY


def handle_red_spaceship_movement(
        keys_pressed,
        red_spaceship
):
    # Using the arrow keys, the yellow spaceship can be moved, with the only
    # condition that it stays in the right half of the screen and doesn't go
    # off-screen.
    if keys_pressed[pygame.K_LEFT] and red_spaceship.x - SPACESHIP_VELOCITY - \
            SPACESHIP_WIDTH // 2 > BORDER.x + BORDER_THICKNESS:
        red_spaceship.x -= SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_DOWN] \
            and red_spaceship.y + SPACESHIP_HEIGHT // 2 + SPACESHIP_VELOCITY \
            < WINDOW_HEIGHT:
        red_spaceship.y += SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_RIGHT] \
            and red_spaceship.x + SPACESHIP_VELOCITY + SPACESHIP_WIDTH < \
            WINDOW_WIDTH:
        red_spaceship.x += SPACESHIP_VELOCITY
    if keys_pressed[pygame.K_UP] \
            and red_spaceship.y - SPACESHIP_VELOCITY - SPACESHIP_HEIGHT // 2 \
            > 0:
        red_spaceship.y -= SPACESHIP_VELOCITY


def handle_bullet_movement(
        on_screen_yellow_bullets,
        on_screen_red_bullets,
        yellow_spaceship,
        red_spaceship
):
    # Bullet fired from each spaceship are added to the on-screen bullet lists
    # and removed if they either hit the other spaceship or go off-screen.
    # The bullet-spaceship collisions are handled using the colliderect method
    # as they both are pygame rectangles.
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
    # Stop the game and print on the centre of the screen "Yellow/Red wins!"
    # according to the one who managed to reduce the opponent's health to zero.
    # The message is displayed for five seconds.
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
    yellow_spaceship = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_spaceship = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    on_screen_yellow_bullets = []
    on_screen_red_bullets = []
    
    yellow_spaceship_health = INITIAL_SPACESHIP_HEALTH
    red_spaceship_health = INITIAL_SPACESHIP_HEALTH
    
    clock = pygame.time.Clock()
    
    while True:
        clock.tick(FRAMES)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(
                        on_screen_yellow_bullets) < MAX_ON_SCREEN_BULLETS:
                    bullet = pygame.Rect(
                        yellow_spaceship.x + SPACESHIP_WIDTH,
                        yellow_spaceship.y + SPACESHIP_HEIGHT // 2 -
                        BULLET_HEIGHT // 2,
                        BULLET_WIDTH,
                        BULLET_HEIGHT
                    )
                    on_screen_yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
                if event.key == pygame.K_RCTRL and len(
                        on_screen_red_bullets) < MAX_ON_SCREEN_BULLETS:
                    bullet = pygame.Rect(
                        red_spaceship.x,
                        yellow_spaceship.y + SPACESHIP_HEIGHT // 2 -
                        BULLET_HEIGHT // 2,
                        BULLET_WIDTH,
                        BULLET_HEIGHT
                    )
                    on_screen_red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            
            if event.type == RED_HIT:
                red_spaceship_health -= 1
                BULLET_HIT_SOUND.play()
            
            if event.type == YELLOW_HIT:
                yellow_spaceship_health -= 1
                BULLET_HIT_SOUND.play()
        
        winner_text = ""
        if red_spaceship_health <= 0:
            winner_text = "Yellow Player Wins!"
        if yellow_spaceship_health <= 0:
            winner_text = "Red Player Wins!"
        if winner_text != "":
            declare_winner(winner_text)
            break
        
        keys_pressed = pygame.key.get_pressed()
        handle_yellow_spaceship_movement(keys_pressed, yellow_spaceship)
        handle_red_spaceship_movement(keys_pressed, red_spaceship)
        handle_bullet_movement(on_screen_yellow_bullets,
                               on_screen_red_bullets,
                               yellow_spaceship,
                               red_spaceship)
        draw_window(
            yellow_spaceship,
            red_spaceship,
            on_screen_yellow_bullets,
            on_screen_red_bullets,
            yellow_spaceship_health,
            red_spaceship_health
        )
    
    game_loop()


if __name__ == "__main__":
    game_loop()
