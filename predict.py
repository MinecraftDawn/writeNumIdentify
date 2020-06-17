from keras.models import load_model
import numpy as np

model = load_model("mnist")

def predict(arr:np.array):
    number = arr.reshape((1,28,28,1))

    predict = model.predict(number)

    print(predict)

    return np.argmax(predict, axis=1)[0]