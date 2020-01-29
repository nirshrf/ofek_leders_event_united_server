#!/usr/bin/env python
# coding: utf-8
import math
import copy
#############################################################################
############################# CONSTANTS #####################################
#############################################################################

def send_drones(heat_map, adopters_requests, free_drones_locations, busy_drones_destinations,
                take_picture_penalty, send_drone_penalty):
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
    check_heat_map_ok(heat_map)
    check_adopters_requests_ok(adopters_requests) 
    check_free_drones_locations_ok(free_drones_locations)
    check_busy_drones_destination_ok(busy_drones_destinations)
    busy_drones_destinations = copy.deepcopy(busy_drones_destinations)
    taking_picture_destinations = {} # the final dictionary that we will return
    for free_drone_id, free_drone_location in free_drones_locations.items():
        grid_scores = [[compute_rect_score(row, col, free_drone_location, heat_map, adopters_requests,
                                           busy_drones_destinations, take_picture_penalty, send_drone_penalty) \
                       for col in range(100)] for row in range(100)]
        best_rect_row, best_rect_col = get_rect_with_highest_score(grid_scores)
        taking_picture_destinations[free_drone_id] = (best_rect_row, best_rect_col)
        # update busy drones destination, to prevent from 2 drones to be sent to the same rectangle:
        busy_drones_destinations[free_drone_id] = (best_rect_row, best_rect_col)
    return taking_picture_destinations 

def check_busy_drones_destination_ok(busy_drones_destination):
    assert(type(busy_drones_destination) == dict)
    for drone_id, drone_dest in busy_drones_destination.items():
        assert(type(drone_id) == str)
        assert(type(drone_dest) == tuple)
        assert(len(drone_dest) == 2)
        row, col = drone_dest
        assert(row in range(100))
        assert(col in range(100))

def check_free_drones_locations_ok(free_drones_locations):
    assert(type(free_drones_locations) == dict)
    for drone_id, drone_loc in free_drones_locations.items():
        assert(type(drone_id) == str)
        assert(type(drone_loc) == tuple)
        assert(len(drone_loc) == 2)
        row, col = drone_loc
        assert(row in range(100))
        assert(col in range(100))
    
def check_adopters_requests_ok(adopters_requests):
    if(type(adopters_requests) != dict):
        raise Exception("""send_drones received adopters_request of type different
                        than dictionary. format received: {0}""".format(str(type(adopters_requests))))
    for adopter_id, animals_list in adopters_requests.items():
        if(type(adopter_id) != str):
            raise Exception("""send_drones received adopters requests with adopter_id
                            of type different from string. type received: {0}""".format(
                            str(type(adopter_id))))
        if(type(animals_list) != list):
            raise Exception("""send_drones received adopters requests with animals_list
                            of type different from list. type received: {0}""".format(
                            str(type(animals_list))))
        if(len(animals_list) not in [1,2]):
            raise Exception("""send_drones received adopters_requests with a request
                            with animal list of illegal length. length of animals
                            list received: {0}""".format(str(len(animals_list))))
        for animal in animals_list:
            if(animal not in ['dog', 'cat', 'rabbit', 'parrot']):
                raise Exception("""send_drones received adopters_requests with
                                a request that contained illegal animal. illegal
                                animal contained: {0}""".format(animal))
    
        
def check_heat_map_ok(heat_map):
    """
    check that format of heat map is o.k. else raise an exception.
    check that:
        1. we received a 100*100 array
        2. each cell contains a dictionary of the right format
        3. each such dictionary from 2 represents a legal distribution
    """
    check_100x100_array(heat_map)
    for row in range(100):
        for col in range(100):
            animals_dist = heat_map[row][col]
            check_animals_distribution_ok(animals_dist)
            
