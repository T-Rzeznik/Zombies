import pygame
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HIEGHT = 600
fps = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIEGHT))

# IMG = pygame.image.load('os.path.join('Assets','filename.png')')   importing img
# IMG = pygame.transform.scale(filename.png, (width, height))        scaling img

player = pygame.Rect((300,250,50,50)) #(x,y(positions), height,width (of box))
clock = pygame.time.Clock() 

run = True
while run :
    screen.fill((0,0,0)) #starts the loop with a black screen so after each update, the screen returns black
    clock.tick(fps)
    
    #screen.blit('filename.png', (x,y) ) // draw png
    
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