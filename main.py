import pygame, sprites, logic

pygame.init()
size = logic.getWidthHight()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
running = True



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    logic.eventLoopLogic()
    screen.fill("#313131")
    screen.blit(sprites.frog.getSurface(), sprites.frog.getRect())
    pygame.display.flip()
    clock.tick(60)
pygame.quit()