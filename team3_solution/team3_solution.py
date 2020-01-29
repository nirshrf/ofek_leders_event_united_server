#!/usr/bin/env python
# coding: utf-8

# # challenge 3

# ## required knowledge to solve this challenge:

# 1. ability to write and understand basic code in python
# 2. good understanding of confusion matrix and their interpreation for evaluation machine learning predictions

# ## introduction - presenting the problem

# in this challenge you should implement a dss algorithm that will match adopters to animals - more accurately: the algorithm
# will match adopters to rectangles on the grid that hopefully will contain an animal that they want.
#
# it is important to understand that our dss algorithm runs at the end of the operational process: i.e. before
# making the decision where to send adopters to based on our algorithm, several things happened:
# 1. drones were sent to collect data from rectangles on the grid, based on team_1 dss algorithm
# 2. the data collected from the drones were analyzed by team 2 and according to their machine learning algorithm a prediction
#     was made on which animal was "seen" in the data.
#
# based on team's 2 predictions on which animals are found on specific rectangles on the grid (which team 1 collected data from)
# and the quality of their learned model you should make a decision where to send each adopter to (if at all - it is perfectly
# legitimate not to send any adopter, i.e. to wait with your recommendation).
#
# the function you will implement for this purpose is the:
# send_adopters(adopters_requests, confusion_matrix, model_predictions)
#
# you will be given a basic implementation for this function will thourogh explanation about it's arguments, and even 2 helper
# functions that can assit you to improve it.
#
# your task is to improve this function to be smarter and make better decision than the basic versoin that is found right know.
# here are some ideas for you to consider when you will improve the algorithm (our recommendation is to first read the basic
# implementation we provided for your so you can better grasp the situation and the arguements of the function, and then
# return to read the inext section that can help you with ideas for how to improve the algorithm.

# ## ideas to consider for improving the algorithm:

# 1. it might be a good idea to send the more "picky" adopters first.
#     for example: if you have one rectangle that your modeled predicted that contains a dog, and 2 adopters with
#     the following requests: {"adopter1": ["dog"], "adopter2": ["dog", "cat"]} using this information only it is
#     obviously better to send adopter_1 to the rectangle (so when future data will be collected we will have higher chances
#     to do matching, because adopter2 is more "liberal").
#
# 2. it could be good idea not to act greedily when doing the matching, but to do some global optimization.
#     an example will make it clearer: imagine that you have 2 rectangles: rectangle_1 contains "cat" and rectangle_2
#     contains "dog". now assume that you have 2 adopters too, with the following requests:
#     {"adopter_1": ["cat", "dog"], "adopter2": ["cat", "parrot", "rabbit"]}.
#     if you we do a greedy matching, there is a chance that you will send adopter_1 to rectangle_1, and decide not to send
#     adopter_2 anywhere (because rectangle_2 doesn't contain an animal it wants), this is obviously sub-optimal.
#     you can send adopter_1 to rectangle_2, and adopter_2 to rectangle_1 thus making 2 matches instead of 1. global
#     optimization for making the matching is required to make such decisoin (as opposed to greedy decision - i.e. decide
#     for each adopter at a time where to send it to).
#
# ***until know we haven't considered the prediction model quality at all. for this purpose we have the confusion matrix
# that gives us data about where our model wrongs and how (i.e. which mistakes it makes). using this confusion matrix
# we can make better decision for our algorithms. for example here are 2 ideas:***
#
# 3. there may be situations where the model isn't sure on it's predictions (it could be detected by the confusion matrix -
#     if our model gave prediction Y we will look at the colum the corresponds to that prediction in the confusion matrix and
#     will see if there are high chances that the true animal was different than y by looking at the row in the column
#     that corresponds to y and see if the number inside it is much larger than the sum of the number in the other rows).
#     if we detect such situation - i.e. a situation where our prediction may be with high chances wrong, we might be better
#     not to send an adopter based on such prediction. in order it will be cleared we implemented 2 helper functions for you
#     that makes some analysis of the confusion matrix that can help you with your improvements. you are welcome to use them,
#     and we recommend to you to look at their code in order to better understand how to analyze the confusion matrix for
#     this purpose.
#
# 4. we may want to analyse how the machine learning model might be wrong for it's prediction and to base our decision
#     accordingly (by looking the confusion matrix). for example, imagine that the model predicted cat, and according
#     to the confusion_matrix in that case it will be correct 2/3 of the times, but 1/3 of the times the true label
#     will be dog. in that case it will be excellent to send an adopter that has a cat and a dog in its requests list
#     because we will have a match for 100%. so analysing the mistakes of the learned model realtive to the specific
#     prediction on the rectangle may help us forming better decisions too.

