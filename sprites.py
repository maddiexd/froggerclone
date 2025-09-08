import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self, location = (0,0), image = './frog.png'):
        self.__location = location
        pygame.sprite.Sprite.__init__(self)
        self.__image = pygame.image.load(image)
        self.__rect = self.__image.get_rect()
        
    def getSurface(self):
        return self.__image

    def getRect(self):
        return self.__rect

    def setRect(self, rect):
        self.__rect = rect

def main():
    global frog
    frog = Character()

main()