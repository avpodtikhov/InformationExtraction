import test
import os
import model

pre = test.Preprocessing('').loadDict('vocab1.npy')
model = model.Model(pre)
with open('example1.txt') as f:
    text = f.read()
pre1 = test.Preprocessing(text)
pre1.loadDict('vocab1.npy')
X = pre1.preprocessing()
del pre1
y = model.predict(X)
post = test.Postprocessing(y)
answer, degree = post.postprocessing()
print('Predicted: ', text[np.min(answer) : np.max(answer) + 1], 'Degree: ', degree)
os.system("pause")