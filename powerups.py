import pygame
import random
from constants import *
from circleshape import CircleShape
from asteroidfield import AsteroidField

class PowerUp(CircleShape):
    def __init__(self, x, y, radius, powerup_type):
        super().__init__(x, y, radius)
        self.type = powerup_type
    def draw(self, screen):
        color_map = {
            "triple": (255, 165, 0),   # Orange
            "speed": (255, 255, 0),      # Yellow
            "shield": (0, 0, 255),   # Blue
            "health": (255, 0, 0),     # Red
        }
        color = color_map.get(self.type, (255, 255, 255))
        pygame.draw.circle(screen, color, self.position, POWERUP_RADIUS, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt

    
class PowerUpSpawns(AsteroidField):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-POWERUP_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + POWERUP_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -POWERUP_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + POWERUP_RADIUS
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        powerup_types = ["triple", "speed", "shield", "health"]
        chosen_type = random.choice(powerup_types)
        powerup = PowerUp(position.x, position.y, radius, chosen_type)
        powerup.velocity = velocity
        
    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > POWERUP_SPAWN_RATE:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            self.spawn(POWERUP_RADIUS, position, velocity)