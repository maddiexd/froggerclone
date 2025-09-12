import pygame
class Character(pygame.sprite.Sprite):
    def __init__(self, location = (388, 548), image = './frog.png'):
        pygame.sprite.Sprite.__init__(self)
        self.__location = location
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (24, 24))
        self.rect = pygame.Rect(self.__location, (24, 24))
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
    def __init__(self, location = (0, 100), speed = (5, 0)):
        Character.__init__(self, location, image = './car.png')
        self.__speed = speed
        direction = lambda: "r" if self.__speed[0] > 0 else "l"
        self.flip(direction())
        self.__location = location

    def move(self):
        self.rect.move_ip(self.__speed)
        if self.rect[0] > 682:
            self.rect = pygame.Rect((118, self.__location[1]), (24, 24))
        elif self.rect[0] < 118:
            self.rect = pygame.Rect((682, self.__location[1]), (24, 24))

    def checkCollision(self, frog:Character):
         return pygame.sprite.collide_rect(self, frog)



frog = Character()
vehicles = pygame.sprite.Group()
vehicles.add(Vehicle([300, 500], (-6, 0)), Vehicle([150, 476], (7, 0)), Vehicle([500, 452], (-5, 0)), Vehicle([400, 428], (8, 0)), Vehicle([200, 404], (-6, 0)))