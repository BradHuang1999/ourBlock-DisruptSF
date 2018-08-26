# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 11:33:53 2018

@author: Drew

This is a basic word2vec algorithm which will plot the vector position of
words relative to one another on the training corpus. The training data is
limited, and will be expanded in future
"""
# Imports
from word2vec import *
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# Define a corpus of phrases that may act as possible submissions via the app
# These have been taken from the file in the GitHub.
corpus = [
          "He’s stabbing her", 
          "She’s stabbing him", 
          "He stabbed her", 
          "She’s stabbed him", 
          "Someone is getting stabbed", 
          "Somebody is shot", 
          "He got shot", 
          "She is shot", 
          "He’s bleeding a lot", 
          "She’s bleeding a lot", 
          "Someone is bleeding a lot", 
          "There is a person who is bleeding a lot", 
          "He's pulling out a gun", 
          "He has a knife",
          'He has a gun',
          'He has a knife',
          'He will shoot',
          "He’s hitting her", 
          "She’s hitting him", 
          "A person just got punched", 
          "A guy was kicking another person who was on the ground", 
          "He hits me", "She hits me", 
          "He pinned her down", 
          "She pinned him down",
          "A red car was stolen", 
          "A green car was stolen", 
          "That car was hijacked", 
          "An alarm in a car is going off", 
          "My car is gone", 
          "Somebody stole my car", 
          "Somebody took my car", 
          "car", 
          "van", 
          "suv", 
          "tesla", 
          "toyota"
          "Somebody broke into my house", 
          "Somebody stole something in my apartment", 
          "Somebody stole something in my house", 
          "Somebody stole something in my condo", 
          "Somebody broke into my apartment unit", 
          "Somebody broke into my condo", 
          "I think he’s breaking into that house", 
          "I think she’s breaking into that condo", 
          "I think he’s breaking into that apartment", 
          "house", 
          "apartment", 
          "condo",
          "He stole my purse", 
          "She stole my money", 
          "Someone took my phone", 
          "Someone ran off after taking something from a person", 
          "He stole my belongings", 
          "Somebody robbed me", 
          "laptop was stolen", 
          "computer was stolen",
          "He stole my bike", 
          "She stole my bike", 
          "My bike is gone", 
          "Someone took my bike", 
          "bike",
          "The car is swerving erratically", 
          "The car moving weird", 
          "I think he’s driving drunk", 
          "I think she’s driving drunk", 
          "Driving drunk",
          "He raped her", 
          "She raped him", 
          "He's touching her inappropriately", 
          "She's touching her inappropriately",
          "I don't think he's ok", 
          "He's shouting", 
          "He's yelling at no one", 
          "I think he has mental health issues", 
          "He's hurting himself", 
          "She's hurting herself", 
          "self harm", 
          "I'm going to kill myself",
          "He's going to kill himself", 
          "She's going to kill herself",
          "The car is swerving erratically", 
          "The car moving weird", 
          "I think he’s driving drunk", 
          "I think she’s driving drunk", 
          "Driving drunk",
          "Heroin needles", 
          "This person seems high", 
          "ectasy", 
          "Amphetamines", 
          "Cocaine", 
          "Methamphetamine", 
          "crack", 
          "on drugs",
          "Marijuana Dispensary", 
          "weed", 
          "smells like weed", 
          "Marijuana",
          "skunk",
          "People doing dumb things because they are drunk", 
          "drunk in public", 
          "smells like alcohol",
          "really drunk guy",
          "drunk girl on subway",
          "guy throwing up",
          "girl throwing up"]

# Convert all characters to lowercase
newcorpus = []
for text in corpus:
    text = text.lower()
    newcorpus.append(text)

# Function to remove any filler words that do not add value to the report
def excess_word_remover(corpus):
    filler_words = ['was', 'to', 'from', 'off', 'after', 'an', 'because', 'on', 
                  'up', 'person', 'like', 'going', 'herself', 'himself', 'he', 
                  "i'm", "she's", "he's", 'there', 'is', 'a', 'will', 'be', 
                  'my', 'was', 'on', 'like', 'this', 'seems', 'I', 'i', 
                  'think', 'the', 'has', "don't", 'into', 'that', 'a', 'lot',
                  'a']
    maincorpus = []
    # Seperate words
    for text in corpus:
        temp = text.split(' ')
        # Remove fillers
        for filler in filler_words:
            if filler in temp:
                temp.remove(filler)
        # Rejoin words for sentance
        maincorpus.append(" ".join(temp))
    return maincorpus

# Execute function to remove filler words
corpus = excess_word_remover(newcorpus)

words = []
for text in corpus:
    for word in text.split(' '):
        words.append(word)

words = set(words)


# Invoke word2vec
word2int = {}

for i,word in enumerate(words):
    word2int[word] = i

sentences = []
for sentence in corpus:
    sentences.append(sentence.split())
   
# Look at importance relative to 4 words around the word
WINDOW_SIZE = 4

data = []
for sentence in sentences:
    for idx, word in enumerate(sentence):
        for neighbor in sentence[max(idx - WINDOW_SIZE, 0) : min(idx + WINDOW_SIZE, len(sentence)) + 1] : 
            if neighbor != word:
                data.append([word, neighbor])
       
# Define dataframe of words and labels         
wordsDataframe = pd.DataFrame(data, columns = ['input', 'label'])

# Create one hot encoding length by taking the number of words in vocabulary
oneHotEncoding = len(words)

# function to convert numbers to one hot vectors
def oneHotEncoder(data_point_index):
    oneHot = np.zeros(oneHotEncoding)
    oneHot[data_point_index] = 1
    return oneHot

# Define variables
X = [] # input word
Y = [] # target word

# Append from dataframe
for x, y in zip(wordsDataframe['input'], wordsDataframe['label']):
    X.append(oneHotEncoder(word2int[ x ]))
    Y.append(oneHotEncoder(word2int[ y ]))

# Convert to numpy array
X_train = np.asarray(X)
Y_train = np.asarray(Y)

# Create Tensorflow shapes and placeholers for input and label
x = tf.placeholder(tf.float32, shape=(None, oneHotEncoding))
y_label = tf.placeholder(tf.float32, shape=(None, oneHotEncoding))

# 2D Visualization
EMBEDDING_DIM = 2 

# Create a single hidden layer with single neuron
W1 = tf.Variable(tf.random_normal([oneHotEncoding, EMBEDDING_DIM]))
b1 = tf.Variable(tf.random_normal([1])) #bias
hidden_layer = tf.add(tf.matmul(x,W1), b1)

# Create softmax output to yielf maximum
W2 = tf.Variable(tf.random_normal([EMBEDDING_DIM, oneHotEncoding]))
b2 = tf.Variable(tf.random_normal([1]))
prediction = tf.nn.softmax(tf.add( tf.matmul(hidden_layer, W2), b2))

# Use cross entopy loss
loss = tf.reduce_mean(-tf.reduce_sum(y_label * tf.log(prediction), axis=[1]))

# Training and optimization
#train_op = tf.train.GradientDescentOptimizer(0.001).minimize(loss)
train_op = tf.train.AdamOptimizer(0.0001).minimize(loss)

# Set Tensorflow to run
sess = tf.Session()
init = tf.global_variables_initializer()
sess.run(init) 

# Training loop
epochs = 100000
for i in range(epochs):
    # X_train input is one hot encoded word
    # Y_train is the neighbouring word
    sess.run(train_op, feed_dict={x: X_train, y_label: Y_train})
    if i % 5000 == 0:
        print('The number of epochs is {0} and the loss is {1}'.format(str(i), sess.run(loss, feed_dict={x: X_train, y_label: Y_train})))
        
# Define the vectors
vectors = sess.run(W1 + b1)
print(vectors)
w2v_wordsDataframe = pd.DataFrame(vectors, columns = ['x1', 'x2'])
w2v_wordsDataframe['word'] = words
w2v_wordsDataframe = w2v_wordsDataframe[['word', 'x1', 'x2']]
print(w2v_wordsDataframe)


# Copy pasted from a Stack Overflow answer that nicely plots the vectors on a graph
fig, ax = plt.subplots()
for word, x1, x2 in zip(w2v_wordsDataframe['word'], w2v_wordsDataframe['x1'], w2v_wordsDataframe['x2']):
    ax.annotate(word, (x1,x2 ))    
PADDING = 1.0
x_axis_min = np.amin(vectors, axis=0)[0] - PADDING
y_axis_min = np.amin(vectors, axis=0)[1] - PADDING
x_axis_max = np.amax(vectors, axis=0)[0] + PADDING
y_axis_max = np.amax(vectors, axis=0)[1] + PADDING 
plt.xlim(x_axis_min,x_axis_max)
plt.ylim(y_axis_min,y_axis_max)
plt.rcParams["figure.figsize"] = (10,10)
plt.show()
