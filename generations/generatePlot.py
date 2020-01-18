import random
import math

speeds = {"dog": (3, 6), "cat": (2, 7), "rabbit": (1, 8), "parrot": (5, 10)}
missing_data_probs = {"dog": 0.01, "cat": 0.01, "rabbit": 0.5, "parrot": 0.5}
moving_angles = {"dog": math.pi / 36, "cat": math.pi / 3, "rabbit": math.pi / 2, "parrot": 2 * math.pi}
# model for parrot is: start to fly at random height in parrot_height interval range, than in each phase change height
# according to normal distribution with sigma = parrot_flight_daviation:
parrot_heights_interval = (10, 50)  # range of height within the parrot flights
parrot_flight_deviation = 0.1  # the sigma of the normal distribution which represents the fluctuation of the parrot jumps
jumps_sizes = {"dog": 0.25, "cat": 0.3, "rabbit": 0.2}
jumps_prob = {"dog": 0.06, "cat": 0.06, "rabbit": 0.12}


def generate_rand_vector(size):
    """
    input: size - scalar
    output:
        a randomized vector with length=size
    """
    vec = (0.1 + random.random() * 0.9, 0.1 + random.random() * 0.9)
    rand_size = math.sqrt(vec[0] ** 2 + vec[1] ** 2)
    vec = (size * vec[0] / rand_size, size * vec[1] / rand_size)
    return vec


def generate_random_plot():
    total_samples = 2 + random.randint(0, 8)
    random_ts = sorted(random.sample(range(60), total_samples))
    random_plot = []
    for ts in random_ts:
        random_plot.append(
            (ts, random.random() * 1000, random.random() * 1000, (random.random() < 0.6) * jumps_sizes["dog"]))
    return random_plot


def removeMissingData(plot, animal):
    """
    remove missing data from plot according to missing data probability
    """
    missing_data_prob = missing_data_probs[animal]
    return [point for point in plot if random.random() > missing_data_prob]


def generate_vector(size, angle):
    return (math.cos(angle) * size, math.sin(angle) * size)


def randomize_in_range(a, b):
    """
    generate random number between a and b inclusive
    """
    return a + random.random() * (b - a)


def generate_plot(animal):
    """
    input:
        animal is a string from: "dog", "cat", "rabbit", "parrot", None
    output:
        a list of tuples of the form (ts, x, y) where ts in time in seconds from last minute (from 0 to 60)and
        x,y are coordinates of the object detected by the sensor (in meters). in max there will be 60 records in this
        list, if the sensor fully detected the object in the rectangle within the given timeframe
    """
    if (animal == 'parrot'):  # parrot is a flying animal while other animals are on the ground
        plot = [(0, 500, 500, randomize_in_range(parrot_heights_interval[0], parrot_heights_interval[1]))]
    else:
        plot = [(0, 500, 500, 0)]
    speed_range = speeds[animal]
    current_speed = speed_range[0] + random.random() * (speed_range[1] - speed_range[0])
    current_angle = random.random() * 2 * math.pi
    for ts in range(1, 60):
        current_angle = current_angle + moving_angles[animal] * (-1 + 2 * random.random())
        current_speed_vector = generate_vector(current_speed, current_angle)
        prev_place = plot[-1]
        if (animal == 'parrot'):
            current_height = prev_place[-1] + random.gauss(0, parrot_flight_deviation)
        else:  # randomize jump from ground
            current_height = randomize_in_range(0, jumps_sizes[animal]) * (random.random() < jumps_prob[animal])

        plot.append(
            (ts, prev_place[1] + current_speed_vector[0], prev_place[2] + current_speed_vector[1], current_height))
    plot = removeMissingData(plot, animal)
    return plot