# ## the algorithm (basic version - your's to improve)

# In[1]:


from copy import deepcopy


# this is the algorithm you need to imporove, i.e. the dss algorithm. everything else in this notebook is to help you
# improving this function:
def send_adopters(adopters_requests, animals_seen, confusion_matrix):
    """
    input:
        adopters_requests:
            this is a dictionary that contains the adopters requrests. this dictionary is of the form:
            {adopter_id_1: animals_list_1,...., adopter_id_n: animals_list_n}, where animals_list_i is a list
            that contains the animals that adopter_i wants to adopt.

        animals_seen:
            this is a dictionary that contains the data collected by our drones.
            this is a dictionary of the format:
            {(row_1, col_1): prediction_1, ....., (row_n, col_n): prediction_n}
            where (row_i, col_i) indicates the location of a rectangle on the grid that one of our drones collected data from,
            and prediction_i indicates which animal team2's algorithms predicted to be on that rectangle, based on the
            motion graph it collected from that rectangle. i.e. this is a dictionary of team_2 predicted animals on the
            rectangles it collected data from.

        confusion_matrix:
            this is a matrix that contains informain about the classification quality of our learned model
            (i.e. the calssifying algorithm that team 2 implements which classify animals based on their motion data).
            this is a pandas data_frame with 5 rows and 5 columns. the rows and columns has labels as the "possible" animals
            i.e.: ["cat", "dog", "rabbit", "parrot", "None"].
            confusion_matrix[animal_i, animal_j] indicates the number of rectangles in the evaluation set which had animal_i
            in them and our model classified them as animal_j.
            for example, if confusion_matrix["cat", "dog"]=300 it indicates that there were 300 rectangles with "cat" in them
            that our model classified as "dog". a perfect model is a model that it's confusion_matrix contain zero for
            animal_i!=animal_j (i.e. it doesn't misclassify).
            the information in the confusion matrix can help us to understand in which cases our prediction model isn't good
            and consider it for the adoption decision that our dss algorithm gets.

    return:
        the function will return a matching between adopters and rectangles on the grid.
        we will return a dictionary of the format: {adopter_id_1: (row_1, col_1),...., adopter_id_n: (row_n, col_n)}
        of course not all adopters must be matched to an animal and it is a legitimate decision not to send any adopter
        (i.e. return an empty dictionary).
        (row_i, col_i) in the returned dictionary represent that our algorithm recommendation is to send adopter_i to
        rectangle in (row_i, col_i)

    """
    # here we implement the first idea from the idea we gave to you above, i.e: greedily pass through the
    # rectangles we have data for, and for each rectangle match the less "peaky" adopter that want the animal in it:
    matching_dict = {}
    unhandled_requests = deepcopy(adopters_requests)  # this will contain the request that hasn't been handled so far
    for rect, animal in animals_seen.items():
        if (animal != 'None'):  # if animal is None, obviously we don't want to send any adopter to it
            matched_adopter = find_most_peaky_adopter_that_wants_animal(unhandled_requests, animal)
            if (matched_adopter != None):
                matching_dict[matched_adopter] = rect
                del (unhandled_requests[matched_adopter])
    return matching_dict


# helper function for the send_adopters basic implementation that we gave:
def find_most_peaky_adopter_that_wants_animal(adopters_requests, animal):
    """
    input:
        adopters_requests - a dictionary that maps each adopter to a list of animals he would like to adopt
        animal - a value from the list: ['cat', 'dog', 'rabbit', 'parrot']

    return:
        an adopter_id that want the given animal (according to adopters_requests) and is the most peaky on
        from all the adopters that want the animal (most_peaky == has low number of animal it wants in his requests list)
        if no adopter want the given animal None will be return
    """
    most_peaky_adopter_id = None
    most_peaky_peakiness = 100
    for adopter_id, requested_animals in adopters_requests.items():
        if (animal in requested_animals):
            adopter_peakiness = len(requested_animals)
            if (adopter_peakiness < most_peaky_peakiness):
                most_peaky_peakiness = adopter_peakiness
                most_peaky_adopter_id = adopter_id
    return most_peaky_adopter_id


# ## helper functions

