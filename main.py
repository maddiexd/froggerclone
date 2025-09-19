import pygame, sprites, logic

pygame.init()
size = logic.getWidthHight()
screen = pygame.display.set_mode(size, flags=pygame.SCALED | pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    logic.eventLoopLogic()
    screen.fill("#606060")
    pygame.draw.rect(screen, "#2F8A2A", pygame.Rect(0, 450, 448, 32))
    pygame.draw.rect(screen, "#2F8A2A", pygame.Rect(0, 256, 448, 32))
    pygame.draw.rect(screen, "#44D0BB", pygame.Rect(0, 48, 448, 208))
    pygame.draw.rect(screen, "#4D9629", pygame.Rect(0, 36, 448, 15))


    for log in sprites.logs:
        log.draw(screen)
    for turtle in sprites.turtles:
        turtle.draw(screen)
    sprites.hedges.draw(screen)
    screen.blit(sprites.frog.getSurface(), sprites.frog.getRect())
    sprites.vehicles.draw(screen)
    
    # pygame.draw.rect(screen, '#000000', pygame.Rect(0, 0, 150, 600))
    # pygame.draw.rect(screen, '#000000', pygame.Rect(650, 0, 150, 600))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()