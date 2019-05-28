#!/usr/local/bin/python3
import numpy as np

class TrainPreprocessing:
    __texts = []
    __nums = []
    def __init__(self, texts, nums, text_len=1500, doc_num=80000):
        self.__texts = texts
        self.__nums = nums
        self.__text_len = text_len
        self.__doc_num = doc_num
    
    def __clear(self):
        i = 0
        while i < len(self.__nums):
            self.__nums[i] = self.__nums[i].replace('№', '')
            num_idx = self.__texts[i].find(self.__nums[i][1:-1])
            if len(self.__texts[i]) > self.__text_len:
                self.__texts[i] = self.__texts[i][:self.__text_len]
            if num_idx >= self.__text_len - len(self.__nums[i][1:-1]):
                del self.__texts[i]
                del self.__nums[i]
                i -= 1
            i += 1
        for i in range(len(self.__nums) - 1, -1, -1):
            if self.__nums[i][1:-1].find('акт') != -1:
                del self.__nums[i]
                del self.__texts[i]
        return

    def __expand_dataset(self):
        num_samples = self.__doc_num // len(self.__texts) + 1
        newX = []
        newY = []
        for i in range(len(self.__texts)):
            samples = np.random.choice(range(len(self.__texts)), num_samples, replace=False)
            if np.in1d(i, samples)[0]:
                samples = np.append(samples, i)
            for idx in samples:
                newX.append(self.__texts[i].replace(' ' + self.__nums[i][1:-1] + ' ',  ' ' + self.__nums[idx][1:-1] + ' '))
                newY.append(self.__nums[idx])
        self.__texts = newX
        self.__nums = newY
        return

    def __create_vocab(self):
        tokens = set()
        for text in self.__texts:
            tokens = tokens | set(text)
        vocab = sorted(tokens)
        j = 0
        token_dict = {}
        for token in vocab:
            token_dict[token] = j
            j = j + 1
        tokens = set()
        for text in self.__nums:
            tokens = tokens | set(text)
        vocab = sorted(tokens)
        j = 0
        token_dict1 = {}
        for token in vocab:
            token_dict1[token] = j
            j = j + 1
        self.__input_token_dict = token_dict
        self.__output_token_dict = token_dict1
        return
    
    def Dicts(self):
        return self.__input_token_dict, self.__output_token_dict

    def pnreprocessing(self):
        self.__clear()
        self.__create_vocab()
        self.__expand_dataset()
        return self.__texts, self.__nums