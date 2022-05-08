import pygame
import random
from models.statics import (
    TRACK_WIDTH, SCREEN_HEIGHT, GREEN, YELLOW, WHITE
)


class Road:
    def __init__(self, SCREEN):
        self.points = [(0, SCREEN_HEIGHT / 2)]  # 0
        self.SCREEN = SCREEN

    def addpoint(self):
        points_length = len(self.points) - 1

        if points_length == 0:
            new_point_y = SCREEN_HEIGHT / 2
        else:
            last_point_y = self.points[points_length][1]
            new_point_y = random.randint(last_point_y - 150, last_point_y + 150)

        if new_point_y > SCREEN_HEIGHT - TRACK_WIDTH - 50:
            new_point_y = SCREEN_HEIGHT - TRACK_WIDTH - 50

        if new_point_y < TRACK_WIDTH + 50:
            new_point_y = TRACK_WIDTH + 50

        if random.randint(0, 20) == 21:
            self.points.append((self.points[points_length][0] + 200, new_point_y))  # 1
        else:
            self.points.append((self.points[points_length][0] + 200, new_point_y))  # 0

    def draw(self, i):
        if i > 0:
            pygame.draw.line(self.SCREEN, YELLOW,
                             (self.points[i - 1][0], self.points[i - 1][1]),
                             (self.points[i][0], self.points[i][1]), TRACK_WIDTH)

            # pygame.draw.line(self.SCREEN, WHITE,
            #                  (self.points[i - 1][0], self.points[i - 1][1] + 5),
            #                  (self.points[i][0], self.points[i][1] + 5), 5)
            #
            # pygame.draw.line(self.SCREEN, WHITE,
            #                  (self.points[i - 1][0], self.points[i - 1][1] - 5),
            #                  (self.points[i][0], self.points[i][1] - 5), 5)

    def shift(self):
        for h in range(5):
            self.points.pop(0)
        for i in range(5):
            self.addpoint()
        for i in range(len(self.points)):
            self.points[i] = (self.points[i][0] - 1000, self.points[i][1])  # , self.points[i][2])
