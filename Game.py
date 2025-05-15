import pygame 
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("images/Player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("images/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("images/Player/jump.png").convert_alpha()
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("audio/jump.wav")
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()
    
class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "fly":
            fly_1 = pygame.image.load("images/Fly/Fly1.png").convert_alpha()
            fly_2 = pygame.image.load("images/Fly/Fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load("images/Snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("images/Snail/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))
        
    def animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation()
        self.rect.x -= 7
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
            
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, enemies, False):
        enemies.empty()
        gameOver_sound.play()
        return False
    else:
        return True

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surf = test_font.render(f"Score: {current_time // 100}", False, "Black")
    score_rect = score_surf.get_rect(center=(width / 2, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def background_move():
    global bg_scroll
    bg_scroll -= 2
    if bg_scroll <= -850:
        bg_scroll = 0
    screen.blit(sky_surface, (bg_scroll, 0))
    screen.blit(sky_surface, (bg_scroll + 850, 0))
    screen.blit(ground_surface, (bg_scroll, 300))
    screen.blit(ground_surface, (bg_scroll + 850, 300))

pygame.init()

# Display setup
width = 800
height = 400
fps = 60
bg_scroll = 0

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("dinoRunner")
icon = pygame.image.load("images/Player/icon.png").convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)
game_active = False
start_time = 0
score = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

enemies = pygame.sprite.Group()

# Background
sky_surface = pygame.image.load("images/Sky2.png").convert()
ground_surface = pygame.image.load("images/ground2.png").convert()

# Text
game_name = test_font.render("Dino runner", False, (100, 225, 150))
game_name_rect = game_name.get_rect(center=(width / 2, 80))
tutor_surf = test_font.render("PRESS SPACE TO PLAY", False, (100, 225, 150))
tutor_rect = tutor_surf.get_rect(center=(width / 2, 330))

# Audio
pygame.mixer.music.load("audio/music.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

gameOver_sound = pygame.mixer.Sound("audio/gameover.wav")

# Player stand image for the menu
player_stand = pygame.image.load("images/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 1.8)
player_stand_rect = player_stand.get_rect(center=(width / 2, height / 2))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                enemies.add(Enemy(choice(['snail', 'fly', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True  
                start_time = pygame.time.get_ticks()
    
    if game_active:
        background_move()
        score = display_score()

        player.draw(screen)
        player.update()
        
        enemies.draw(screen)
        enemies.update()
        
        game_active = collision_sprite()
    else:
        screen.fill((90, 120, 160))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)
        player_score = test_font.render(f"Your Score: {score // 100}", False, (100, 225, 150))
        player_score_rect = tutor_surf.get_rect(center=(width / 2 + 50, 330))
        if score == 0:
            screen.blit(tutor_surf, tutor_rect)
        else:
            screen.blit(player_score, player_score_rect)
        enemies.empty() 
        
    pygame.display.update()
    clock.tick(fps)
    
            