# in this section we give you 2 helper functions that may help you in your imporvements of the dss algorithm.
# those 2 functions analyse the confusion matrix and return some processed information about it that can help you with
# your decision. we highly recommend to you to look at the code and try to understand it. this may help you to understand the confusion matrix and how to analyze it.

# In[2]:


import pandas as pd


def compute_animals_prob_based_on_prediction(confusion_matrix, prediction):
    """
    input:
    confusion_matrix:
            this is a matrix that contains informain about the classification quality of our learned model
            (i.e. the calssifying algorithm that team 2 implements which classify animals based on their motion data).
            this is a pandas data_frame with 5 rows and 5 columns. the rows and columns has labels as the "possible" animals
            i.e.: ["cat", "dog", "rabbit", "parrot", "None"].
            confusion_matrix[animal_i, animal_j] indicates the number of rectangles in the evaluation set which had animal_i
            in them and our model classified them as animal_j.
            for example, if confusion_matrix["cat", "dog"]=300 it indicates that there were 300 rectangles with "cat" in them
            that our model classified as "dog". a perfect model is a model that it's confusion_matrix contain zero for
            animal_i!=animal_j (i.e. it doesn't misclassify).
            the information in the confusion matrix can help us to understand in which cases our prediction model isn't good
            and consider it for the adoption decision that our dss algorithm gets.
    prediction: the animal the model predicted for the rectangle

    output:
    the function will return the probabilities for each animal to be on the ractangle based on the confusion matrix.
    i.e. it analyse the errors of the learned model based on the confusion matrix for this purpose. for a perfect
    model with 100% accuracy if the model predicted X then the function will return 1 for x and 0 for the others animals
    (if the model always right, then if it predicted a cat there is indeed a cat on the rectangle).
    the format of the output will be a dictionary of the form:
    {"dog": dog_probability, "cat": cat_probability, "rabbit": rabbit_probability, "parrot": parrot_probability,
    "None": probability_for_no_animal}
    """
    predicted_animal_column_in_confusion_matrix = confusion_matrix[prediction]
    total_samples_predicted_as_prediction = sum(predicted_animal_column_in_confusion_matrix)
    none_prob = predicted_animal_column_in_confusion_matrix["None"] / total_samples_predicted_as_prediction
    dog_prob = predicted_animal_column_in_confusion_matrix["dog"] / total_samples_predicted_as_prediction
    cat_prob = predicted_animal_column_in_confusion_matrix["cat"] / total_samples_predicted_as_prediction
    rabbit_prob = predicted_animal_column_in_confusion_matrix["rabbit"] / total_samples_predicted_as_prediction
    parrot_prob = predicted_animal_column_in_confusion_matrix["parrot"] / total_samples_predicted_as_prediction
    return {"None": none_prob, "dog": dog_prob, "cat": cat_prob, "rabbit": rabbit_prob, "parrot": parrot_prob}


# In[3]:


def compute_error_prob_for_prediction(prediction, confusion_matrix):
    """
    input:
    confusion_matrix:
            this is a matrix that contains informain about the classification quality of our learned model
            (i.e. the calssifying algorithm that team 2 implements which classify animals based on their motion data).
            this is a pandas data_frame with 5 rows and 5 columns. the rows and columns has labels as the "possible" animals
            i.e.: ["cat", "dog", "rabbit", "parrot", "None"].
            confusion_matrix[animal_i, animal_j] indicates the number of rectangles in the evaluation set which had animal_i
            in them and our model classified them as animal_j.
            for example, if confusion_matrix["cat", "dog"]=300 it indicates that there were 300 rectangles with "cat" in them
            that our model classified as "dog". a perfect model is a model that it's confusion_matrix contain zero for
            animal_i!=animal_j (i.e. it doesn't misclassify).
            the information in the confusion matrix can help us to understand in which cases our prediction model isn't good
            and consider it for the adoption decision that our dss algorithm gets.
    prediction: the animal the model predicted for the rectangle

    output:
    the function will return the probability that the given prediction the model gave is correct, based on the
    given confusion_matrix of the model.
    """
    predicted_animal_column_in_confusion_matrix = confusion_matrix[prediction]
    total_samples_in_prediction_column = sum(predicted_animal_column_in_confusion_matrix)
    prob_prediction_true = predicted_animal_column_in_confusion_matrix[prediction] / total_samples_in_prediction_column
    return 1.0 - prob_prediction_true