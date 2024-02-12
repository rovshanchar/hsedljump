# import libraries
import pygame
import random

# initialise pygame
pygame.init()

# game window dimension
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("hsedl jump")

# set FPS
clock = pygame.time.Clock()
FPS = 60

# game
GRAVITY = 1
MAX_PLATFORMS = 10

# colours
WHITE = (255, 255, 255)

# load image
bg_image = pygame.image.load("assets/bg.jpg").convert_alpha()
player_image = pygame.image.load("assets/player.png").convert_alpha()
platform_image = pygame.image.load("assets/platform.jpg").convert_alpha()

# Взято из туториала

# player class
class Player:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(player_image, (45, 45))
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.vel_y = 0
        self.rect.center = (x, y)
        self.flip = False

    def draw(self):
        screen.blit(
            pygame.transform.flip(self.image, self.flip, False),
            (self.rect.x - 12, self.rect.y - 5),
        )
        pygame.draw.rect(screen, WHITE, self.rect, 2)

    def move(self):
        # variables
        dx = 0
        dy = 0
        # Взято из туториала

        # keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -10
            self.flip = True
        if key[pygame.K_d]:
            dx = 10
            self.flip = False

        # gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # screen contol
        if self.rect.left + dx < 10:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        # check platform collision
        for platform in platform_group:
            # collision
            if platform.rect.colliderect(
                self.rect.x, self.rect.y + dy, self.width, self.height
            ):
                # check if above the platform
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20

        # check ground collision
        if self.rect.bottom + dy > SCREEN_HEIGHT:
            dy = 0
            self.vel_y = -20

        # udpate rectangle posotion
        self.rect.x += dx
        self.rect.y += dy


# platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# player instance
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

# create sprite groups
platform_group = pygame.sprite.Group()

# create temperary platforms
for p in range(MAX_PLATFORMS):
    p_w = random.randint(40, 60)
    p_x = random.randint(0, SCREEN_WIDTH - p_w)
    p_y = p * random.randint(80, 120)
    platform = Platform(p_x, p_y, p_w)
    platform_group.add(platform)

# gmae loop
run = True
while run:

    clock.tick(FPS)

    player.move()

    # draw background
    screen.blit(bg_image, (0, 0))

    # draw spirites
    platform_group.draw(screen)
    player.draw()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update diplay window
    pygame.display.update()