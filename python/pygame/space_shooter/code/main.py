from pygame.sprite import Group
import os
import random

import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join('image', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT/2)) # type:ignore
        self.direction = pygame.Vector2()
        self.speed = 300

        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

        self.mask = pygame.mask.from_surface(self.image) #type: ignore

    def laser_time(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN] - keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction

        if pygame.key.get_just_pressed()[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites)) # type: ignore
            laser_sound.play()
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_time()

        self.rect.center += self.direction * self.speed * dt #type:ignore

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_frect(center = ( #type:ignore
            random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)
        )) 

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf: pygame.Surface, pos: pygame.Vector2, groups: pygame.sprite.Group):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos) #type: ignore
        self.speed = 500


    def update(self, dt):
        self.rect.centery -= self.speed * dt #type: ignore

        if self.rect.bottom < 0: # type: ignore
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_frect(center = pos) #type: ignore
        self.speed = random.randint(400, 500)
        self.creation_time = pygame.time.get_ticks()
        self.kill_time = 3000
        self.direction = pygame.Vector2(random.uniform(-0.5, 0.5),1)
        self.rotation = 0
        self.rotation_speed = random.randint(100, 200)


    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt # type: ignore
        current_time = pygame.time.get_ticks()
        if current_time - self.creation_time >= self.kill_time:
            self.kill()

        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center) #type: ignore

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frames_index = 0
        self.image = frames[self.frames_index]
        self.rect = self.image.get_frect( center = pos) #type: ignore

    def update(self, dt):
        self.frames_index += 20 * dt
        if self.frames_index < len(self.frames):
            self.image = self.frames[int(self.frames_index)]
        else:
            self.kill()

def collisions():
    global running
    meteor_collisions = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask) #type: ignore
    if meteor_collisions:
         explosion_sound.play()
         running = False
    # pygame.sprite.groupcollide(laser_sprites, meteor_sprites, True, True)
    for laser in laser_sprites:
        if pygame.sprite.spritecollide(laser, meteor_sprites, True):
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play()

def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(f"{current_time}", True, (240,240,240) )
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, (240,240,240), text_rect.inflate(20, 16).move(0,-7), 5, 10)

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("Space shooter")
running = True

clock = pygame.time.Clock()

#imports
star_surf = pygame.image.load(os.path.join('image', 'star.png')).convert_alpha()
meteor_surf = pygame.image.load(os.path.join('image', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(os.path.join('image', 'laser.png')).convert_alpha()
font = pygame.font.Font(os.path.join("image", "Oxanium-Bold.ttf"), 40)
explosion_frames = [pygame.image.load(os.path.join("image", "explosion", f"{i}.png")).convert_alpha() for i in range(21)]
laser_sound = pygame.mixer.Sound(os.path.join("audio", "laser.wav"))
laser_sound.set_volume(0.5)
explosion_sound = pygame.mixer.Sound(os.path.join("audio", "explosion.wav"))
explosion_sound.set_volume(0.5)
damage_sound = pygame.mixer.Sound(os.path.join("audio", "damage.ogg"))
damage_sound.set_volume(0.5)
game_music_sound = pygame.mixer.Sound(os.path.join("audio", "game_music.wav"))
game_music_sound.set_volume(0.2)
game_music_sound.play(loops=-1)

# creation
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for _ in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)


# custom events: meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor(
                    meteor_surf,
                    (random.randint(0, WINDOW_WIDTH), random.randint(-200, -100)),
                    (all_sprites, meteor_sprites)
                )

    all_sprites.update(dt)
    collisions()
    display_surface.fill("#3a2e3f")
    all_sprites.draw(display_surface)
    display_score()
    pygame.display.update()

pygame.quit()
