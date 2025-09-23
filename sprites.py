import pygame, random


'''
This class is the base class for the cars, logs, turtles and the main class for the original frog player character.
It uses a frame-by frame countdown system, in order to ensure the movement is smooth.
'''
class Character(pygame.sprite.Sprite):
    def __init__(self, location = (224, 454), image = './frog.png', size = (24, 24)):
        pygame.sprite.Sprite.__init__(self) # initialise all reqired variables
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
    
    def checkBounds(self):
        if self.rect[0] < 0:
            self.rect[0] = 0
        if self.rect[0] > 416:
            self.rect[0] = 416
        if self.rect[1] > 480:
            self.rect[1] = 480
        if self.rect[1] < 0:
            self.rect[1] = 0

    def checkRiverBounds(self):
        if self.rect[0] < 0:
            self.die()
        if self.rect[0] > 480:
            self.die()
    
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
        
'''
This is the basic vehicle class for the cars on the road. It adds wraparound and collision checking.
'''
class Vehicle(Character):
    def __init__(self, location = (0, 96), image = './car.png', speed = (5, 0), size = (24, 24)):
        Character.__init__(self, location, image, size)
        self.__speed = speed
        self.__direction = lambda: "r" if self.__speed[0] > 0 else "l"
        self.flip(self.__direction())
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

'''
This is a log piece class, this is a 32x32 segment of log, with smaller hit boundaries for when the frog land on it.
'''
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


'''
This is the class for the overall log, with the ability to wrap around as a whole log instead of piece by piece
ensuring the logs stay stuck together and are of even length and gap between them.
'''
class Log(pygame.sprite.Group):
    def __init__(self, size, gap, lane, startpos, speed, logAmount):
        super().__init__()
        self.__size = size
        self.__lane = lane
        self.__startpos = startpos
        self.__speed = speed
        self.__gap = gap
        self.__logAmount = logAmount
        for piece in range(self.__size): # adds all the log pieces to the sprite group.
            super().add(LogItem([self.__startpos + (32 * piece + 1), logLaneCoord[self.__lane]], speed = speed))
        self.__loop = self.checkLoop()
        
    def move(self): # movement with extra logic for wraparound
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

    def checkLoop(self): # checks for wrapping around at the end, dynamically adjusting the runway depending on log and gap size
        loop = False
        if super().sprites()[0].rect[0] > self.calculateRunway():
            loop = True
        elif super().sprites()[self.__size - 1].rect[0] < (-32 * self.__size)+ (-1* self.__gap) + (32 *(self.__size -1)):
            loop = True
            # print("loop",self.__lane)
        return loop
    
    def checkCollision(self, frog): # pass through collision
        hitSprite = None
        hit = False
        for i, sprite in enumerate(super().sprites()):
            if sprite.checkCollision(frog):
                hit = True
                hitSprite = sprite
        return hit, hitSprite

    def draw(self, surface, bgd = None, special_flags = 0): # pass through drawing.
        return super().draw(surface, bgd, special_flags)
    
    def calculateRunway(self): # calculate length of lane depending on log and gap size
        runway = (self.__logAmount) * ((self.__size *32)+ self.__gap) // 2
        return runway

        
'''
Adjustting the logItem to add the ducking and changing the image
'''
class Turtle(LogItem):
    def __init__(self, location=[0, 356], image='turtleStage1.png', 
                 speed=(5, 0), 
                 size=(32, 32), 
                 canDuck = False
                 ):
        super().__init__(location, image, speed, size)
        self.__canDuck = canDuck
        self.__ducking = False
        self.__duckCount = 0
        self.__duckIter = -1
        self.__speed = speed
        # self.image = image
        self.__direction = lambda: "r" if self.__speed[0] > 0 else "l"
        
        self.__currentDir = self.__direction()

    def checkDuck(self): # creating timers and changing stage based on a 250 frame loop
        if self.__canDuck:
            if self.__duckCount < 50:
                self.__duckCount += self.__duckIter
                self.__ducking = True
                # print(self.__duckCount)
                self.image = pygame.image.load("turtleStage4.png")
                self.image = pygame.transform.scale(self.image, super().getRect()[2:4])
                self.flip(self.__currentDir)
            elif self.__duckCount < 110:
                self.__ducking = False
                self.__duckCount += self.__duckIter
                self.image = pygame.image.load("turtleStage3.png")
                self.image = pygame.transform.scale(self.image, super().getRect()[2:4])
                self.flip(self.__currentDir)
            elif self.__duckCount < 170:
                self.__ducking = False
                self.__duckCount += self.__duckIter
                self.image = pygame.image.load("turtleStage2.png")
                self.image = pygame.transform.scale(self.image, super().getRect()[2:4])
                self.flip(self.__currentDir)
            else:
                self.__ducking = False
                self.__duckCount += self.__duckIter
                # print("not ducking")
                self.image = pygame.image.load("turtleStage1.png")
                self.image = pygame.transform.scale(self.image, super().getRect()[2:4])
                self.flip(self.__currentDir)

            if self.__duckCount < 0:
                self.__duckIter = 1
            if self.__duckCount > 250:
                self.__duckIter = -1

    def getDucking(self):
        return self.__ducking
    
    def flip(self, dir):
        angle = {
            "l": 90,
            "r": -90,
            "u": 0,
            "d": 180
        }
        self.image = pygame.transform.rotate(self.image, angle[dir])


