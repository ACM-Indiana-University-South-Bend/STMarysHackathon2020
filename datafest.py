import pandas as pd
import numpy as np
from numba import jit, cuda
imp = pd.read_csv("./CompetitionDataFinal/impressions-train.csv")
fin = pd.read_csv("./CompetitionDataFinal/ratings-final.csv")
test = pd.read_csv("./CompetitionDataFinal/test.csv")

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

def get_person_opinion_on_movie(person, movid):
    
    outl = movie_data[movie_data["person"] == person]

    outl = outl[outl["movie"] == movid]
    
    r = outl[outl['rating'] >= 0]['rating']
    e = outl[outl['expect'] >= 0]['expect']
    
    if(r.any()):
        if int(r) >= 0:
            return int(r)
        elif int(e) >= 0:
            return int(e)
    else:
        return -1

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

# Input : top 10% of people with similar tastes
#       : movie id
# Output: recommended score for movie 
def predict(people, movie):
    #print(people)
    opinions = get_person_opinion_on_movie(people, movie)
    return opinions

#main function
#@jit(target ="cuda") 
def get_recommend(subject, movie):
    print("In get_recommend for movie " + str(movie))
    
    subject_opinions = get_person_opinions(subject)
    
    score = {}
    #572 people
    for person in range(573):
        #print('people = ' + str(person))
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
    
    top = int(len(score)/10) + 1
    matches = [x[0] for x in score[1:top]]
    #print(matches)
    
    ratings = {}
    
    for i in matches: 
        ratings[i] = predict(i, movie)
        
    recommended = {2:0, 1:0, 0:0, -1:0}
    for i in ratings.values():
        recommended[i] += 1
    recommended.pop(-1)
    recommended = sorted(recommended.items(), key=lambda x: x[1],reverse=True)
    print(recommended)
    print("Recommneded rating for movie " + str(movie) + ":" + str(recommended[0][0]))
    
    

    
#person = 36
    outl = movie_data[movie_data["person"] == person]

    outl = outl[outl["movie"] == movid]
    
for person in test['reviewerid']:
    testperson = test[test["reviewerid"] == person]
    print(test[test["reviewerid"] == person])
    for movie in testperson['movie-code']:
        get_recommend(person, movie)
