import pandas as pd
import numpy as np
from numba import jit, cuda
imp = pd.read_csv("C:/Users/rober/Documents/NetBeansProjects/STMarysHackathon/CompetitionDataFinal/impressions-train.csv")
fin = pd.read_csv("C:/Users/rober/Documents/NetBeansProjects/STMarysHackathon/CompetitionDataFinal/ratings-final.csv")
test = pd.read_csv("C:/Users/rober/Documents/NetBeansProjects/STMarysHackathon/CompetitionDataFinal/test.csv")
#codes = pd.read_txt("C:/Users/rober/Documents/NetBeansProjects/STMarysHackathon/CompetitionDataFinal/test.csv")

movie_data = pd.concat([imp, fin], sort=True)

def get_ratings(movie, df):
    outl = df[df["movie"] == movie] 
    ratings = outl[outl['rating']>=0]
    return ratings

def get_expects(movie, df):
    outl = df[df["movie"] == movie] 
    expects = outl[outl['expect']>=0]
    return expects

def get_person_rating(person, rating):
    outl = movie_data[movie_data["person"] == person]
    r = outl[outl['rating'] == rating]
    return r

def get_person_expect(person, rating):
    outl = movie_data[movie_data["person"] == person]
    e = outl[outl['expect'] == rating]
    return e

#Returns the list of everyone that rated this movie the same
def same_rating(df, movie, rating):
    a = df[df['rating'] == rating]
    return a

def same_expect(df, movie, rating):
    a = df[df['expect'] == rating]
    #print(a)
    return a

def get_movid(person, rating): 
    #Get a movie that person likes
    personrating = get_person_rating(person, rating)
     # movid is the movie id    
    movid = personrating[personrating['rating'] == rating].iloc[0]['movie']
    return movid

def get_other_likers(person, rating):
    # Gets a movie from the person's rating
    movid = get_movid(person, rating)
    
    #gets all opintions of movie movid
    outl = movie_data[movie_data["movie"] == movid] 
    rec = outl[outl['rating']>=0]
    outl = movie_data[movie_data["movie"] == movid] 
    exp = outl[outl['expect']>=0]
    
    #print(exp)
    rep = pd.concat([exp[exp["expect"] == 2], rec[rec["rating"] == rating]], sort=True)
    #print(rep)
    return rep



def get_person_opinions(person):
    person_opinions = {}
    
    outl = movie_data[movie_data["person"] == person]
    r = outl[outl['rating'] >= 0]
    e = outl[outl['expect'] >= 0]
    opinions = pd.concat([r, e], sort=True)
    
    for h in opinions['movie']: # h is movie id
        
        rat = opinions[opinions['movie'] == h]['rating'].values[0]
        exp = opinions[opinions['movie'] == h]['expect'].values[0]
        
        if rat >= 0: 
            person_opinions[h] = rat
        elif exp >= 0:
            person_opinions[h] = exp
    return person_opinions

#main function
#@jit(target ="cuda") 
def get_recommend(subject):
    print("In get_recommend")
    
    subject_opinions = get_person_opinions(subject)
    
    score = {}
    #572 people
    for person in range(573):
        print('people = ' + str(person))
        person_opinions = get_person_opinions(person)
        score[person] = 0
        
        for movid in subject_opinions:
                if movid in person_opinions.keys():
                    sub = subject_opinions[movid]
                    per = person_opinions[movid]
                    if sub == per:
                        score[person] += 2
                    elif (sub != 0 and per != 0):
                        score[person] += 1
    score = sorted(score.items(), key=lambda x: x[1],reverse=True)
    print(score)
    
person = 0
get_recommend(person)
