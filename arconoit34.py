from pygame import *
from random import randint
from time import time as timer
mixer.init()
mixer.music.load('Simon_Viklund_-_Black_Yellow_Moebius_(patefon.org).mp3')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
lost = 0

class GameSprite(sprite.Sprite):

    def __init__(self, player_image,player_x, player_y,size_x,size_y,player_speed):
        super(). __init__()

        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if (keys[K_LEFT] or keys[K_a]) and self.rect.x>5:
            self.rect.x -= self.speed
        if (keys[K_RIGHT] or keys[K_d]) and self.rect.x< win_wight-80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet,self.rect.centerx,self.rect.top,15,20,-10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >win_height:
            self.rect.y = 0 
            self.rect.x = randint(80,win_wight - 80)
            self.speed = randint(1,5)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()

font.init()
fon = font.Font(None,36)
img_bullet = "bullet.png"
img_bg = 'Gallery0000.webp'
img_Player = 'gun-removebg-preview (1).png'
img_enemy = 'ballas3-removebg-preview.png'
win_wight = 700
win_height = 500
ship = Player(img_Player,5,win_height-100,80,100,10)
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy,randint(80,win_wight - 80),
                    -40,80,50,randint(1,5))
    monsters.add(monster)
display.set_caption('Shooter')
window = display.set_mode((win_wight,win_height))
bg = transform.scale(image.load(img_bg),(win_wight,win_height))
timer = time.Clock()
game = True
finish = False
score = 0
num_fire = 0
rel_fire = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
            
        elif e.type ==KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <7 and rel_fire == False:
                    fire_sound.play()
                    ship.fire()
                if num_fire >=5 and rel_fire == False:
                    lasr_time = timer()
                    rel_fire = True
    if not finish:
        if rel_fire == True:
            now_time = timer()
            if now_time - time <3:
                window.blit(fon.render("reload..",True,(255,255,255)),(325,225))
            else:
                num_fire=0
                rel_fire = False
        text = fon.render('рахунок ' + str(score),1,(0,0,0))
        window.blit(text,(10,20))
        text_lost = fon.render('пропушено '  + str(lost),1,(0,0,0))
        window.blit(text_lost,(10,50))

        ship.update()
        monsters.update()
        bullets.update()

        monsters.draw(window)
        ship.reset()
        bullets.draw(window)
        colides = sprite.groupcollide(monsters, bullets,True,True)
        for  c in colides:
            score +=1
            monster = Enemy(img_enemy,randint(80,win_wight - 80),
                    -40,80,50,randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters,False) or lost >= 10:
            finish = True
            window.blit(fon.render("LOSE",True,(86, 11, 95)),(300,200))
        if score >= 15:
            finish = True
            window.blit(fon.render("WIN",True,(36, 171, 0)),(300,200))
        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        for i in bullets:
            i.kill()
        for i in monsters:
            i.kill()
        time.delay(3000)
        for i in range(1,8):
            monster = Enemy (img_enemy,randint(80,win_wight - 80),
                    -40,80,50,randint(1,5))
        monsters.add(monster)
             
    timer.tick(60)