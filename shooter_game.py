#Создай собственный Шутер!

from random import *
from pygame import *
font.init()
mixer.init()

skipped = 0
score = 0
fire_flag = True

class Player(sprite.Sprite):
    def __init__(self, pl_img, pl_x, pl_y, pl_sp):
        super().__init__()
        self.image = transform.scale(image.load(pl_img), (60, 90))
        self.rect =  self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y
        self.speed = pl_sp

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x >= 50:
            self.rect.x -= self.speed
            
        if keys_pressed[K_RIGHT] and self.rect.x <= 575:
            self.rect.x += self.speed

        self.fire()
    
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

    def colliderect(self, rect):
        return self.rect.colliderect(rect)

    def fire(self):
        if count == 1:
            global bullets
            b = Bullet("bullet.png", self.rect.centerx, self.rect.top, 5)
            bullets.add(b)
            fire.play()
            
class Enemy(sprite.Sprite):
    def __init__(self, pl_img, pl_x, pl_y, pl_sp):
        super().__init__()
        self.image = transform.scale(image.load(pl_img), (75, 50))
        self.speed = pl_sp
        self.rect =  self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

    def new(self):
        self.rect.x = randint(50, 575)
        self.rect.y = 15

    def update(self):
        if self.rect.y <= 500:
            self.rect.y += self.speed
        else:
            self.new()
            global skipped
            skipped += 1

class Asteroid(sprite.Sprite):
    def __init__(self, pl_img, pl_x, pl_y, pl_sp):
        super().__init__()
        self.image = transform.scale(image.load(pl_img), (60, 45))
        self.speed = pl_sp
        self.rect =  self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

    def new(self):
        self.rect.x = randint(50, 575)
        self.rect.y = 15

    def update(self):
        if self.rect.y <= 500:
            self.rect.y += self.speed
        else:
            self.new()

class Bullet(sprite.Sprite):
    def __init__(self, pl_img, pl_x, pl_y, pl_sp):
        super().__init__()
        self.image = transform.scale(image.load(pl_img), (15, 30))
        self.speed = pl_sp
        self.rect =  self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

    def colliderect(self, rect):
        return self.rect.colliderect(rect)

    def update(self):
        collide = False
        for m in monsters:
            if self.colliderect(m):
                m.new()
                global score
                score += 1
                collide = True

        if self.rect.y < 10 or collide:
            self.kill()
        else:
            self.rect.y -= self.speed

win = display.set_mode((700, 500))
display.set_caption('Hehe')
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

mixer.music.load("space.ogg")
mixer.music.play()
fire = mixer.Sound("fire.ogg")

font1 = font.SysFont('Arial', 30)
score_text = font1.render('Score: '+str(score), True, (255, 255, 255))
skipped_text = font1.render('Skipped: '+str(skipped), True, (255, 255, 255))
fire_text = font1.render('Fire: '+str(fire_flag), True, (255, 255, 255))

font2 = font.SysFont('Arial', 60)
winn = font2.render('YOU WIN!', True, (255, 215, 0))
lose = font2.render('YOU LOSE', True, (255, 0, 0))

font3 = font.SysFont('Arial', 40)
restart = font3.render('press "r" to restart', True, (255, 255, 255))

rocket = Player("rocket.png", 50, 380, 10)

monsters = sprite.Group()
monsters.add(Enemy("ufo.png", 100, 50, 2))
monsters.add(Enemy("ufo.png", 200, 35, 1))
monsters.add(Enemy("ufo.png", 300, 20, 1))
monsters.add(Enemy("ufo.png", 124, 73, 2))
monsters.add(Enemy("ufo.png", 466, 25, 1))

asteroids = sprite.Group()
asteroids.add(Asteroid("asteroid.png", 153, 12, 2))
asteroids.add(Asteroid("asteroid.png", 154, 56, 1))
asteroids.add(Asteroid("asteroid.png", 134, 25, 1))
asteroids.add(Asteroid("asteroid.png", 358, 27, 2))
asteroids.add(Asteroid("asteroid.png", 164, 98, 1))

hurtst = list()
hurtsf = list()
for h in range(3):
    hurtst.append(transform.scale(image.load("hurttrue.png"), (115, 115)))
    hurtsf.append(transform.scale(image.load("hurtfalse.png"), (115, 115)))

bullets = sprite.Group()

hurts = 3
counter = 0
count = 0
finish = True
clock = time.Clock()
FPS = 60
game = True
while game:

    win.blit(background, (0, 0))

    if finish != False:

        rocket.update()
        rocket.reset()

        count = 0
        bullets.update()
        bullets.draw(win)
        
        monsters.update()
        monsters.draw(win)

        asteroids.update()
        asteroids.draw(win)

        if counter == 80:
            counter = -40
        counter += 1
        
        for e in event.get():
            if e.type == QUIT:
                game = False 
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if counter < 80 and counter > 0:
                        count += 1
            elif e.type == KEYUP:
                if e.key == K_SPACE:
                    count = 0

        for h in range(0, len(hurtsf)):
            win.blit(hurtsf[h], (525+50*h, 5))

        for h in range(0, hurts):
            win.blit(hurtst[h], (525+50*h, 5))

        collide = False
        for m in monsters:
            if rocket.colliderect(m):
                collide = True
                m.new()
        for a in asteroids:
            if rocket.colliderect(a):
                collide = True
                a.new()
        if collide:
            hurts -= 1

        if score >= 10:
            result = 1
            finish = False
        elif skipped >= 7:
            result = 2
            finish = False
        else:
            if hurts == 0:
                finish = False
                result = 2

        if counter < 40 and counter > 0:
            fire_flag = True
        else: 
            fire_flag = False

        score_text = font1.render('Score: '+str(score), True, (255, 255, 255))
        skipped_text = font1.render('Skipped: '+str(skipped), True, (255, 255, 255))
        fire_text = font1.render('Fire: '+str(fire_flag), True, (255, 255, 255))

        win.blit(score_text, (15, 15))
        win.blit(skipped_text, (15, 50)) 
        win.blit(fire_text, (15, 85))         
    else:
        for e in event.get():
            if e.type == QUIT:
                game = False 
            if e.type == KEYDOWN:
                if e.key == K_r:
                    finish = True
                    count = 0
                    for m in monsters:
                        m.new()
                    for a in asteroids:
                        a.new()
                    score = 0
                    skipped = 0
                    hurts = 3

        if result == 1:
            win.blit(winn, (210, 200))
            win.blit(restart, (200, 260))
        elif result == 2:
            win.blit(lose, (210, 200))
            win.blit(restart, (200, 260))

    display.update()
    clock.tick(FPS)