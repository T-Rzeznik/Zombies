import pygame
import sys
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HIEGHT = 600
fps = 60

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIEGHT))
clock = pygame.time.Clock() 



class PlayerBullet:
    def __init__(self,x,y,mouse_x,mouse_y):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 15
        self.angle = math.atan2(y-mouse_y, x-mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

    def main(self, display):
        self.x -= int(self.x_vel)
        self.y-= int(self.y_vel)


        pygame.draw.circle(display, (0,0,0) , (self.x, self.y), 5)

class Player:
    def __init__(self, x, y , width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def main(self, display):
        pygame.draw.rect(display,(255,0,0), (self.x, self.y, self.width, self.height))


player = Player(400, 300, 32, 32)

display_scroll = [0,0]

player_bullets = []


while True :
    display.fill((24,164,86)) #starts the loop with a black screen so after each update, the screen returns black

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #if you click the x on the top right, game is quit
            sys.exit()
            pygame.QUIT


        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player_bullets.append(PlayerBullet(player.x, player.y, mouse_x, mouse_y ))

    keys = pygame.key.get_pressed()

    pygame.draw.rect(display, (255,255,255), (100 - display_scroll[0],100-display_scroll[1],16,16))

    if keys[pygame.K_a]:
        display_scroll[0] -= 3
        for bullet in player_bullets:
            bullet.x += 3
    if keys[pygame.K_d]:
        display_scroll[0] += 3
        for bullet in player_bullets:
            bullet.x -= 3
    if keys[pygame.K_w]:
        display_scroll[1] -= 3
        for bullet in player_bullets:
            bullet.y += 3
    if keys[pygame.K_s]:
        display_scroll[1] += 3
        for bullet in player_bullets:
            bullet.y -= 3 


    player.main(display)

    for bullet in player_bullets:
        bullet.main(display)


    clock.tick(fps)
    pygame.display.update()         
