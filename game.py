def game(screen, number):

    import pygame
    from random import choice
    from load_image import load_image

    spawn_sprite = 0
    enemy_way1, enemy_way2, enemy_way3 = [], [], []
    enemy_way_last = 2
    wave_const = 0
    hp = 20
    enemy_hp = 10
    boss_hp = 100

    def lose_hp(h=1):
        nonlocal hp
        hp -= h
        if hp == 0:
            win(0)

    def write(n):
        nonlocal number
        filename = "data/" + 'levels.txt'
        with open(filename, 'r') as file:
            txt = file.read()
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        a = level_map[-1 * number]
        b = 'lv' + str(number) + '_' + str(n)
        txt = txt.replace(a, max(a, b))
        with open(filename, 'w') as file:
            file.write(txt)

    def win(hp):
        nonlocal wins, speed
        wins = True
        Pausa()
        Menu1()
        speed = 0
        if hp == 20:
            Zvezda(True, 572, 400)
            Zvezda(True, 872, 450)
            Zvezda(True, 1172, 400)
            Nadpis(True)
            write(3)
        elif hp > 10:
            Zvezda(True, 572, 400)
            Zvezda(True, 872, 450)
            Zvezda(False, 1172, 400)
            Nadpis(True)
            write(2)
        elif hp > 0:
            Zvezda(True, 572, 400)
            Zvezda(False, 872, 450)
            Zvezda(False, 1172, 400)
            Nadpis(True)
            write(1)
        else:
            Zvezda(False, 572, 400)
            Zvezda(False, 872, 450)
            Zvezda(False, 1172, 400)
            Nadpis(False)

    def magaz():
        Magaz()
        nonlocal knopki_list
        knopki_list += [Knopka(1560, 65, 'mass')]
        knopki_list += [Knopka(1560, 255, 'luchnik')]
        knopki_list += [Knopka(1560, 445, 'zam')]
        knopki_list += [Knopka(1560, 635, 'dal')]
        knopki_list += [Knopka(1560, 825, 'sila')]
        MassImage(1780, 90)
        LuchnikImage(1780, 280)
        ZamImage(1780, 470)
        DalImage(1780, 660)
        SilaImage(1780, 850)
        Paus()
        knopki_list += [Speed()]
        Heart()
        Coin()


    class Heart(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(magaz_sprites, all_sprites)
            self.image = image_list['heart']
            self.rect = self.image.get_rect().move(1840, 990)
            self.x = 1840
            self.y = 8


    class Coin(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(magaz_sprites, all_sprites)
            self.image = image_list['coin']
            self.rect = self.image.get_rect().move(1660, 990)
            self.x = 1840
            self.y = 8


    def generate_level(level):
        nonlocal spawn_sprite
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    level[y][x] = None
                elif level[y][x] == '#':
                    level[y][x] = Stena(x, y)
                elif level[y][x] in ['-', '1', '2', '3', '4', '5', '6', '7', '8']:
                    level[y][x] = Doroga(x, y)
                elif level[y][x] in ['l', 'u', 'r', 'd']:
                    spawn_sprite = Spawn(x, y, type=level[y][x])
                    level[y][x] = spawn_sprite
                elif level[y][x] in ['L', 'U', 'R', 'D']:
                    end_sprite = End(x, y, type=level[y][x])
                    level[y][x] = end_sprite

        return level

    def load_level(filename, number):
        nonlocal wave_const, enemy_hp, boss_hp
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        lines = level_map.index('lv' + str(number))
        info_round = level_map[lines + 11: lines + 15]
        level_map = level_map[lines + 1: lines + 11]
        wave_const = int(info_round[0])
        boss_hp = int(info_round[1])
        enemy_hp = int(info_round[2])
        for i in range(len(level_map)):
            level_map[i] = list(level_map[i])
            if 'l' in level_map[i]:
                posy = i
                posx = level_map[i].index('l')
                drctn = 'l'
            elif 'u' in level_map[i]:
                posy = i
                posx = level_map[i].index('u')
                drctn = 'u'
            elif 'r' in level_map[i]:
                posy = i
                posx = level_map[i].index('r')
                drctn = 'r'
            elif 'd' in level_map[i]:
                posy = i
                posx = level_map[i].index('d')
                drctn = 'd'
        nonlocal enemy_way1, enemy_way2, enemy_way3
        while True:
            s = level_map[posy][posx]
            if s == '-':
                if drctn == 'l':
                    enemy_way1 += [(i, tile * posy + (tile // 6)) for i in
                                  range(tile * (posx + 1) - 1, tile * posx - 1, -1)]
                    enemy_way2 += [(i, tile * posy + tile // 2) for i in
                                  range(tile * (posx + 1) - 1, tile * posx - 1, -1)]
                    enemy_way3 += [(i, tile * posy + (5 * tile // 6)) for i in
                                  range(tile * (posx + 1) - 1, tile * posx - 1, -1)]
                elif drctn == 'r':
                    enemy_way1 += [(i, tile * posy + (5 * tile // 6)) for i in range(tile * posx, tile * (posx + 1))]
                    enemy_way2 += [(i, tile * posy + tile // 2) for i in range(tile * posx, tile * (posx + 1))]
                    enemy_way3 += [(i, tile * posy + (tile // 6)) for i in range(tile * posx, tile * (posx + 1))]
                elif drctn == 'd':
                    enemy_way1 += [(tile * posx + (tile // 6), i) for i in range(tile * posy, tile * (posy + 1))]
                    enemy_way2 += [(tile * posx + tile // 2, i) for i in range(tile * posy, tile * (posy + 1))]
                    enemy_way3 += [(tile * posx + (5 * tile // 6), i) for i in range(tile * posy, tile * (posy + 1))]
                elif drctn == 'u':
                    enemy_way1 += [(tile * posx + (5 * tile // 6), i) for i in
                                  range(tile * (posy + 1) - 1, tile * posy - 1, -1)]
                    enemy_way2 += [(tile * posx + tile // 2, i) for i in
                                  range(tile * (posy + 1) - 1, tile * posy - 1, -1)]
                    enemy_way3 += [(tile * posx + (tile // 6), i) for i in
                                  range(tile * (posy + 1) - 1, tile * posy - 1, -1)]
            elif s == '1':  # снизу влево
                enemy_way1 += ([(tile * posx + (5 * tile // 6), i)
                               for i in range(tile * (posy + 1) - 1, tile * posy + (tile // 6) - 1, -1)]
                              + [(i, tile * posy + (tile // 6))
                                 for i in range(tile * posx + (5 * tile // 6) - 1, tile * posx - 1, -1)])
                enemy_way2 += ([(tile * posx + tile // 2, i)
                               for i in range(tile * (posy + 1) - 1, tile * posy + tile // 2 - 1, -1)]
                              + [(i, tile * posy + tile // 2)
                                 for i in range(tile * posx + tile // 2 - 1, tile * posx - 1, -1)])
                enemy_way3 += ([(tile * posx + (tile // 6), i)
                               for i in range(tile * (posy + 1) - 1, tile * posy + (5 * tile // 6) - 1, -1)]
                              + [(i, tile * posy + (5 * tile // 6))
                                 for i in range(tile * posx + (tile // 6) - 1, tile * posx - 1, -1)])
                drctn = 'l'
            elif s == '2':  # снизу вправо
                enemy_way1 += ([(tile * posx + (5 * tile // 6), i)
                               for i in range(tile * (posy + 1) - 1, tile * posy + (5 * tile // 6) - 1, -1)]
                              + [(i, tile * posy + (5 * tile // 6))
                                 for i in range(tile * posx + (5 * tile // 6), tile * (posx + 1))])
                enemy_way2 += ([(tile * posx + tile // 2, i)
                               for i in range(tile * (posy + 1) - 1, tile * posy + tile // 2 - 1, -1)]
                              + [(i, tile * posy + tile // 2)
                                 for i in range(tile * posx + tile // 2, tile * (posx + 1))])
                enemy_way3 += ([(tile * posx + (tile // 6), i)
                               for i in range(tile * (posy + 1) - 1, tile * posy + (tile // 6) - 1, -1)]
                              + [(i, tile * posy + (tile // 6))
                                 for i in range(tile * posx + (tile // 6), tile * (posx + 1))])
                drctn = 'r'
            elif s == '3':  # сверху влево
                enemy_way1 += ([(tile * posx + (tile // 6), i)
                               for i in range(tile * posy, tile * posy + (tile // 6))]
                              + [(i, tile * posy + (tile // 6))
                                 for i in range(tile * posx + (tile // 6) - 1, tile * posx - 1, -1)])
                enemy_way2 += ([(tile * posx + tile // 2, i)
                               for i in range(tile * posy, tile * posy + tile // 2)]
                              + [(i, tile * posy + tile // 2)
                                 for i in range(tile * posx + tile // 2 - 1, tile * posx - 1, -1)])
                enemy_way3 += ([(tile * posx + (5 * tile // 6), i)
                               for i in range(tile * posy, tile * posy + (5 * tile // 6))]
                              + [(i, tile * posy + (5 * tile // 6))
                                 for i in range(tile * posx + (5 * tile // 6) - 1, tile * posx - 1, -1)])
                drctn = 'l'
            elif s == '4':  # сверху вправо
                enemy_way1 += ([(tile * posx + (tile // 6), i)
                               for i in range(tile * posy, tile * posy + (5 * tile // 6))]
                              + [(i, tile * posy + (5 * tile // 6))
                                 for i in range(tile * posx + (tile // 6), tile * (posx + 1))])
                enemy_way2 += ([(tile * posx + tile // 2, i)
                               for i in range(tile * posy, tile * posy + tile // 2)]
                              + [(i, tile * posy + tile // 2)
                                 for i in range(tile * posx + tile // 2, tile * (posx + 1))])
                enemy_way3 += ([(tile * posx + (5 * tile // 6), i)
                               for i in range(tile * posy, tile * posy + (tile // 6))]
                              + [(i, tile * posy + (tile // 6))
                                 for i in range(tile * posx + (5 * tile // 6), tile * (posx + 1))])
                drctn = 'r'
            elif s == '5':  # слева вниз
                enemy_way1 += ([(i, tile * posy + (5 * tile // 6))
                               for i in range(tile * posx, tile * posx + (tile // 6))]
                              + [(tile * posx + (tile // 6), i)
                                 for i in range(tile * posy + (5 * tile // 6), tile * (posy + 1))])
                enemy_way2 += ([(i, tile * posy + tile // 2)
                               for i in range(tile * posx, tile * posx + tile // 2)]
                              + [(tile * posx + tile // 2, i)
                                 for i in range(tile * posy + tile // 2, tile * (posy + 1))])
                enemy_way3 += ([(i, tile * posy + (tile // 6))
                               for i in range(tile * posx, tile * posx + (5 * tile // 6))]
                              + [(tile * posx + (5 * tile // 6), i)
                                 for i in range(tile * posy + (tile // 6), tile * (posy + 1))])
                drctn = 'd'
            elif s == '6':  # слева вверх
                enemy_way1 += ([(i, tile * posy + (5 * tile // 6))
                               for i in range(tile * posx, tile * posx + (5 * tile // 6))]
                              + [(tile * posx + (5 * tile // 6), i)
                                 for i in range(tile * posy + (5 * tile // 6) - 1, tile * posy - 1, -1)])
                enemy_way2 += ([(i, tile * posy + tile // 2)
                               for i in range(tile * posx, tile * posx + tile // 2)]
                              + [(tile * posx + tile // 2, i)
                                 for i in range(tile * posy + tile // 2 - 1, tile * posy - 1, -1)])
                enemy_way3 += ([(i, tile * posy + (tile // 6))
                               for i in range(tile * posx, tile * posx + (tile // 6))]
                              + [(tile * posx + (tile // 6), i)
                                 for i in range(tile * posy + (tile // 6) - 1, tile * posy - 1, -1)])
                drctn = 'u'
            elif s == '7':  # справа вниз
                enemy_way1 += ([(i, tile * posy + (tile // 6))
                               for i in range(tile * (posx + 1) - 1, tile * posx + (tile // 6) - 1, -1)]
                              + [(tile * posx + (tile // 6), i)
                                 for i in range(tile * posy + (tile // 6), tile * (posy + 1))])
                enemy_way2 += ([(i, tile * posy + tile // 2)
                               for i in range(tile * (posx + 1) - 1, tile * posx + tile // 2 - 1, -1)]
                              + [(tile * posx + tile // 2, i)
                                 for i in range(tile * posy + tile // 2, tile * (posy + 1))])
                enemy_way3 += ([(i, tile * posy + (5 * tile // 6))
                               for i in range(tile * (posx + 1) - 1, tile * posx + (5 * tile // 6) - 1, -1)]
                              + [(tile * posx + (5 * tile // 6), i)
                                 for i in range(tile * posy + (5 * tile // 6), tile * (posy + 1))])
                drctn = 'd'
            elif s == '8':  # справа вверх
                enemy_way1 += ([(i, tile * posy + (tile // 6))
                               for i in range(tile * (posx + 1) - 1, tile * posx + (5 * tile // 6) - 1, -1)]
                              + [(tile * posx + (5 * tile // 6), i)
                                 for i in range(tile * posy + (tile // 6) - 1, tile * posy - 1, -1)])
                enemy_way2 += ([(i, tile * posy + tile // 2)
                               for i in range(tile * (posx + 1) - 1, tile * posx + tile // 2 - 1, -1)]
                              + [(tile * posx + tile // 2, i)
                                 for i in range(tile * posy + tile // 2 - 1, tile * posy - 1, -1)])
                enemy_way3 += ([(i, tile * posy + (5 * tile // 6))
                               for i in range(tile * (posx + 1) - 1, tile * posx + (tile // 6) - 1, -1)]
                              + [(tile * posx + (tile // 6), i)
                                 for i in range(tile * posy + (5 * tile // 6) - 1, tile * posy - 1, -1)])
                drctn = 'u'
            elif s in ['r', 'l', 'u', 'd']:
                if drctn == 'l':
                    enemy_way1 += [(i, tile * posy + (tile // 6))
                                  for i in range(tile * posx + 5 * (tile // 6) - 1, tile * posx - 1, -1)]
                    enemy_way2 += [(i, tile * posy + tile // 2)
                                  for i in range(tile * posx + 5 * tile // 6 - 1, tile * posx - 1, -1)]
                    enemy_way3 += [(i, tile * posy + (5 * tile // 6))
                                  for i in range(tile * posx + 5 * (tile // 6) - 1, tile * posx - 1, -1)]
                elif drctn == 'r':
                    enemy_way1 += [(i, tile * posy + (5 * tile // 6))
                                  for i in range(tile * posx + (tile // 6), tile * (posx + 1))]
                    enemy_way2 += [(i, tile * posy + tile // 2)
                                  for i in range(tile * posx + tile // 6, tile * (posx + 1))]
                    enemy_way3 += [(i, tile * posy + (tile // 6))
                                  for i in range(tile * posx + (tile // 6), tile * (posx + 1))]
                elif drctn == 'd':
                    enemy_way1 += [(tile * posx + (tile // 6), i)
                                  for i in range(tile * posy + (tile // 6), tile * (posy + 1))]
                    enemy_way2 += [(tile * posx + tile // 2, i)
                                  for i in range(tile * posy + tile // 6, tile * (posy + 1))]
                    enemy_way3 += [(tile * posx + (5 * tile // 6), i)
                                  for i in range(tile * posy + (tile // 6), tile * (posy + 1))]
                elif drctn == 'u':
                    enemy_way1 += [(tile * posx + (5 * tile // 6), i)
                                  for i in range(tile * posy + 5 * (tile // 6) - 1, tile * posy - 1, -1)]
                    enemy_way2 += [(tile * posx + tile // 2, i)
                                  for i in range(tile * posy + 5 * tile // 6 - 1, tile * posy - 1, -1)]
                    enemy_way3 += [(tile * posx + (tile // 6), i)
                                  for i in range(tile * posy + 5 * (tile // 6) - 1, tile * posy - 1, -1)]
            elif s in ['U', 'D', 'L', 'R']:
                if drctn == 'l':
                    enemy_way1 += [(i + tile // 6, tile * posy + (tile // 6))
                                  for i in range(tile * posx + 5 * (tile // 6) - 1, tile * posx - 1, -1)]
                    enemy_way2 += [(i + tile // 6, tile * posy + tile // 2)
                                  for i in range(tile * posx + 5 * tile // 6 - 1, tile * posx - 1, -1)]
                    enemy_way3 += [(i + tile // 6, tile * posy + (5 * tile // 6))
                                  for i in range(tile * posx + 5 * (tile // 6) - 1, tile * posx - 1, -1)]
                elif drctn == 'r':
                    enemy_way1 += [(i - tile // 6, tile * posy + (5 * tile // 6))
                                  for i in range(tile * posx + (tile // 6), tile * (posx + 1))]
                    enemy_way2 += [(i - tile // 6, tile * posy + tile // 2)
                                  for i in range(tile * posx + tile // 6, tile * (posx + 1))]
                    enemy_way3 += [(i - tile // 6, tile * posy + (tile // 6))
                                  for i in range(tile * posx + (tile // 6), tile * (posx + 1))]
                elif drctn == 'd':
                    enemy_way1 += [(tile * posx + (tile // 6), i - tile // 6)
                                  for i in range(tile * posy + (tile // 6), tile * (posy + 1))]
                    enemy_way2 += [(tile * posx + tile // 2, i - tile // 6)
                                  for i in range(tile * posy + tile // 6, tile * (posy + 1))]
                    enemy_way3 += [(tile * posx + (5 * tile // 6), i - tile // 6)
                                  for i in range(tile * posy + (tile // 6), tile * (posy + 1))]
                elif drctn == 'u':
                    enemy_way1 += [(tile * posx + (5 * tile // 6), i + tile // 6)
                                  for i in range(tile * posy + 5 * (tile // 6) - 1, tile * posy - 1, -1)]
                    enemy_way2 += [(tile * posx + tile // 2, i + tile // 6)
                                  for i in range(tile * posy + 5 * tile // 6 - 1, tile * posy - 1, -1)]
                    enemy_way3 += [(tile * posx + (tile // 6), i + tile // 6)
                                  for i in range(tile * posy + 5 * (tile // 6) - 1, tile * posy - 1, -1)]
                break
            if drctn == 'l':
                posx -= 1
            elif drctn == 'r':
                posx += 1
            elif drctn == 'd':
                posy += 1
            elif drctn == 'u':
                posy -= 1
        return level_map

    class Paus(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(magaz_sprites, all_sprites)
            self.image = image_list['paus']
            self.rect = self.image.get_rect().move(1840, 8)
            self.x = 1840
            self.y = 8

    class Zvezda(pygame.sprite.Sprite):
        def __init__(self, n, x, y):
            super().__init__(paus_sprites)
            if n:
                self.image = image_list['zvezda1']
            else:
                self.image = image_list['zvezda2']
            self.rect = self.image.get_rect().move(x, y)

    class Nadpis(pygame.sprite.Sprite):
        def __init__(self, n):
            super().__init__(paus_sprites)
            if n:
                self.image = image_list['nadpis1']
            else:
                self.image = image_list['nadpis2']
            self.rect = self.image.get_rect().move(0, 0)

    class Pausa(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(paus_sprites)
            self.image = pygame.Surface((2000, 2000), pygame.SRCALPHA)
            self.image.fill((50, 50, 50, 200))
            self.rect = self.image.get_rect().move(0, 0)

    class Prodoljit(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(paus_sprites)
            self.image = image_list['prodoljit']
            self.rect = self.image.get_rect().move(696, 150)
            self.x = 1840
            self.y = 8

    class Restart(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(paus_sprites)
            self.image = image_list['restart']
            self.rect = self.image.get_rect().move(696, 450)
            self.x = 1840
            self.y = 8

    class Menu(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(paus_sprites)
            self.image = image_list['menu']
            self.rect = self.image.get_rect().move(696, 750)
            self.x = 1840
            self.y = 8

    class Menu1(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(paus_sprites)
            self.image = image_list['menu']
            self.rect = self.image.get_rect().move(696, 800)
            self.x = 1840
            self.y = 8

    class Speed(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(magaz_sprites, all_sprites)
            self.image = image_list['speed'][0]
            self.rect = self.image.get_rect().move(1700, 8)
            self.x = 1700
            self.y = 8

        def speed(self):
            nonlocal speed
            if speed == 1:
                speed = 2
                self.image = image_list['speed'][1]
                self.rect = self.image.get_rect().move(1700, 8)
            else:
                self.image = image_list['speed'][0]
                self.rect = self.image.get_rect().move(1700, 8)
                speed = 1

    class Magaz(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(magaz_sprites, all_sprites)
            self.image = image_list['magaz']
            self.rect = self.image.get_rect().move(1540, 0)
            self.x = 1540
            self.y = 0

    class Knopka(pygame.sprite.Sprite):
        def __init__(self, x, y, name):
            super().__init__(magaz_sprites, all_sprites, knopki_sprites)
            self.image = image_list['knopka'][name][0]
            self.rect = self.image.get_rect().move(x, y)
            self.x = x
            self.y = y
            self.name = name
            self.mask = pygame.mask.from_surface(self.image)

        def update(self):
            self.image = image_list['knopka'][self.name][0]
            self.rect = self.image.get_rect().move(self.x, self.y)

        def new(self):
            self.image = image_list['knopka'][self.name][1]
            self.rect = self.image.get_rect().move(self.x, self.y)
            return self.name

    class LuchnikImage(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__(magaz_sprites, all_sprites)
            self.image = image_list['luchnik'][0]
            self.rect = self.image.get_rect().move(x, y)
            self.x = x
            self.y = y

    class MassImage(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__(magaz_sprites, all_sprites)
            self.image = image_list['mass'][0]
            self.rect = self.image.get_rect().move(x, y)
            self.x = x
            self.y = y

    class SilaImage(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__(magaz_sprites, all_sprites)
            self.image = image_list['sila'][0]
            self.rect = self.image.get_rect().move(x, y)
            self.x = x
            self.y = y

    class DalImage(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__(magaz_sprites, all_sprites)
            self.image = image_list['dal'][0]
            self.rect = self.image.get_rect().move(x, y)
            self.x = x
            self.y = y

    class ZamImage(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__(magaz_sprites, all_sprites)
            self.image = image_list['zam'][0]
            self.rect = self.image.get_rect().move(x, y)
            self.x = x
            self.y = y

    class Luchnik(pygame.sprite.Sprite):
        def __init__(self, x, y):
            nonlocal coin
            super().__init__(tower_sprites, all_sprites)
            self.coin = [60, 80, 120]
            self.sales = [30, 70, 130]
            coin -= 60
            self.lv = 1
            self.image = image_list['luchnik'][0]
            self.rect = self.image.get_rect().move(tile * x + sd_x, tile * y + sd_y)
            self.x = x
            self.y = y
            self.rad = Rad(x, y, int(2 * tile))
            self.reload = 500
            self.n_reload = 500
            self.last_shoot = 0
            self.damage = [7, 16, 29]

        def info(self):
            nonlocal inform
            self.rad.new()
            Info('sale', self.x, self.y, self.lv, 'luchnik')
            Info('buy', self.x, self.y, self.lv, 'luchnik')
            Info('info', self.x, self.y, self.lv, 'luchnik')
            inform = True

        def lvup(self):
            nonlocal coin
            if coin >= self.coin[self.lv]:
                self.lv += 1
                coin -= self.coin[self.lv - 1]
                self.image = image_list['luchnik'][self.lv - 1]
                self.rect = self.image.get_rect().move(tile * self.x + sd_x, tile * self.y + sd_y)

        def sale(self):
            nonlocal coin
            coin += self.sales[self.lv - 1]
            level[self.y][self.x] = None
            self.kill()

        def shoot(self, targets):
            bullet = Bullet(targets[0], self.x * tile + tile // 2 + sd_x,
                            self.y * tile + tile // 2 + sd_y, 7, self.damage[self.lv - 1])
            bullet_sprites.add(bullet)
            self.last_shoot = pygame.time.get_ticks()

    class Mass(pygame.sprite.Sprite):
        def __init__(self, x, y):
            nonlocal coin
            super().__init__(tower_sprites, all_sprites)
            self.coin = [60, 80, 120]
            self.sales = [30, 70, 130]
            self.lv = 1
            coin -= 60
            self.image = image_list['mass'][0]
            self.rect = self.image.get_rect().move(tile * x + sd_x, tile * y + sd_y)
            self.x = x
            self.y = y
            self.rad = Rad(x, y, int(1.5 * tile))
            self.rad = Rad(x, y, int(1.5 * tile))
            self.last_shoot = 0
            self.n_reload = 800
            self.reload = 800
            self.damage = [4, 9, 17]

        def info(self):
            nonlocal inform
            self.rad.new()
            Info('sale', self.x, self.y, self.lv, 'mass')
            Info('buy', self.x, self.y, self.lv, 'mass')
            Info('info', self.x, self.y, self.lv, 'mass')
            inform = True

        def lvup(self):
            nonlocal coin
            if coin >= self.coin[self.lv]:
                self.lv += 1
                coin -= self.coin[self.lv - 1]
                self.image = image_list['mass'][self.lv - 1]
                self.rect = self.image.get_rect().move(tile * self.x + sd_x, tile * self.y + sd_y)

        def sale(self):
            nonlocal coin
            coin += self.sales[self.lv - 1]
            level[self.y][self.x] = None
            self.kill()

        def shoot(self, targets):
            for i in targets:
                bullet = Bullet(i, self.x * tile + tile // 2 + sd_x,
                                self.y * tile + tile // 2 + sd_y, 5, self.damage[self.lv - 1])
                bullet_sprites.add(bullet)
            self.last_shoot = pygame.time.get_ticks()

    class Sila(pygame.sprite.Sprite):
        def __init__(self, x, y):
            self.lv = 1
            nonlocal coin
            super().__init__(tower_sprites, all_sprites)
            self.coin = [250, 320, 400]
            self.sales = [120, 280, 480]
            coin -= 250
            self.image = image_list['sila'][0]
            self.rect = self.image.get_rect().move(tile * x + sd_x, tile * y + sd_y)
            self.x = x
            self.y = y
            self.rad = Rad(x, y, int(1.5 * tile))
            self.reload = 800
            self.n_reload = 800
            self.last_shoot = 0
            self.damage = [70, 160, 270]

        def info(self):
            nonlocal inform
            self.rad.new()
            Info('sale', self.x, self.y, self.lv, 'sila')
            Info('buy', self.x, self.y, self.lv, 'sila')
            Info('info', self.x, self.y, self.lv, 'sila')
            inform = True

        def lvup(self):
            nonlocal coin
            if coin >= self.coin[self.lv]:
                self.lv += 1
                coin -= self.coin[self.lv - 1]
                self.image = image_list['sila'][self.lv - 1]
                self.rect = self.image.get_rect().move(tile * self.x + sd_x, tile * self.y + sd_y)

        def sale(self):
            nonlocal coin
            coin += self.sales[self.lv - 1]
            level[self.y][self.x] = None
            self.kill()

        def shoot(self, targets):
            bullet = Bullet(targets[0], self.x * tile + tile // 2 + sd_x,
                            self.y * tile + tile // 2 + sd_y, 5, self.damage[self.lv - 1])
            bullet_sprites.add(bullet)
            self.last_shoot = pygame.time.get_ticks()

    class Dal(pygame.sprite.Sprite):
        def __init__(self, x, y):
            nonlocal coin
            super().__init__(tower_sprites, all_sprites)
            self.coin = [180, 200, 250]
            self.sales = [90, 190, 310]
            self.lv = 1
            coin -= 180
            self.image = image_list['dal'][0]
            self.rect = self.image.get_rect().move(tile * x + sd_x, tile * y + sd_y)
            self.x = x
            self.y = y
            self.rad = Rad(x, y, int(10 * tile))
            self.reload = 6000
            self.n_reload = 6000
            self.last_shoot = 0
            self.damage = [170, 360, 600]

        def info(self):
            nonlocal inform
            self.rad.new()
            Info('sale', self.x, self.y, self.lv, 'dal')
            Info('buy', self.x, self.y, self.lv, 'dal')
            Info('info', self.x, self.y, self.lv, 'dal')
            inform = True

        def lvup(self):
            nonlocal coin
            if coin >= self.coin[self.lv]:
                self.lv += 1
                coin -= self.coin[self.lv - 1]
                self.image = image_list['dal'][self.lv - 1]
                self.rect = self.image.get_rect().move(tile * self.x + sd_x, tile * self.y + sd_y)

        def sale(self):
            nonlocal coin
            coin += self.sales[self.lv - 1]
            level[self.y][self.x] = None
            self.kill()

        def shoot(self, targets):
            print(0)
            bullet = Bullet(targets[0], self.x * tile + tile // 2 + sd_x,
                            self.y * tile + tile // 2 + sd_y, 10, self.damage[self.lv - 1])
            bullet_sprites.add(bullet)
            self.last_shoot = pygame.time.get_ticks()

    class Zam(pygame.sprite.Sprite):
        def __init__(self, x, y):
            nonlocal coin
            super().__init__(tower_sprites, all_sprites)
            self.reload = 0
            self.last_shoot = 0
            self.coin = [90, 120, 150]
            self.sales = [40, 100, 180]
            coin -= 90
            self.lv = 1
            self.image = image_list['zam'][0]
            self.rect = self.image.get_rect().move(tile * x + sd_x, tile * y + sd_y)
            self.x = x
            self.y = y
            self.rad = Rad(x, y, int(1.5 * tile))
            self.rad_zam = Rad_zam(x, y, int(1.5 * tile))
            self.rad_zam.new()
            self.zam_k = [0.6, 0.54, 0.48]

        def shoot(self, targets):
            for i in targets:
                i.speed *= self.zam_k[self.lv - 1]

        def info(self):
            nonlocal inform
            self.rad.new()
            Info('sale', self.x, self.y, self.lv, 'zam')
            Info('buy', self.x, self.y, self.lv, 'zam')
            Info('info', self.x, self.y, self.lv, 'zam')
            inform = True

        def lvup(self):
            nonlocal coin
            if coin >= self.coin[self.lv]:
                self.lv += 1
                coin -= self.coin[self.lv - 1]
                self.image = image_list['zam'][self.lv - 1]
                self.rect = self.image.get_rect().move(tile * self.x + sd_x, tile * self.y + sd_y)

        def sale(self):
            nonlocal coin
            self.rad_zam.kill()
            coin += self.sales[self.lv - 1]
            level[self.y][self.x] = None
            self.kill()

    class Stena(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__(okr_sprites, all_sprites)
            self.image = choice(image_list['stena'])
            self.rect = self.image.get_rect().move(tile * x + sd_x, tile * y + sd_y)
            self.x = x
            self.y = y

        def info(self):
            pass

    class Doroga(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__(okr_sprites, all_sprites)
            self.image = image_list['doroga']
            self.rect = self.image.get_rect().move(tile * x + sd_x, tile * y + sd_y)
            self.x = x
            self.y = y

        def info(self):
            pass

    class Rad(pygame.sprite.Sprite):
        def __init__(self, x, y, rad):
            super().__init__(all_sprites)
            self.x = x
            self.y = y
            self.rad = rad
            self.image = pygame.Surface((2 * rad, 2 * rad), pygame.SRCALPHA, 32)
            pygame.draw.circle(self.image, pygame.Color(128, 128, 128, 20), (rad, rad), rad)
            self.rect = self.image.get_rect().move(int(tile * (x + 0.5)) - rad + sd_x,
                                                   int(tile * (y + 0.5)) - rad + sd_y)

        def new(self):
            nonlocal rad_sprite
            rad_sprite.add(self)

    class Rad_zam(pygame.sprite.Sprite):
        def __init__(self, x, y, rad):
            super().__init__(rad_zam_sprites, all_sprites)
            self.x = x
            self.y = y
            self.rad = rad
            self.image = pygame.Surface((2 * rad, 2 * rad), pygame.SRCALPHA, 32)
            pygame.draw.circle(self.image, pygame.Color(0, 191, 255, 0), (rad, rad), rad)
            self.rect = self.image.get_rect().move(int(tile * (x + 0.5)) - rad + sd_x,
                                                   int(tile * (y + 0.5)) - rad + sd_y)

        def new(self):
            self.image = pygame.Surface((2 * self.rad, 2 * self.rad), pygame.SRCALPHA, 32)
            pygame.draw.circle(self.image, pygame.Color(0, 191, 255, 50), (self.rad, self.rad), self.rad)
            self.rect = self.image.get_rect().move(int(tile * (self.x + 0.5)) - self.rad + sd_x,
                                                   int(tile * (self.y + 0.5)) - self.rad + sd_y)

    class Fon(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(fon_sprites, all_sprites)
            self.image = load_image('fon.png')
            self.rect = self.image.get_rect().move(0, 0)

    class Info(pygame.sprite.Sprite):
        def __init__(self, name, x, y, lv, tower):
            super().__init__(info_sprites, all_sprites)
            self.lv = lv
            lv = lv - 1
            self.name = name
            self.x = x
            self.y = y
            if self.name == 'buy':
                self.image = image_list['buy'][tower][lv]
                if y < 5:
                    self.rect = self.image.get_rect().move(x * tile + sd_x - 30, y * tile + sd_y + 150)
                else:
                    self.rect = self.image.get_rect().move(x * tile + sd_x - 30, y * tile + sd_y - 125)
            elif self.name == 'sale':
                self.image = image_list['sale'][tower][lv]
                if y < 5:
                    self.rect = self.image.get_rect().move(x * tile + sd_x + 55, y * tile + sd_y + 150)
                else:
                    self.rect = self.image.get_rect().move(x * tile + sd_x + 55, y * tile + sd_y - 125)
            else:
                self.image = image_list['info'][tower][lv]
                if y < 5:
                    self.rect = self.image.get_rect().move(x * tile + sd_x - 50, y * tile + sd_y + 110)
                else:
                    self.rect = self.image.get_rect().move(x * tile + sd_x - 50, y * tile + sd_y - 40)

        def update(self):
            if pygame.sprite.spritecollideany(self, mouse_sprites):
                if self.name == 'buy' and self.lv != 3:
                    level[self.y][self.x].lvup()
                elif self.name == 'sale':
                    level[self.y][self.x].sale()

    class Mouse(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__(mouse_sprites)
            self.x = x
            self.y = y
            self.image = pygame.Surface((1, 1), pygame.SRCALPHA, 32)
            pygame.draw.circle(self.image, pygame.Color(128, 128, 128, 0), (1, 1), 1)
            self.rect = self.image.get_rect().move(x, y)

    class Spawn(pygame.sprite.Sprite):
        def __init__(self, x, y, type=None):
            super().__init__(all_sprites, okr_sprites)
            self.image = load_image(f'vuhod{type}.png')
            self.rect = self.image.get_rect().move(tile * x + sd_x, tile * y + sd_y)
            self.x = x
            self.y = y
            self.enemy = 20
            self.t = False
            self.wave_health = 0

        def update(self):
            nonlocal wave, wave_type, spawn_event, boss_hp
            if len(enemy_sprites) == 0 and self.enemy == 20:
                self.wave_health += int((1 + wave / 10) * enemy_hp)
                number = ['1', '2', '3']
                del number[int(wave_type) - 1]
                wave_type = choice(number)
                if self.t:
                    wave += 1
                else:
                    self.t = True
                if wave > wave_const:
                    win(hp)
                spawn_event = 5000
                self.enemy = 0
            elif wave == wave_const and self.enemy < 20:
                enemy = Enemy(boss_hp, 1, 4)
                all_sprites.add(enemy)
                enemy_sprites.add(enemy)
                self.enemy = 20
            elif self.enemy < 20:
                enemy = Enemy(self.wave_health, 1, wave_type)
                all_sprites.add(enemy)
                enemy_sprites.add(enemy)
                self.enemy += 1
                spawn_event = 500
            else:
                spawn_event = 100


        def info(self):
            pass

    class End(pygame.sprite.Sprite):
        def __init__(self, x, y, type=None):
            super().__init__(all_sprites, okr_sprites)
            self.image = load_image(f'vhod{type}.png')
            self.rect = self.image.get_rect().move(tile * x + sd_x, tile * y + sd_y)
            self.x = x
            self.y = y

        def info(self):
            pass

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, target, x, y, s, d):
            super().__init__(bullet_sprites, all_sprites)
            self.speed = s
            self.damage = d
            self.x, self.y = x, y
            self.target = target
            self.image = load_image('bullet.png', colorkey=(255, 255, 255))
            self.rect = self.image.get_rect().move(self.x, self.y)

        def update(self):
            nonlocal speed
            if self.target.alive():
                x_r = self.target.x - self.x
                y_r = self.target.y - self.y
                L = ((x_r) ** 2 + (y_r) ** 2) ** 0.5
                if L:
                    self.x += int(self.speed * speed * x_r / L)
                    self.y += int(self.speed * speed * y_r / L)
                    self.rect = self.image.get_rect().move(self.x, self.y)
            else:
                self.kill()

        def popadanie(self):
            self.target.ect_probitie(self.damage)
            self.kill()

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, h, s, t):
            nonlocal enemy_way_last, enemy_way1, enemy_way2, enemy_way3
            super().__init__(enemy_sprites, all_sprites)
            number = [1, 2, 3]
            del number[enemy_way_last - 1]
            if t == 4:
                self.enemy_way = enemy_way2
            else:
                number = choice(number)
                enemy_way_last = number
                if number == 1:
                    self.enemy_way = enemy_way1
                elif number == 2:
                    self.enemy_way = enemy_way2
                else:
                    self.enemy_way = enemy_way3
            self.coord = 0
            self.max_health = h
            self.health = h
            self.speed = s
            self.n_speed = s
            self.x, self.y = self.enemy_way[0][0] + sd_x, self.enemy_way[0][1] + sd_y
            if t != 4:
                self.size = 25
            else:
                self.size = 40
            self.type = t
            if self.type == '2':
                self.speed *= 1.5
                self.n_speed *= 1.5
                self.max_health //= 1.5
                self.health //= 1.5
            elif self.type == '3':
                self.speed *= 0.75
                self.n_speed *= 0.75
                self.max_health *= 1.5
                self.health *= 1.5
            self.image = load_image(f'enemy{t}.png')
            self.image.set_colorkey((255, 255, 255))
            self.rect = self.image.get_rect().move(self.x - self.size // 2, self.y - self.size // 2)
            self.last = pygame.time.get_ticks()

        def update(self):
            nonlocal speed
            ticks = pygame.time.get_ticks()
            self.coord += self.speed * speed * (ticks - self.last) / 8
            self.last = ticks
            if self.coord >= len(self.enemy_way):
                self.kill()
                if self.type != 4:
                    lose_hp()
                else:
                    lose_hp(5)
            else:
                self.x, self.y = self.enemy_way[int(self.coord)][0] + sd_x, self.enemy_way[int(self.coord)][1] + sd_y
                new_size = self.size * (0.6 * self.health / self.max_health + 0.4)
                self.image = pygame.transform.scale(load_image(f'enemy{self.type}.png').convert(), (new_size, new_size))
                self.rect = self.image.get_rect().move(self.x - new_size // 2, self.y - new_size // 2)
                self.speed = self.n_speed
                self.image.set_colorkey((255, 255, 255))


        def ect_probitie(self, damage):
            nonlocal coin
            self.health -= damage
            if self.health <= 0:
                coin += int(3 + wave)
                self.kill()


    image_list = {'luchnik': [load_image('luchnik1.png'), load_image('luchnik2.png'), load_image('luchnik3.png')],
                  'mass': [load_image('mass1.png'), load_image('mass2.png'), load_image('mass3.png')],
                  'sila': [load_image('sila1.png'), load_image('sila2.png'), load_image('sila3.png')],
                  'dal': [load_image('dal1.png'), load_image('dal2.png'), load_image('dal3.png')],
                  'zam': [load_image('zam1.png'), load_image('zam2.png'), load_image('zam3.png')],
                  'stena': [load_image('stena1.png'), load_image('stena2.png'), load_image('stena3.png'),
                            load_image('stena4.png'), load_image('stena5.png'), load_image('stena6.png'),
                            load_image('stena7.png'), load_image('stena8.png'), load_image('stena9.png')],
                  'doroga': load_image('doroga.png'), 'magaz': load_image('magaz.png'),
                  'knopka': {'luchnik': [load_image('knopkaluchnik1.png'), load_image('knopkaluchnik2.png')],
                             'mass': [load_image('knopkaluchnik1.png'), load_image('knopkaluchnik2.png')],
                             'sila': [load_image('knopkasila1.png'), load_image('knopkasila2.png')],
                             'dal': [load_image('knopkadal1.png'), load_image('knopkadal2.png')],
                             'zam': [load_image('knopkazam1.png'), load_image('knopkazam2.png')]},
                  'buy': {
                      'luchnik': [load_image('buyluchnik1.png'), load_image('buyluchnik2.png'), load_image('buy3.png')],
                      'mass': [load_image('buymass1.png'), load_image('buymass2.png'), load_image('buy3.png')],
                      'sila': [load_image('buysila1.png'), load_image('buysila2.png'), load_image('buy3.png')],
                      'dal': [load_image('buydal1.png'), load_image('buydal2.png'), load_image('buy3.png')],
                      'zam': [load_image('buyzam1.png'), load_image('buyzam2.png'), load_image('buy3.png')]},
                  'sale': {'luchnik': [load_image('saleluchnik1.png'), load_image('saleluchnik2.png'),
                                       load_image('saleluchnik3.png')],
                           'mass': [load_image('salemass1.png'), load_image('salemass2.png'),
                                    load_image('salemass3.png')],
                           'sila': [load_image('salesila1.png'), load_image('salesila2.png'),
                                    load_image('salesila3.png')],
                           'dal': [load_image('saledal1.png'), load_image('saledal2.png'), load_image('saledal3.png')],
                           'zam': [load_image('salezam1.png'), load_image('salezam2.png'), load_image('salezam3.png')]},
                  'info': {'luchnik': [load_image('infoluchnik1.png'), load_image('infoluchnik2.png'),
                                       load_image('infoluchnik3.png')],
                           'mass': [load_image('infomass1.png'), load_image('infomass2.png'),
                                    load_image('infomass3.png')],
                           'sila': [load_image('infosila1.png'), load_image('infosila2.png'),
                                    load_image('infosila3.png')],
                           'dal': [load_image('infodal1.png'), load_image('infodal2.png'), load_image('infodal3.png')],
                           'zam': [load_image('infozam1.png'), load_image('infozam2.png'), load_image('infozam3.png')]},
                  'paus': load_image('paus.png'), 'speed': [load_image('speed1.png'), load_image('speed2.png')],
                  'menu': load_image('menu.png'), 'prodoljit': load_image('prodoljit.png'),
                  'restart': load_image('restart.png'),
                  'zvezda1': load_image('zvezda.png'), 'zvezda2': load_image('zvezda2.png'),
                  'nadpis1': load_image('nadpis1.png'), 'nadpis2': load_image('nadpis2.png'),
                  'heart': load_image('heart.png'), 'coin': load_image('coin.png')}

    inform = False
    all_sprites = pygame.sprite.Group()
    tower_sprites = pygame.sprite.Group()
    okr_sprites = pygame.sprite.Group()
    magaz_sprites = pygame.sprite.Group()
    knopki_sprites = pygame.sprite.Group()
    rad_zam_sprites = pygame.sprite.Group()
    rad_sprite = pygame.sprite.Group()
    fon_sprites = pygame.sprite.Group()
    info_sprites = pygame.sprite.Group()
    mouse_sprites = pygame.sprite.Group()
    paus_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    spawn_event = 0
    coin = 200
    knopki_list = []
    tile = 100
    sd_x = 20
    sd_y = 20

    Fon()
    running = True
    clock = pygame.time.Clock()
    level = generate_level(load_level('levels.txt', number))
    magaz()
    t = 0
    p = False
    speed = 1
    font = pygame.font.Font(None, 50)
    wins = False
    wave = 1
    wave_type = 3
    while running:
        spawn_event -= clock.tick() * speed
        if not (p) and len(tower_sprites) != 0:
            p = True
        if spawn_event <= 0 and p:
            spawn_sprite.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and wins:
                x, y = event.pos
                if x > 696 and x < 1224 and y > 800 and y < 956:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and speed == 0:
                x, y = event.pos
                if x > 696 and x < 1224 and y > 150 and y < 306:
                    paus_sprites = pygame.sprite.Group()
                    speed = speed1
                elif x > 696 and x < 1224 and y > 450 and y < 606:
                    running = False
                    game(screen, number)
                elif x > 696 and x < 1224 and y > 750 and y < 906:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                rad_sprite = pygame.sprite.Group()
                x, y = event.pos
                Mouse(x, y)
                if inform:
                    inform = False
                    info_sprites.update()
                    info_sprites = pygame.sprite.Group()
                elif x > 20 and x < 1520 and y > 20 and y < 1020:
                    x, y = (x - 20) // 100, (y - 20) // 100
                    if level[y][x] == None and t != 0:
                        if t == 'luchnik' and coin >= 60:
                            level[y][x] = Luchnik(x, y)
                        elif t == 'mass' and coin >= 60:
                            level[y][x] = Mass(x, y)
                        elif t == 'dal' and coin >= 180:
                            level[y][x] = Dal(x, y)
                        elif t == 'sila' and coin >= 250:
                            level[y][x] = Sila(x, y)
                        elif t == 'zam' and coin >= 90:
                            level[y][x] = Zam(x, y)
                    elif level[y][x] != None and t == 0:
                        level[y][x].info()
                elif x > 1560 and x < 1900 and y > 65 and y < 215:
                    knopki_sprites.update()
                    if t != 'mass':
                        t = knopki_list[0].new()
                    else:
                        t = 0
                elif x > 1560 and x < 1900 and y > 260 and y < 410:
                    knopki_sprites.update()
                    if t != 'luchnik':
                        t = knopki_list[1].new()
                    else:
                        t = 0
                elif x > 1560 and x < 1900 and y > 455 and y < 605:
                    knopki_sprites.update()
                    if t != 'zam':
                        t = knopki_list[2].new()
                    else:
                        t = 0
                elif x > 1560 and x < 1900 and y > 650 and y < 800:
                    knopki_sprites.update()
                    if t != 'dal':
                        t = knopki_list[3].new()
                    else:
                        t = 0
                elif x > 1560 and x < 1900 and y > 845 and y < 995:
                    knopki_sprites.update()
                    if t != 'sila':
                        t = knopki_list[4].new()
                    else:
                        t = 0
                elif x > 1830 and x < 1900 and y > 0 and y < 65:
                    knopki_sprites.update()
                    Pausa()
                    Prodoljit()
                    Restart()
                    Menu()
                    speed1 = speed
                    speed = 0
                elif x > 1700 and x < 1800 and y > 0 and y < 65:
                    knopki_list[-1].speed()
                mouse_sprites = pygame.sprite.Group()
        hits = pygame.sprite.groupcollide(bullet_sprites, enemy_sprites, False, False)
        for bullet in hits:
            bullet.popadanie()
        for tower in tower_sprites:
            if speed != 0 and pygame.time.get_ticks() > tower.last_shoot + tower.reload // speed:
                pass
                may_be_shooted = pygame.sprite.spritecollide(tower.rad, enemy_sprites, False)
                if len(may_be_shooted) > 0:
                    tower.shoot(may_be_shooted)
        bullet_sprites.update()
        enemy_sprites.update()
        fon_sprites.draw(screen)
        tower_sprites.draw(screen)
        okr_sprites.draw(screen)
        enemy_sprites.draw(screen)
        bullet_sprites.draw(screen)
        rad_zam_sprites.draw(screen)
        rad_sprite.draw(screen)
        info_sprites.draw(screen)
        magaz_sprites.draw(screen)
        string_rendered = font.render(str(int(coin)), True, pygame.Color('white'))
        string_rendered2 = font.render(str(int(hp)), True, pygame.Color('white'))
        string_rendered3 = font.render(str(int(wave if wave < wave_const else wave_const)) + '/' + str(wave_const),
                                       True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect2 = string_rendered2.get_rect()
        intro_rect3 = string_rendered2.get_rect()
        intro_rect.top = 996
        intro_rect.x = 1570
        intro_rect2.top = 996
        intro_rect2.x = 1790
        intro_rect3.top = 20
        intro_rect3.x = 1580
        screen.blit(string_rendered, intro_rect)
        screen.blit(string_rendered2, intro_rect2)
        screen.blit(string_rendered3, intro_rect3)
        paus_sprites.draw(screen)
        pygame.display.flip()