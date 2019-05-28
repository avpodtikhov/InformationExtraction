#!/usr/local/bin/python3
import pandas as pd
import numpy as np
import tqdm
import pickle

class LoadTrainData:
    __texts = []
    __nums = []
    __path = None

    def load_data(self, path):
        self.__texts = []
        self.__path = pathl
        data = pd.read_csv(self.__path + 'Doc_number.csv', sep=';')
        for doc in tqdm.tqdm(data.values):
            self.__texts.append(self.__get_file(doc[0]).lower())
            self.__nums.append('\t' + doc[1].lower() + '\n')

    def __get_file(self, fn):
        with open(self.__path + 'text_layer/' + fn + '.txt') as f:
            text = f.read()
        return text
    
    def train_test_split(self, test_size=0.2):
        from sklearn.model_selection import train_test_split
        return train_test_split(self.__texts, self.__nums, test_size=test_size, random_state=42)
    
    def load_pickle(self, text_path, num_path):
        with open(text_path, 'rb') as f:
            self.__texts = pickle.load(f)
        with open(num_path, 'rb') as f:
            self.__nums = pickle.load(f)
            
    def save_pickle(self, text_path, num_path):
        with open(text_path, 'wb') as f:
            pickle.dump(self.__texts, f)
        with open(num_path, 'wb') as f:
            pickle.dump(self.__nums, f)
    @property
    def Texts(self):
        return self.__texts

    @property
    def Nums(self):
        return self.__nums