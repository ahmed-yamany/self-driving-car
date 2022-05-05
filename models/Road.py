import pygame
import os
import random
from models.statics import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TRACK_WIDTH,
    TRAF_WIDTH, GREEN
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
        # pygame.draw.circle(self.screen, (0, 255, 110, 0), self.points[i], 3)
        if i > 0:
            pygame.draw.line(self.SCREEN, GREEN,
                             (self.points[i - 1][0], self.points[i - 1][1] + TRACK_WIDTH),
                             (self.points[i][0], self.points[i][1] + TRACK_WIDTH), 10)

            pygame.draw.line(self.SCREEN, GREEN,
                             (self.points[i - 1][0], self.points[i - 1][1] - TRACK_WIDTH),
                             (self.points[i][0], self.points[i][1] - TRACK_WIDTH), 10)

        # if (self.points[i][2] == 1):
        #     pygame.draw.line(self.SCREEN, (255, 0, 0, 255), (self.points[i][0], self.points[i][1] + TRAF_WIDTH),
        #                      (self.points[i][0], self.points[i][1] - TRAF_WIDTH), 5)
        #
        # if self.points[i][2] == 2:
        #     pygame.draw.line(self.SCREEN, (0, 255, 0, 255), (self.points[i][0], self.points[i][1] + TRAF_WIDTH),
        #                      (self.points[i][0], self.points[i][1] - TRAF_WIDTH), 5)

    def shift(self):
        for h in range(5):
            self.points.pop(0)
        for i in range(5):
            self.addpoint()
        for i in range(len(self.points)):
            self.points[i] = (self.points[i][0] - 1000, self.points[i][1])  # , self.points[i][2])

    # def change_traf(self, i):
    #     if (self.points[i][2] == 1):
    #         self.points[i] = (self.points[i][0], self.points[i][1], 2)
    #
