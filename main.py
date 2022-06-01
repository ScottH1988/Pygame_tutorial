import pygame
import os
pygame.font.init()
pygame.init()

# Creates the initial pygame surface, constant variabls are written in CAPS
WIDTH,HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Name the window
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
FPS = 60
VEL = 5
BULLET_VELOCITY = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('space.png')), (WIDTH, HEIGHT))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)


# Initial image/surface/characters
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('spaceship_yellow.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('spaceship_red.png'))

# How to resize images/surfaces/characters
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale
    (YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale
    (RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

# Creates new and custom events in Pygame, must got up in sequence +1, +2 etc.
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Draw order matters, images appear in the order they are coded
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
        # Colours the background
        #WIN.fil (WHITE)
        # Adds background image and starting position    
        WIN.blit(SPACE, (0, 0))
        pygame.draw.rect(WIN, BLACK, BORDER)
      
        
        # Draws font onto the game surface
        red_health_text = HEALTH_FONT.render(
            "Health: " + str(red_health), 1, WHITE)
        yellow_health_text = HEALTH_FONT.render(
            "Health " + str(yellow_health), 1, WHITE)

        # Adds text to right handside of the screen with some padding       
        WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
        # Adds text to left of the screen
        WIN.blit(yellow_health_text, (10, 10))
       
        # Adds a surface/image/character to the main display
        WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
        WIN.blit(RED_SPACESHIP, (red.x, red.y))
               


        # Draws the bullets
        for bullet in red_bullets:
            pygame.draw.rect(WIN, RED, bullet)

        for bullet in yellow_bullets:
            pygame.draw.rect(WIN, YELLOW, bullet)



        # Keeps the display updated
        pygame.display.update()   

# Character movement for Yellow
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT : #DOWN
        yellow.y += VEL   

# Character movement for Red
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width : #LEFT
            red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #RIGHT
            red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #UP
            red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: #DOWN
            red.y += VEL   

# Bullet firing & collision function
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


# Main game loop
def main():
    # Draws the ships/characters
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    # List for storing bullets fired
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10


    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # Shooting projectiles and setting an "ammo limit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
            # Tracks health
            if event.type == RED_HIT:
                red_health -= 1
            
            if event.type == YELLOW_HIT:
                yellow_health -= 1
        
    

    winner_text = ""
    # How to track and announce winner
    if red_health <= 0:
        winner_text = "Yellow Wins"

    if yellow_health <= 0:
        winner_text = "Red Wins"

    if winner_text != "":
        pass # SOMEONE WON

        # Game keyboard controls
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)
    
    main()

# ensures main runs at the correct time
if __name__ == "__main__":
    main()

