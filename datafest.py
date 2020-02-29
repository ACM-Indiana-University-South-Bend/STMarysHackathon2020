from distutils.core import setup
from Cython.Build import cythonize
import pandas as pd
import multiprocessing
from numba import jit, autojit


#import numpy as np
#from numba import jit, cuda
imp = pd.read_csv("./CompetitionDataFinal/impressions-train.csv")
fin = pd.read_csv("./CompetitionDataFinal/ratings-final.csv")
test = pd.read_csv("./CompetitionDataFinal/test.csv")
test = test.sort_values(by=['reviewerid'])
print(test)
movie_data = pd.concat([imp, fin], sort=True) 

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
def predict(person, movie):
    #print(people)
    outl = movie_data[movie_data["person"] == person]

    outl = outl[outl["movie"] == movie]
    
    r = outl[outl['rating'] >= 0]['rating']
    e = outl[outl['expect'] >= 0]['expect']
    
    if(r.any()):
        if int(r) >= 0:
            return int(r)
        elif int(e) >= 0:
            return int(e)
    else:
        return -1

#main function

def get_recommend(subject, movie):
    #print("In get_recommend for movie " + str(movie))
    
    subject_opinions = get_person_opinions(subject)
    
    score = {}
    #572 people
    
    for person in range(10):
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
    
    ratings = {}
    
    for i in matches: 
        ratings[i] = predict(i, movie)
        
    recommended = {2:0, 1:0, 0:0, -1:0}
    for i in ratings.values():
        recommended[i] += 1
    recommended.pop(-1)
    recommended = sorted(recommended.items(), key=lambda x: x[1],reverse=True)
    
    print("Recommended rating for movie " + str(movie) + ":" + str(recommended[0][0]))
    #outl = movie_data[movie_data["person"] == person]
    #outl = outl[outl["movie"] == movid]
    return recommended[0][0]

def main():  
    i=0
    for person in range(573):
        print("person = " + str(person))
        testperson = test[test["reviewerid"] == person]
        print(test[test["reviewerid"] == person])
        
        for movie in testperson['movie-code']:
            #testmovie = testperson[testperson['movie-code'] == movie]
            test['rating'].iloc[i] = int(get_recommend(person, movie))
            i+=1
            print(test[test['reviewerid'] == person])
            #test[test[test["reviewerid"] == person][testperson['movie-code'] == movie]]["rating"] = 
        test.to_csv("./CompetitionDataFinal/test.csv", index=False)
    

#pool = multiprocessing.Pool(processes=6)
main()
#pool.close()