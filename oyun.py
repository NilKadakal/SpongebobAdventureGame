import pygame
import random
import math

WIDTH = 480
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (65, 65))
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.lives = 3
        self.speed_multiplier = 1.0 

    def update(self):
        speed_x = 0
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.image = pygame.transform.flip(self.original_image, True, False)
            speed_x = -8 * self.speed_multiplier 
        if keys[pygame.K_RIGHT]:
            self.image = self.original_image
            speed_x = 8 * self.speed_multiplier
            
        self.rect.x += speed_x
        if self.rect.right > WIDTH: self.rect.right = WIDTH
        if self.rect.left < 0: self.rect.left = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed_bonus):
        super().__init__()
        self.image = pygame.image.load("enemy.png").convert_alpha()
  
        self.image = pygame.transform.scale(self.image, (50, 50))
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        
       
        self.y_pos = float(self.rect.y) 
        self.speed_y = random.randrange(1,4) + speed_bonus

    def update(self):
        
        self.y_pos += self.speed_y
        offset = math.sin(self.y_pos * 0.02) * 1.2
        self.rect.y = int(self.y_pos)
        self.rect.x += offset
        
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.y_pos = float(self.rect.y) 
            return True 
        return False
    
class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("burger.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-500, -100)
        self.speed_y = 5

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()

def show_go_screen(final_score=None):
    global highscore 
    screen.blit(background, (0, 0))
    
    if final_score is None:
        draw_text(screen, "SPONGEBOB ADVENTURE", 35, WIDTH // 2, HEIGHT / 6)
        sb_rect = GIRIS_RESMI.get_rect()
        sb_rect.center = (WIDTH // 2, HEIGHT // 2 - 30)
        screen.blit(GIRIS_RESMI, sb_rect)
        draw_text(screen, f"HIGH SCORE: {highscore}", 22, WIDTH // 2, HEIGHT * 0.65)
        draw_text(screen, "Use Arrow Keys to Move", 20, WIDTH // 2, HEIGHT * 0.80)
    else:
        if final_score > highscore:
            highscore = final_score
            save_highscore(highscore)
            draw_text(screen, "NEW HIGH SCORE!", 32, WIDTH // 2, HEIGHT / 2 - 80)

        draw_text(screen, "GAME OVER", 64, WIDTH // 2, HEIGHT / 4)
        draw_text(screen, f"TOTAL SCORE: {final_score}", 32, WIDTH // 2, HEIGHT / 2)
        draw_text(screen, f"HIGH SCORE: {highscore}", 22, WIDTH // 2, HEIGHT / 2 + 50)
        draw_text(screen, "Press any key to play again", 22, WIDTH // 2, HEIGHT * 0.80)

    draw_text(screen, "Press any key to continue", 18, WIDTH // 2, HEIGHT * 0.90)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                waiting = False
import os
HS_FILE = "highscore.txt"

def load_highscore():
    if os.path.exists(HS_FILE):
        with open(HS_FILE, "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def save_highscore(new_score):
    with open(HS_FILE, "w") as f:
        f.write(str(new_score))
highscore = load_highscore()

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("arkası.jpg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
clock = pygame.time.Clock()
font_name = pygame.font.match_font('arial')
GIRIS_RESMI = pygame.image.load("giriskısmı.png").convert_alpha()
GIRIS_RESMI = pygame.transform.smoothscale(GIRIS_RESMI, (200, 200))
heart_img = pygame.image.load("heart.png").convert_alpha()
heart_img = pygame.transform.smoothscale(heart_img, (30, 30))

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 35 * i  
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def reset_game():
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    powerups = pygame.sprite.Group() 
    player = Player()
    all_sprites.add(player)
    for i in range(8):
        m = Enemy(0)
        all_sprites.add(m)
        enemies.add(m)
    return all_sprites, enemies, powerups, player


score = 0
level = 1
level_up_timer = 0
speed_bonus = 0  
running = True
game_over = True


while running:
    if game_over:
        if score > 0:
            show_go_screen(score)
        else:
            show_go_screen() 
            
        game_over = False
        all_sprites, enemies, powerups, player = reset_game()
        score = 0
        speed_bonus = 0

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
    all_sprites.update()
    for enemy in enemies:
        if enemy.update(): 
            score += 10
            new_level = (score // 500) + 1
            if new_level > level:
               level = new_level
               level_up_timer = pygame.time.get_ticks()
               new_enemy = Enemy(speed_bonus)
               all_sprites.add(new_enemy)
               enemies.add(new_enemy)
            speed_bonus = (score // 100) * 0.2
            print(f"Speed Bonus: {speed_bonus}")
    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        player.lives -= 1
        m = Enemy(speed_bonus)
        all_sprites.add(m)
        enemies.add(m)
        if player.lives <= 0:
            game_over = True

        
    if random.random() < 0.005:
       p = PowerUp()
       all_sprites.add(p)
       powerups.add(p)


    burger_hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in burger_hits:
        if player.lives < 5:
            player.lives += 1
        player.speed_multiplier = 1.5


    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, f"Score: {score} Level: {level}", 18, WIDTH // 2, 10)
    draw_lives(screen, WIDTH - 120, 15, player.lives, heart_img)
    if pygame.time.get_ticks() - level_up_timer < 2000:
       draw_text(screen, f"LEVEL {level}", 64, WIDTH // 2, HEIGHT // 2)
       draw_text(screen, "GET READY!", 32, WIDTH // 2, HEIGHT // 2 + 60)
    pygame.display.flip()

pygame.quit()