def check_100x100_array(heat_map):
    """
    check that the heat_map is a 100*100 array
    raise exception otherwise
    """
    if(type(heat_map) != list):
        raise Exception("""send_drones received a heat map which is not of type list.
                        type received instead was {0}""".format(str(type(heat_map))))
    if(len(heat_map) != 100):
        raise Exception("""send_drones received an heat map with number of rows different from 100.
                        number or rows received: {0}""".format(str(len(heat_map))))
    if(type(heat_map[17]) != list):
        raise Exception("""send_drones recieved an heat map with each row not represented as a list,
                        but as a {0} instead""".format(str(type(heat_map[17]))))
    if(len(heat_map[43]) != 100):
        raise Exception("""send_drones received an heat map with number of columns different from 100.
                        number of columns received: {0}""".format(str(len(heat_map[43]))))
        
def check_animals_distribution_ok(animals_dist):
    """
    check that the given animals_dist is a dictionary of animals:probabilities types
    that contains number that represent a distribution.
    raise Exception if its not the case
    """
    if(type(animals_dist)!=dict):
        raise Exception(""" send_drones received an heat map that doesn't contains
                        dictionaries within, but instead values of type {0}""".format(
                        str(type(animals_dist))))
    probs_sum = 0
    for animal, animal_prob in animals_dist.items():
        if(animal not in ['dog', 'cat', 'rabbit', 'parrot']):
            raise Exception(""" send_drones received an heat map with a cell that
                            contains dictionary with illegal animal. illegal animal found: {0}""".format(
                            animal))
        if(type(animal_prob) != float):
            raise Exception("""send drones received an heat map with a cell that 
                            contains dictionary with probability that is not of type
                            float, but of type: {0} instead""".format(str(type(animal_prob))))
        if((animal_prob < 0) or (animal_prob > 1)):
            raise Exception("""  send_drones recieved an heat map with a cell that
                            contains illegal probability. probability received: {0}""".format(
                            str(animal_prob)))
        probs_sum += animal_prob
    if(probs_sum > 1):
        raise Exception(""" send_drones received an heat map with a cell that contains
                        dictionary with animals probs summed for more than 1.
                        sum af animals probs found: {0}.""".format(str(probs_sum)))
            

def compute_rect_score(row, col, free_drone_location, heat_map, adopters_requests,
                        busy_drones_destinations, take_picture_penalty, send_drone_penalty):
    """
    input:
        row, col - indexes of rectangle for computing score for
        free_drone_location - score will be computed relative to this rectangle. this one is a tuple that holds
            the drone location (i.e. (drone_row, drone_col))
        for the other argument meanings - please see the send_drones() documentation
    output:
        the function will compute a score for the rectangle, which reflect how worthy is it for the given free drone
        to be sent to the rectangle. the score function will reflect all the consideration that we have written above 
        this cell, as a guideline for the challenge. the higher the score - the more worthy for the drone to be sent to
        the rectangle
    """
    # the score will be basically based on the max chance for fulfilling an adopter request if it will be sent to
    # the rectangle (i.e. we will find the adopter that his chance to be satisfied if he will be sent to the rectangle,
    # will be maximal - because this is probably what will be doing when send adopters later on - sending the adopter
    # which is the most likely to be satisfied). of course we will make so "corrections" on this score to reflect deeper
    # considerations:
    free_drone_row, free_drone_col = free_drone_location
    matching_probability = computing_matching_prob(row, col, heat_map, adopters_requests)
    score = matching_probability
    time_to_take_picture = compute_time_for_taking_picture(free_drone_row, free_drone_col, row, col, take_picture_penalty,
                                                          send_drone_penalty)
    # every second that we postpone our decision to send an adopter we potentially "loose" 1/3600 from the maximal score
    # so we need to reflect it in our score:
    score = score - time_to_take_picture/3600
    # what we really want to do is not maximizing the score for a mission, but achieving more points per second of
    # the mission, i.e. - maximizing the throughput. for example: if we can earn 10 points in 5 seconds, or 8 points in 2
    # seconds - we will probably want the second option. so let's normalize the score to be throughput:
    score = score/time_to_take_picture
    # the final thing that we want to do, is to consider the movement of the busy drones. basically, if the closest busy
    # drone to the rectangle has a potential for be sent to the given rectangle with very high throughput we may want
    # to sent it to this rectangle, while sending our free drone to somewhere else. so for each rectangle that we consider
    # to send our free drone to, we have some "competition" with another busy drone that is heading near by. basically
    # we will reflect this competition by reducing the score with the score that could be achieved from our best 
    # competition, so the score will reflect the marginal value of the free drone to the total mission.
    # note: there are more options to reflect this competition. probably even better ones. this is only, very simplified
    # way to reflect this:
    if(len(busy_drones_destinations)!=0): # there are busy drones to relate to
        closest_busy_drone_row, closest_busy_drone_col = find_closest_busy_drone(row, col, busy_drones_destinations)
        closest_busy_drone_time_to_take_picture = compute_time_for_taking_picture(closest_busy_drone_row,
                                                                                  closest_busy_drone_col, row, col,
                                                                                  take_picture_penalty, send_drone_penalty)
        competition_score = matching_probability - closest_busy_drone_time_to_take_picture/3600
        competition_score = competition_score / closest_busy_drone_time_to_take_picture
        score = score - competition_score
    return score

