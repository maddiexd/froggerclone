import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self, location = (0,0), image = './frog.png'):
        self.__location = location
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.__moveCounter = [0, 0]
        
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

def main():
    global frog
    frog = Character()

main()