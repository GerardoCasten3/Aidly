# Importamos librerias necesarias
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

# Creamos instancia de lematizador
lemmatizer = WordNetLemmatizer()

# Cargamos archivos
intents = json.loads(open('dataset/spanish_intents.json', encoding='utf-8').read())
words = pickle.load(open('dataset/words.pkl', 'rb'))
classes = pickle.load(open('dataset/classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

# Creamos función para limpiar la entrada del usuario
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# Creamos función para crear la bolsa de palabras desde la entrada del usuario
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Creamos función para predecir la clase de la intención
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

# Creamos función para obtener la respuesta
def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result