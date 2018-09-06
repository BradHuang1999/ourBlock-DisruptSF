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

data.to_csv('datashort.csv')

#"""
#ML
#"""
import re
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2

#removal = SnowballStemmer('english')
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

#data['cleaned'] = data['message'].apply(lambda x: " ".join([removal.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in stoppingwords]).lower())
data['cleaned'] = data['message']

#X_train, X_test, y_train, y_test = train_test_split(data['message'], data.category, test_size=0.3)

X_train, X_test, y_train, y_test = train_test_split(data['cleaned'], data.category, test_size=0.2)

pipeline = Pipeline([('vect', TfidfVectorizer(ngram_range=(1, 2), stop_words="english", sublinear_tf=True)),
                     ('chi',  SelectKBest(chi2, k=485)),
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
#    predictstring = predictstring.join([removal.stem(i) for i in re.sub("[^a-zA-Z]", " ", predictstring).split() if i not in stoppingwords]).lower()
    print(model.predict([predictstring]))
    return model.predict([predictstring])

# Tests

predict("I saw a guy in a blue hoodie and jeans doing meth in Earlmere Park, near the fountain earlier today. He was using a pipe.")

predict("Some guy shot another guy at the corner of 65th and Ingleside. He was wearing red shoes, a black shirt and a True Religion jeans in the park, he was 6' 2''. He got away in a White van with numner plate X2H7ZB")

predict("This girl in yoga pants and a blue tanktop broke a bike lock and stole a bike in Easting Park at 3PM.")

predict("Some dude in a muscle tee and joggers just tried to rob a house at 13 Elm St. He was there for 10 minutes.")

predict("A person wearing all black and Yeezys just pulled up to the park and kidnapped this little girl and threw her in a van.")

predict("Someone is about to jump off the Dunderson Bridge.")
predict("This guy is making weird noises and running around on Eastern Ave. I don't think he's OK.")

predict("A green Honda Civiv is driving erratically and ran past a red light. The license plate was 3D5 M4J")


predict("Some guy is freaking out on the train")

predict("A dude in a black shirt is trying to kill a girl")


predict("My friend Brad in a blue sweater just ran a red light and is driving weird. His number plate is N5J8LZ. He drives an Audi and was on 4th and Houston")

predict("A white woman with brown hair was punching another girl at 19th and Lexington. She's wearing a blue blouse and a red skirt.")

# Export to CSV
#data.to_csv('output_data.csv')
