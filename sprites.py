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
        if self.rect[0] > 480:
            self.rect = pygame.Rect((-32, self.__location[1]), self.__size)
        elif self.rect[0] < -32:
            self.rect = pygame.Rect((480, self.__location[1]), self.__size)

    def checkCollision(self, frog:Character):
         return pygame.sprite.collide_rect(self, frog)

class LogItem(Vehicle):
    def __init__(self, location=[0, 356], image = 'log.png', speed=(5, 0), size = (32, 32)):
        super().__init__(location, image, speed, size)
        self.__size = size
        self.__speed = speed

    def checkCollision(self, frog:Character):
        hit = pygame.sprite.collide_rect_ratio(0.65).__call__(self, frog)
        return hit
    def getSpeed(self):
        return self.__speed
    
    def move(self):
        self.rect.move_ip(self.__speed)


class Log(pygame.sprite.Group):
    def __init__(self, size, gap, lane, startpos, speed, logAmount):
        super().__init__()
        self.__size = size
        self.__lane = lane
        self.__startpos = startpos
        self.__speed = speed
        self.__gap = gap
        self.__logAmount = logAmount
        for piece in range(self.__size):
            super().add(LogItem([self.__startpos + (32 * piece + 1), logLaneCoord[self.__lane]], speed = speed))
        self.__loop = self.checkLoop()
        
    def move(self):
        # print(self.__logAmount)
        self.__loop = self.checkLoop()
        # print(self.calculateRunway())
        for i, sprite in enumerate(super().sprites()):
            if self.__loop:
                if self.__speed[0] > 0:
                    sprite.rect = pygame.Rect(( 32 *(-1 * self.__size)+ (-1*self.__gap) + (32 *(i)), sprite.getRect()[1])
                                              , sprite.getRect()[2:4])
                else:
                    sprite.rect = pygame.Rect((self.calculateRunway()+(32*i), sprite.getRect()[1]), sprite.getRect()[2:4])
            sprite.move()
            # print(super().sprites()[0].getRect())

    def checkLoop(self):
        loop = False
        if super().sprites()[0].rect[0] > self.calculateRunway():
            loop = True
        elif super().sprites()[self.__size - 1].rect[0] < (-32 * self.__size)+ (-1* self.__gap) + (32 *(self.__size -1)):
            loop = True
            # print("loop",self.__lane)
        return loop
    
    def checkCollision(self, frog):
        hitSprite = None
        hit = False
        for i, sprite in enumerate(super().sprites()):
            if sprite.checkCollision(frog):
                hit = True
                hitSprite = sprite
        return hit, hitSprite

    def draw(self, surface, bgd = None, special_flags = 0):
        return super().draw(surface, bgd, special_flags)
    
    def calculateRunway(self):
        runway = (self.__logAmount) * ((self.__size *32)+ self.__gap) // 2
        return runway

        

class Turtle(LogItem):
    def __init__(self, location=[0, 356], image='turtle.png', speed=(5, 0), size=(32, 32), canDuck = False):
        super().__init__(location, image, speed, size)
        self.__canDuck = canDuck
        self.__ducking = False
        self.__duckCount = 0

    def checkDuck(self):
        if self.__canDuck:
            if self.__duckCount < 150:
                self.__duckCount = self.__duckCount  - 1
                self.__ducking = True
                # print(self.__duckCount)
                self.image = pygame.image.load("duckingTurtle.png")
                self.image = pygame.transform.scale(self.image, super().getRect()[2:4])
            else:
                self.__ducking = False
                self.__duckCount = self.__duckCount  - 1
                # print("not ducking")
                self.image = pygame.image.load("turtle.png")
                self.image = pygame.transform.scale(self.image, super().getRect()[2:4])

            if self.__duckCount < 0:
                self.__duckCount = 400

    def getDucking(self):
        return self.__ducking
    

class turtleGroup(Log):
    def __init__(self, size, gap, lane, startpos, speed, logAmount, ducking = False):
        super().__init__(size, gap, lane, startpos, speed, logAmount)
        super().empty()
        self.__size = size
        self.__lane = lane
        self.__startpos = startpos
        self.__speed = speed
        self.__gap = gap
        self.__logAmount = logAmount
        self.__ducking = ducking
        for piece in range(size):
            super().add(Turtle([startpos + (32 * piece + 1), logLaneCoord[lane]], speed = speed, canDuck = ducking))
        self.__loop = self.checkLoop()
        self.__ducked = False

    def checkDuck(self):
        for turtle in super().sprites():
            turtle.checkDuck()


    def move(self):
        self.__loop = self.checkLoop()
        for i, sprite in enumerate(super().sprites()):
            if self.__loop:
                if self.__speed[0] > 0:
                    sprite.rect = pygame.Rect(( 32 *(-1 * self.__size)+ (-1*self.__gap) + (32 *(i)), sprite.getRect()[1])
                                              , sprite.getRect()[2:4])
                else:
                    sprite.rect = pygame.Rect((self.calculateRunway()+(32*i), sprite.getRect()[1]), sprite.getRect()[2:4])
            sprite.move()
            self.checkDuck()

    def checkCollision(self, frog):
        hitSprite = None
        hit = False
        for i, sprite in enumerate(super().sprites()):
            if sprite.checkCollision(frog) and not sprite.getDucking():
                hit = True
                hitSprite = sprite
        return hit, hitSprite





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
logs = []
turtles = []
logLaneCoord = {
    1: 96,
    2: 128,
    3: 160,
    4: 192,
    5: 224
}


logLanes = [1, 3, 4]
for laneNo in range(3):
    speed = random.randint(1, 4)* pow(-1, (laneNo % 2))
    gapSize = random.randint(2, 4)
    logSize = random.randint(2, 6)
    logAmount = ((14 // (logSize+gapSize))+1)*2
    lastX = 0
    for log in range(logAmount):
        logs.append(Log(logSize, 32 * (gapSize), logLanes[laneNo], lastX, [speed, 0], logAmount))
        lastX = lastX + ((logSize) * 32) + (gapSize)*32

turtleLanes = [2, 5]
for laneNo in range(2):
    speed = random.randint(1, 3)* pow(-1, (laneNo % 2))
    gapSize = random.randint(1, 2)
    turtleGroupSize = random.randint(2, 3)
    turtleGroupAmount = ((14 // (turtleGroupSize+gapSize))+1)*2
    lastX = 0
    ducking = [random.randint(1, turtleGroupAmount), random.randint(1, turtleGroupAmount), random.randint(1, turtleGroupAmount), random.randint(1, turtleGroupAmount)]
    
    for turtlegroup in range((turtleGroupAmount //2)+1):
        canDuck = (lambda: True if turtlegroup in ducking else False)
        turtles.append(turtleGroup(turtleGroupSize, 32 * (gapSize), turtleLanes[laneNo], lastX, [speed, 0], turtleGroupAmount, canDuck()))
        lastX = lastX + ((turtleGroupSize) * 32) + (gapSize)*32
# lastX = 0
# gapSize = 6
# logSize = 7
# logAmount = ((14 // (logSize+gapSize))+1)*2
# print(logAmount)
# for log in range(logAmount):
#     logs.append(Log(logSize, 32 * (gapSize), 5, lastX, [5, 0], logAmount))
#     lastX = lastX + ((logSize) * 32) + (gapSize)*32

# totalRunway = (logLength + gapLength) * logAmount