import pygame
import sys
import constants
from constants import *
from asteroidfield import AsteroidField
from asteroids import Asteroids
from player import Player
from controller import Controller
from shoot import Shot
from powerups import PowerUp, PowerUpSpawns
from powerups import *


def main():
    pygame.init()
    pygame.joystick.init()  # Initialize joystick support if needed
    pygame.font.init()  # Initialize font module
    
    font = pygame.font.Font(FONT, FONT_SIZE)  # Load the font
    
    # Debug: Print number of joysticks and their names
    joystick_count = pygame.joystick.get_count()
    print(f"Number of joysticks detected: {joystick_count}")
    for i in range(joystick_count):
        js = pygame.joystick.Joystick(i)
        js.init()
        print(f"Joystick {i}: {js.get_name()}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()  # Set frame rate to 60 FPS
    dt = 0
    

    # joystick_count = pygame.joystick.get_count()
    # joysticks = []
    # for i in range(joystick_count):
    #     joystick = pygame.joystick.Joystick(i)
    #     joystick.init()
    #     joysticks.append(joystick)
    #     print(f"Initialized Joystick {i}: {joystick.get_name()}")

    # Create groups for updatable and drawable objects
    updatables = pygame.sprite.Group()
    drawables = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shoot = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
 

    # Create Player
    Player.containers = (updatables, drawables)
    controller = Controller()  # Initialize the controller
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, controller=controller)
   
   # Create Asteroids
    Asteroids.containers = (asteroids, updatables, drawables)
    AsteroidField.containers = (updatables)
    asteroid_field = AsteroidField()

    # Shoot initialization
    Shot.containers = (shoot ,updatables, drawables)
    
    PowerUp.containers = (powerups, updatables, drawables)
    PowerUpSpawns.containers = (updatables)
    powerup = PowerUpSpawns() 
    
    
    

    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}", f"\nScreen height: {SCREEN_HEIGHT}")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                controller.add_joystick(event.device_index)
            if event.type == pygame.QUIT:
                return
            

        screen.fill((0, 0, 0))
        
        # draw all game objects
        for sprite in drawables:
            sprite.draw(screen)
        
        # Update all game objects
        updatables.update(dt)
        player.timer -= dt

        
        # Check for collisions
        if player.shield_timer > 0:
            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    asteroid.kill()
        else:
            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    player.damage()
                    player.triple_shot_timer = 0
                    asteroid.kill()

        for asteroid in asteroids:
            for shot in shoot:
                if shot.collides_with(asteroid):
                    asteroid.split()
                    shot.kill()
        if player.triple_shot_timer > 0 or player.speed_boost_timer > 0 or player.shield_timer > 0:
            None
        else: 
            for powerup in powerups:
                for shot in shoot:
                    if player.collides_with(powerup) or shot.collides_with(powerup):
                        if powerup.type == "triple":
                            player.triple_shot_timer = 5
                        elif powerup.type == "speed":
                            player.speed_boost()
                            player.speed_boost_timer = 5
                        elif powerup.type == "shield":
                            player.shield_timer = 5
                        elif powerup.type == "health":
                            player.health_back()
                            player.health_timer = 0.5
                        powerup.kill()
            
        player.triple_shot_timer -= dt
        player.speed_boost_timer -= dt
        player.shield_timer -= dt
        player.health_timer -= dt

        lives_text = font.render(f"Lives: {constants.PLAYER_LIVES}", True, (255, 255, 255))
        asteroids_destroyed_text = font.render(f"Asteroids Destroyed: {constants.ASTEROIDS_DESTROYED}", True, (255, 255, 255))
        screen.blit(asteroids_destroyed_text, (10, 30))
        screen.blit(lives_text, (10, 10))  # Draw lives at the
        pygame.display.flip()
        dt = clock.tick(60) / 1000.0  # Convert milliseconds to 
pygame.quit()


if __name__ == "__main__":
    main()
