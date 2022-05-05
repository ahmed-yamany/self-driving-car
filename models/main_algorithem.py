import pygame
import pickle
import sys
from models import Road
from models.car import Car
from models.statics import (
    SCREEN, SPEED, SCORES, GRAY
)
import neat

pygame.init()

FONT = pygame.font.Font('freesansbold.ttf', 20)
generation_count = 0


def remove(index):
    cars.pop(index)
    ge.pop(index)
    nets.pop(index)


def eval_genomes(genomes, config):
    clock = pygame.time.Clock()

    fit = 1
    global cars, ge, nets, shifts
    global generation_count

    generation_count += 1

    shifts = 0

    global traf_l_pos
    traf_l_pos = 0

    cars = []
    ge = []
    nets = []
    SCREEN.fill(GRAY)

    trak = Road.Road(SCREEN=SCREEN)

    check = 0
    next_lane = False
    for i in range(15):
        trak.addpoint()

    trak.points[5] = (trak.points[5][0], trak.points[5][1], 1)

    # LOADING SAVED GENOME!
    # file = open("winner.p",'rb')
    # winner_genome = pickle.load(file)
    # file.close()

    for genome_id, genome in genomes:
        car_object = Car(SCREEN=SCREEN)
        car_object.traf_l_pos = 2000

        cars.append(pygame.sprite.GroupSingle(car_object))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    # LOADING SAVED GENOME
    # cars.append(pygame.sprite.GroupSingle(Car(SCREEN)))
    # ge.append(winner_genome[1])
    # net = neat.nn.FeedForwardNetwork.create(winner_genome[1], config)
    # nets.append(net)
    # winner_genome[1].fitness = 0

    def score():
        global shifts
        text = FONT.render(f'Driven sections:  {str(shifts)}', True, (0, 0, 0))
        SCREEN.blit(text, (50, 620))

    def statistics():
        global cars, ge

        text_1 = FONT.render(f'Cars Alive:  {str(len(cars))}', True, (0, 0, 0))
        text_2 = FONT.render(f'Generation:  {generation_count}', True, (0, 0, 0))
        # text_3 = FONT.render(f'Game Speed:  {str(game_speed)}', True, (0, 0, 0))

        SCREEN.blit(text_1, (50, 640))
        SCREEN.blit(text_2, (50, 660))
        # SCREEN.blit(text_3, (50, 510))

    time = 0
    # command = [0,0,0,0]
    run = True
    # command = [0,0,0,0]
    countdown = False
    redlight_time = 0
    while True:
        time += 1
        # print(mycar.x_velocity)
        SCREEN.fill(GRAY)
        # print(traf_l_pos)
        if countdown:
            redlight_time += 1
        if redlight_time > 500:
            countdown = False
            redlight_time = 0
            for i in range(10):
                if trak.points[i][2] == 1:
                    # trak.points[i][2] = 2
                    trak.change_traf(i)
                    # print("GREEN LIGHT!")
                    break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if len(cars) == 1:
            # print(ge[0].fitness)
            with open("Winner.p", "wb") as f:
                pickle.dump(genomes[0], f)
                f.close()

        if len(cars) == 0:
            SCORES.append(shifts)
            # print("fin")
            # print(SCORES)
            break

        for i, car in enumerate(cars):

            if (traf_l_pos - car.sprite.rect.centerx) < 200 and ((traf_l_pos - car.sprite.rect.centerx) > 0):

                ge[i].fitness -= fit * car.sprite.x_velocity * 0.1
                if car.sprite.x_velocity <= 1:
                    # pygame.draw.circle(SCREEN, (255,80,100,100), (car.sprite.rect.centerx, 690), 2)
                    ge[i].fitness += fit
            elif car.sprite.x_velocity > 1:
                ge[i].fitness += fit

            if car.sprite.crashed:
                # ge[i].fitness -= 0.5

                remove(i)

            if car.sprite.rect.x >= 1100:
                car.sprite.finish_portion = True
                # car.sprite.shift()
                # trak.shift()
                # car.sprite.crashed = False

        for i, car in enumerate(cars):
            output = nets[i].activate(car.sprite.data())
            if output[0] > 0.7:
                car.sprite.command[0] = 1
                car.sprite.command[3] = 0
            if output[1] > 0.7:
                car.sprite.command[1] = 1
                car.sprite.command[2] = 0
            if output[0] <= 0.7:
                car.sprite.command[3] = 1
                car.sprite.command[0] = 0
            if output[1] <= 0.4:
                car.sprite.command[2] = 1
                car.sprite.command[1] = 0
            if 0.4 < output[1] <= 0.7:
                car.sprite.command[2] = 0
                car.sprite.command[1] = 0

        check = 0
        for i, car in enumerate(cars):
            if car.sprite.finish_portion:
                check += 1
            else:
                break
            if check == len(cars):
                next_lane = True
                check = 0

        if next_lane:
            next_lane = False
            # print("ole")
            trak.shift()
            for i, car in enumerate(cars):
                car.sprite.shift()
                car.sprite.crashed = False
                car.sprite.finish_portion = False
            shifts += 1

        for i in range(len(trak.points)):
            trak.draw(i)

        for car in cars:
            car.sprite.rot_center()
            car.draw(SCREEN)
            car.update()

        clock.tick(SPEED)
        statistics()
        score()
        pygame.display.update()

        for car in cars:
            car.sprite.crashed = car.sprite.detect_collision()
