from keras.utils import to_categorical

class Preprocessing:
    __token_dict = {}
    __text = None
    __maxlen = None
    n_tokens = None    

    def __init__(self, text, maxlen=500):
        self.__text = text
        self.__maxlen = maxlen

    def preprocessing(self):
        ch_num = 1
        X = []
        for ch in self.__text:
            if self.__maxlen > ch_num:
                t = [' '] * (self.__maxlen - ch_num)
                for i in range(ch_num):
                    t.append(self.__text[i])
            else:
                t = []
                for i in range(ch_num - self.__maxlen, ch_num):
                    t.append(self.__text[i])
            X.append(t)
            ch_num += 1
        for i in range(len(X)):
            for j in range(len(X[i])):
                if X[i][j] not in self.__token_dict:
                    X[i][j] = self.__token_dict[' ']
                else:
                    X[i][j] = self.__token_dict[X[i][j]]
        X = np.array(X)
        X = to_categorical(X, num_classes=self.n_tokens)
        return X

    def loadDict(self, path):
        self.__token_dict = np.load(path).item()
        self.n_tokens = len(self.__token_dict)
        return self.n_tokens

class Postprocessing:
    __y_pred = None
    __y_prob = None
    __len = 0
    
    def __init__(self, y):
        self.__y_pred = y[0]
        self.__y_prob = y[1]
        self.__len = y[0].shape[0]
    
    def __fill_zero_center(self):
        for i in range(1, self.__len):
            if self.__y_pred[i] == 0:
                if (self.__y_pred[i-1] == 1) and (self.__y_pred[i+1] == 1):
                    self.__y_pred[i] = 1

    def postprocessing(self):
        self.__fill_zero_center()
        j = 0
        answer = []
        degrees = []
        while j < self.__len:
            if self.__y_pred[j] == 1:
                i = j
                degrees.append(0.)
                prob_ans = []
                if j != 0:
                    if self.__y_prob[j - 1][1] > 0.2:
                        prob_ans.append(j - 1)
                        degrees[-1] += self.__y_prob[j-1][1]
                while i < self.__len:
                    if self.__y_pred[i] != 1:
                        break;
                    else:
                        prob_ans.append(i)
                        degrees[-1] += self.__y_prob[i][1]
                    i += 1
                if (i + 1 < self.__len):
                    if self.__y_prob[i + 1][1] > 0.2:
                        prob_ans.append(i + 1)
                        degrees[-1] += self.__y_prob[i][1]
                degrees[-1] /= len(prob_ans)
                answer.append(prob_ans)
                j = i
            j += 1
        i = 0
        for j in range(len(answer)):
            if degrees[j] > degrees[i]:
                i = j
        if (len(answer) == 0):
            return 'б/н', 0.
        self.answer = answer
        self.degrees = degrees
        self.index = i
        return answer[i], degrees[i]

