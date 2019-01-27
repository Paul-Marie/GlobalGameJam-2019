#!/usr/bin/env python3

import pygame
from random import randint, choice
from sys import argv, stderr, exit
#from os import environ

#environ['SDL_VIDEO_WINDOW_POS'] = "-10,-10".format(-100, -100)
Dialog = {'': "",
          '': "",
          '': ""}
Image = {'Background': pygame.image.load("Ressources/Images/BackgroundTmp.jpg"),
         'People': pygame.image.load("Ressources/Images/square.jpg"),
         'Car': 2}
Sound = {}

# Do not modify this class, his default comportement is necessary for the program
class   BadArgumentError(Exception):
    def __init__(self, message, errors = "BadArgumentError"):
        super().__init__(message)
        self.errors = errors

class   Entity():
    """  """
    time = 0
    def __init__(self, position, image, state, surface, velocity = 0,
        territory = [], direction = (0, 0), type = 0, size = 100):
        """  """
        self.position = position
        self.image = image
        self.state = state
        self.surface = surface
        self.territory = territory
        self.velocity = velocity
        self.direction = direction
        self.type = type
        self.size = size

    def display(self, window):
        """  """
        window.blit(self.image, self.position, self.surface[self.state])

    def collider(self, new_pos, obj):
        """ Return 1 if one or many point of the two HitBox's Entity object will collide"""
        if (new_pos['x'] > self.territory[0][0] and new_pos['y'] > self.territory[0][1]
        and new_pos['x'] + self.direction[0] < self.territory[1][0]
        and new_pos['y'] + self.direction[1] < self.territory[1][1]):
            if (obj is self or len(list(filter(
                    lambda x: x in range(new_pos['x'], new_pos['x'] + self.size['x']),
                    range(obj.position[0], obj.position[0] + obj.size['x'])))) != 0
                and len(list(filter(
                    lambda y: y in range(new_pos['y'], new_pos['y'] + self.size['y']),
                    range(obj.position[1], obj.position[1] + obj.size['y'])))) != 0):
                return 1
        return 0

    def update(self, object_list, elapsed_time):
        """  """
        self.time += elapsed_time + randint(0, 10)
        new_pos = {'x': self.position[0] + self.direction[0],
                   'y': self.position[1] + self.direction[1]}
        if sum([self.collider(new_pos, obj) for obj in object_list]) == 1:
            self.position = (new_pos['x'], new_pos['y'])
        if self.time >= 1000:
            self.direction = (randint(0, 2) - 1, randint(0, 2) - 1)
            self.state = (self.state + 1) % len(self.surface)
            self.time = 0

# Default object class
class   People(Entity):
    """ Definition of People class """
    type = 1
    velocity = 1000
    size = {'x': 50, 'y': 50}
    territory = [(10, 10), (700, 500)]
    surface = [(0, 0, 49, 49), (51, 0, 49, 49), (0, 51, 49, 49), (51, 51, 49, 49)]
    def __init__(self, position = (0, 0), image = Image['People'], state = 0):
        """  """
        position = (randint(self.territory[0][0], self.territory[1][0]),
                    randint(self.territory[0][1], self.territory[1][1]))
        direction = (randint(0, 2) - 1, randint(0, 2) - 1)
        Entity.__init__(self, position, image, state, self.surface, self.velocity,
                        self.territory, direction, self.type, self.size)
        self.state = randint(0, 3)

    def __repr__(self):
        return "[position: {}\tstate: {}\ttime: {}\tdirection: {}]".format(
            self.position, self.state, self.time, self.direction)

# Default object class
class   Car(Entity):
    """ Definition of People class """
    type = 2
    velocity = 2000
    size = {'x': 250, 'y': 100}
    #territory = [(10, 10), (700, 500)]
    #surface = [(0, 0, 49, 49), (51, 0, 49, 49), (0, 51, 49, 49), (51, 51, 49, 49)]
    def __init__(self, position = (0, 0), image = Image['Car'], state = 0):
        """  """
        #position = (randint(self.territory[0][0], self.territory[1][0]),
        #            randint(self.territory[0][1], self.territory[1][1]))
        #direction = (randint(0, 2) - 1, randint(0, 2) - 1)
        Entity.__init__(self, position, image, state, self.surface, self.velocity,
                        self.territory, direction, self.type, self.size)
        self.state = randint(0, 3)

    def __repr__(self):
        return "[position: {}\tstate: {}\ttime: {}\tdirection: {}]".format(
            self.position, self.state, self.time, self.direction)

class   Game():
    """  """
    mouse = (0, 0)
    people_list = []
    resolution = (1920, 1080)
    def __init__(self, state = False):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Kilian tape l'incruste")
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(self.resolution)
        self.state = state

    def checkAction(self):
        """  """
        self.mouse = pygame.mouse.get_pos()
        milliseconds = self.clock.get_time()
        [people.update(self.people_list, milliseconds) for people in self.people_list]
        #[print(people) for people in self.people_list]
        return

    def display(self):
        """  """
        self.window.blit(Image['Background'], (0, 0))
        [people.display(self.window) for people in self.people_list]
        #[car.display(self.window) for car in self.car_list]
        #[object.display(self.window) for object in self.object_list]
        pygame.display.update()
        return

    def gameHandler(self):
        """  """
        while not self.state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = True
            self.clock.tick(60)
            self.checkAction()
            self.display()
        return

    def startMenu(self, menu_number):
        """  """
        if menu_number == 1:
            [self.people_list.append(People()) for i in range(0, 6)]
            #[self.car_list.append(People()) for i in range(0, 6)]
            #[self.car_list.append(People()) for i in range(0, 6)]
        return

# Do not put more information in this function, it's must be clearer as possible
def     main():
    """ Main function who perform program's core action like arguments resolution """
    game = Game()
    #game.menu()
    game.startMenu(1)
    game.gameHandler()
    pygame.quit()

# Don't touch at this except if u don't worry of problems
if __name__ == "__main__":
    #try:
    main()
    #except BaseException as error:
    #    stderr.write(str(type(error).__name__) + ": {}\n".format(error))
    #    exit(84)
