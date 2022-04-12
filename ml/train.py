from keras.datasets import boston_housing  # type: ignore
from tensorflow import keras  # type: ignore
from tensorflow.keras import layers  # type: ignore


def train():
    (x_train, y_train), (x_test, y_test) = boston_housing.load_data()

    model = keras.Sequential(
        [
            layers.Dense(64, activation="relu", input_shape=[x_train.shape[1]]),
            layers.Dense(128, activation="relu"),
            layers.Dense(1),
        ]
    )
    model.compile(loss="mae", optimizer="adam", metrics=["mae", "mse"])

    model.fit(
        x_train,
        y_train,
        epochs=50,
    )

    model.save("models/sample")


if __name__ == "__main__":
    train()
