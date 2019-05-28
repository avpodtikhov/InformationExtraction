#!/usr/local/bin/python3
import load_train, train_preprocessing, batch_gen
from sklearn.model_selection import train_test_split
from keras.models import Model, load_model
from keras.layers import Input, LSTM, Dense, Bidirectional, Dropout, Embedding, GlobalMaxPool1D, MaxPooling1D, Conv1D
import pickle

class Seq2SeqModel:
    def __init__(self, input_token_dict=None, output_token_dict=None, batch_size=None, epochs=None, latent_dim=None):
        self.input_token_dict = input_token_dict
        self.output_token_dict = output_token_dict
        self.в = batch_size
        self.latent_dim = latent_dim
        self.epochs = epochs
        
    def encdec(self):
        try:
            encoder_inputs = self.model.input[0]
            encoder_outputs, state_h_enc, state_c_enc = self.model.get_layer('lstm_2').output
            encoder_states = [state_h_enc, state_c_enc]
            encoder_model = Model(encoder_inputs, encoder_states)

            decoder_state_input_h = Input(shape=(self.latent_dim,))
            decoder_state_input_c = Input(shape=(self.latent_dim,))
            decoder_inputs = self.model.input[1]
            decoder_lstm = self.model.get_layer('lstm_3')

            decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
            decoder_outputs1, state_h, state_c = decoder_lstm(decoder_inputs, initial_state=decoder_states_inputs)
            decoder_states = [state_h, state_c]

            decoder_dense = self.model.get_layer('dense_2')

            decoder_outputs = decoder_dense(decoder_outputs1)
            decoder_model = Model(
                [decoder_inputs] + decoder_states_inputs,
                [decoder_outputs] + decoder_states)
        except:
            encoder_inputs = self.model.input[0]
            encoder_outputs, state_h_enc, state_c_enc = self.model.get_layer('lstm_2').output
            encoder_states = [state_h_enc, state_c_enc]
            encoder_model = Model(encoder_inputs, encoder_states)

            decoder_state_input_h = Input(shape=(self.latent_dim,))
            decoder_state_input_c = Input(shape=(self.latent_dim,))
            decoder_inputs = self.model.input[1]
            decoder_lstm = self.model.get_layer('lstm_3')

            decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
            decoder_outputs1, state_h, state_c = decoder_lstm(decoder_inputs, initial_state=decoder_states_inputs)
            decoder_states = [state_h, state_c]

            decoder_dense = self.model.get_layer('dense_2')

            decoder_outputs = decoder_dense(decoder_outputs1)
            decoder_model = Model(
                [decoder_inputs] + decoder_states_inputs,
                [decoder_outputs] + decoder_states)
        return encoder_model, decoder_model
    
    def fit(self, X, y):
        input_tokens = len(self.input_token_dict)
        output_tokens = len(self.output_token_dict)
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.12)
        encoder_inputs = Input(shape=(50, input_tokens))
        encoder_dense = Dense(8, activation='relu')(encoder_inputs)
        encoder = Bidirectional(LSTM(self.latent_dim, return_sequences=True))(encoder_dense)
        drop = Dropout(0.2)(encoder)
        encoder2 = LSTM(self.latent_dim, return_state=True)
        encoder_outputs, state_h, state_c = encoder2(drop)
        encoder_states = [state_h, state_c]
        decoder_inputs = Input(shape=(None, output_tokens))
        decoder_lstm = LSTM(self.latent_dim, return_sequences=True, return_state=True)
        decoder_outputs, _, _ = decoder_lstm(decoder_inputs,
                                             initial_state=encoder_states)
        decoder_dense = Dense(output_tokens, activation='softmax')
        decoder_outputs = decoder_dense(decoder_outputs)
        model2 = Model([encoder_inputs, decoder_inputs], decoder_outputs)
        model2.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        training_generator = batch_gen.DataGenerator(X_train, y_train, self.batch_size, self.input_token_dict, self.output_token_dict)
        validation_generator = batch_gen.DataGenerator(X_val, y_val, self.batch_size, self.input_token_dict, self.output_token_dict)
        model2.fit_generator(generator=training_generator,
                             validation_data=validation_generator,
                             epochs=self.epochs)
        self.model = model2
        self.save_model('./model/')
    
    def save_model(self, path):
        self.model.save(path + 'model.h5')
        with open(path + 'input_dict.pkl', 'wb') as f:
            pickle.dump(input_token_dict, f)
        with open(path + 'output_dict.pkl', 'wb') as f:
            pickle.dump(output_token_dict, f)

    def model_load(self, path):
        self.model = load_model(path + 'model.h5')
        self.model.summary()
        with open(path + 'input_dict.pkl', 'rb') as f:
            self.input_token_dict = pickle.load(f)
        with open(path + 'output_dict.pkl', 'rb') as f:
            self.output_token_dict = pickle.load(f)
        return self.input_token_dict, self.output_token_dict

if __name__ == "__main__":
    train = load_train.LoadTrainData()
    train.load_pickle('./train/texts.pkl', './train/nums.pkl')
    train_texts, test_texts, train_nums, test_nums = train.train_test_split()
    pre = train_preprocessing.TrainPreprocessing(train_texts, train_nums)
    X, y = pre.preprocessing()
    input_token_dict, output_token_dict = pre.Dicts()
    m = Seq2SeqModel(input_token_dict, output_token_dict, 2, 10, 32)
    m.fit(X, y)