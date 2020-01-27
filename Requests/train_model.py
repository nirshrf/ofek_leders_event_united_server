import team2_ai_solution as team2_ai_solution
import pickle

###########################################
####   1. loading the training data  ######
###########################################


def load_train_data(pickle_file_path):
    """
    return value:
    [(plot_1, label_1),(plot_2, label_2),.....,(plot_m, label_m)]
    m -> the number of grid cells, i.e 10000.
    plot:
    [(ts_1, x_1, y_1, z_1),..., (ts_n, x_n, y_n, z_n)]
    0 <= n < 60
    """
    with open(pickle_file_path, 'rb') as f:
        labeled_plots = pickle.load(f)
    return labeled_plots


def create_model(train_data_path):
    labeled_plots = load_train_data(train_data_path)
#   compute_features and train model
    x_train = team2_ai_solution.compute_features_df([plot for plot, label in labeled_plots])
    y_train = [label for plot, label in labeled_plots]
    model = team2_ai_solution.train_model(x_train, y_train)
    return model


