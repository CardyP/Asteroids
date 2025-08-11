import pygame
from constants import *
from player import Player

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()  # Set frame rate to 60 FPS
    dt = 0

    #Player
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}", f"\nScreen height: {SCREEN_HEIGHT}")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill((0, 0, 0))
        player.draw(screen)
        player.update(dt)
        
        
        pygame.display.flip()

       

        dt = clock.tick(60) / 1000.0  # Convert milliseconds to seconds
if __name__ == "__main__":
    main()
