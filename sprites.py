import pygame
class Character(pygame.sprite.Sprite):
    def __init__(self, location = (388, 548), image = './frog.png', size = (24, 24)):
        pygame.sprite.Sprite.__init__(self)
        self.__location = location
        self.__size = size
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = pygame.Rect(self.__location, size)
        self.__moveCounter = [0, 0]
        self.__currentDir = "u"
        
    def getSurface(self):
        return self.image

    def getRect(self):
        return self.rect

    def setRect(self, rect):
        self.rect = rect
    
    def setMoveCounter(self, count):
        self.__moveCounter = count
    
    def getMoveCounter(self):
        return self.__moveCounter
    
    def flip(self, dir):
        angle = {
            "l": 90,
            "r": -90,
            "u": 0,
            "d": 180
        }
        self.image = pygame.transform.rotate(self.image, angle[dir] - angle[self.__currentDir])
        self.__currentDir = dir
        

class Vehicle(Character):
    def __init__(self, location = (0, 100), image = './car.png', speed = (5, 0), size = (24, 24)):
        Character.__init__(self, location, image, size)
        self.__speed = speed
        direction = lambda: "r" if self.__speed[0] > 0 else "l"
        self.flip(direction())
        self.__location = location
        self.__size = size

    def move(self):
        self.rect.move_ip(self.__speed)
        if self.rect[0] > 682:
            self.rect = pygame.Rect((118, self.__location[1]), self.__size)
        elif self.rect[0] < 118:
            self.rect = pygame.Rect((682, self.__location[1]), self.__size)

    def checkCollision(self, frog:Character):
         return pygame.sprite.collide_rect(self, frog)

class Log(Vehicle):
    def __init__(self, location=(0, 356), image = 'log.png', speed=(5, 0), size = (24, 24)):
        super().__init__(location, image, speed, size)
        self.__size = size
        self.__speed = speed

    def checkCollision(self, frog:Character):
        if pygame.sprite.collide_rect_ratio(0.1).__call__(self, frog):
            frog.rect.move_ip(self.__speed)


frog = Character()
vehicles = pygame.sprite.Group()
vehicles.add(
            Vehicle(location = [150, 500], speed = (-4, 0)),
            Vehicle(location = [250, 500], speed = (-4, 0)),
            Vehicle(location = [550, 500], speed = (-4, 0)),
            Vehicle(location = [350, 476], speed = (7, 0)),
            Vehicle(location = [150, 476], speed = (7, 0)),
            Vehicle(location = [350, 452], speed = (-5, 0)),
            Vehicle(location = [400, 428], speed = (8, 0)),
            Vehicle(location = [150, 404], speed = (-7, 0)),
            Vehicle(location = [200, 404], speed = (-7, 0)))
logs = pygame.sprite.Group()
logs.add(
    Log(location=(150, 356)),
    Log(location=(174, 356)),
    Log(location=(198, 356)),
    Log(location=(214, 356)),
    Log(location=(238, 356)),

    Log(location=(150, 332), speed = (-5, 0)),
    Log(location=(174, 332), speed = (-5, 0)),
    Log(location=(198, 332), speed = (-5, 0)),
    Log(location=(214, 332), speed = (-5, 0)),
    Log(location=(238, 332), speed = (-5, 0)),
)