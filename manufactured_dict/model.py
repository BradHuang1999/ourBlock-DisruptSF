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

# Read in file
data = pd.read_csv('shortPoliceReports.csv')
#data = pd.read_csv('PoliceReports.csv')



# Drop categories that won't be used - reduces memory use.
data = data.drop(['DayOfWeek', 'Date', 'Time', 'PdDistrict', 'Address', 'Location', 'PdId', 'Resolution', 'Address', 'X', 'Y'], axis=1)
# The first column is finnicky
data = data.drop(data.columns[0], axis=1)


#Rename the columns
data = data.rename(columns={'Category': 'category', 'Descript': 'message'})


data = data.drop_duplicates('message')

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


#data = data.replace({'THEFT': 'STOLE, steal'}, regex=True)
#data = data.replace({'AUTOMOBILE': 'car, chevy, toyota, tesla, wheels, bmw, mercedes'}, regex=True)
#data = data.replace({'AUTO': 'car, chevy, toyota, tesla, wheels, bmw, mercedes'}, regex=True)
#data = data.replace({'POSSESSION': 'has, had, selling, taking, snorting, smoking, taking'}, regex=True)
#data = data.replace({'POSS': 'has, had, kept, hid, '}, regex=True)
#data = data.replace({'PARAPHERNALIA': 'bong, needles, joints, injection'}, regex=True)
#data = data.replace({'FIREARM': 'gun, rifle, glock, handgun, pistol'}, regex=True)
#data = data.replace({'SEXUAL BATTERY': 'groped, raped'}, regex=True)
#data = data.replace({'HARASSING PHONE CALLS': 'prank calls'}, regex=True)
#data = data.replace({'BURGLARY': 'broke in, stole, theft'}, regex=True)
#data = data.replace({'FOUND PERSON': 'found missing person'}, regex=True)
#data = data.replace({'INFLICT INJURY': 'hit, punched, kicked, slapped'}, regex=True)
#data = data.replace({'COHABITEE': 'roommate, friend'}, regex=True)
#data = data.replace({'ASSAULT WITH CAUSTIC CHEMICALS': 'sprayed, splashed, threw acid'}, regex=True)
#data = data.replace({'DEADLY WEAPON': 'gun, knife, rifle, assualt rifle, bat'}, regex=True)
#data = data.replace({'BATTERY': 'beat up, hit, punched, kicked, slapped, stomped'}, regex=True)
#data = data.replace({'DOMESTIC VIOLENCE': 'beat, girlfriend, wife, boyfriend, husband, slapped, arguing, hit'}, regex=True)
#data = data.replace({'PARTNER': 'girlfriend, wife, boyfriend, husband, partner'}, regex=True)
#data = data.replace({'FORCIBLE ENTRY': 'break in, broke in, broke lock, cut lock, broke window'}, regex=True)
#data = data.replace({'UNLAWFUL ENTRY': 'break in, broke in, broke lock, cut lock, broke window, broke door, broke window, trespassed'}, regex=True)
#data = data.replace({'THREATS AGAINST LIFE': 'threats, threatened'}, regex=True)
#data = data.replace({'AMMUNITION': 'bullets'}, regex=True)
#data = data.replace({'AGGRAVATED ASSAULT OF POLICE OFFICER,BODILY FORCE': 'hit cop, killed cop, punched cop, punched police, assaulted police'}, regex=True)
#data = data.replace({'AGGRAVATED ASSAULT WITH A GUN': 'shot, killed with gun, popped, gun, pistol'}, regex=True)
#data = data.replace({'AGGRAVATED ASSAULT WITH A KNIFE': 'stabbed, knife, shanked, shank, stab, poked, bleeding'}, regex=True)
#data = data.replace({'AGGRAVATED ASSAULT WITH BODILY FORCE': 'punched, kicked, hit, beat up, slapped, smacked, ganged up, fight, brawl, boxing, team up'}, regex=True)
#data = data.replace({'ATTEMPTED ARSON': 'tried to burn down, fire, arson, molotov cocktail, burnt, matches, gas, oil, petrol'}, regex=True)
#data = data.replace({'HOMICIDE': 'murder, kill, shot, gun, killed'}, regex=True)
#data = data.replace({'ATTEMPTED ROBBERY': 'rob, robbery, robbed'}, regex=True)
#data = data.replace({'SUICIDE': 'killed himself, suicide, jumped, hanged'}, regex=True)
#data = data.replace({'VEHICLE': 'car, truck, bike'}, regex=True)
#data = data.replace({'BICYCLE': 'bike, bicycle'}, regex=True)
#data = data.replace({'CARJACKING': 'stole car, carjacking'}, regex=True)

import wordreformat as wrf

data = pd.concat([data, wrf.dictcompile()])

"""
ML
"""
import re
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2

removal = SnowballStemmer('english')
stoppingwords = stopwords.words("english")


#stoppingwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 
#                 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', 
#                 "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 
#                 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 
#                 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 
#                 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 
#                 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 
#                 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 
#                 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
#                 "don't", 'should', "should've", 'now', "aren't", 'couldn', "couldn't",
#                 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn',
#                 "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 
#                 'won', "won't", 'wouldn', "wouldn't", 'someone', 'guy', 'girl', 'man', 'women', 'group', 'kept', ]

data['cleaned'] = data['message'].apply(lambda x: " ".join([removal.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in stoppingwords]).lower())

#X_train, X_test, y_train, y_test = train_test_split(data['message'], data.category, test_size=0.3)

X_train, X_test, y_train, y_test = train_test_split(data['cleaned'], data.category, test_size=0.3)

pipeline = Pipeline([('vect', TfidfVectorizer(ngram_range=(1, 2), stop_words="english", sublinear_tf=True)),
                     ('chi',  SelectKBest(chi2, k=500)),
                     ('clf', LinearSVC(C=1.0, penalty='l1', max_iter=30000, dual=False))])


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

print("accuracy score: " + str(model.score(X_test, y_test)))

def predict(stringin):
    predictstring = stringin
    predictstring = predictstring.lower()
    predictstring = predictstring.join([removal.stem(i) for i in re.sub("[^a-zA-Z]", " ", predictstring).split() if i not in stoppingwords]).lower()
    print(model.predict([predictstring]))

# Tests
predict('He was doing meth in the park')
predict('I just saw someone get killed at 65th and Ingleside')
predict('Some guy just tried to steal a car')
predict('He kidnap her in a white van')

# Export to CSV
data.to_csv('output_data.csv')
