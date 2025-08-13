import pygame
import sys
from constants import *
from circleshape import CircleShape
from shoot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0  # Player's rotation angle
        self.timer = 0  # Timer for shooting cooldown
        
    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c] 

    def shoot(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shot_velocity = forward * PLAYER_SHOOT_SPEED
        return Shot(self.position.x, self.position.y, SHOOT_RADIUS, shot_velocity)

    
    def draw(self, screen):
        pygame.draw.polygon(screen, PLAYER_COLOR, self.triangle())    

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def accelerate(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_ACCELERATION * dt 

    def damage(self):        
        global PLAYER_LIVES
        PLAYER_LIVES -= 1
        PLAYER_COLOR = PLAYER_DAMAGE  # Change color to indicate damage
        print(f"Lives left: {PLAYER_LIVES}")
        if PLAYER_LIVES <= 0:
            print("Game Over!")
            pygame.quit()
            sys.exit()
    

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.accelerate(dt)
    
        self.position += self.velocity * dt
        self.velocity *= PLAYER_DAMPING  # Apply damping to the velocity
        
        if keys[pygame.K_SPACE]:
            if self.timer <= 0:
                self.shoot()
                self.timer = PLAYER_SHOOT_COOLDOWN

        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
