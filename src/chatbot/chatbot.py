import json
import numpy
import pickle
import random
import tflearn
import tensorflow
from tensorflow.python.framework import ops

tensorflow.compat.v1.disable_resource_variables()

import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

with open("/Python/linkedin-bot/src/chatbot/intents/intents.json") as file:
    data = json.load(file)


try:
    with open("/Python/linkedin-bot/src/chatbot/data.pickle", "rb") as file:
        words, labels, training, output = pickle.load(file)
except FileNotFoundError:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            _words = nltk.word_tokenize(pattern)
            words.extend(_words)
            docs_x.append(_words)
            docs_y.append(intent["tag"])

            if intent["tag"] not in labels:
                labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(words))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w) for w in doc]

        for w in words:
            bag.append(1 if w in wrds else 0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open("/Python/linkedin-bot/src/chatbot/data.pickle", "wb") as file:
        pickle.dump((words, labels, training, output), file)

ops.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)

def chat():
    print("Start talking to the bot!")

    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break
    
        results = model.predict([bag_of_words(inp, words)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]

        for tg in data["intents"]:
            if tg["tag"] == tag:
                responses = tg["responses"]

            print(random.choice(responses))

chat()