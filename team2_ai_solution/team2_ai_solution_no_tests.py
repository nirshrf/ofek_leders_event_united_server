import pandas as pd
import math
from sklearn.ensemble import RandomForestClassifier
"""
the compute_features_df is the main function that you should be focused in.
this function computes features from the plots of the animals. 
the features should represents the behaviour of the animals using numbers. in the end, the machine learning
function will use the features that you computed in this function in order to learn a model that match between plots
and animals types.

you should focus on the business data that was described in the previous section, and try to qunatify each behaviour
with the relevent feature. this feature should be inserted to the data_frame.

for example we modeled behaviour 6 for you in the basic solution: it was described that different animals have different
probability to jump, so we catched it up by the number of jumps detected in the plot.
"""


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
    plots_sizes = [len(plot) for plot in plots]
    max_speeds = [computeMaxSpeed(plot) for plot in plots]
    diameter = [computeMaxDistFromStart(plot) for plot in plots]
    max_heights = [computeMaxHeight(plot) for plot in plots]
    # try to compute more feature based on the business data and insert them into the dataframe:
    df = pd.DataFrame( {"diameter": diameter,
                       "max_speed": max_speeds,
                        "plot_size": plots_sizes,
                        "max_heights": max_heights,
                        "total_jumps": total_jumps} )
    return df


def computeTotalJumps(plot):
    """
    plot:
        list of the form [(ts_1, x_1, y_1, z_1),...., (ts_n, x_n, y_n, z_n)] which represents the
        motion of an animal.
    return:
        the number of points in the plot that are jumps (which is correlative to the jump probability)
    """
    return sum([point[-1]>0 for point in plot])


def computeSpeed(point1, point2):
    """
    point1, point2 - points of the format (ts, x, y)
    we want to compute the speed between those 2 points
    """
    ts1, x1, y1, z1 = point1
    ts2, x2, y2, z2 = point2
    dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return dist/(ts2-ts1)


def computeMaxSpeed(plot):
    return max([computeSpeed(plot[i], plot[i+1]) for i in range(len(plot)-1)])


def computeMinSpeed(plot):
    return min([computeSpeed(plot[i], plot[i+1]) for i in range(len(plot)-1)])


def computeMaxDistFromStart(plot):
    """
    return the max distance of a point in the plot from the starting point
    """
    p1 = plot[0]
    distances = [math.sqrt((p2[1]- p1[1])**2 + (p2[2]-p1[2])**2) for p2 in plot]
    return max(distances)


def computeMaxHeight(plot):
    """
    compute the maximal height in the plot
    """
    return max([point[-1] for point in plot])


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
