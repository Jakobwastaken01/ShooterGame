import pygame
import os
import random

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define Game Variables

Gravity = 0.75
TILE_SIZE = 40
#Player variables action

moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False
#load images
#bullet
#bullet_img = pygame.image.load('C:\\Users\\Admin\\PycharmProjects\\ShooterGame\Shooter-main\\Shooter-main\\img\\icons\\bullet.png').convert_alpha()
working_dir = os.getcwd()
bullet_img = pygame.image.load(f'{working_dir}\Shooter-main\\Shooter-main\\img\\icons\\bullet.png').convert_alpha()
#grenade
#grenade_img = pygame.image.load('C:\\Users\\Admin\\PycharmProjects\\ShooterGame\Shooter-main\\Shooter-main\\img\\icons\\grenade.png').convert_alpha()
working_dir = os.getcwd()
grenade_img = pygame.image.load(f'{working_dir}\Shooter-main\\Shooter-main\\img\\icons\\grenade.png').convert_alpha()
#pickup boxes
health_box_img = pygame.image.load('C:\\Users\\Admin\\PycharmProjects\\ShooterGame\Shooter-main\\Shooter-main\\img\\icons\\health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('C:\\Users\\Admin\\PycharmProjects\\ShooterGame\Shooter-main\\Shooter-main\\img\\icons\\ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('C:\\Users\\Admin\\PycharmProjects\\ShooterGame\Shooter-main\\Shooter-main\\img\\icons\\grenade_box.png').convert_alpha()
item_boxes = {
    'Health'   : health_box_img,
    'Ammo'  : ammo_box_img,
    'Grenade'   : grenade_box_img
}


#define Colors
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

#define font
font = pygame.font.SysFont('Futura', 31)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))
class Soldier(pygame.sprite.Sprite):
    def __init__(self,char_type, x, y, scale, speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.grenades = grenades
        self.health = 100
        self.maxhealth = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        #create ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0


        #load all images for the players
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:

            #reset temporary list of images
            temp_list = []
            #count number of files in the folder
            number_of_frames = len(os.listdir(f'C:\\Users\\Admin\\PycharmProjects\\ShooterGame\\Shooter-main\\Shooter-main\\img\\{self.char_type}\\{animation}'))
            for i in range(number_of_frames):
                img = pygame.image.load(f'C:\\Users\\Admin\\PycharmProjects\\ShooterGame\\Shooter-main\\Shooter-main\\img\\{self.char_type}\\{animation}\\{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)

            self.animation_list.append(temp_list)



        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def update(self):
        self.update_animation()
        self.check_alive()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


    def move(self, moving_left, moving_right):
        #reset movement variables
        dx = 0
        dy = 0
        if moving_left:
            dx = - self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        #apply gravity
        self.vel_y += Gravity
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        #updating rectangle pos
        self.rect.x += dx
        self.rect.y += dy


    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (self.rect.size[0] * 0.75 * self.direction), self.rect.centery,self.direction)
            bullet_group.add(bullet)
            #after shot ammo is reduced by one
            self.ammo -= 1


    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)  # 0: Idle
                self.idling = True
                self.idling_counter = 50
            #check if ai is near the player
            if self.vision.colliderect(player.rect):
                #stop running and face the player
                self.update_action(0)#0: idle
                #shooting
                self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)#1: run
                    self.move_counter += 1
                    #update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    #pygame.draw.rect(screen, RED, self.vision)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1

                else:
                    self.idling_counter -= 1
                    if self.idling_counter == 0:
                        self.idling = False



    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]


        #Check if enough Time has past since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if run out reset
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        #check if new action is different to prvious one
        if new_action != self.action:
            self.action = new_action
            #update animations settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()



    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)


    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip,False), self.rect)





class ItemBox(pygame.sprite.Sprite):
    def __init__(self,item_type, x ,y ):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE / 2, y + (TILE_SIZE - self.image.get_height()))


    def update(self):
        #check if player has picked up the box
        if pygame.sprite.collide_rect(self, player):
            #check what kind of box it was
            if self.item_type == 'Health':
                player.health += 25
            if player.health > player.maxhealth:
                player.health = player.maxhealth

            elif self.item_type == 'Ammo':
                player.ammo += 15
            elif self.item_type == 'Grenade':
                player.grenades += 3

            #delete item box
            self.kill()


