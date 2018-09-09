# Generates a dictionary object that makes anime IDs to their respective 
# anime title, then pickles the object

import pickle
import pandas as pd
import operator

anime_title_file = "data/datatitle-all-share-new.csv"
anime_title_data = pd.read_csv(anime_title_file, delimiter="|")
anime_title_data = anime_title_data.dropna(axis=0)

anime_title_dictionary = {}
for index, row in anime_title_data.iterrows():
    anime_title_dictionary[row["Anime_ID"]] = row["Anime_name"]

# Finish by pickling the dictioanry
save_anime_title_dictionary = open("anime_title_dictionary", "wb")
pickle.dump(anime_title_dictionary, save_anime_title_dictionary)
save_anime_title_dictionary.close()

    
