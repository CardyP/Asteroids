import pygame
import sys
import time
import constants
from circleshape import CircleShape
from shoot import Shot

class Player(CircleShape):
    def __init__(self, x, y, controller=None):
        super().__init__(x, y, constants.PLAYER_RADIUS)
        self.rotation = 0  # Player's rotation angle
        self.timer = 0  # Timer for shooting cooldown
        self.controller = controller
        self.triple_shot_timer = 0  # Timer for triple shot duration
        self.speed_boost_timer = 0  # Timer for speed boost duration
        self.shield_timer = 0  # Timer for shield duration
        self.health_timer = 0  # Timer for health regeneration
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
        shot_velocity = forward * constants.PLAYER_SHOOT_SPEED
        return Shot(self.position.x, self.position.y, constants.SHOOT_RADIUS, shot_velocity)

    def get_color(self):   
        if self.shield_timer > 0:
            return (0, 0, 255)      # Blue for shield
        elif self.speed_boost_timer > 0:
            return (255, 255, 0)    # Yellow for speed
        elif self.triple_shot_timer > 0:
            return (255, 165, 0)    # Orange for triple shot
        elif self.health_timer > 0:
            return (255, 0, 0)      # Green for health
        else:
            return constants.PLAYER_COLOR
    
    
    def triple_shot(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        left = pygame.Vector2(0, 1).rotate(self.rotation - 30)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 30)
        shot_velocity = forward * constants.PLAYER_SHOOT_SPEED
        shot_velocity_left = left * constants.PLAYER_SHOOT_SPEED
        shot_velocity_right = right * constants.PLAYER_SHOOT_SPEED
        # Draw three shots in a triangular formation
        return Shot(self.position.x, self.position.y, constants.SHOOT_RADIUS, shot_velocity), Shot(self.position.x + 10, self.position.y + 10, constants.SHOOT_RADIUS, shot_velocity_left), Shot(self.position.x - 10, self.position.y + 10, constants.SHOOT_RADIUS, shot_velocity_right)
    
    def health_back(self):
        constants.PLAYER_LIVES += 1
        print(self.health_timer)
        if self.health_timer > 0:
            constants.PLAYER_COLOR = (255, 0, 0)  # Change color

    def speed_boost(self):
        if self.speed_boost_timer > 0:
            self.velocity *= 1.5

    def shield(self):
        if self.shield_timer > 0:
            constants.PLAYER_COLOR = (0, 0, 255)

    def draw(self, screen):
        color = self.get_color()
        pygame.draw.polygon(screen, color, self.triangle())    

    def rotate(self, dt):
        self.rotation += constants.PLAYER_TURN_SPEED * dt
    
    def accelerate(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * constants.PLAYER_ACCELERATION * dt 

    def damage(self):        
        constants.PLAYER_LIVES -= 1
        #constants.PLAYER_COLOR = constants.PLAYER_DAMAGE  # Change color to indicate damage
        constants.PLAYER_COLOR = (255, 255, 255)
        print(f"Lives left: {constants.PLAYER_LIVES}")
        if constants.PLAYER_LIVES <= 0:
            self.triple_shot_timer = 0
            print("Game Over!")
            time.sleep(2)
            pygame.quit()
            sys.exit()
    

    def update(self, dt):
        keys = pygame.key.get_pressed()
        joystick = self.controller.joysticks[0] if self.controller and self.controller.joysticks else None

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.accelerate(dt)
    
        self.position += self.velocity * dt
        self.velocity *= constants.PLAYER_DAMPING  # Apply damping to the velocity
        

        
        if keys[pygame.K_SPACE]:
            if self.timer <= 0:
                if self.triple_shot_timer > 0:
                    self.triple_shot()  # Assuming you want to draw the triple shot
                else:
                    self.shoot()
                self.timer = constants.PLAYER_SHOOT_COOLDOWN

        if joystick:
            axis_x = joystick.get_axis(0)
            axis_y = joystick.get_axis(1)
            if abs(axis_x) > 0.1:
                self.rotate(axis_x * dt * constants.PLAYER_TURN_SPEED / 300)
            if abs(axis_y) > 0.1:
                self.accelerate(axis_y * -dt * constants.PLAYER_ACCELERATION / 300)
            if joystick.get_button(0):
                if self.timer <= 0:
                    if self.triple_shot_timer > 0:
                        self.triple_shot()  # Assuming you want to draw the triple shot
                    else:
                        self.shoot()
                    self.timer = constants.PLAYER_SHOOT_COOLDOWN

        if self.position.x < 0:
            self.position.x = constants.SCREEN_WIDTH
        if self.position.x > constants.SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = constants.SCREEN_HEIGHT
        if self.position.y > constants.SCREEN_HEIGHT:
            self.position.y = 0
