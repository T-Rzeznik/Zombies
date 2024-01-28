import pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HIEGHT = 600


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIEGHT))


player = pygame.Rect((300,250,50,50)) #(x,y(positions), height,width (of box))



run = True
while run :
    screen.fill((0,0,0)) #starts the loop with a black screen so after each update, the screen returns black

    
    pygame.draw.rect(screen, (255,0,0), player) #draws the player onscreen

    key = pygame.key.get_pressed()
      #move in position
    if key[pygame.K_a] == True: #a key is pressed
        player.move_ip(-1,0)
    elif key[pygame.K_d] == True: #d key is pressed
        player.move_ip(1,0)
    elif key[pygame.K_w] == True: #w key is pressed
        player.move_ip(0,-1)
    elif key[pygame.K_s] == True: #s key is pressed
        player.move_ip(0,1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #if you click the x on the top right, game is quit
            run = False

    pygame.display.update()         
pygame.quit()