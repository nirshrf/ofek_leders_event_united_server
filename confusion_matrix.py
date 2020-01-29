import team2_ai_solution
from sklearn.metrics import confusion_matrix
import pickle
import pandas as pd
VALIDATION_SET_PATH = "Data/validation.pickle"


def compute_confusion_matrix(model):
    """
    input:
        model - a trained model
    output:
        a pandas dataFrame that represent the confusion matrix of the trained model
    """
    with open(VALIDATION_SET_PATH, "rb") as f:
        labeled_plots = pickle.load(f)
    true_labels = [label for plot, label in labeled_plots]
    X = team2_ai_solution.compute_features_df([plot for plot, label in labeled_plots])
    predictions = model.predict(X)
    conf_matrix = confusion_matrix(true_labels, predictions, labels=["none", "dog", "cat", "rabbit", "parrot"])
    conf_matrix = pd.DataFrame(conf_matrix, columns=["none", "dog", "cat", "rabbit", "parrot"],
                               index=["none", "dog", "cat", "rabbit", "parrot"])
    return conf_matrix