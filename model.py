from train_model import create_model


def generate_model():
    model = create_model("Data/train_data.pickle")
    print("trained model")
    return model

