def menu2(screen):

    import pygame
    from load_image import load_image
    from game import game

    class Fon(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(all_sprites)
            self.image = load_image('fon.png')
            self.rect = self.image.get_rect().move(0, 0)

    class Yroven(pygame.sprite.Sprite):
        def __init__(self, n, k=0):
            super().__init__(all_sprites)
            filename = "data/" + 'levels.txt'
            with open(filename, 'r') as mapFile:
                level_map = [line.strip() for line in mapFile]
            self.image = load_image(level_map[-1 * n] + '.png')
            self.rect = self.image.get_rect().move(150 + (n - 1 - k * 5) * 350, 125 + k * 355)
            self.x = 818
            self.y = 830

    class Nazad(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(all_sprites)
            self.image = load_image('nazad.png')
            self.rect = self.image.get_rect().move(818, 830)
            self.x = 818
            self.y = 830

    all_sprites = pygame.sprite.Group()

    Fon()
    Nazad()
    for i in range(1, 6):
        Yroven(i)
    for i in range(1, 6):
        Yroven(i + 5, 1)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x > 818 and x < 1101 and y > 830 and y < 981:
                    running = False
                elif y > 125 and y < 362:
                    if x > 150 and x < 388:
                        game(screen, 1)
                    elif x > 500 and x < 738:
                        game(screen, 2)
                    elif x > 850 and x < 1088:
                        game(screen, 3)
                    elif x > 1200 and x < 1438:
                        game(screen, 4)
                    elif x > 1550 and x < 1788:
                        game(screen, 5)
                elif y > 480 and y < 717:
                    if x > 150 and x < 388:
                        game(screen, 6)
                    elif x > 500 and x < 738:
                        game(screen, 7)
                    elif x > 850 and x < 1088:
                        game(screen, 8)
                    elif x > 1200 and x < 1438:
                        game(screen, 9)
                    elif x > 1550 and x < 1788:
                        game(screen, 10)
        all_sprites.draw(screen)
        pygame.display.flip()