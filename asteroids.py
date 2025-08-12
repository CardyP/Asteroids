import pygame
import random
from circleshape import CircleShape
from main import asteroid
from constants import *

class Asteroids(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def split(self):
        self.kill()  # Remove the current asteroid
        if self.radius <= ASTEROID_MIN_RADIUS:
            return "Asteroid too small to split"
        else:
            rand_angle = random.uniform(20, 50)
            
            velocity1 = self.velocity.rotate(rand_angle) * 1.2
            velocity2 = self.velocity.rotate(-rand_angle) * 1.2

            new_radius = self.radius - ASTEROID_MIN_RADIUS
            
            asteroid1 = Asteroids(self.position, new_radius, velocity1)
            asteroid2 = Asteroids(self.position, new_radius, velocity2)
            return asteroid1, asteroid2
        
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt