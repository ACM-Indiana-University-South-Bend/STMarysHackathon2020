import pandas as pd
import numpy as np
imp = pd.read_csv("C:/Users/rober/Documents/NetBeansProjects/STMarysHackathon/CompetitionDataFinal/impressions-train.csv")
fin = pd.read_csv("C:/Users/rober/Documents/NetBeansProjects/STMarysHackathon/CompetitionDataFinal/ratings-final.csv")
test = pd.read_csv("C:/Users/rober/Documents/NetBeansProjects/STMarysHackathon/CompetitionDataFinal/test.csv")

final = pd.concat([imp, fin], sort=True)

def get_ratings(movie):
    outl = final[final["movie"] == movie] 
    ratings = outl[outl['rating']>=0]
    return ratings
def get_expects(movie):
    outl = final[final["movie"] == movie] 
    expects = outl[outl['expect']>=0]
    return expects
def get_person_rating(person, rating):
    outl = final[final["person"] == person]
    r = outl[outl['rating'] == rating]
    return r
def get_person_expect(person, rating):
    outl = final[final["person"] == person]
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

def get_other_likers(person):
    #Get a movie that person likes
    personrating = get_person_rating(person, 2)
     # movid is the movie id    
    movid = personrating[personrating['rating'] == 2].iloc[0]['movie']
 
    #gets all ratings of movie movid
    rec = get_ratings(movid)
    exp = get_expects(movid)
    #print(exp)
    
    opinions=[None, None, None]
    for i in range(3): 
        recsme = same_rating(rec, movid, i)
        expsme = same_expect(exp, movid, i)
        opinions[i] = len(recsme) + len(expsme)
    #"""
    print("Person: " + str(person) + "\nMovie: " + str(movid) + "\nOther Ratings:")
    for i in range(3):
        print(str(i) + ": " + str(opinions[i]))
    #"""
    #print(rec[rec["rating"] == 2]["person"])
    rep = pd.concat([exp[exp["expect"] == 2]["person"], rec[rec["rating"] == 2]["person"]], sort=True)
    #print(rep)
    return rep
    
def get_reccomend(person):
    likers = get_other_likers(person)
    likes = {}
    for i in likers: 
        #print(i)
        for h in pd.concat([get_person_rating(i, 2)['movie'], get_person_expect(i, 2)['movie']], sort=True):
            #print(h)
            if h in likes: 
                likes[h] += 1
            else: 
                likes[h] = 1
    
    print(max(likes, key=likes.get))
    print(max(likes.values()))
    
    
person = 100
get_reccomend(person)
