import pygame
import os
import math

import numpy as np

from models.statics import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TRACK_WIDTH,
    TRAF_WIDTH, CAR, MAX_VELOCITY, GREEN, WHITE, FUCSIA
)


class Car(pygame.sprite.Sprite):
    def __init__(self, SCREEN, img=CAR):

        super().__init__()
        self.SCREEN = SCREEN
        self.image_ori = img

        self.image_width = img.get_width()
        self.image_height = img.get_height()

        self.image = img

        self.front_acc_time = 0

        self.x = 100
        self.y = 350
        self.x_velocity = 0
        self.y_velocity = 0
        self.x_accelleration = 0
        self.y_accelleration = 0
        self.body_orientation = 0

        self.pedal_time = 0

        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.left_sensor = [0, 0]
        self.right_sensor = [0, 0]

        self.radars = []

        self.crashed = False

        self.command = [0, 0, 0, 0]
        self.previous_pos = [0, 0]
        self.still = 0

        self.finish_line = False

        self.finish_portion = False

        self.infraction = False
        # self.traf_l_pos = 0

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

    def draw_sensors(self):
        if 90 >= self.body_orientation >= 0:
            self.left_sensor = [self.rect.x + self.image_width * (math.cos(np.radians(self.body_orientation))),
                                self.rect.y]
            self.right_sensor = [self.rect.x + self.image.get_width(),
                                 self.rect.y + self.image_height * math.cos(np.radians(self.body_orientation))]
        elif 360 > self.body_orientation >= 270:
            self.left_sensor = [self.rect.x + self.image.get_width(),
                                self.rect.y + self.image_width * (-1) * math.sin(np.radians(self.body_orientation))]
            self.right_sensor = [self.rect.x + self.image_width * math.cos(np.radians(self.body_orientation)),
                                 self.rect.y + self.image.get_height()]
        elif 180 <= self.body_orientation < 270:
            self.left_sensor = [self.rect.x + self.image_height * (-1) * math.sin(np.radians(self.body_orientation)),
                                self.rect.y + self.image.get_height()]
            self.right_sensor = [self.rect.x,
                                 self.rect.y + self.image_width * (-1) * math.sin(np.radians(self.body_orientation))]
        elif 90 < self.body_orientation < 180:
            self.left_sensor = [self.rect.x,
                                self.rect.y + self.image_height * (-1) * math.cos(np.radians(self.body_orientation))]
            self.right_sensor = [self.rect.x + self.image_height * math.sin(np.radians(self.body_orientation)),
                                 self.rect.y]

        # pygame.draw.line(self.SCREEN, GREEN, self.left_sensor, (500,300))

        # pygame.draw.circle(self.SCREEN, FUCSIA, self.left_sensor, 1)
        # pygame.draw.circle(self.SCREEN, FUCSIA, self.right_sensor, 1)

        # self.know = [self.rect.x, self.rect.y]
        # self.know2 = [self.rect.x + self.image.get_width(), self.rect.y + self.image.get_height()]
        # self.know3 = [self.rect.x + self.image.get_width(), self.rect.y]
        # self.know4 = [self.rect.x, self.rect.y + self.image.get_height()]

    def input_analisys(self):
        self.previous_pos[0] = self.left_sensor[0]
        self.previous_pos[1] = self.left_sensor[1]

        if self.command[0] == 1:  # w
            self.pedal_time += 2
            if self.pedal_time > 90:
                self.pedal_time = 90

            self.x_velocity = self.accelleration(self.pedal_time) * np.cos(np.radians(self.body_orientation))
            self.y_velocity = self.accelleration(self.pedal_time) * np.sin(np.radians(self.body_orientation))

        elif self.command[3] == 1:
            self.pedal_time -= 4
            if self.pedal_time < 0:
                self.pedal_time = 0

            self.x_velocity = self.accelleration(self.pedal_time) * np.cos(np.radians(self.body_orientation))
            self.y_velocity = self.accelleration(self.pedal_time) * np.sin(np.radians(self.body_orientation))

        else:
            self.pedal_time -= 1
            if self.pedal_time < 0:
                self.pedal_time = 0

            self.x_velocity = self.accelleration(self.pedal_time) * np.cos(np.radians(self.body_orientation))
            self.y_velocity = self.accelleration(self.pedal_time) * np.sin(np.radians(self.body_orientation))

        if self.command[1] == 1 and ((self.x_velocity ** 2 + self.y_velocity ** 2) ** 0.5) > 1.5:  # a
            if abs((self.x_velocity ** 2 + self.y_velocity ** 2) ** 0.5 <= 5):
                self.body_orientation += 5
            elif (abs(self.x_velocity ** 2 + self.y_velocity ** 2) ** 0.5 <= 20 and abs(
                    self.x_velocity ** 2 + self.y_velocity ** 2) ** 0.5 > 5):
                self.body_orientation += 5

        if self.command[2] == 1 and ((self.x_velocity ** 2 + self.y_velocity ** 2) ** 0.5) > 1.5:  # a
            if abs((self.x_velocity ** 2 + self.y_velocity ** 2) ** 0.5 <= 5):
                self.body_orientation -= 5
            elif (abs(self.x_velocity ** 2 + self.y_velocity ** 2) ** 0.5 <= 20 and abs(
                    self.x_velocity ** 2 + self.y_velocity ** 2) ** 0.5 > 5):
                self.body_orientation -= 5

        if self.body_orientation >= 360:
            self.body_orientation = 0
        if self.body_orientation < 0:
            self.body_orientation += 360

    def move(self):

        if not self.finish_portion:
            self.x_velocity += self.x_accelleration / 30
            self.y_velocity += self.y_accelleration / 30
            if self.x_velocity > 30:
                self.x_velocity = 30
                if self.y_velocity > 30:
                    self.y_velocity = 30

            self.rect.x += self.x_velocity
            self.rect.y -= self.y_velocity

        if self.finish_portion:
            self.x_velocity = 0
            self.y_velocity = 0

    def shift(self):
        self.rect.x -= 1000

    def accelleration(self, time):

        velocity = MAX_VELOCITY * time / 40
        if velocity > MAX_VELOCITY:
            velocity = MAX_VELOCITY
        return velocity

    def rot_center(self):
        self.image = pygame.transform.rotate(self.image_ori, self.body_orientation)
        self.rect = self.image.get_rect(center=self.rect.center)

    def radar(self, radar_angle):
        length = 10
        x = int(self.rect.center[0])
        y = int(self.rect.center[1])
        # print(x,y)
        while not self.SCREEN.get_at((x, y)) == GREEN and length < 250:
            # print(x,y)
            length += 1
            x = int(self.rect.center[0] + math.cos(math.radians(self.body_orientation + radar_angle)) * length)
            if x < 50:
                x = 50
            y = int(self.rect.center[1] - math.sin(math.radians(self.body_orientation + radar_angle)) * length)
            if y < 5:
                y = 5
            if y > SCREEN_HEIGHT - 5:
                y = SCREEN_HEIGHT - 5
        # Draw Radar
        pygame.draw.line(self.SCREEN, WHITE, self.rect.center, (x, y), 1)
        pygame.draw.circle(self.SCREEN, (0, 255, 0, 0), (x, y), 2)

        dist = int(math.sqrt(math.pow(self.rect.center[0] - x, 2)
                             + math.pow(self.rect.center[1] - y, 2)))

        self.radars.append([radar_angle, dist])

    def detect_collision(self):
        x_l = int(self.left_sensor[0])
        y_l = int(self.left_sensor[1])
        x_r = int(self.right_sensor[0])
        y_r = int(self.right_sensor[1])
        # print(x_r,x_l)
        if (x_l < 50 or x_l < 50 or y_l < 10 or y_r < 10 or y_l > (SCREEN_HEIGHT - 15) or y_r > (
                SCREEN_HEIGHT - 15) or self.SCREEN.get_at((x_l, y_l)) == GREEN or self.SCREEN.get_at(
            (x_r, y_r)) == GREEN):

            # print((self.left_sensor[0], self.left_sensor[1]))
            # if (x_l < 50 or x_l < 50 or y_l < 10 or y_r < 10 or y_l > (SCREEN_HEIGHT - 15) or y_r > (
            #         SCREEN_HEIGHT - 15)):
            #     print("BOUNDARIES")
            #

            if (self.SCREEN.get_at((x_l, y_l)) == GREEN or self.SCREEN.get_at(
                    (x_r, y_r)) == GREEN):
                # print("COLLISION")

                return True

        if self.x_velocity == 0 and self.y_velocity == 0:
            self.still += 1
        else:
            self.still = 0
        if self.still >= 30 and self.rect.centerx < 200:
            # print("Too slow")
            return True
        if self.still >= 100 and self.rect.centerx >= 200:
            return True
        return False

    # def detect_finishline(self):
    #     if(self.left_sensor[0] <= 485 and self.left_sensor[0] >= 470 and self.left_sensor[1] >= 600 and self.left_sensor[1] < 900):
    #         return True
    #     else:
    #         return False

    def update(self):

        self.draw_sensors()
        self.input_analisys()
        self.move()
        # self.crashed = self.detect_collision()
        # self.finish_line = self.detect_finishline()
        self.radars.clear()
        angles = [-60, -30, 0, 30, 60]
        for i in range(len(angles)):
            self.radar(angles[i])

    def data(self):
        input = [0, 0, 0, 0, 0, 0]
        for i, radar in enumerate(self.radars):
            input[i] = int(radar[1])
        # if ((self.traf_l_pos - self.left_sensor[0]) < 200) and ((self.traf_l_pos - self.left_sensor[0]) > 0):
        #     input[5] = 1
        # else:

        input[5] = 0
        if input[5] == 1:
            pass
            # pygame.draw.circle(SCREEN, (0, 0, 0, 0), (self.rect.centerx, 50), 3)
        if input[5] == 0:
            pass
            # pygame.draw.circle(SCREEN, (0, 255, 255, 0), (self.rect.centerx, 50), 3)
        return input
