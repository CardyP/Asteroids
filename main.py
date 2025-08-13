import pygame
import sys
from constants import *
from asteroidfield import AsteroidField
from asteroids import Asteroids
from player import Player
from shoot import Shot


def main():
    pygame.init()
    pygame.joystick.init()  # Initialize joystick support if needed

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()  # Set frame rate to 60 FPS
    dt = 0
    joystick = []

    # Create groups for updatable and drawable objects
    updatables = pygame.sprite.Group()
    drawables = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shoot = pygame.sprite.Group()

    # Create Player
    Player.containers = (updatables, drawables)
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
   
   # Create Asteroids
    Asteroids.containers = (asteroids, updatables, drawables)
    AsteroidField.containers = (updatables)
    asteroid_field = AsteroidField()

    # Shoot initialization
    Shot.containers = (shoot ,updatables, drawables)
    
    

    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}", f"\nScreen height: {SCREEN_HEIGHT}")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                print("Joystick added:", event.joy)
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
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                print("Game Over!")
                pygame.quit()
                sys.exit()

        for asteroid in asteroids:
            for shot in shoot:
                if shot.collides_with(asteroid):
                    asteroid.split()
                    shot.kill()
        
        
        pygame.display.flip()
        dt = clock.tick(60) / 1000.0  # Convert milliseconds to seconds
pygame.quit()


if __name__ == "__main__":
    main()
