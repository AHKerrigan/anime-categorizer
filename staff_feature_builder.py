# Builds the featureset for anime staff
import pandas as pd
import pickle 
import operator
from collections import Counter

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


if __name__ == "__main__":
    anime_staff_data = build_panda("data/datastaff-all-share-new.csv")
    build_staff_features(anime_staff_data)
    staff_features = build_staff_features(anime_staff_data)

    
    
