#!/usr/bin/env python3

import pygame
from math import radians, cos, sin, tan, pi
from random import randint, choice
from sys import argv, stderr, exit
#from os import environ

#environ['SDL_VIDEO_WINDOW_POS'] = "-10,-10".format(-100, -100)
Dialog = {'': "",
          '': "",
          '': ""}
Image = {'Background': pygame.image.load("Ressources/Images/Background.jpg"),
         'People': pygame.image.load("Ressources/Images/YellowJacket.png"),
         'Player': pygame.image.load("Ressources/Images/Player.png"),
         'Car': pygame.image.load("Ressources/Images/Car.png")}
Sound = {}

# Do not modify this class, his default comportement is necessary for the program
class   BadArgumentError(Exception):
    def __init__(self, message, errors = "BadArgumentError"):
        super().__init__(message)
        self.errors = errors

class   Entity():
    """ An 'Entity' is an object who can interact with other pair """
    time = 0
    speed = 0
    def __init__(self, position, image, state, surface, velocity = 0,
        territory = [], direction = (0, 0), type = 0, size = 100):
        """ Instanciate an 'Entity' """
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
        """ Display an 'Entity' sprite onto the 'window' """
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
        """ Update the object' sprite and position """
        self.time += elapsed_time + randint(0, 10)
        new_pos = {'x': self.position[0] + self.speed * self.direction[0],
                   'y': self.position[1] + self.speed * self.direction[1]}
        if sum([self.collider(new_pos, obj) for obj in object_list]) == 1:
            self.position = (new_pos['x'], new_pos['y'])
        if self.time >= self.velocity + randint(-10, 10):
            if self.type == 1:
                self.direction = (randint(0, 2) - 1, randint(0, 2) - 1)
                self.state = (self.state + 1) % len(self.surface)
            elif self.type == 0:
                if self.direction != (0, 0):
                    self.state = (self.state + 1) % len(self.surface)
            self.time = 0

class   Player(Entity):
    """ Definition of Player class """
    type = 0
    speed = 5
    velocity = 500
    orientation = 'back'
    size = {'x': 50, 'y': 50}
    territory = [(0, 0), (1920, 1080)]
    surface = {'up': [(0, 0, 50, 50), (50, 0, 50, 50), (100, 0, 50, 50), (150, 0, 50, 50)],
        'back': [(0, 50, 50, 50), (50, 50, 50, 50), (100, 50, 50, 50), (150, 50, 50, 50)],
        'left': [(0, 100, 50, 50), (50, 100, 50, 50), (100, 100, 50, 50), (150, 100, 50, 50)],
        'right': [(0, 150, 50, 50), (50, 150, 50, 50), (100, 150, 50, 50), (150, 150, 50, 50)]}
    def __init__(self, position = (1300, 1000), image = Image['Player'], state = 0):
        """ Instanciate a player """
        direction = (0, 0)
        self.position = position
        Entity.__init__(self, self.position, image, state, self.surface, self.velocity,
                        self.territory, direction, self.type, self.size)

    def display(self, window):
        """ Overload  'Entity.update' to use the 'Player.orientation' """
        window.blit(self.image, self.position, self.surface[self.orientation][self.state])

    def update(self, object_list, elapsed_time):
        """ update the 'Player' object and assign it his sprite """
        Entity.update(self, object_list + [self], elapsed_time)
        if self.direction[1] != 0:
            self.orientation = ['back', 'back', 'up'][self.direction[1] + 1]
        if self.direction[0] != 0:
            self.orientation = ['left', 'back', 'right'][self.direction[0] + 1]

    def __repr__(self):
        return "[position: {}\tstate: {}\ttime: {}\tdirection: {}\torientation: {}]".format(
            self.position, self.state, self.time, self.direction, self.orientation)

# Default object class
class   People(Entity):
    """ A 'People' is an 'Entity' who move randomly and 'Player' can interact with """
    type = 1
    speed = 1
    velocity = 1000
    size = {'x': 50, 'y': 50}
    territory = [(10, 10), (700, 500)]
    surface = [(0, 0, 49, 49), (51, 0, 49, 49), (0, 51, 49, 49), (51, 51, 49, 49)]
    def __init__(self, position = (0, 0), image = Image['People'], state = 0):
        """ Inititalise 'People' object at a random 'position' / 'direction' """
        position = (randint(self.territory[0][0], self.territory[1][0]),
                    randint(self.territory[0][1], self.territory[1][1]))
        direction = (randint(0, 2) - 1, randint(0, 2) - 1)
        Entity.__init__(self, position, image, state, self.surface, self.velocity,
                        self.territory, direction, self.type, self.size)
        self.state = randint(0, len(self.surface) - 1)

    def __repr__(self):
        return "[position: {}\tstate: {}\ttime: {}\tdirection: {}]".format(
            self.position, self.state, self.time, self.direction)

