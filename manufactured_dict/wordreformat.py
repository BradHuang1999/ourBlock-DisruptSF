# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 19:53:22 2018

@author: Drew
"""


import pandas as pd
    
def dictcompile():
    
    startlist = ["He ", "She ", "They ", "Us ", "A guy ", "A girl ", "A man ", "A woman ", "That guy ",
                 "My neighbour ", "My friend ", "a person ", "My ", "I ", "We ", "men ", "women ", "a guy ",
                 "that person ", "them ", "I see ", "There is ", "Another "]
    #newlist = []
    
    kidnap = ["missing", "can't find", "Don't see", "gone", "disappeared", "haven't seen", "kidnapped her", "kidnapped him",
              "kidnapped", "took from park", "took from school", "forced into car", "pushed into van", "found person", 
             "found", "child taking", "child stealing", "kidnapping adult", "kidnapping kid", "tried to kidnap", "has hostages", 
             "hostage", "taken", "abducted", "my child", "my daughter", "my son", "human trafficking"]
    
    drugs = ["took drugs", "snorted drugs", "had drugs", "smoked drugs", "injected drugs", "doing drugs",
             "heroin", "had meth", "had crack", "had weed", "had coke", "had cocaine", "doing meth", "doing coke",
             "was selling drugs", "was selling coke", "was selling meth", "was selling weed","cocaine", "coke", 
             "was selling xanax", "smoked weed", "smoked crack", "smoked meth", "smoked from a pipe",
             "had a joint", "smells like weed", "smells like skunk", "had needles", "dropped needles", 
             "has Heroin needles", " seems high", "has used ecstasy", "has used Amphetamines", "has used Cocaine", 
             "has used Methamphetamine", "has used crack", "on drugs", "Marijuana Dispensary", "weed", "smells like weed", 
             "Marijuana", "did dumb things because they are drunk", "drunk in public", 
             "smells like alcohol", "blacked out", "was drinking", " had vodka", " has beer", "at a bar", "gin",
             "possession", "bong", "selling drugs", "dealing drugs", "dealing weed", "rock", "ounce", "gram", 
             "has white powder", "trafficking", "has a lot of drugs", "has a shipment", "hallucinating", "tripping out", 
             "took acid", "is addicted to", "growing weed", "cooking meth", "making meth", "is making drugs", "smoking a blunt", 
             "tripping out", "drank too much", "greened out", "shooting up at", "shooting up in", "alley", "trap"]
    
    theft = ["stole my bike", "stole a bike", "bike is gone", "took bike", "bike", "bike lock", "stealing", "stole",
             "broke", "theft", "thief", "steal", "took it", "car stolen", "car was hijacked", "alarm in a car is going off", 
             "car is gone", "stole car", "took car", "car", "van", "suv", "tesla", "toyota", "honda", "bmw", "mercedes",
             "truck", "lock", "broke lock", "opened door", "Somebody broke into my house", "break into"
             "stole something in my apartment", "stole something", "stole something in my condo", "broke into my apartment", 
             "broke into my condo", "breaking into that house", "breaking into that condo", "breaking into that apartment", 
             "house", "apartment", "condo", "stole purse", "stole money", "took phone", "ran off after taking something", 
             "stole belongings", "robbed me", "laptop stolen", "computer stolen", "took from locked car", "took credit card", 
             "stole wallet", "shoplifting", "shop lifted", "took from store", "stole from mall", "lost it", "stolen bike", 
             "stolen motorcycle", "burglar", "robbery", "robbed", "robbing", "robbed me with gun", "robbed me with knife", "pickpocket",
             "get into", "store", "jewellery", "break in", "smash window"]
    
    mental = ["isn't ok", "shouting", "yelling at no one", "has mental health issues", 
              "hurting himself", "hurting herself", "self harm", "cutting", "kill myself", 
              "kill themselves", "going to kill himself", "going to kill herself", "hanging",
              "slit wrists", "jumped", "jump off", "phone calls", "prank", "pranked", "pranking", "calling", "prank calls", 
              "attempted suicide", "loitering", "standing around", "sleeping", "suicide", "needs help", "issues",
              "paranoid", "weird", "something wrong", "ghosts", "demons", "freaking out", "screaming", "not OK", 'crazy',
              'mental', 'gone mad', 'lost it', 'losing it', "out of it"] 
    
    sex = ["raped", "rape", "sexual assault", "forced", "groped", " touching her inappropriately", "touching inappropriately",
           "sex", "fucked", "kissing", "made out", "harassed", "cat called", "spanked", "slapped", "butt", "boob", "breast",
           "forced", "oral", "mouth", "minors", "paedophile", "molested", "penetrated", "whip", "dominate", "anal", "bleed from sex",
           "used her", "ass", "molested", "molesting", "harass", "harassing", "stalking", "creepy man", "stalk", "staring", "sexual",
           "make out", "slipped something in drink", "sexual abuse", "human trafficking", "brothel", "pimp", "prostitute", "prostitution"]
    
    traffic = ["car is swerving erratically", "car moving weird", "driving drunk", "ran a red light", "has a suspended license", 
               "cannot drive", "hit and run", "had an accident", "crashed into someone", "broke their car", "ran a stop sign", 
               "hit someone with their car", "is driving while high", "is speeding", "is too fast", "driving like a maniac", "reckless driving",
               "dangerous driving", "license", "driver", "passenger", "pedestrian", "hit someone", "police car", "tailgate", "roadrage",
               "demerit points", "red light", "speeding camera", "red light camera", "rear-end", "traffic", "crashed", "hydro pole", "self-driving",
               "pedestrian", "cross walk", "crossing", "stop light", "stoplight", "Uber"]
    
    violence = ["stabbing", "stabbed", "killing", "killed", "is getting stabbed", "is shot", "shot someone", "shot him", 
                "stabbed someone", "stabbed him", "got stabbed", "got shot", "bleeding a lot", "is bleeding", "blood", 
                "bloody", "pulling out a gun", "has a knife", "shooting", "gun", "knife", "shooting", "hit them", "hit him",
                "hit her", "domestic violence", "assaulted", "assaulting", "beat up", "is beating", "punching", "punched",
                "kicking", "kicked", "threatened to kill", "threatened to hit", "threatened", "abused", "abuse", "battery", 
                "shot", "hid his gun", "bullets", "gun shots", "arson", "burning", "firing", "fired", "burned", "exploded",
                "has explosives", "is resisting", "gang", "part of gang", "in a gang", "has gangs", "fighting", "fought", "is stalking",
                "arson", "fire", "trying to kill", "killing", "going to kill", "kill", "murder", "going to kill me", "will kill me", "gonna kill me"]
    
    def listmaker(alist):
        newlist = []
        for word in startlist:
            for crime in alist:
                newlist.append(word + crime)
        return(newlist)
    
    kidnapped = listmaker(kidnap)
    drug = listmaker(drugs)
    steal = listmaker(theft)
    mental_bully = listmaker(mental)
    sexassault = listmaker(sex)
    traffic_viol = listmaker(traffic)
    violent = listmaker(violence)
    
    def labelcolumn(data, label):
        df = pd.DataFrame(data)
        df['category'] = label
        return df
    
    
    kidnapping = labelcolumn(kidnapped, 'Kidnapping')
    drugs = labelcolumn(drug, 'Drug/Narcotics')
    theft = labelcolumn(steal, 'Larceny/Theft')
    mental = labelcolumn( mental_bully, 'Mental Health/Bullying')
    sex = labelcolumn( sexassault, 'Sex Offences')
    traffic = labelcolumn( traffic_viol, 'Traffic Violation')
    violent = labelcolumn( violent, 'Violence/Homicide')
    
    dfmain = pd.concat([kidnapping,drugs,theft,mental,sex,traffic,violent])
    dfmain = dfmain.reset_index()
    dfmain = dfmain.drop('index', axis=1)
    
    dfmain = dfmain.rename(columns={0: 'message'})
    
    
    columnsTitles=["category","message"]
    dfmain = dfmain.reindex(columns=columnsTitles)
    return(dfmain)
    
data = dictcompile()
