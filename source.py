import pygame
import sys
import math
import random
import os

pygame.init()

# Set the working directory to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
fps = 60

# Load the parking lot tile image
parking_lot_tile = pygame.image.load('image.png')

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class PlayerBullet:
    def __init__(self, x, y, mouse_x, mouse_y, angle_offset=0, damage=1, max_penetration=1):
        self.x = x
        self.y = y
        self.speed = 15
        self.angle = math.atan2(mouse_y - y, mouse_x - x) + angle_offset  # gets angle from player to mouse
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
        self.damage = damage
        self.penetration = 0
        self.max_penetration = max_penetration

    def main(self, display):
        self.x += self.x_vel
        self.y += self.y_vel
        # Draw a glow effect
        pygame.draw.circle(display, (255, 255, 0), (int(self.x), int(self.y)), 5)
        pygame.draw.circle(display, (0, 0, 0), (int(self.x), int(self.y)), 4)

class Zombie:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.health = 2  # Default health for zombies
        self.endurance = 5
        self.agility = 3

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
        #Attributes
        self.health = 100
        self.max_health = 100 
        self.agility = 10 # Speed
        self.endurance = 10 # health regen
        self.luck = 5
        self.unlocked_weapons = ['pistol']  # Start with pistol unlocked
        self.gun = 'pistol'  # current gun
        self.last_shot = 0
        self.shot_delay = 500  # milliseconds between shots for semi-auto guns
        self.damage = {
            'pistol': 1,
            'shotgun': 1,
            'rifle': 1,
            'submachine': 0.5,
            'sniper': 2,
            'admin': 9000
        }
        self.penetration = {
            'pistol': 1,
            'shotgun': 1,
            'rifle': 1,
            'submachine': 1,
            'sniper': 3,
            'admin': 10
        }

    def switch_gun(self, new_gun):
        self.gun = new_gun

    def display_current_gun(self, display):  # Added method
        font = pygame.font.SysFont(None, 30)
        text = font.render(f'Current Gun: {self.gun.capitalize()}', True, (255, 255, 255))
        display.blit(text, (SCREEN_WIDTH - text.get_width() - 10, 10))
        
    def unlock_weapon(self, weapon):
        if weapon not in self.unlocked_weapons:
            self.unlocked_weapons.append(weapon)
        
    def can_unlock_weapon(self, wave):
        unlocked_weapon = None
        if wave >= 3 and 'shotgun' not in self.unlocked_weapons:
            self.unlock_weapon('shotgun')
            unlocked_weapon = 'Shotgun'
        if wave >= 5 and 'submachine' not in self.unlocked_weapons:
            self.unlock_weapon('submachine')
            unlocked_weapon = 'Submachine Gun'
        if wave >= 10 and 'rifle' not in self.unlocked_weapons:
            self.unlock_weapon('rifle')
            unlocked_weapon = 'Rifle'
        if wave >= 20 and 'sniper' not in self.unlocked_weapons:
            self.unlock_weapon('sniper')
            unlocked_weapon = 'Sniper'

        return unlocked_weapon
    
    def reset_weapon(self):
        self.unlocked_weapons = ['pistol']


    def is_weapon_unlocked(self, weapon):
        return weapon in self.unlocked_weapons

    def main(self, display):
        if self.animation_count + 1 >= 16:  # 4 frames x 4 animations = 16
            self.animation_count = 0
        self.animation_count += 1

        pygame.draw.rect(display, (255, 0, 0), (self.x, self.y, self.width, self.height))
        self.moving_right = False
        self.moving_left = False

    def draw_health_bar(self, display):
        # Draw the health bar
        pygame.draw.rect(display, (255, 0, 0), (10, 10, 100, 10))  # Background health bar
        pygame.draw.rect(display, (0, 255, 0), (10, 10, self.health, 10))  # Current health

    def shoot(self, mouse_x, mouse_y):
        current_time = pygame.time.get_ticks()
        if self.gun == 'pistol':
            if current_time - self.last_shot > self.shot_delay:
                player_bullets.append(PlayerBullet(self.x + self.width // 2, self.y + self.height // 2, mouse_x, mouse_y, damage=self.damage['pistol'], max_penetration=self.penetration['pistol']))
                self.last_shot = current_time
        elif self.gun == 'shotgun':
            if current_time - self.last_shot > self.shot_delay:
                for angle_offset in [-0.2, 0, 0.2]:  # spread of bullets
                    player_bullets.append(PlayerBullet(self.x + self.width // 2, self.y + self.height // 2, mouse_x, mouse_y, angle_offset, damage=self.damage['shotgun'], max_penetration=self.penetration['shotgun']))
                self.last_shot = current_time
        elif self.gun == 'rifle':
            if current_time - self.last_shot > 200:  # Slower fire rate for rifle
                player_bullets.append(PlayerBullet(self.x + self.width // 2, self.y + self.height // 2, mouse_x, mouse_y, damage=self.damage['rifle'], max_penetration=self.penetration['rifle']))
                self.last_shot = current_time
        elif self.gun == 'submachine':
            if current_time - self.last_shot > 100:  # Even faster fire rate for submachine gun
                player_bullets.append(PlayerBullet(self.x + self.width // 2, self.y + self.height // 2, mouse_x, mouse_y, damage=self.damage['submachine'], max_penetration=self.penetration['submachine']))
                self.last_shot = current_time
        elif self.gun == 'sniper':
            if current_time - self.last_shot > 1000:  # Slowest fire rate for sniper
                player_bullets.append(PlayerBullet(self.x + self.width // 2, self.y + self.height // 2, mouse_x, mouse_y, damage=self.damage['sniper'], max_penetration=self.penetration['sniper']))
                self.last_shot = current_time
        elif self.gun == 'admin':
            if current_time - self.last_shot > 100:
                for angle_offset in [-0.2,-0.1,0,0.1, 0.2]:  # spread of bullets
                    player_bullets.append(PlayerBullet(self.x + self.width // 2, self.y + self.height // 2, mouse_x, mouse_y, angle_offset, damage=self.damage['admin'], max_penetration=self.penetration['admin']))
                self.last_shot = current_time


    def main(self, display):
        if self.animation_count + 1 >= 16:  # 4 frames x 4 animations = 16
            self.animation_count = 0
        self.animation_count += 1

        pygame.draw.rect(display, (255, 0, 0), (self.x, self.y, self.width, self.height))
        self.moving_right = False
        self.moving_left = False

    def draw_health_bar(self, display):
        # Draw the health bar
        pygame.draw.rect(display, (255, 0, 0), (10, 10, 100, 10))  # Background health bar
        pygame.draw.rect(display, (0, 255, 0), (10, 10, self.health, 10))  # Current health

    def shoot(self, mouse_x, mouse_y):
        current_time = pygame.time.get_ticks()
        if self.gun == 'pistol':
            if current_time - self.last_shot > self.shot_delay:
                player_bullets.append(PlayerBullet(self.x + self.width // 2, self.y + self.height // 2, mouse_x, mouse_y, damage=self.damage['pistol'], max_penetration=self.penetration['pistol']))
                self.last_shot = current_time
        elif self.gun == 'shotgun':
            if current_time - self.last_shot > self.shot_delay:
                for angle_offset in [-0.2, 0, 0.2]:  # spread of bullets
                    player_bullets.append(PlayerBullet(self.x + self.width // 2, self.y + self.height // 2, mouse_x, mouse_y, angle_offset, damage=self.damage['shotgun'], max_penetration=self.penetration['shotgun']))
                self.last_shot = current_time
        elif self.gun == 'rifle':
            if current_time - self.last_shot > 200:  # Slower fire rate for rifle
                player_bullets.append(PlayerBullet(self.x + self.width // 2, self.y + self.height // 2, mouse_x, mouse_y, damage=self.damage['rifle'], max_penetration=self.penetration['rifle']))
                self.last_shot = current_time
        elif self.gun == 'submachine':
            if current_time - self.last_shot > 100:  # Even faster fire rate for submachine gun
                player_bullets.append(PlayerBullet(self.x + self.width // 2, self.y + self.height // 2, mouse_x, mouse_y, damage=self.damage['submachine'], max_penetration=self.penetration['submachine']))
                self.last_shot = current_time
        elif self.gun == 'sniper':
            if current_time - self.last_shot > 1000:  # Slowest fire rate for sniper
                player_bullets.append(PlayerBullet(self.x + self.width // 2, self.y + self.height // 2, mouse_x, mouse_y, damage=self.damage['sniper'], max_penetration=self.penetration['sniper']))
                self.last_shot = current_time
        elif self.gun == 'admin':
            if current_time - self.last_shot > 100:
                for angle_offset in [-0.2,-0.1,0,0.1, 0.2]:  # spread of bullets
                    player_bullets.append(PlayerBullet(self.x + self.width // 2, self.y + self.height // 2, mouse_x, mouse_y, angle_offset, damage=self.damage['admin'], max_penetration=self.penetration['admin']))
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
    push_zombies_away_from_player()

def push_zombies_away_from_player():
    safe_distance = 150  # Minimum distance from the player
    for zombie in zombies:
        distance = math.sqrt((zombie.x - player.x) ** 2 + (zombie.y - player.y) ** 2)
        if distance < safe_distance:
            angle = math.atan2(zombie.y - player.y, zombie.x - player.x)
            zombie.x = player.x + math.cos(angle) * safe_distance
            zombie.y = player.y + math.sin(angle) * safe_distance

def show_weapon_switch_menu():
    display.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 30)
    text = font.render('Choose Your Weapon', True, (250, 250, 250))
    display.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 60))

     # List of weapons that are unlocked
    unlocked_weapons = [weapon for weapon in player.unlocked_weapons if player.is_weapon_unlocked(weapon)]

    y_position = 150
    for weapon in unlocked_weapons:
        button_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, y_position, 250, 30)
        pygame.draw.rect(display, (0, 0, 255), button_rect)
        weapon_text = font.render(weapon.capitalize(), True, (255, 255, 255))
        display.blit(weapon_text, (button_rect.x + 100, button_rect.y + 10))
        y_position += 70

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, weapon in enumerate(unlocked_weapons):
                    button_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, 150 + i * 70, 250, 30)
                    if button_rect.collidepoint(event.pos):
                        player.switch_gun(weapon)
                        return


def show_start_menu():
    display.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 55)
    text = font.render('Zombie Game', True, (255, 255, 255))
    display.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 100))

    start_button = pygame.Rect(SCREEN_WIDTH//2 - 150, 300, 300, 50)
    quit_button = pygame.Rect(SCREEN_WIDTH//2 - 150, 400, 300, 50)
    pygame.draw.rect(display, (0, 0, 255), start_button)
    pygame.draw.rect(display, (255, 0, 0), quit_button)
    start_text = font.render('Start', True, (255, 255, 255))
    quit_text = font.render('Quit', True, (255, 255, 255))
    display.blit(start_text, (start_button.x + 100, start_button.y + 10))
   

    display.blit(quit_text, (quit_button.x + 100, quit_button.y + 10))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def show_game_over_menu():
    display.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 55)
    text = font.render('Game Over', True, (255, 255, 255))
    display.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 100))

    restart_button = pygame.Rect(SCREEN_WIDTH//2 - 150, 300, 300, 50)
    quit_button = pygame.Rect(SCREEN_WIDTH//2 - 150, 400, 300, 50)
    pygame.draw.rect(display, (0, 0, 255), restart_button)
    pygame.draw.rect(display, (255, 0, 0), quit_button)
    restart_text = font.render('Restart', True, (255, 255, 255))
    quit_text = font.render('Quit', True, (255, 255, 255))
    display.blit(restart_text, (restart_button.x + 100, restart_button.y + 10))
    display.blit(quit_text, (quit_button.x + 100, quit_button.y + 10))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def draw_wave_number(display, wave):
    font = pygame.font.SysFont(None, 55)
    text = font.render(f'Wave: {wave}', True, (255, 255, 255))
    display.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 20))

def draw_background(display, tile):
    tile_width, tile_height = tile.get_size()
    for x in range(0, SCREEN_WIDTH, tile_width):
        for y in range(0, SCREEN_HEIGHT, tile_height):
            display.blit(tile, (x, y))

def display_unlocked_message(display, message, player_x, player_y, timer):
    font = pygame.font.SysFont(None, 20)  
    text = font.render(message, True, (255, 255, 255))
    text_width, text_height = font.size(message)
    text_x = player_x + 16 - text_width // 2  # Center the text above player
    text_y = player_y - 20  # Position it above the player
    display.blit(text, (text_x, text_y))
    return timer  # Return the timer value to continue counting

def main():
    global wave  # Declare wave as global
    show_start_menu()
    spawn_zombies(wave)

    shooting = False
    unlocked_weapon_message = None
    weapon_unlocked = False  # Flag to track if a weapon was unlocked
    unlocked_weapon_message_timer = 0

    while True:
        draw_background(display, parking_lot_tile)  # Draw the tiled background

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if you click the x on the top right, game is quit
                sys.exit()
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # on event click "fire" a bullet
                if event.button == 1:
                    shooting = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    shooting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:  # Press "T" key for weapon upgrade menu
                    show_weapon_switch_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Press "P" **ADMIN GUN**
                    player.switch_gun('admin')        
            
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

        if shooting:
            player.shoot(mouse_x, mouse_y)

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
                    show_game_over_menu() #End Screen
                    player.health = 100
                    player.x = 400
                    player.y = 300
                    zombies.clear()
                    player.reset_weapon()
                    player_bullets.clear()
                    wave = 1
                    spawn_zombies(wave)
                    show_start_menu()

        # Collision detection
        for bullet in player_bullets[:]:
            for zombie in zombies[:]:
                if zombie.x < bullet.x < zombie.x + 32 and zombie.y < bullet.y < zombie.y + 32:
                    try:
                        zombie.health -= bullet.damage
                        bullet.penetration += 1
                        if zombie.health <= 0:
                            zombies.remove(zombie)
                        if bullet.penetration >= bullet.max_penetration:
                            player_bullets.remove(bullet)
                    except ValueError:
                        pass
        

        if wave == 3:
            unlocked_weapon_message = "Shotgun"               
        elif wave == 5:
            unlocked_weapon_message = "Submachine Gun"
        elif wave == 5:
            unlocked_weapon_message = "Rifle" 
        elif wave == 5:
            unlocked_weapon_message = "Sniper"          

        if unlocked_weapon_message_timer > 0:
            unlocked_weapon_message_timer -= 1
            display_unlocked_message(display, f'Unlocked {unlocked_weapon_message}', player.x, player.y - 20, unlocked_weapon_message_timer)


        # Check if all zombies are dead to spawn a new wave
        if not zombies:
            wave += 1
            unlocked_weapon = player.can_unlock_weapon(wave)  # Check for weapon unlocking
            if unlocked_weapon:
                unlocked_weapon_message_timer = fps * 2
            spawn_zombies(wave)

        draw_wave_number(display, wave)  # Draw the wave number
        player.display_current_gun(display)  # Display current gun


        clock.tick(fps)
        pygame.display.update()

if __name__ == '__main__':
    main()

