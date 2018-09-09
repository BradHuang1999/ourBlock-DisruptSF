# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 01:00:00 2018

@author: Drew

Required packages:
    - Python 3.5
    - Pandas
"""
# Imports
import pandas as pd
import os

# Read in file
module_dir = os.path.abspath(os.path.dirname(__file__))
#data = pd.read_csv(os.path.join(module_dir,'shortPoliceReports.csv'))
data = pd.read_csv(os.path.join(module_dir,'PoliceReports.csv'),encoding='latin3')

# Drop categories that won't be used - reduces memory use.
#data = data.drop(['DayOfWeek', 'Date', 'Time', 'PdDistrict', 'Address', 'Location', 'PdId', 'Resolution', 'Address', 'X', 'Y'], axis=1)
# The first column is finnicky
#data = data.drop(data.columns[0], axis=1)

#Rename the columns
#data = data.rename(columns={'Category': 'category', 'Descript': 'message'})
#data = data.drop_duplicates('message')

# Remove the categories we don't want
data = data[data.category != 'NON-CRIMINAL']
data = data[data.category != 'EXTORTION']
data = data[data.category != 'PORNOGRAPHY/OBSCENE MAT']
data = data[data.category != 'PROSTITUTION']
data = data[data.category != 'BRIBERY']
data = data[data.category != 'FRAUD']
data = data[data.category != 'GAMBLING']
data = data[data.category != 'TREA']
data = data[data.category != 'BAD CHECKS']
data = data[data.category != 'FAMILY OFFENSES']
data = data[data.category != 'EMBEZZLEMENT']
data = data[data.category != 'FORGERY/COUNTERFEITING']
data = data[data.category != 'SUSPICIOUS OCC']
data = data[data.category != 'WARRANTS']
data = data[data.category != 'RUNAWAY']
data = data[data.category != 'TRESPASS']
data = data[data.category != 'VANDALISM']

# Recategorize the fields to general categories
# Larceny/Theft
data['category'] = data['category'].replace(['ROBBERY' , 'BURGLARY' , 'LARCENY/THEFT' , 'VEHICLE THEFT' , 'RECOVERED VEHICLE' , 'STOLEN PROPERTY'], 'Larceny/Theft')
# Violence/Homicide
data['category'] = data['category'].replace(['ASSAULT' , 'SECONDARY CODES' , 'WEAPON LAWS' , 'ARSON' , 'DISORDERLY CONDUCT'], 'Violence/Homicide')
# Drug/Narcotics
data['category'] = data['category'].replace(['LIQUOR LAWS','DRUNKENNESS' , 'DRUG/NARCOTIC'], 'Drug/Narcotics')
# Drug/Narcotics
data['category'] = data['category'].replace(['MISSING PERSON','KIDNAPPING'], 'Kidnapping')
# Traffic Violation
data['category'] = data['category'].replace(['DRIVING UNDER THE INFLUENCE'], 'Traffic Violation')
# Sex Offences
data['category'] = data['category'].replace(['SEX OFFENSES, FORCIBLE' , 'SEX OFFENSES, NON FORCIBLE'], 'Sex Offences')
# Mental Health/Bullying
data['category'] = data['category'].replace(['SUICIDE' , 'LOITERING'], 'Mental Health/Bullying')

# Recategorize some special categories based on their description to general ones.
data.loc[data.message == 'DRIVERS LICENSE, SUSPENDED OR REVOKED', 'category'] = "Traffic Violation"
data.loc[data.message == 'FALSE EVIDENCE OF VEHICLE REGISTRATION', 'category'] = "Traffic Violation"
data.loc[data.message == 'LOST/STOLEN LICENSE PLATE', 'category'] = "Traffic Violation"
data.loc[data.message == 'RECKLESS DRIVING', 'category'] = "Traffic Violation"
data.loc[data.message == 'TRAFFIC COLLISION, HIT & RUN, PROPERTY DAMAGE', 'category'] = "Traffic Violation"
data.loc[data.message == 'TRAFFIC VIOLATION', 'category'] = "Traffic Violation"
data.loc[data.message == 'TRAFFIC VIOLATION ARREST', 'category'] = "Traffic Violation"
data.loc[data.message == 'FAILURE TO REGISTER AS SEX OFFENDER', 'category'] = "Sex Offences"
data.loc[data.message == 'HARASSING PHONE CALLS', 'category'] = "Mental Health/Bullying"
data.loc[data.message == 'OBSCENE PHONE CALLS(S)', 'category'] = "Mental Health/Bullying"
data.loc[data.message == 'POSSESSION OF BURGLARY TOOLS', 'category'] = "Larceny/Theft"
data.loc[data.message == 'POSSESSION OF BURGLARY TOOLS W/PRIORS', 'category'] = "Larceny/Theft"
data.loc[data.message == 'TAMPERING WITH A VEHICLE', 'category'] = "Larceny/Theft"

# Remove other data
data = data[data.category != 'OTHER OFFENSES']

# Merge word frames
import wordreformat as wrf
data = pd.concat([data, wrf.dictcompile()])
data.to_csv('datashort.csv')

"""
ML
"""
import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2

stoppingwords = stopwords.words("english")
stoppingwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your',
                 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it',
                 "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this',
                 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
                 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
                 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after',
                 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
                 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
                 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
                 "don't", 'should', "should've", 'now', "aren't", 'couldn', "couldn't",
                 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn',
                 "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't",
                 'won', "won't", 'wouldn', "wouldn't", 'someone', 'guy', 'girl', 'man', 'women', 'group', 'kept', 'hoodie', 'shorts', 'pants',
                 'dude', 'maybe', 'park', 'wearing', 'a mask']
data['cleaned'] = data['message']

X_train, X_test, y_train, y_test = train_test_split(data['cleaned'], data.category, test_size=0.3)
pipeline = Pipeline([('vect', TfidfVectorizer(ngram_range=(1, 2), stop_words="english", sublinear_tf=True)),
                     ('chi',  SelectKBest(chi2, k=500)),
                     ('clf', LinearSVC(C=1.0, penalty='l1', max_iter=500, dual=False))])
model = pipeline.fit(X_train, y_train)
vectorizer = model.named_steps['vect']
chi = model.named_steps['chi']
clf = model.named_steps['clf']
feature_names = vectorizer.get_feature_names()
feature_names = [feature_names[i] for i in chi.get_support(indices=True)]
feature_names = np.asarray(feature_names)

target_names = ['Drug/Narcotics', 'Kidnapping', 'Larceny/Theft', 'Mental Health/Bullying', 'Sex Offences', 'Traffic Violation', 'Violence/Homicide']
print("top 10 keystoppingwords per class:")
for i, label in enumerate(target_names):
    top10 = np.argsort(clf.coef_[i])[-10:]
    print("%s: %s" % (label, " ".join(feature_names[top10])))

print("Train accuracy score: " + str(model.score(X_train, y_train)))
print("Test accuracy score: " + str(model.score(X_test, y_test)))

def predict(stringin):
    predictstring = stringin
    predictstring = predictstring.lower()
    return model.predict([predictstring])
# Export to CSV
#data.to_csv('output_data.csv')