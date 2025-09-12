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
    screen.fill("#606060")
    pygame.draw.rect(screen, "#2F8A2A", pygame.Rect(150, 380, 550, 24))
    pygame.draw.rect(screen, "#2F8A2A", pygame.Rect(150, 524, 550, 88))
    pygame.draw.rect(screen, "#52BBFF", pygame.Rect(150, 260, 550, 120))
    sprites.logs.draw(screen)
    screen.blit(sprites.frog.getSurface(), sprites.frog.getRect())
    sprites.vehicles.draw(screen)
    
    pygame.draw.rect(screen, '#000000', pygame.Rect(0, 0, 150, 600))
    pygame.draw.rect(screen, '#000000', pygame.Rect(650, 0, 150, 600))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()