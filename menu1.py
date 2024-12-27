def menu1(screen):

    import pygame
    from load_image import load_image
    from menu2 import menu2

    class Fon(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(all_sprites)
            self.image = load_image('fon.png')
            self.rect = self.image.get_rect().move(0, 0)

    class Nachat(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(all_sprites)
            self.image = load_image('nachat.png')
            self.rect = self.image.get_rect().move(595, 600)
            self.x = 595
            self.y = 600

    class Vuhod(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(all_sprites)
            self.image = load_image('vuhod.png')
            self.rect = self.image.get_rect().move(818, 830)
            self.x = 818
            self.y = 830

    class TvS(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(all_sprites)
            self.image = load_image('TvS.png')
            self.rect = self.image.get_rect().move(810, 300)
            self.x = 810
            self.y = 300

    all_sprites = pygame.sprite.Group()

    Fon()
    TvS()
    Vuhod()
    Nachat()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x > 595 and x < 1325 and y > 600 and y < 764:
                    menu2(screen)
                if x > 818 and x < 1101 and y > 830 and y < 981:
                    running = False
        all_sprites.draw(screen)
        pygame.display.flip()