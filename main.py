import neat
from models.main_algorithem import fittness_function

if __name__ == '__main__':
    configurations_path = '/Users/ahmedyamany/PycharmProjects/self-driving-car/models/config.txt'

    configurations = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        configurations_path
    )

    Population = neat.Population(configurations)

    Population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    Population.add_reporter(stats)

    winner = Population.run(fittness_function, 300)

    print('\nBest genome:\n{!s}'.format(winner))