'''
Change some things for the turtles based on the log object to allow them to be all treated as one.
'''
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

'''
Adds the finishing hedges, which also gets reused for the happy frogs at the end, very simple sprite type.
'''
class Hedge(pygame.sprite.Sprite):
    def __init__(self, slot, image = 'hedge.png'):
        super().__init__()
        self.__location = (-30 + slot*46, 48)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = pygame.Rect(self.__location, (48, 48))

    def checkCollision(self, frog):
         return pygame.sprite.collide_rect(self, frog), self


# initialise variables to be used by other files.
frog = Character()
vehicles = pygame.sprite.Group()

logs = []
turtles = []
# dictionary to convert lanes to coordinates for the logs
logLaneCoord = {
    1: 96,
    2: 128,
    3: 160,
    4: 192,
    5: 224
}
# level data, s is size, l is length, g is the gap between
logConfig = {
    0: {
        1: {
            "s": 1.5,
            "l": 4,
            "g": 2
        },
        3: {
            "s": 2.5,
            "l": 5,
            "g": 3
        },
        4: {
            "s": 1,
            "l": 3,
            "g": 3
        }
    }
}


turtleConfig = {
    0: {
        2: {
            "s": -2.5,
            "l": 2,
            "g": 2
        },
        5: {
            "s": -2.5,
            "l": 3,
            "g": 1
        }
    }
}
# cars have more smarter entry naming, count is the amount of cars, offset is the initial offset the cars start from. Speed and gap are self-explanatory.
carConfig = {
    0: {
        1: {
            "speed": -2,
            "count": 2,
            "gap": 3,
            "offset": 8
        },
        2: {
            "speed": 1.5,
            "count": 1,
            "gap": 1,
            "offset": 15
        },
        3: {
            "speed": -1,
            "count": 3,
            "gap": 3,
            "offset": 5
        },
        4: {
            "speed": 1,
            "count": 3,
            "gap": 3,
            "offset": 5
        },
        5: {
            "speed": -1,
            "count": 3,
            "gap": 3,
            "offset": 4
        }

    }
}


# add cars based on data
for carLane in range(1, 6):
    config = carConfig[0][carLane]
    for car in range(config["count"]):
        vehicles.add(Vehicle((config["gap"]*car*32 + 32*config["offset"], 260+32*carLane), speed = (config["speed"], 0)))


logLanes = [1, 3, 4] # sets the lanes where the logs are
level = 0 # level counter but there are no levels, but there could be in the future (never).
for laneNo in range(3):
    speed = (logConfig[0][logLanes[laneNo]])["s"]
    gapSize = (logConfig[0][logLanes[laneNo]])["g"]
    logSize = (logConfig[0][logLanes[laneNo]])["l"]
    logAmount = ((14 // (logSize+gapSize))+1)*2
    lastX = 0
    for log in range((logAmount//2) + 1):
        logs.append(Log(logSize, 32 * (gapSize), logLanes[laneNo], lastX, [speed, 0], logAmount))
        lastX = lastX + ((logSize) * 32) + (gapSize)*32


turtleLanes = [2, 5] # sets the lanes for the turtles


for laneNo in range(2): # applies the turtles according to the saves
    speed = (turtleConfig[0][turtleLanes[laneNo]])["s"]
    gapSize = (turtleConfig[0][turtleLanes[laneNo]])["g"]
    turtleGroupSize = (turtleConfig[0][turtleLanes[laneNo]])["l"]
    turtleGroupAmount = ((14 // (turtleGroupSize+gapSize))+1)*2
    lastX = 0
    ducking = [random.randint(1, turtleGroupAmount), 
               random.randint(1, turtleGroupAmount), 
               random.randint(1, turtleGroupAmount)
               ]
    
    for turtlegroup in range((turtleGroupAmount //2)+1):
        canDuck = (lambda: True if turtlegroup in ducking else False)
        turtles.append(turtleGroup(turtleGroupSize, 32 * (gapSize), 
                                   turtleLanes[laneNo], lastX, [speed, 0], 
                                   turtleGroupAmount, canDuck()
                                   )
                        )
        lastX = lastX + ((turtleGroupSize) * 32) + (gapSize)*32

# add the hedges to the correct position
hedges = pygame.sprite.Group()

for hedgeNo in range(0, 12, 2):
    hedges.add(Hedge(hedgeNo))