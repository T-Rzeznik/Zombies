import pygame
import sys
import math
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
fps = 60

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class PlayerBullet:
    def __init__(self, x, y, mouse_x, mouse_y, angle_offset=0):
        self.x = x
        self.y = y
        self.speed = 15
        self.angle = math.atan2(mouse_y - y, mouse_x - x) + angle_offset  # gets angle from player to mouse
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

    def main(self, display):
        self.x += self.x_vel
        self.y += self.y_vel
        pygame.draw.circle(display, (0, 0, 0), (int(self.x), int(self.y)), 5)


class Zombie:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2

    def move_towards_player(self, player):
        angle = math.atan2(player.y - self.y, player.x - self.x)
        self.x += math.cos(angle) * self.speed
        self.y += math.sin(angle) * self.speed

    def main(self, display):
        pygame.draw.rect(display, (0, 255, 0), (int(self.x), int(self.y), 32, 32))


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_count = 0
        self.moving_right = False
        self.moving_left = False
        self.health = 100
        self.gun = 'pistol'  # current gun
        self.last_shot = 0
        self.shot_delay = 500  # milliseconds between shots for semi-auto guns

    def main(self, display):
        if self.animation_count + 1 >= 16:  # 4 frames x 4 animations = 16
            self.animation_count = 0
        self.animation_count += 1

        pygame.draw.rect(display, (255, 0, 0), (self.x, self.y, self.width, self.height))
        self.moving_right = False
        self.moving_left = False

    def draw_health_bar(self, display):
        pygame.draw.rect(display, (255, 0, 0), (10, 10, 100, 10))  # Background health bar
        pygame.draw.rect(display, (0, 255, 0), (10, 10, self.health, 10))  # Current health

    def shoot(self, mouse_x, mouse_y):
        current_time = pygame.time.get_ticks()
        if self.gun == 'pistol':
            if current_time - self.last_shot > self.shot_delay:
                player_bullets.append(PlayerBullet(self.x + self.width // 2, self.y + self.height // 2, mouse_x, mouse_y))
                self.last_shot = current_time
        elif self.gun == 'shotgun':
            if current_time - self.last_shot > self.shot_delay * 2:
                for angle_offset in [-0.2, 0, 0.2]:  # spread of bullets
                    player_bullets.append(PlayerBullet(self.x + self.width // 2, self.y + self.height // 2, mouse_x, mouse_y, angle_offset))
                self.last_shot = current_time


player = Player(400, 300, 32, 32)
player_bullets = []
zombies = []
wave = 1

def spawn_zombies(wave):
    for _ in range(wave * 5):  # Increase number of zombies with each wave
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        zombies.append(Zombie(x, y))

def show_upgrade_menu():
    display.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 55)
    text = font.render('Choose Your Upgrade', True, (255, 255, 255))
    display.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 100))

    pistol_button = pygame.Rect(SCREEN_WIDTH//2 - 150, 200, 300, 50)
    shotgun_button = pygame.Rect(SCREEN_WIDTH//2 - 150, 300, 300, 50)

    pygame.draw.rect(display, (0, 0, 255), pistol_button)
    pygame.draw.rect(display, (0, 0, 255), shotgun_button)

    pistol_text = font.render('Pistol', True, (255, 255, 255))
    shotgun_text = font.render('Shotgun', True, (255, 255, 255))

    display.blit(pistol_text, (pistol_button.x + 100, pistol_button.y + 10))
    display.blit(shotgun_text, (shotgun_button.x + 80, shotgun_button.y + 10))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pistol_button.collidepoint(event.pos):
                    player.gun = 'pistol'
                    return
                elif shotgun_button.collidepoint(event.pos):
                    player.gun = 'shotgun'
                    return


spawn_zombies(wave)

while True:
    display.fill((24, 164, 86))  # starts the loop with a black screen so after each update, the screen returns black

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # if you click the x on the top right, game is quit
            sys.exit()
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:  # on event click "fire" a bullet
            if event.button == 1:
                player.shoot(mouse_x, mouse_y)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player.x -= 3
        player.moving_left = True
    if keys[pygame.K_d]:
        player.x += 3
        player.moving_right = True
    if keys[pygame.K_w]:
        player.y -= 3
    if keys[pygame.K_s]:
        player.y += 3

    player.main(display)
    player.draw_health_bar(display)  # Draw the health bar

    for bullet in player_bullets:  # drawing the bullets every frame
        bullet.main(display)

    for zombie in zombies:
        zombie.move_towards_player(player)
        zombie.main(display)
        # Check for collision with player
        if zombie.x < player.x + player.width and zombie.x + 32 > player.x and zombie.y < player.y + player.height and zombie.y + 32 > player.y:
            player.health -= 1
            if player.health <= 0:
                print("Game Over")
                pygame.quit()
                sys.exit()

    # Collision detection
    for bullet in player_bullets[:]:
        for zombie in zombies[:]:
            if zombie.x < bullet.x < zombie.x + 32 and zombie.y < bullet.y < zombie.y + 32:
                try:
                    player_bullets.remove(bullet)
                    zombies.remove(zombie)
                except ValueError:
                    pass

    # Check if all zombies are dead to spawn a new wave
    if not zombies:
        wave += 1
        if wave % 3 == 0:
            show_upgrade_menu()
        spawn_zombies(wave)

    clock.tick(fps)
    pygame.display.update()
