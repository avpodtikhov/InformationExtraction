import pandas as pd
import numpy as np
import tqdm

class LoadTrainData:
    __texts = []
    __nums = []
    __path = None

    def __init__(self, path):
        self.__texts = []
        self.__path = path
        data = pd.read_csv(self.__path + 'Doc_number.csv', sep=';')
        for doc in tqdm.tqdm(data.values):
            self.__texts.append(self.__get_file(doc[0]))
            self.__nums.append(doc[1])
        self.__texts = np.array(self.__texts)
        self.__nums = np.array(self.__nums)

    def __get_file(self, fn):
        with open(self.__path + 'text_layer/' + fn + '.txt') as f:
            text = f.read()
        return text
    
    def train_test_split(self, test_size=0.2):
        from sklearn.model_selection import train_test_split
        return train_test_split(self.__texts, self.__nums, test_size=test_size, random_state=42)

    @property
    def Texts(self):
        return self.__texts

    @property
    def Nums(self):
        return self.__nums

class TrainPreprocessing:
    __token_dict = {}
    __texts = None
    __maxlen = None
    __n_tokens = None    

    def __init__(self, texts, nums, maxlen=500):
        self.__texts = texts
        self.__nums = nums
        self.__maxlen = maxlen

    def preprocessing(self):
        self.__create_vocab()
        self.__n_tokens = len(self.__token_dict)
        self.__doc_num_to_binary()
        self.__cut_texts()
        return self.__create_dataset()

    @property
    def getDict(self):
        return self.__token_dict
    
    def saveDict(self, path):
        np.save(path, self.__token_dict)
    
    def __create_dataset(self):
        X = []
        y = []
        for i in tqdm.tqdm(range(len(self.__texts))):
            text = self.__texts[i]
            ch_num = 1
            for ch in text:
                if ch_num > self.__maxlen:
                    break
                t = [self.__token_dict[' ']] * (self.__maxlen - ch_num)
                for j in range(ch_num):
                    t.append(self.__token_dict[text[j]])
                X.append(t)
                y.append(self.__ans[i][ch_num - 1])
                ch_num += 1
        return np.array(X), np.array(y)
    
    def __doc_num_to_binary(self):
        import re
        ans = []
        for i in range(len(self.__nums)):
            ans.append(np.full((len(self.__texts[i]), 2), [1, 0]))
            for m in re.finditer(self.__nums[i], self.__texts[i]):
                ans[i][m.start() : m.end(), 0] = 0
                ans[i][m.start() : m.end(), 1] = 1
        self.__ans = ans
    
    def __cut_texts(self):
        for i in range(len(self.__texts)):
            if len(self.__texts[i]) > self.__maxlen:
                self.__texts[i] = self.__texts[i][:self.__maxlen]

    def __create_vocab(self):
        tokens = set()
        for text in self.__texts:
            tokens = tokens | set(text)
        vocab = sorted(tokens)
        j = 0
        for token in vocab:
            self.__token_dict[token] = j
            j = j + 1