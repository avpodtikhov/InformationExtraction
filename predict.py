#!/usr/local/bin/python3
import train
import numpy as np
from collections import Counter
import test_preprocessing
import pandas as pd
import os

class Predict:
    def __init__(self, encoder_model, decoder_model, input_token_dict, output_token_dict):
        self.encoder_model = encoder_model
        self.decoder_model = decoder_model
        self.reverse_target_char_index = dict((i, char) for char, i in output_token_dict.items())
        self.input_token_dict = input_token_dict
        self.output_token_dict = output_token_dict

    def __decode_sequence(self, input_seq, input_text):
        states_value = self.encoder_model.predict(input_seq)
        target_seq = np.zeros((1, 1, len(self.output_token_dict)))
        target_seq[0, 0, self.output_token_dict['\t']] = 1.
        stop_condition = False
        decoded_sentence = ''
        proba = 1.
        while not stop_condition:
            output_tokens, h, c = self.decoder_model.predict(
                [target_seq] + states_value)
            prob_ans = np.argsort(output_tokens[0, -1, :])[::-1]
            for i in prob_ans:
                sampled_token_index = i
                sampled_char = self.reverse_target_char_index[i]
                if input_text.find(decoded_sentence + sampled_char) != -1 or sampled_char == '\n':
                    break
            proba = proba + output_tokens[0, -1, :][i]
            decoded_sentence += sampled_char
            if (sampled_char == '\n' or
            len(decoded_sentence) > 30):
                stop_condition = True
            target_seq = np.zeros((1, 1, len(self.output_token_dict)))
            target_seq[0, 0, sampled_token_index] = 1.
            states_value = [h, c]
        proba -= 1
        proba /= len(decoded_sentence)
        return decoded_sentence, proba
    
    def __predict_one(self, text):
        p = test_preprocessing.Preprocessing(text, self.input_token_dict)
        test_data, new_texts1 = p.preprocessing()
        prob_ans = []
        proba = {}
        for i in range(test_data.shape[0]):
            input_seq = test_data[i:i+1]
            decoded_sentence, p = self.__decode_sequence(input_seq, new_texts1[i])
            proba[decoded_sentence] = p
            if decoded_sentence != '\n':
                prob_ans.append(decoded_sentence)
        str = ''
        if len(prob_ans) == 0:
            return 0, ''
        else:  
            str = Counter(prob_ans).most_common(1)[0][0]
            if proba[str] >= 0.5 and str[:-1] != '':
                str = str[:-1]
                pos = text[0].find(str)
                for c in range(pos - 1, -1, -1):
                    if text[0][c] != ' ':
                        str = text[0][c] + str
                    else:
                        break
                for c in range(pos + len(str), len(text[0])):
                    if text[0][c] != ' ':
                        str = str + text[0][c]
                    else:
                        break
                return 1, str
            else:
                return 0, ''
    
    def predict(self, path):
        d1 = {'name' : [], 'value' : []}
        d0 = {'name' : []}
        for filename in os.listdir(path):
            text = ''
            with open(path + '/' + filename, 'r') as f:
                text = f.read()
            cl, ans = self.__predict_one(text)
            if cl:
                d1['name'].append(filename)
                d1['value'].append(ans)
            else:
                d0['name'].append(filename)
        df1 = pd.DataFrame(d1)
        df1.to_csv('./doc_num.csv', index=False)
        df0 = pd.DataFrame(d0)
        df0.to_csv('./doc_num_manual.csv', index=False)
        return d1, d0