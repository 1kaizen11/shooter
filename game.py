import pygame
from random import randint

pygame.init()


wind_width, wind_height = 700, 500


window = pygame.display.set_mode((wind_width, wind_height))


FPS = 120

clock = pygame.time.Clock()

bullet_img = pygame.image.load("bullet.png")
back = pygame.image.load("galaxy.jpg")
back = pygame.transform.scale(back, (wind_width, wind_height))

shooting = True
score = 0
max_score = 0
count = 0
# enemies = []
enemies_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image
        self.speed = speed
    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    # def __init__(self, x, y, w, h, image):
    #     super().__init__(x, y, w, h, image)
   
    def move(self, down, up, left, right):
        k = pygame.key.get_pressed()
        if k[down]:
            if self.rect.bottom <= wind_height:
                self.rect.y += self.speed
        if k[up]:
            if self.rect.y >= 0:
                self.rect.y -= self.speed
        if k[right]:
            if self.rect.right <= wind_width:
                self.rect.x += self.speed
        if k[left]:
            if self.rect.x>= 0:
                self.rect.x -= self.speed

    def collide(self, obj):
        if self.rect.colliderect(obj.rect):
            return True
        else:
            return False
        
    def shoot(self):
        # k = pygame.key.get_pressed()
        # if k[pygame.K_SPACE]:
        bullet = Bullet(self.rect.x+23, self.rect.y, 10, 20, bullet_img, 10)
        fire_snd.play()
        
class Enemy(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image, speed)
        # enemies.append(self)
        enemies_group.add(self)

    def update(self):
            global count
            self.rect.y += self.speed
            if self.rect.y >= 500:
                # enemies.remove(self)
                enemies_group.remove(self)
                count += 1
                print(count)

class Bullet(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image, speed)
        bullet_group.add(self)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom <= 0:
            enemies_group.remove(self)
            
fire_snd = pygame.mixer.Sound("fire.ogg")
enemy_img = pygame.image.load("ufo.png")       

font = pygame.font.SysFont("Comic Sans", 80)
font1 = pygame.font.SysFont("Comic Sans", 20)

player_img = pygame.image.load("rocket.png")
player1 = Player(300, 400, 55, 55, player_img, 4)
player1.lifes = 3

life_x = 20
player_lifes = []

for i in range(player1.lifes):
    player_life = GameSprite(life_x, 20, 30, 30, player_img, 0)
    player_lifes.append(player_life)
    life_x += 33

new_game_lb = font1.render("Press space to try again", True, (255, 0, 0))
game_over = font.render("Game Over.", True, (255, 0, 0))

enemy_wait = 20

try:
    with open("data.txt", "r") as file:
        max_score = int(file.read())
except FileNotFoundError:
    file = open("data.txt", "x")
    file.close()
except ValueError:
    pass

print(max_score)
finish = False
game = True
while game:

    if not finish:
        window.blit(back, (0, 0))

        counter = font1.render("Пропущенных:"+ str(count), True, (255, 0, 0))
        counter1 = font1.render("Убито:"+ str(score), True, (255, 0, 0))
        window.blit(counter, (20, 10))
        window.blit(counter1, (20, 40))
        for player_life in player_lifes:
            player_life.update()

        if enemy_wait == 0:
            enemy = Enemy(randint(50, 650), 50, 50, 50, enemy_img, randint(1, 2))
            enemy_wait = 200
        else:
            enemy_wait -= 1

        # for enemy in enemies:
        #     enemy.update()
        #     enemy.move()

        enemies_group.draw(window)
        enemies_group.update()

        bullet_group.draw(window)
        bullet_group.update()
        # player1.shoot()

        if pygame.sprite.spritecollide(player1, enemies_group, True):
            player1.lifes -= 1
            player_lifes.pop(player1.lifes)
            print(player1.lifes)

        if player1.lifes == 0 or count >= 3:
            finish = True
            if score > max_score:
                max_score = score
                record = font1.render("Поздравляем! Новый рекорд: " + str(max_score), True, (255, 0, 0))
                with open("data.txt", "w") as file:
                    file.write(str(max_score))
            else:
                record = font1.render("Набрано: " + str(score) + " очков", True, (255, 0, 0))

        player1.update()
        player1.move(pygame.K_s, pygame.K_w, pygame.K_a, pygame.K_d)

    else:
        window.fill((255, 255, 255))
        window.blit(game_over, (wind_width/2-200, wind_height/2-100))
        window.blit(new_game_lb, (wind_width/2-100, wind_height/2))
        window.blit(record, (wind_width/2-90, wind_height/2-150))
        pygame.display.update()
        player1 = Player(300, 400, 55, 55, player_img, 4)


    if pygame.sprite.groupcollide(enemies_group, bullet_group, True, False):
        score += 1


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and finish:
            finish = False
            player1.lifes = 3
            count = 0
            score = 0
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and shooting:
            player1.shoot()
                


    pygame.display.update()
    clock.tick(FPS)