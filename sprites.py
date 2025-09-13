import pygame
class Character(pygame.sprite.Sprite):
    def __init__(self, location = (212, 454), image = './frog.png', size = (24, 24)):
        pygame.sprite.Sprite.__init__(self)
        self.__location = location
        self.__size = size
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = pygame.Rect(self.__location, size)
        self.__moveCounter = [0, 0]
        self.__currentDir = "u"
        self.onlog = False
        
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

    def die(self):
        self.__location = (208, 454)
        self.rect = pygame.Rect(self.__location, self.__size)
        self.__moveCounter = [0, 0]
        self.flip("u")
        self.onlog = False
        

class Vehicle(Character):
    def __init__(self, location = (0, 96), image = './car.png', speed = (5, 0), size = (24, 24)):
        Character.__init__(self, location, image, size)
        self.__speed = speed
        direction = lambda: "r" if self.__speed[0] > 0 else "l"
        self.flip(direction())
        self.__location = location
        self.__size = size

    def move(self):
        self.rect.move_ip(self.__speed)
        if self.rect[0] > 544:
            self.rect = pygame.Rect((-32, self.__location[1]), self.__size)
        elif self.rect[0] < -32:
            self.rect = pygame.Rect((544, self.__location[1]), self.__size)

    def checkCollision(self, frog:Character):
         return pygame.sprite.collide_rect(self, frog)

class Log(Vehicle):
    def __init__(self, location=(0, 356), image = 'log.png', speed=(5, 0), size = (32, 32)):
        super().__init__(location, image, speed, size)
        self.__size = size
        self.__speed = speed

    def checkCollision(self, frog:Character):
        hit = pygame.sprite.collide_rect_ratio(0.5).__call__(self, frog)
        return hit
    def getSpeed(self):
        return self.__speed


frog = Character()
vehicles = pygame.sprite.Group()
vehicles.add(
            Vehicle(location = [150, 388], speed = (-3, 0)),
            Vehicle(location = [250, 388], speed = (-3, 0)),
            Vehicle(location = [550, 388], speed = (-3, 0)),
            Vehicle(location = [350, 356], speed = (5, 0)),
            Vehicle(location = [150, 356], speed = (5, 0)),
            Vehicle(location = [350, 324], speed = (-2, 0)),
            Vehicle(location = [400, 324], speed = (-2, 0)),
            Vehicle(location = [150, 292], speed = (-7, 0)),
            Vehicle(location = [200, 292], speed = (-7, 0)),
            Vehicle(location = [150, 420], speed = (2, 0)),
            Vehicle(location = [200, 420], speed = (2, 0)),
            Vehicle(location = [250, 420], speed = (2, 0)))
logs = pygame.sprite.Group()
logs.add(
    Log(location=(150, 224), speed = (4, 0)),
    Log(location=(182, 224), speed = (4, 0)),
    Log(location=(214, 224), speed = (4, 0)),
    Log(location=(246, 224), speed = (4, 0)),
    Log(location=(278, 224), speed = (4, 0)),

    Log(location=(150, 192), speed = (-4, 0)),
    Log(location=(182, 192), speed = (-4, 0)),
    Log(location=(214, 192), speed = (-4, 0)),
    Log(location=(246, 192), speed = (-4, 0)),
    Log(location=(278, 192), speed = (-4, 0)),

    Log(location=(150, 160), speed = (4, 0)),
    Log(location=(182, 160), speed = (4, 0)),
    Log(location=(214, 160), speed = (4, 0)),
    Log(location=(246, 160), speed = (4, 0)),
    Log(location=(278, 160), speed = (4, 0)),

    Log(location=(150, 128), speed = (-4, 0)),
    Log(location=(182, 128), speed = (-4, 0)),
    Log(location=(214, 128), speed = (-4, 0)),
    Log(location=(246, 128), speed = (-4, 0)),
    Log(location=(278, 128), speed = (-4, 0)),

    Log(location=(150, 96), speed = (4, 0)),
    Log(location=(182, 96), speed = (4, 0)),
    Log(location=(214, 96), speed = (4, 0)),
    Log(location=(246, 96), speed = (4, 0)),
    Log(location=(278, 96), speed = (4, 0)))