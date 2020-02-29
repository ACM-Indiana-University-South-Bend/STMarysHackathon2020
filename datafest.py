import pandas as pd
import numpy as np
imp = pd.read_csv("C:/Users/rober/Documents/NetBeansProjects/STMarysHackathon/CompetitionDataFinal/impressions-train.csv")
fin = pd.read_csv("C:/Users/rober/Documents/NetBeansProjects/STMarysHackathon/CompetitionDataFinal/ratings-final.csv")

final = pd.concat([imp, fin])



def get_rating(movie):
    outl = final[final["movie"] == 14] 
    ratings = outl[outl['rating']>=0]
    return ratings


#print(final.head)
#final.to_csv(r'C:/Users/rober/Documents/NetBeansProjects/STMarysHackathon/out.csv', index=False)