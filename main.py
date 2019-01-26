#!/usr/bin/env python3

import pygame
from random import randint, choice
from sys import argv, stderr, exit

Sound = {}
Image = {'Background': pygame.image.load("Ressources/Images/BackgroundTmp.jpg"),
         'People': 1,
         'Car': 2}

# Do not modify this class, his default comportement is necessary for the program
class   BadArgumentError(Exception):
    def __init__(self, message, errors = "BadArgumentError"):
        super().__init__(message)
        self.errors = errors

class   Entity():
    """  """
    def __init__(self, position, image, state, surface, territory = None):
        self.position = position
        self.image = image
        self.state = state
        self.surface = surface
        self.territory = territory

# Default object class
class   People(Entity):
    """ Definition of People class """
    territory = [(0, 100), (200, 300)]
    surface = [(), (), (), ()]
    def __init__(self, position = (randint(territory[0][0], territory[1][0]),
        randint(territory[1][0], territory[1][1])), image = Image['People'], state = 0):
        """ Initialise Separation's instance and check little errors """
        Entity.__init__(self, position, image, state, self.surface, self.territory)

    def __repr__(self):
        return "[position: {}\tstate: {}]".format(self.position, self.state)

class   Game():
    """  """
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Kilian tape l'incruste")
    resolution = (1366, 728)
    mouse = (0, 0)
    def __init__(self, state = False):
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(self.resolution)
        self.state = state

    def checkAction(self):
        """  """
        return

    def gameHandler(self):
        """  """
        while not self.state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = True
            self.clock.tick()
            self.checkAction()
        return

# Do not put more information in this function, it's must be clearer as possible
def     main():
    """ Main function who perform program's core action like arguments resolution """
    game = Game()
    obj = People()
    print(obj)
    #game.menu()
    game.gameHandler()

# Don't touch at this except if u don't worry of problems
if __name__ == "__main__":
    #try:
    main()
    #except BaseException as error:
    #    stderr.write(str(type(error).__name__) + ": {}\n".format(error))
    #    exit(84)
