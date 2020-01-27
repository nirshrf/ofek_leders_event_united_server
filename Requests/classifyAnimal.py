# -*- coding: utf-8 -*-
"""
hi nir, this is a script for you that demonstrate how to
run team 2 solution during the different phases of the challenge.
i hope it will help to make some sense.
"""

# team2_ai_solution is the python file that team 2 will push to
# the git repository and you should call code from. i provided for
# you 2 such script: team2_ai_solution.py which is a basic solution
# for the challenge (we gave the student to improve) and "school_solution2.py"
# which is a solution that i've implemented as a school solution
# (shai requrested from me)
import team2_ai_solution
from Requests.train_model import create_model
import numpy as np
from team2_ai_solution.team2_ai_solution import compute_features_df

model = create_model("Data/train_data.pickle")
print("trained model")
##############################################################################
########     when you want to classify an animal using it's graph  ###########
##############################################################################

def classify_animal(plots):
    '''
    plots - > [(ts_1,x_1,y_1,z_1),.....,(ts_n,x_n,y_n,z_n)]
    0<=n<60
    return value:
    item from list - ["none", "cat", "dog", "parrot", "rabbit"]
    '''
    features_df = compute_features_df(plots)
    model_predictions = list(model.predict(features_df))
    return model_predictions
