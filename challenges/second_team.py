import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier


def compute_features_df(plots):
    """
    input:
        plots - list of plots, i.e. list of the format [plot_1, plot_2,..., plot_n]
        each plot is a list of the form [(ts_1, x_1, y_1, z_1),...., (ts_n, x_n, y_n, z_n)] which represents the
        motion of an animal.
    output: 
        dataFrame of features extracted from the plots list
    """
    total_jumps = [computeTotalJumps(plot) for plot in plots]
    # try to compute more feature based on the business data and insert them into the dataframe:
    df = pd.DataFrame({"total_jumps": total_jumps})
    return df


def computeTotalJumps(plot):
    """
    plot:
        list of the form [(ts_1, x_1, y_1, z_1),...., (ts_n, x_n, y_n, z_n)] which represents the
        motion of an animal.
    return:
        the number of points in the plot that are jumps (which is correlative to the jump probability)
    """
    return sum([point[-1] > 0 for point in plot])

def train_model(features_vectors, labels):
    """
    input:
        features_vectors - pandas dataFrame that contain features_vectors computed from the train data using
            the compute_features_df(plot) function you implemented above.

        labels - the labels of the features vectors. i.e. labels[i] is the animals that corresponds to the feature_vector
                in features_vectors[i]. 

    output:
        a trained model from the training set (scikit model)
    """
    # this is the training itself. we used the randomForestClassifier in here. there is really no need to try to
    # use another learning model - the area that you should emphasize in is the compute_features_df. however you can
    model = RandomForestClassifier(n_estimators=1000).fit(features_vectors, labels)
    return model



