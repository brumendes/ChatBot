import json
import string
import random
import pickle
import asyncio

import nltk
import numpy as np
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
# nltk.download("punkt")
# nltk.download("wordnet")
# nltk.download('omw-1.4')

model = load_model('ipo_model/ipo_model.h5')

#Load the intents file
data_file = open('ipo_model/intents.json')
data = json.load(data_file)

# Load the vocabulary and classes
words = pickle.load(open("ipo_model/words.pkl", "rb"))
classes = pickle.load(open("ipo_model/classes.pkl", "rb"))

lemmatizer = WordNetLemmatizer()

#Preprocessing the input
def clean_text(text):
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return tokens

def bag_of_words(text, vocab):
    tokens = clean_text(text)
    bow = [0] * len(vocab)
    for w in tokens:
        for idx, word in enumerate(vocab):
            if word == w:
                bow[idx] = 1
    return np.array(bow)

def pred_class(text, vocab, labels):
    bow = bag_of_words(text, vocab)
    result = model.predict(np.array([bow]))[0]
    thresh = 0.5
    y_pred = [[indx, res] for indx, res in enumerate(result) if res > thresh]
    y_pred.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in y_pred:
        return_list.append(labels[r[0]])
    return return_list

def get_response(intents_list, intents_json):
    if len(intents_list) == 0:
        result = "sorry! I don't understand."
    else:
        tag = intents_list[0]
        list_of_intents = intents_json["intents"]
        for i in list_of_intents:
            if i["tag"] == tag:
                result = random.choice(i["responses"])
                break
    return result

async def chatbot_response(msg):
    ints = pred_class(msg, words, classes)
    res = get_response(ints, data)
    return res


#Interacting with the chatbot
# print("Press 0 if you don't want to chat with our Chatbot.")
# while True:
#     message = input("")
#     if message == "0":
#         break
#     intents = pred_class(message, words, classes)
#     result = get_response(intents, data)
#     print(result)