class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        #update self.health
        self.health = health
        #calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x ,y , direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction


    def update(self):
        #move bullet
        self.rect.x += (self.direction * self.speed)
        #check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        #check collision with character
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x ,y , direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction


    def update(self):
        self.vel_y += Gravity
        dx = self.direction * self.speed
        dy = self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.speed = 0

        # check collision with walls
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            self.direction *= -1
            dx = self.direction * self.speed

        #update grenade pos
        self.rect.x += dx
        self.rect.y += dy

        #countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
            #do damage to anyone nearby
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                 player.health -= 50

            #if really close made by myself
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE and \
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE:
                    player.health -= 100


            # for enemies

            for enemy in enemy_group:

                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                        enemy.health -= 50
                #if really close made by myself
            #der enemy bei rect.centerx ist der von for enemy in enemy_group
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE and \
                    abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE:
                        enemy.health -= 100




class Explosion(pygame.sprite.Sprite):
    def __init__(self, x ,y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f'C:\\Users\\Admin\\PycharmProjects\\ShooterGame\\Shooter-main\\Shooter-main\\img\\explosion\\exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)

        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        EXPLOSION_SPEED = 4
        #Update explosion animation
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            #animation complete delete explosion
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]


#create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()

#temp -create item boxes
'''item_box = ItemBox('Health', 100, 262)
item_box_group.add(item_box)
item_box = ItemBox('Ammo', 400, 262)
item_box_group.add(item_box)
item_box = ItemBox('Grenade', 600, 262)
item_box_group.add(item_box)'''
item_box_group.add(ItemBox('Health', 100, 262))
item_box_group.add(ItemBox('Ammo', 400, 262))
item_box_group.add(ItemBox('Grenade', 600, 262))


player = Soldier('player', 200, 200, 1.65, 5, 20, 5)
health_bar = HealthBar(10, 10, player.health, player.health)
enemy = Soldier('enemy', 200, 249, 1.65, 2, 20, 0)
enemy2 = Soldier('enemy', 400, 249, 1.65, 2, 20, 0)
enemy_group.add(enemy)
enemy_group.add(enemy2)




x = 200
y = 200
scale = 3
img = pygame.image.load('C:\\Users\\Admin\\PycharmProjects\\ShooterGame\\Shooter-main\\Shooter-main\\img\\player\\Idle\\0.png')
img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
rect = img.get_rect()
rect.center = (x, y)

run = True
while run:

    clock.tick(FPS)
    draw_bg()
    #show player health
    health_bar.draw(player.health)
    #draw text
    draw_text('AMMO: ', font, WHITE, 10, 35)
    for x in range(player.ammo):
        screen.blit(bullet_img, (90 + (x * 10), 40))
    draw_text('GRENADES: ', font, WHITE, 10, 60)
    for x in range(player.grenades):
        screen.blit(grenade_img, (135 + (x * 15), 60))




    player.update()
    player.draw()


    for enemy in enemy_group:
        enemy.ai()
        enemy.update()
        enemy.draw()


#update and draw groups
    bullet_group.update()
    grenade_group.update()
    explosion_group.update()
    item_box_group.update()
    bullet_group.draw(screen)
    grenade_group.draw(screen)
    explosion_group.draw(screen)
    item_box_group.draw(screen)





    if player.alive:
        #shoot bullets
        if shoot:
           player.shoot()

        #throw grenades
        elif grenade and grenade_thrown == False and player.grenades > 0:
            grenade = Grenade(player.rect.centerx + (player.rect.size[0] * 0.5 * player.direction),\
                              player.rect.top, player.direction)
            grenade_group.add(grenade)
            grenade_thrown = True
            player.grenades -= 1

        if player.in_air:
            player.update_action(2)# Jump
        elif moving_left or moving_right:
            player.update_action(1)#to one means run
        else: player.update_action(0)
        player.move(moving_left, moving_right)# idle


    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_q:
                shoot = True
            if event.key == pygame.K_e:
                grenade = True
            if event.key == pygame.K_SPACE and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False


        #keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_q:
                shoot = False
            if event.key == pygame.K_e:
                grenade = False
                grenade_thrown = False


    pygame.display.update()
pygame.quit()