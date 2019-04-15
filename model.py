from keras import backend as K
from keras.layers import Embedding, Dense, LSTM, Dropout
from keras.models import Sequential
from keras.utils import to_categorical
import tensorflow as tf
from keras.models import load_model
    
class Model:
    def __init__(self, n_tokens, maxlen=500):
        self.reset_tf_session()
        self.__model = Sequential()
        self.__model.add(LSTM(8, input_shape=(maxlen, n_tokens), return_sequences=False))
        self.__model.add(Dense(32, activation='tanh'))
        self.__model.add(Dense(2, activation='softmax'))
        self.__model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
    
    def reset_tf_session(self):
        curr_session = tf.get_default_session()
        if curr_session is not None:
            curr_session.close()
        K.clear_session()
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        s = tf.InteractiveSession(config=config)
        K.set_session(s)
        return s

    def __train_iterator(self, batch_size):
        while 1:
            random_indices = np.random.randint(0, len(self.__X), size=batch_size)
            X_batch = self.__X[random_indices]
            y_batch = self.__y[random_indices]
            X_batch = to_categorical(X_batch, num_classes=n_tokens)
            yield X_batch, y_batch

    def model_load(self, path):
        self.__model = load_model(path)

    def train(self, X, y, epochs=5, batch_size = 1024):
        self.__X = X
        self.__y = y
        self.__model.fit_generator(
            self.__train_iterator(batch_size), 
            steps_per_epoch=X.shape[0] // batch_size,
            epochs=epochs,
            verbose=1)
    
    def predict(self, X):
        return self.__model.predict_classes(X), self.__model.predict(X)

    def model_save(self, path):
        self.__model.save(path)

    def summary(self):
        return self.__model.summary()