def computing_matching_prob(row, col, heat_map, adopters_requests):
    """
    this function computes the probability for a matching for a specific rectangle.
    parameters:
        row, col - the indexes of the rectangle to compute matching probability for
        adopters_request - the adopters requests to computing matching probability relative to.
                            for understaing the format of this - look at the send_drones arguments documentation.
        heat_map - look at the send_drones() arguments documentation 
    return:
        the probability for the rectangle to make a matching to an adopter. i.e. compute for each adopter request
        the probability for it to be satisfied, and return the max probability.
    """
    max_matching_prob = 0
    for adopter_id, animals_adopter_wants in adopters_requests.items():
        matching_prob_for_current_adopter = 0
        for animal in animals_adopter_wants:
            matching_prob_for_current_adopter += heat_map[row][col][animal]
        max_matching_prob = max(max_matching_prob, matching_prob_for_current_adopter)
    return max_matching_prob

def compute_time_for_taking_picture(free_drone_row, free_drone_col, row, col, take_picture_penalty, send_drone_penalty):
    """
    the function will compute the time that it will take for the free drone to take picture, if he currently
    at location: (free_drone_row, free_drone_col) and it should take a picture at (row, col).
    """
    distance_to_dest = compute_distance(free_drone_row, free_drone_col, row, col)
    return distance_to_dest * send_drone_penalty + take_picture_penalty

def compute_distance(row1, col1, row2, col2):
    """
    compute distance between (row1, col1) and (row2, col2)
    """
    return math.sqrt((row2-row1)**2 + (col2-col1)**2)

def find_closest_busy_drone(row, col, busy_drones_destinations):
    """
    this function will return the location of the (destination of the) closest busy drone (in terms
    of destination) to the given rectangle. 
    
    input:
        row, col - location of the rectangle we will compute closest drone relative to
        busy_drones_destinations - a dictionary that maps each busy_drone_id to the destination it is heading to
                                (destination will be represented by (row, col) of destination rectangle)
    output:
        the function will return the destination from busy_drones_destinations which is closest to (row, col)
    """
    min_dist = 10000
    closest_destination_row = 0
    closest_destination_col = 0
    for busy_drone_id, destination in busy_drones_destinations.items():
        distance_from_destination = compute_distance(row, col, destination[0], destination[1])
        if(distance_from_destination < min_dist):
            min_dist = distance_from_destination
            closest_destination_row = destination[0]
            closest_destination_col = destination[1]
    return closest_destination_row, closest_destination_col

def get_rect_with_highest_score(grid_scores):
    """
    input:
        grid_scores - 100*100 2-dimensional array that holds score for each rectangle in the grid
    output:
        the function will return the row and column of the rectangle in the grid with the highest score
    """
    highest_score = -100000000
    highest_rect_row = -1
    highest_rect_col = -1
    for row in range(100):
        for col in range(100):
            if(grid_scores[row][col] > highest_score):
                highest_score = grid_scores[row][col]
                highest_rect_row = row
                highest_rect_col = col
    return highest_rect_row, highest_rect_col
