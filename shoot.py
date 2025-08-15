import pygame 
from constants import *
from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, x, y, radius, velocity):
        super().__init__(x, y, radius)
        self.velocity = pygame.Vector2(velocity)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, SHOOT_RADIUS, 2)
    
    

    def update(self, dt):
        self.position += self.velocity * dt
        # Remove the shot if it goes off-screen
        if (self.position.x < 0 or self.position.x > SCREEN_WIDTH or
            self.position.y < 0 or self.position.y > SCREEN_HEIGHT):
            self.kill()  # Remove this sprite from all groups