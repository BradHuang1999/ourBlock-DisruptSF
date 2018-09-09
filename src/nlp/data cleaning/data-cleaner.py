# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 21:40:29 2018

@author: Drew

Data Cleaning Script for JSON

This script will clean the input CSV of unnecessary rows, and relabel in the
desired format. It will output a JSON file. 

Required packages:
    - Python 3.5
    - Pandas 
"""
# Imports
import pandas as pd

# To Strip out all information, for pure output
#data = pd.read_csv('shortPoliceReports.csv')
#data = data.drop(['DayOfWeek', 'Date', 'Time', 'PdDistrict', 'Resolution', 'Address', 'X',	'Y', 'Location', 'PdId'], axis=1)
#data = data.drop(data.columns[0], axis=1)

# Read in file
data = pd.read_csv('shortPoliceReports.csv',parse_dates=[['Date', 'Time']])
# CAN ALSO CALL 'fatPoliceReports.csv' if you have the local file
# TOO LARGE FOR GIT
# MESSAGE CHARLIE LIN FOR 'fatPoliceReports.csv'

# ----------------------------------------------------------------

# Drop categories that won't be used - reduces memory use.
data = data.drop(['DayOfWeek','PdDistrict', 'Address', 'Location', 'PdId'], axis=1)
# The first column is finnicky
data = data.drop(data.columns[1], axis=1)

#Rename the columns
data = data.rename(columns={'Category': 'category', 'Descript': 'message', 
                            'Date_Time': 'time','Resolution': 'status', 
                            'X': 'long', 'Y': 'lat'})

# Add the requested columns
data["privacy"] = "public"
data["reportingUser"] = "system"
data["anonymous"] = False

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

# Relabel status to simplify
data['status'] = data['status'].replace(['ARREST, BOOKED' , 'ARREST, CITED', 'CLEARED-CONTACT JUVENILE FOR MORE INFO', 'EXCEPTIONAL CLEARANCE', 'JUVENILE BOOKED'], 'solved by police')
data['status'] = data['status'].replace(['NONE'], 'pending')
data['status'] = data['status'].replace(['UNFOUNDED'], 'solved by public')
# Remove others
data = data[data.status != 'NONE']

# Export to JSON
data.to_json('sample-reports.json', orient='records')
