from cache_decorator import Cache
from .utils import standard_test
from time import sleep

try:
    import numpy as np
    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Input, Dense

    def get_model():
        i = h = Input(shape=(2,))
        h = Dense(10, activation="relu")(h)
        o = Dense(1, activation="sigmoid")(h)
        model = Model(i, o)

        model.compile(
            optimizer="nadam",
            loss="binary_crossentropy",
            metrics=["accuracy"],
        )
        return model

    @Cache(
        cache_path="{cache_dir}/keras_model_{_hash}.keras.tar.gz",
        cache_dir="./test_cache",
        log_level="debug",
        backup=False,
    )
    def train(x_train, y_train):
        model = get_model()
        sleep(3)
        return model

    def test_keras_model():
        x_train = np.random.randint(0, 2, size=(1000, 2))
        y_train = np.array([
            a ^ b
            for a, b in x_train
        ])

        standard_test(train, args=((x_train, y_train),
                      (x_train, y_train), (x_train + 1, y_train), ))

    def test_keras_model_performance():
        x_train = np.random.randint(0, 2, size=(1000, 2))
        y_train = np.array([
            a ^ b
            for a, b in x_train
        ])

        trained_model1 = train(x_train, y_train)

        trained_model2 = train(x_train, y_train)

        assert trained_model1.evaluate(x_train, y_train, verbose=False) == trained_model2.evaluate(
            x_train, y_train, verbose=False)

except ModuleNotFoundError:
    pass
