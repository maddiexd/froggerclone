import pygame, random
class Character(pygame.sprite.Sprite):
    def __init__(self, location = (224, 454), image = './frog.png', size = (24, 24)):
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
        self.__location = (224, 454)
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
        if self.rect[0] > 512:
            self.rect = pygame.Rect((-32, self.__location[1]), self.__size)
        elif self.rect[0] < -32:
            self.rect = pygame.Rect((512, self.__location[1]), self.__size)

    def checkCollision(self, frog:Character):
         return pygame.sprite.collide_rect(self, frog)

class Log(Vehicle):
    def __init__(self, location=(0, 356), image = 'log.png', speed=(5, 0), size = (32, 32)):
        super().__init__(location, image, speed, size)
        self.__size = size
        self.__speed = speed

    def checkCollision(self, frog:Character):
        hit = pygame.sprite.collide_rect_ratio(0.65).__call__(self, frog)
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
logLaneCoord = {
    1: 96,
    2: 128,
    3: 160,
    4: 192,
    5: 224
}
for laneNo in range(1, 6):
    logAmount = random.randint(5, 8)

    speed = max(0.4, (random.random() * 2.5) + 0.8) * random.choice([1, -1])
    sparseness = random.randint(0, 2)
    logSize = max(1, (32 // logAmount) - sparseness)
    lastX = random.randint(0, 4) * 32
    for log in range(logAmount):
        for piece in range(logSize):
            logs.add(Log(((lastX+(32 * piece)), logLaneCoord[laneNo]), speed=(speed, 0)))
        lastX += logSize * 32 + sparseness*32 + 32