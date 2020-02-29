import pandas as pd
import numpy as np
imp = pd.read_csv("C:/Users/rober/Documents/NetBeansProjects/STMarysHackathon/CompetitionDataFinal/impressions-train.csv")
fin = pd.read_csv("C:/Users/rober/Documents/NetBeansProjects/STMarysHackathon/CompetitionDataFinal/ratings-final.csv")
test = pd.read_csv("C:/Users/rober/Documents/NetBeansProjects/STMarysHackathon/CompetitionDataFinal/test.csv")
#codes = pd.read_txt("C:/Users/rober/Documents/NetBeansProjects/STMarysHackathon/CompetitionDataFinal/test.csv")

final = pd.concat([imp, fin], sort=True)

def get_ratings(movie, df):
    outl = df[df["movie"] == movie] 
    ratings = outl[outl['rating']>=0]
    return ratings

def get_expects(movie, df):
    outl = df[df["movie"] == movie] 
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
    outl = final[final["movie"] == movid] 
    rec = outl[outl['rating']>=0]
    outl = final[final["movie"] == movid] 
    exp = outl[outl['expect']>=0]
    
    #print(exp)
    rep = pd.concat([exp[exp["expect"] == 2], rec[rec["rating"] == rating]], sort=True)
    #print(rep)
    return rep

def get_movie_opinions(movid, df):
 
    #gets all ratings of movie movid
    rec = get_ratings(movid, df)
    exp = get_expects(movid, df)
    #print(exp)
    
    #Gets array of opinions in order 0, 1, 2
    opinions=[None, None, None]
    for i in range(3): 
        recsme = same_rating(rec, movid, i)
        expsme = same_expect(exp, movid, i)
        opinions[i] = len(recsme) + len(expsme)
        
    # Print 0, 1, 2 values
    """
    print("Person: " + str(person) + "\nMovie: " + str(movid) + "\nOther Ratings:")
    for i in range(3):
        print(str(i) + ": " + str(opinions[i]))
    """
    return opinions

#main function
def get_recommend(person):
    # Gets a movie that a person likes, and gets the list of everyone else that has an opinion of 2
    # likers_df is the DataFrame, likers is the names
    likers_df = get_other_likers(person, 2)
    likers = likers_df["person"]
    # Dict of all movies that likers opinion as 2
    likes = {}
    for i in likers: 
        #print(i)
        for h in pd.concat([get_person_rating(i, 2)['movie'], get_person_expect(i, 2)['movie']], sort=True):
            #print(h)
            if h in likes: 
                likes[h] += 1
            else: 
                likes[h] = 1
    # Prints largest amount of rating = 2
    print("Key: " + str(max(likes, key=likes.get)))
    print("Value: " + str(max(likes.values())))
    scores = {}
    current_likers = final[final["person"] == likers.iloc[0]]
    #print(likers_df['person'])
    for i in likers_df["person"]:
        # current_liker is the dataframe of the liker at position i from the list of likers that like the movie we are looking at
        # it has expect, movie, person, and rating for all of the movies they like 
        #this_liker = final[final["person"] == i]
        #pd.concat([current_likers, this_liker], sort=True)
        current_likers = pd.concat([final[final["person"] == i], current_likers])
        #print(final[final["person"]==i])
    
        #print(current_likers)
    print(current_likers)
    
person = 4
get_recommend(person)
