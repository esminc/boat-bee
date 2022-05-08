def predict():
    import tensorflow as tf  # type: ignore # pylint: disable=import-outside-toplevel

    model = tf.keras.models.load_model("./models/sample")

    sample_x = [
        18.0846,
        0.0,
        18.1,
        0.0,
        0.679,
        6.434,
        100.0,
        1.8347,
        24.0,
        666.0,
        20.2,
        27.25,
        29.05,
    ]

    return model.predict([sample_x])
