import matplotlib
import matplotlib.pyplot as plt
import os
import tensorflow as tf
import numpy as np
import pandas as pd
import h5py
import os.path
import keras
from keras.models import load_model
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.layers.core import Dense, Dropout, Activation,Flatten
from keras.layers.embeddings import Embedding # 詞向量
from keras.layers.core import Dense, Dropout, Activation,Flatten
from tensorflow.python.keras.backend import set_session
from tensorflow.python.keras.models import load_model
import json
import lxml, requests



BASE = os.path.dirname(os.path.abspath(__file__))



#model = load_model(os.path.join(BASE, "testModel1.h5"))

#model.summary()
#model._make_predict_function()
#graph = tf.get_default_graph()
#global model
#model = tf.contrib.keras.models.load_model(os.path.join(BASE, "RNN.h5"))



def predict(input_text):
    

    model = tf.contrib.keras.models.load_model(os.path.join(BASE, "RNN.h5"))
    model.summary()

    token = Tokenizer(num_words=2000)
    with open(os.path.join(BASE, "data.json") , 'r') as reader:
        word_file = json.loads(reader.read())
    #print(type(token))
    token.word_index = word_file
    #print(token.document_count)
    #print(token.word_index)

    input_seq = token.texts_to_sequences([input_text])
    pad_input_seq = sequence.pad_sequences(input_seq,maxlen=100)
    print(input_text)
    print(pad_input_seq)
    #input = "'''"+ input_text + "'''"
    #print(input)

    predict_result = model.predict_classes(pad_input_seq)
    
    #with graph.as_default():
        #predict_result = model.predict_classes(pad_input_seq)

    print(predict_result)

    if predict_result == 1:
        print("1")
        return True
    else:
        print("0")
        return False

def load_in_model():
    global model
    model = tf.contrib.keras.models.load_model(os.path.join(BASE, "RNN.h5"))
    global graph
    graph = tf.get_default_graph()
    model.summary()
    print("model have been load")
    return True

