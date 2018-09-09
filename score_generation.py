# Script that takes the animenewsnetwork data and creates a list of good anime
# and bad anime that we can use to create features

import pandas as pd
import operator
import pickle

anime_reviews_file_path = "data/datascorehist-all-share-new.csv"
anime_review_data = pd.read_csv(anime_reviews_file_path, delimiter="|")
anime_review_data = anime_review_data.dropna(axis=0)

average_scores = {}

# The data uses a distributed score system, so we we multiply each percentge
# by 100, then use these "scores" to generate an avergae score for each 
# anime
for index, row in anime_review_data.iterrows():
    current_score = 0
    for i in range(11):
        current_score += (row[str(i)] * 100)*i
    current_score = current_score / 11

    # Once we have a score for each anime, we assign the key for the entry as the
    # anime ID, then it's new score as it's value
    average_scores[row['Anime_ID']] = current_score

# Creates a sorted list of tuples of each anime, sorting them by their average score
sorted_anime = sorted(average_scores.items(), key=operator.itemgetter(1))


# The anime list is sorted in ascending order, so the bad anime are the first
# half of the list, and the best anime are the bottom half of the list
# Anime scores tend to skew toward the postive end of the review spectrum
# so this is a reasonable compromise to have adaquate data
bad_anime = sorted_anime[:2014]
good_anime = sorted_anime[2014:]

# Lastly we pickle both lists of anime and their respective scores
save_bad_anime = open("bad_anime.pickle", "wb")
save_good_anime = open("good_anime.pickle", "wb")

pickle.dump(good_anime, save_good_anime)
pickle.dump(bad_anime, save_bad_anime)

save_bad_anime.close()
save_good_anime.close()