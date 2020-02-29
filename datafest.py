import pandas as pd
imp = pd.read_csv("C:/Users/rober/Documents/NetBeansProjects/STMarysHackathon/CompetitionDataFinal/impressions-train.csv")
fin = pd.read_csv("C:/Users/rober/Documents/NetBeansProjects/STMarysHackathon/CompetitionDataFinal/ratings-final.csv")

imp.merge(fin,left_on='rating', right_on='rkey')