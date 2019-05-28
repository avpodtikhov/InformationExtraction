#!/usr/local/bin/python3
import numpy as np
import keras

class DataGenerator(keras.utils.Sequence):
    def create_new_dataset(self, X, y, window_size):
        newX = []
        newY = []
        step = window_size // 10
        for text,num in zip(X, y):
            for i in range(window_size, len(text) + 1, step):
                newX.append(text[i - window_size : i])
                if newX[-1].find(num[1:-1]) != -1:
                    newY.append(num)
                else:
                    newY.append('\t\n')
            if i < len(text):
                newX.append(text[len(text) - window_size : len(text)])
                if newX[-1].find(num[1:-1]) != -1:
                    newY.append(num)
                else:
                    newY.append('\t\n')
        return newX, newY

    def cut(self, X, y, maxlen_text = 100, maxlen_num=30):
        encoder_input_data = np.zeros((len(X), maxlen_text, len(self.input_token_dict)), dtype='float32')
        decoder_input_data = np.zeros((len(X), maxlen_num, len(self.output_token_dict)), dtype='float32')
        decoder_target_data = np.zeros((len(X), maxlen_num, len(self.output_token_dict)),dtype='float32')
        for i, (text, num) in enumerate(zip(X, y)):
            for t, char in enumerate(text):
                if char in self.input_token_dict:
                    encoder_input_data[i, t, self.input_token_dict[char]] = 1.
            for t, char in enumerate(num):
                if char in self.output_token_dict:
                    decoder_input_data[i, t, self.output_token_dict[char]] = 1.
                    if t > 0:
                        decoder_target_data[i, t - 1, self.output_token_dict[char]] = 1.
        return encoder_input_data, decoder_input_data, decoder_target_data

    def __init__(self, x_set, y_set, batch_size, input_token_dict, output_token_dict,shuffle=True):
        self.X, self.y = x_set, y_set
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.on_epoch_end()
        self.input_token_dict = input_token_dict
        self.output_token_dict = output_token_dict

    def __len__(self):
        return int(np.ceil(len(self.X) / float(self.batch_size)))

    def __getitem__(self, idx):
        indexes = self.indexes[idx*self.batch_size:(idx+1)*self.batch_size]
        
        batch_x = [self.X[k] for k in indexes]
        batch_y = [self.y[k] for k in indexes]
        
        new_texts1, new_nums1 = self.create_new_dataset(batch_x, batch_y, 50)
        encoder_input_data, decoder_input_data, decoder_target_data = self.cut(new_texts1, new_nums1, 50, 30)
        return [encoder_input_data, decoder_input_data], decoder_target_data
    
    def on_epoch_end(self):
        self.indexes = np.arange(len(self.X))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)
