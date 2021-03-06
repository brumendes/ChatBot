import json
import string
import random

import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
import tensorflow as tf
from keras import Sequential
from keras.layers import Dense, Dropout
nltk.download("punkt")
nltk.download("wordnet")
nltk.download('omw-1.4')

#Load the intents file
data_file = open('intents.json')
data = json.load(data_file)

#Create data_x and data_y
words = []
classes = []
data_x = []
data_y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        tokens = nltk.word_tokenize(pattern)
        words.extend(tokens)
        data_x.append(pattern)
        data_y.append(intent["tag"])

    if intent["tag"] not in classes:
        classes.append(intent["tag"])

#Initialize lemmatizer to get stem of words
lemmatizer = WordNetLemmatizer()

#lemmatize all words in the vocab and convert to lowercase if words don't appear in punctuation
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in string.punctuation]

#sort vocab and classes in alphabetical order and taking the # set to ensure no duplicates occur
words = sorted(set(words))
classes = sorted(set(classes))

#Convert text to numbers - more machine learning friendly
training = []
out_empty = [0] * len(classes)

#Create the bag of words model
for idx, doc in enumerate(data_x):
    bow = []
    text = lemmatizer.lemmatize(doc.lower())
    for word in words:
        bow.append(1) if word in text else bow.append(0)
    #mark the index of class that the current pattern is associated
    output_row = list(out_empty)
    output_row[classes.index(data_y[idx])] = 1
    #add the one hot encoded bow and associated classes to training
    training.append([bow, output_row])

#shuffle the data and convert to array
random.shuffle(training)
training = np.array(training, dtype=object)
#split features and target labels
train_x = np.array(list(training[:, 0]))
train_y = np.array(list(training[:, 1]))

# The Neural Network Model
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation="softmax"))
adam = tf.keras.optimizers.Adam(learning_rate=0.01, decay=1e-6)
model.compile(
    loss="categorical_crossentropy",
    optimizer=adam,
    metrics=["accuracy"]
)
print(model.summary())
model.fit(x=train_x, y=train_y, epochs=150, verbose=1)
model.save('ipo_model')