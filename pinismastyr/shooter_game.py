from pygame import *
import random

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (55, 55))  
        self.speed = player_speed
        self.rect = self.image.get_rect() 
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0: 
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - self.rect.width:  
            self.rect.x += self.speed

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, win_width - self.rect.width)

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (10, 20))  
        self.rect = self.image.get_rect()
        self.rect.x = player_x + 22  
        self.rect.y = player_y

    def update(self):
        self.rect.y -= self.speed  
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))  
display.set_caption("ракетка гребанная") 
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))  

player = Player('rocket.png', 5, win_height - 80, 10) 

enemies = sprite.Group()
for _ in range(5):  
    enemy = Enemy('ufo.png', random.randint(0, win_width - 55), random.randint(-100, -40), random.randint(2, 5))
    enemies.add(enemy)

bullets = sprite.Group()

score_kills = 0  
score_missed = 0  
font.init()  
font = font.Font(None, 36)

mixer.init()
mixer.music.load('space.ogg')  
mixer.music.play(-1) 

fire_sound = mixer.Sound('fire.ogg')  

clock = time.Clock()
FPS = 60  
running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:  
                bullet = Bullet('bullet.png', player.rect.centerx, player.rect.top, 15)  
                bullets.add(bullet)  
                fire_sound.play()  

    player.update()
    enemies.update()
    bullets.update()

    collisions = sprite.groupcollide(enemies, bullets, True, True)  
    for enemy in collisions:
        score_kills += 1  
        enemy = Enemy('ufo.png', random.randint(0, win_width - 55), random.randint(-100, -40), random.randint(2, 5))  
        enemies.add(enemy)

    for enemy in enemies:
        if enemy.rect.y > win_height:  
            score_missed += 1  
            enemy.rect.y = random.randint(-100, -40)  
            enemy.rect.x = random.randint(0, win_width - 55) 

    player_collision = sprite.spritecollide(player, enemies, False)
    if player_collision:
        running = False  

    if score_missed >= 3:
        running = False  
    if score_kills >= 10:
        running = False  

    window.blit(background, (0, 0))
    player.reset()
    enemies.draw(window)
    bullets.draw(window)  

    score_text = font.render(f"Сбито: {score_kills} Пропущено: {score_missed}", True, (255, 255, 255))
    window.blit(score_text, (10, 10))

    if score_missed >= 3:
        end_text = font.render("Проиграл! Пропущено 3 врага.", True, (255, 0, 0))
        window.blit(end_text, (win_width // 2 - end_text.get_width() // 2, win_height // 2))
    elif score_kills >= 10:
        end_text = font.render("Победа! Повержено 10 врагов.", True, (0, 255, 0))
        window.blit(end_text, (win_width // 2 - end_text.get_width() // 2, win_height // 2))

    display.update()  
    clock.tick(FPS)

quit()
