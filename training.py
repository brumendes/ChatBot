import json
import string
import random
import pickle
import nltk
import numpy as np
from nltk.stem import RSLPStemmer, WordNetLemmatizer
import tensorflow as tf
from keras import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
nltk.download("punkt")
nltk.download("wordnet")
nltk.download('omw-1.4')

#Load the intents file
with open('ipo_model/intents.json') as data_file:
    data = json.load(data_file)

#Create data_x and data_y
words = []
classes = []
documents = []
igonore_words = ["?", "!"]
stopwords = nltk.corpus.stopwords.words('portuguese')
print(stopwords)

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        tokens = nltk.word_tokenize(pattern, language="portuguese")
        words.extend(tokens)
        documents.append((tokens, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

#Initialize lemmatizer to get stem of words
lemmatizer = WordNetLemmatizer()
lemmatizer_pt = RSLPStemmer()

#lemmatize all words in the vocab and convert to lowercase if words don't appear in punctuation
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in string.punctuation]
print(words)

#sort vocab and classes in alphabetical order and taking the # set to ensure no duplicates occur
words = sorted(set(words))
classes = sorted(set(classes))

# documents = combination between patterns and intents
print(len(documents), "documents")

# classes = intents
print(len(classes), "classes", classes)

# words = all words, vocabulary
print(len(words), "unique lemmatized words", words)
pickle.dump(words,open("ipo_model/words.pkl", "wb"))
pickle.dump(classes, open("ipo_model/classes.pkl", "wb"))

#Convert text to numbers - more machine learning friendly
training = []
out_empty = [0] * len(classes)

#Create the bag of words model
for idx, doc in enumerate(documents):
    bow = []
    pattern_words = doc[0]
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    for word in words:
        bow.append(1) if word in pattern_words else bow.append(0)
    #mark the index of class that the current pattern is associated
    output_row = list(out_empty)
    output_row[classes.index(doc[1])] = 1
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
sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(
    loss="categorical_crossentropy",
    optimizer=sgd,
    metrics=["accuracy"]
)
print(model.summary())
hist = model.fit(x=train_x, y=train_y, epochs=150, batch_size=5, verbose=1)
model.save('ipo_model/ipo_model.h5', hist)
print("model created")