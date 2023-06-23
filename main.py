import pygame, sys, time
from settings import *
from sprites import BG, Flower, Cat, Obstacle
from os import path

graphics_dir = path.join(path.dirname(__file__), 'graphics')
sounds_dir = path.join(path.dirname(__file__), 'sounds')

class Game:
    def __init__(self):

        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('MeowCrash by 20201190 NGUYEN THI NGOC ANH')
        self.clock = pygame.time.Clock()
        self.active = True
        
        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # scale factor
        bg_height = pygame.image.load(path.join(graphics_dir, "background.png")).get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # sprite setup
        BG(self.all_sprites,self.scale_factor)
        Flower([self.all_sprites,self.collision_sprites],self.scale_factor)
        self.cat = Cat(self.all_sprites,self.scale_factor / 1.7)

        # timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer,1400)

        # text
        self.font = pygame.font.Font('BD_Cartoon_Shout.ttf',30)
        self.score = 0
        self.start_offset = 0

        # menu
        self.menu_surf = pygame.image.load(path.join(graphics_dir,'menu.png')).convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2))

        # music
        self.music = pygame.mixer.Sound(path.join(sounds_dir,'music.mp3'))
        self.music.play(loops = -1)

    def collisions(self):
        if pygame.sprite.spritecollide(self.cat,self.collision_sprites,False,pygame.sprite.collide_mask)\
        or self.cat.rect.top <= 0:
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.active = False
            self.cat.kill()

    def display_score(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)

        score_surf = self.font.render(str(self.score),True,'black')
        score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2, y))
        self.display_surface.blit(score_surf,score_rect)

    def run(self):
        last_time = time.time()
        while True:

            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.cat.jump()
                    else:
                        self.cat = Cat(self.all_sprites,self.scale_factor / 1.7)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()

                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.all_sprites,self.collision_sprites],self.scale_factor * 1.1)

            # game logic
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()

            if self.active:
                self.collisions()
            else:
                self.display_surface.blit(self.menu_surf,self.menu_rect)

            pygame.display.update()
            # self.clock.tick(FRAMERATE)

if __name__ == '__main__':
    game = Game()
    game.run()

