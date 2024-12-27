import pygame
from menu1 import menu1

pygame.init()
pygame.display.set_caption('TvS')
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
menu1(screen)