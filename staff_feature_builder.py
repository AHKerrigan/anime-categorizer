# Builds the featureset for anime staff
import pandas as pd
import pickle 
import operator
from collections import Counter
from sklearn.linear_model import LogisticRegression, SGDClassifier
import random
import nltk
from nltk.classify import ClassifierI
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB

#def find_features(document):
#    words = word_tokenize(document)
#    features = {}
#    for w in word_features:
#        features[w] = (w in words)
#
#    return features

# Takes a filename representing a csv file and returns a pandas object with the
# proper delimiter applied
def build_panda(filename):
    panda_file = filename
    return_object = pd.read_csv(panda_file, delimiter="|")
    return_object = return_object.dropna(axis=0)
    return return_object

# Builds both a full featureset of staff (by id)
def build_staff_features(anime_staff_data):

    # We create a frequency distribution of 
    all_staff = []
    for index, row in anime_staff_data.iterrows():
        all_staff.extend(row["Staff_ID"].split(";"))
    all_staff = dict(Counter(all_staff))
    staff_features = []

    # We include the staff member in our featurelist if they have worked on 
    # at least 4 anime. Otherwise they might skew our data
    # This results in 10k features. Normally, we would use fewer, the issue 
    # bad staff tend to work on fewer anime, so excluding them would only
    # make our model predictive for good anime
    for staff in all_staff.keys():
        if all_staff[staff] >= 5:
            staff_features.append(staff)

    return staff_features

# We need to build a document that associates some list of staff with 
# a postive or negative score
def document_builder(anime_staff_data):
    bad_anime_list_f = open("pickled_objects/bad_anime.pickle", "rb")
    good_anime_list_f = open("pickled_objects/good_anime.pickle", "rb")

    # We convert the lists to dictionaries, because the only thing we need them
    # for in this step is checking to see which list each anime is in
    bad_anime_list = dict(pickle.load(bad_anime_list_f))
    good_anime_list = dict(pickle.load(good_anime_list_f))

    document = []

    for index, row in anime_staff_data.iterrows():
        if row["Anime_ID"] in bad_anime_list:
            document.append((row["Staff_ID"].split(";"), "neg"))
        if row["Anime_ID"] in good_anime_list:
            document.append((row["Staff_ID"].split(";"), "pos"))

    return document

def build_featureset(documents, staff_features):
    featuresets = []
    for (staff_list, rev) in documents:
        features = {}
        for staff in staff_features:
            features[staff] = (staff in staff_list)
        featuresets.append((features, rev))
    
    return featuresets

if __name__ == "__main__":
    anime_staff_data = build_panda("data/datastaff-all-share-new.csv")
    build_staff_features(anime_staff_data)
    staff_features = build_staff_features(anime_staff_data)
    documents = document_builder(anime_staff_data)
    featureset = build_featureset(documents, staff_features)
    
    # Shuffle the featureset, then pickle and save
    random.shuffle(featureset)
    save_staff_features = open("pickled_objects/staff_featuresets.pickle", "wb")
    pickle.dump(featureset, save_staff_features)
