import os

from group import AllSprites
from player import Player
from pytmx.util_pygame import load_pygame
from settings import *
from sprites import *


class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire Shooter")
        self.clock = pygame.Clock()
        self.running = True

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()

        # sprites

    def setup(self):
        map = load_pygame(os.path.join("data", "maps", "world.tmx"))

        for x, y, image in map.get_layer_by_name('Ground').tiles(): #type:ignore
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name('Objects'): #type:ignore
            CollisionSprite((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

        for obj in map.get_layer_by_name('Collisions'): #type:ignore
            InvisibleCollisionSprite((obj.x, obj.y), (obj.width, obj.height), [self.collision_sprites])

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == "Player":
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)




    def run(self):

        while self.running:

            # dt
            dt = self.clock.tick(30) / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill("darkblue")
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
