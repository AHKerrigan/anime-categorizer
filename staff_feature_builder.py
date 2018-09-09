# Builds the featureset for anime staff
import pandas as pd
import pickle 

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

if __name__ == "__main__":
    anime_staff_data_file = build_panda("data/datastaff-all-share-new.csv")
    print(anime_staff_data_file)
    
    
