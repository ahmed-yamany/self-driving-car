import pygame
import os

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700

TRACK_WIDTH = 50

TRAF_WIDTH = 15
SPEED = 50

RED = (200, 0, 0)
FUCSIA = (255, 0, 255)
YELLOW = (255, 255, 0)
GRAY = pygame.Color(170, 170, 170)
WHITE = pygame.Color(255, 255, 255, 255)
GREEN = pygame.Color(2, 105, 31, 255)

air_density = 1.225
friction_coef = 1.7
drag_coef = 0.7
lift_coef = -2.0

g = 9.8
MAX_FRONT_ACC = 10
DRAG_SCALING = 0.1
MAX_VELOCITY = 10

SCORES = []

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# FONT = pygame.font.Font('freesansbold.ttf', 20)


CAR = pygame.image.load(
    os.path.join("/Users/ahmedyamany/PycharmProjects/self-driving-car/imgs", "car5.png"))

CAR = pygame.transform.scale(CAR, (54, 37))  # change car size by the distinations
