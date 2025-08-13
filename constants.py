import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 0.8  # seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300  # degrees per second
PLAYER_SPEED = 200  # pixels per second
PLAYER_ACCELERATION = 200       # pixels per second squared
PLAYER_DAMPING = 0.99   # velocity damping factor per frame
PLAYER_LIVES = 3
PLAYER_COLOR = (255, 255, 255)
PLAYER_DAMAGE = (10, 10, 10)  # RGB color for damage effect   

SHOOT_RADIUS = 5
PLAYER_SHOOT_SPEED = 500  # pixels per second
PLAYER_SHOOT_COOLDOWN = 0.3  # seconds

pygame.font.init()
FONT = pygame.font.Font("8-bit.ttf", 24)