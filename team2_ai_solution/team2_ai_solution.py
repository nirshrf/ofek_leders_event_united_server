import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import math
    

def compute_features_df(plots):
    """
    input:
        plots - list of plots, i.e. list of the format [plot_1, plot_2,..., plot_n]
        each plot is a list of the form [(ts_1, x_1, y_1, z_1),...., (ts_n, x_n, y_n, z_n)] which represents the
        motion of an animal.
    output: 
        dataFrame of features extracted from the plots list
    """
    if(type(plots) != list):
        raise Exception("""compute features df received plots not as list type,
                        but instead as {0} type""".format(str(type(plots))))
    for plot in plots:
        if(type(plot) != list):
            raise Exception("""compute_features_ds receives plot not as list type,
                            but instead as {0} type""".format(str(type(plot))))
        if(len(plot) > 61):
            raise Exception("compute_features_df received a plot with more than 60 points!")
        for point in plot:
            if(type(point) != tuple):
                raise Exception("""compute features df received a point in plot
                                which is not of typle tuple, but instead of {0}
                                type""".format(str(type(point))))
            if(len(point) != 4):
                raise Exception("""compute_features_df received a point which is not
                                a tuple of length 4 (ts,x,y,z) but instead a tuple
                                of length: {0}""".format(str(len(point))))
            ts, x, y, z = point
            if(ts not in range(61)):
                raise Exception("""compute_features_df receives ts in a point that
                                is not in range(61). ts received: {0}""".format(str(ts)))
            if((x<0) or (x>1000) or (y<0) or (y>1000) or (z<0) or (z>1000)):
                raise Exception("""compute_features_df received x,y,z which is not
                                between 0 and 1000. ({0},{1},{2}) received:""".format(
                                str(x), str(y), str(z)))
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
    if(len(features_vectors) != len(labels)):
        raise Exception("""train_model received features_vectors and labels with
                        different sizes. size of features_vectors: {0}, size of
                        labels: {1}""".format(str(len(features_vectors)),
                        str(len(labels))))
    if(type(labels) != list):
        raise Exception("""train_model received labels which is not of type list,
                        but instead of type: {0}""".format(str(type(labels))))
    if(type(features_vectors) != pd.core.frame.DataFrame):
        raise Exception("""train_model received features_vectors which is not
                        of type pd.core.frame.DataFrame, but instead of type: {0}""".format(
                        str(type(features_vectors))))
    for label in labels:
        if(type(label) != type("cat")):
            raise Exception("""train_model received a label in labels which is not
                            of type string. but instead of type: {0}""".format(str(type(label))))
        if(label not in ["dog", "cat", "rabbit", "parrot", "None"]):
            raise Exception("""train_model received label in labels which is not from
                            the list: ["dog", "cat", "rabbit", "parrot", "none"].
                            label received: {0}""".format(label))
    # features_vectors should adapt to compute_features_df function:
    if(list(features_vectors.columns) != ["diameter", "max_speed", "plot_size",
       "max_heights","total_jumps"]):
        raise Exception("""train_model received features_vectors with columns that
                        are not matched to the columns produced by the compute_features_df
                        function. expected columns in features_vectors df: {0},
                        while columns received: {1}""".format(
                        str(["diameter", "max_speed", "plot_size",
                             "max_heights","total_jumps"]),
                        str(list(features_vectors.columns))))
    if(len(labels) < 5000):
        raise Exception("""train_model rceived too little labels to learn with.
                        train_model should receive at least 5000 labels, while
                        in practive, it received: {0} labels""".format(str(len(labels))))
    check_labels_distribution_ok(labels)
    # this is the training itself. we used the randomForestClassifier in here. there is really no need to try to
    # use another learning model - the area that you should emphasize in is the compute_features_df. however you can
    model = RandomForestClassifier(n_estimators=1000).fit(features_vectors, labels)
    return model
    
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

def compute_animals_distribution(labels):
    """
    compute animals distribution
    """
    animals_distribution = {"dog": 0, "cat": 0, "rabbit": 0, "parrot": 0,
                            "None": 0}
    for animal in labels:
        animals_distribution[animal] += 1/len(labels)
    return animals_distribution

def check_labels_distribution_ok(labels):
    """
    this function checks if the labels given distributes approximaltely according
    to the labels distribution we know (i.e.: {dog: 480, cat: 450, rabbit: 340, parrot: 230, None: 8500})
    """
    expected_animals_distribution = {"dog": 480/10000, "cat": 450/10000,
                                 "rabbit": 340/10000, "parrot": 230/10000,
                                 "None": 0.85}
    received_animals_distribution = compute_animals_distribution(labels)
    for animal in expected_animals_distribution:
        if(abs(expected_animals_distribution[animal] - received_animals_distribution[animal]) >
           0.02):
            raise Exception("""train_model received labels which don't distribute like
                            the real distribution in the world.
                            distribution of labels receiced {0}""".format(
                            str(received_animals_distribution)))


