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
# CAN ALSO CALL 'fatPoliceReports.csv' if you have the local file
# TOO LARGE FOR GIT

# ----------------------------------------------------------------

# Drop categories that won't be used - reduces memory use.
data = data.drop(['DayOfWeek', 'Date', 'Time', 'PdDistrict', 'Address', 'Location', 'PdId', 'Resolution', 'Address', 'X', 'Y'], axis=1)
# The first column is finnicky
data = data.drop(data.columns[0], axis=1)

#Rename the columns
data = data.rename(columns={'Category': 'category', 'Descript': 'message'})

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

data['cleaned'] = data['message'].apply(lambda x: " ".join([removal.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in stoppingwords]).lower())


X_train, X_test, y_train, y_test = train_test_split(data['cleaned'], data.category, test_size=0.2)

pipeline = Pipeline([('vect', TfidfVectorizer(ngram_range=(1, 2), stop_words="english", sublinear_tf=True)),
                     ('chi',  SelectKBest(chi2, k=250)),
                     ('clf', LinearSVC(C=1.0, penalty='l1', max_iter=25000, dual=False))])


model = pipeline.fit(X_train, y_train)

vectorizer = model.named_steps['vect']
chi = model.named_steps['chi']
clf = model.named_steps['clf']

feature_names = vectorizer.get_feature_names()
feature_names = [feature_names[i] for i in chi.get_support(indices=True)]
feature_names = np.asarray(feature_names)

target_names = ['Mental Health/Bullying', 'Larceny/Theft', 'Sex Offences', 'Violence/Homicide', 'Kidnapping', 'Drug/Narcotics', 'Traffic Violation']
print("top 10 keystoppingwords per class:")
for i, label in enumerate(target_names):
    top10 = np.argsort(clf.coef_[i])[-10:]
    print("%s: %s" % (label, " ".join(feature_names[top10])))

print("accuracy score: " + str(model.score(X_test, y_test)))




print(model.predict(['traffic']))

# Export to CSV
data.to_csv('output_data.csv')
