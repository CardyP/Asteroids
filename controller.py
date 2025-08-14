import pygame

class Controller():
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joysticks = []

    def add_joystick(self, joystick_index):
        joystick = pygame.joystick.Joystick(joystick_index)
        joystick.init()
        self.joysticks.append(joystick)
        print(f"Initialized Joystick {joystick_index}: {joystick.get_name()}")