# Default object class
class   Car(Entity):
    """ A 'Car' is an 'Entity' who spawn randomly from one point, move on the round about and leave """
    type = 2
    trim = 0
    speed = 10
    velocity = 200
    size = {'x': 250, 'y': 100}
    surface = [(0, 0, 1000, 1000)]
    territory = [(0, 0), (2500, 2500)]
    spawn_point = [(1300, 1080), (1920, 500)]
    def __init__(self, position = (0, 0), image = Image['Car'], state = 0, direction = (0, -1)):
        """ Initialise 'Car' object and spawn it at one of the two available 'spawn_point' """
        position = self.spawn_point[0]
        self.increment = 90
        Entity.__init__(self, position, image, state, self.surface, self.velocity,
                        self.territory, direction, self.type, self.size)
        self.image = pygame.transform.rotate(self.image, self.increment)
        self.trim = 0

    def circle(self, increment):
        """   """
        radius = 200
        self.angle = increment * (pi / (360 / 2));
        new_pos = {'x': int(1300 + (radius * cos(self.angle))),
                   'y': int(500 + (radius * sin(self.angle)))};
        rotation = [45, -45, -45, -45, -45, 45, 0, 0, 0]
        if increment % 45 == 0:
            tmp = self.image.get_rect().center
            self.image = pygame.transform.rotate(
                self.image, rotation[(int(increment / 45) - 2) % len(rotation)])
            self.image.get_rect().center = tmp
        self.position = (new_pos['x'], new_pos['y'])

    def update(self, object_list, elapsed_time):
        """  """
        Entity.update(self, object_list, elapsed_time)
        if self.trim == 0 and self.position[1] <= 700:
            self.direction = (0, -1)
            self.trim = 1
        if self.trim == 1:
            self.circle(self.increment)
            self.increment += 1
            if self.increment >= 360:
                self.direction = (1, 0)
                self.trim = 2
        if self.trim == 2 and self.position[0] >= 1920:
            del self

    def __repr__(self):
        return "[position: {}\tstate: {}\ttime: {}\tdirection: {}]".format(
            self.position, self.state, self.time, self.direction, self.angle)

class   Game():
    """ 'Game' is our motor, who perform each object move and display """
    mouse = (0, 0)
    object_list = []
    player = Player()
    resolution = (1920, 1080)
    def __init__(self, state = False):
        """ Create the game by initialising pygame with a 'window' and 'clock' """
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Kilian tape l'incruste")
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(self.resolution)
        self.state = state

    def checkAction(self):
        """ Perform an 'update' on each object """
        self.mouse = pygame.mouse.get_pos()
        milliseconds = self.clock.get_time()
        if randint(0, 100) == 5:
            print("Car() created !")
            self.object_list.append(Car())
        [obj.update(self.object_list + [self.player], milliseconds)
         for obj in self.object_list + [self.player]]
        self.player.update(self.object_list, milliseconds)
        return

    def display(self):
        """ display each object on the screen """
        self.window.blit(Image['Background'], (0, 0))
        [obj.display(self.window) for obj in self.object_list]
        self.player.display(self.window)
        pygame.display.update()
        return

    def handleEvent(self, event):
        """ Get the list of all events occured, and update 'player''s direction """
        if event.type == pygame.QUIT:
            self.state = True
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            keys = pygame.key.get_pressed()
            self.player.direction = (-keys[pygame.K_LEFT] + keys[pygame.K_RIGHT],
                                     -keys[pygame.K_UP] + keys[pygame.K_DOWN])

    def gameHandler(self):
        """ Handle the game """
        while not self.state:
            for event in pygame.event.get():
                self.handleEvent(event)
            self.clock.tick(60)
            self.checkAction()
            self.display()
        return

    def startMenu(self, menu_number):
        """ Start a menu (ON HOLD) """
        if menu_number == 1:
            [self.object_list.append(People()) for i in range(0, 6)]
        return

# Do not put more information in this function, it's must be clearer as possible
def     main():
    game = Game()
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
