#!/usr/local/bin/python3
import numpy as np

class Preprocessing:
    __text = []
    def __init__(self, text,input_token_dict, text_len=1500,  window_size=50, maxlen_num=30):
        self.__text = text
        self.__text_len = text_len
        self.__window_size = window_size
        self.__maxlen_num = maxlen_num
        self.__input_token_dict = input_token_dict
    
    def __clear(self):
        if len(self.__text) > self.__text_len:
            self.__texts = self.__text[:self.__text_len]

    def __create_new_dataset(self):
        newX = []
        step = self.__window_size // 10
        for i in range(self.__window_size, len(self.__text) + 1, step):
            newX.append(self.__text[i - self.__window_size : i])
        if i < len(self.__text):
            newX.append(self.__text[len(self.__text) - self.__window_size : len(self.__text)])
        self.__X = newX

    def __cut(self):
        encoder_input_data = np.zeros((len(self.__X), self.__window_size, len(self.__input_token_dict)), dtype='float32')
        for i, text in enumerate(self.__X):
            for t, char in enumerate(text):
                if char in self.__input_token_dict:
                    encoder_input_data[i, t, self.__input_token_dict[char]] = 1.
        return encoder_input_data

    def preprocessing(self):
        self.__clear()
        self.__create_new_dataset()
        encoder_input_data = self.__cut()
        return encoder_input_data, self.__X