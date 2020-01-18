def send_drones(heat_map, adopters_requests, free_drones_locations, busy_drones_destinations, take_picture_penalty, send_drone_penalty):
    """
    this function is responsible to send drones to take "pictures" on rectangles.
    input:
        heat_map - a 100*100 two-dimensional array that holds for each rectangle in the grid a dictionary of the form:
            {"cat": cat_prob, "dog": dog_prob, "parrot": parrot_prob, "rabbit": rabbit_prob}, i.e. it represent the
            a-priori probabilities for each animals to be found on the rectangle.

        adopters_requests - a dictionary that holds for each adopter that not yet matched an animal,
                            a list of the animals it would like to adopt, something of the form:
                            {adopter_id_1: ["dog", "rabbit"], ...., adopter_id_n: ["parrot"]}

        free_drones_locations - a dictionary that holds for each "free drone" (that is not in a flight - i.e. free to be sent),
                            the location it is currently at (as a (row, col) tuple). i.e., something of the form:
                            {drone_id_1: (row_1, col_1),....., drone_id_n: (row_n, col_n)}

        busy_drones_destinations - a dictionary that holds for each "busy drone" that is on its trip to take picture,
                                    the rectangle location that it's heading to.
                                    this dictionary is of the format:
                                    {drone_id_1: (row1, col1),....., drone_id_n: (row_n, col_n)}

        take_picture_penalty - the cost for taking picture. the proportion between this cost, and the cost for sending the
                                drone to the site to take pictures of highly influence our decision of where to send each
                                drone. this is a fixed cost for each taking_picture mission.

        send_drone_penalty - the cost of sending a drone to the rectangle. this cost is per "rectangle_unit", i.e., if
                            the drone should pass x rectangles in order to arrive to the required_rectangle to take pictures
                            of, then the penalty for this "travel" will be x*send_drone_penalty

    output:
        a dictionary that matches each drone to it's rectagle to pictures, i.e. a data structure of the format:
        {drone_id1: rectangle_ind_1, ....., drone_id_n: rectangle_ind_n}
        where each rectangle_ind is represented by a tuple of the form (row, col) which indicates the coordinates of the
        rectangle on the grid (0 <= row, col < 100)
    """
    # here is a basic solution that will give you some start. it is based on some of the ideas that are mentioned above
    # (but not all of them).
    # things that are not considered at all in this solution and that you may like to add consideration for:
    # 1. cost of sending the drone to take picture (as described in the guideline)
    # 2. different tactics for the beginning of the mission where all drones aree free and while it is running
    #   and having mostly one free drone at a time (as described in the guideline)

    taking_picture_destinations = {}  # the final dictionary that we will return
    most_demanded_animal = get_most_demanded_animal(adopters_requests)
    for free_drone_id, free_drone_location in free_drones_locations.items():
        # free_drone_location is a tuple of the form (row, col) that represents the current location of the drone on grid
        best_destination_location = (0, 0)
        best_destionation_score = 0
        for row in range(100):  # pass through each rectangle on the grid
            for col in range(100):
                """we don't want to send a drone to a rectangle which another drones is currently heading to, so
                this is the purpose of this if. put attention: sending a drone to a location that is near a location
                that another drone is heading to is sub-optimal to, because in terms of costs it will be better to
                send the busy drone to that location after it will arrive to it's destination. so there is room
                for improvement here that you may like to tackle. """
                if (row, col) not in busy_drones_destinations.values():
                    """the score that we compute for a rectangle is the probability for the most wanted animal to be found
                    at. this is a reasonable score function but it's far from being optimal.
                    there are 2 obvious optimization that we cani insert to this score:
                    1. send the drone to a rectangle that has the highest probability to satisfy some adopter demand.
                    for this logic you may like to iterate all of the adopter, and compute for each adopter the probability
                    that it's demands will be satisfied if he will be sent to that rectangle (think on how to evaluate this
                    probability using the heat_map), a reasonable score for this may be the max probability over each of the
                    adopters.
                    2. however the previous heuristics may sound appealing it has one main disadvantage: we don't consdier
                    what happen with the other drones around. there may be a situation where the score computed for a rectangle
                    is based on an adopter that hat like probability to be sent to another rectangle that was taken picture
                    by another drone. in that location the score that we computed may be a little biased because it was
                    highly based according to that specific adopter. so it may be good idea to make the score more robust 
                    relative to adopters, or a least make some sophisticated consideration on adopters that has high chances
                    to be sent in the near future to a rectangle that was pictured by another drone in the area.
                    """
                    most_demanded_animal_prob = heat_map[row][col][most_demanded_animal]
                    if most_demanded_animal_prob > best_destionation_score:
                        best_destionation_score = most_demanded_animal_prob
                        best_destination_location = (row, col)
        taking_picture_destinations[free_drone_id] = best_destination_location
    return taking_picture_destinations


# and here is some helper function for our send drones function:
def get_most_demanded_animal(adopters_requests):
    """
    adopters_requests - a dictionary that holds for each adopter that not yet matched an animal,
                        a list of the animals it would like to adopt, something of the form:
                        {adopter_id_1: ["dog", "rabbit"], ...., adopter_id_n: ["parrot"]}
    return:
        the function will return the most demanded animal, i.e. - the animal that most adopter want
    """
    # count demand for each animal:
    animals_counts = {"dog": 0, "cat": 0, "rabbit": 0, "parrot": 0}
    for adopter_animals_list in adopters_requests.values():
        for animal in adopter_animals_list:
            animals_counts[animal] += 1
    # find the animal that has the max demand:
    max_count = max(animals_counts.values())
    for animal in animals_counts:
        if animals_counts[animal] == max_count:
            return animal
