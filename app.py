import json
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient
import pymongo


df = pd.read_csv("perfected.csv")
df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'], inplace=True)
df["combined_name_desc"] = df["Description"] + df["Name"]
sel = df.head(15000) #no of books data
print(sel)
tfv = TfidfVectorizer(min_df=2, max_features=1800, strip_accents='unicode',
                      analyzer='word', token_pattern=r'\w{1,}', stop_words='english') #ngram not used
# tf*idf matrix the words are converted to vector word
tfv_matrix = tfv.fit_transform(sel["combined_name_desc"])
cosine_sim = cosine_similarity(tfv_matrix, tfv_matrix)
indices = pd.Series(sel.index, index=sel['Name']).drop_duplicates()
name_dict = {"Name": [], "Genre": [], "Description": []}


def get_recommendations(Name, cosine_sim, indices):

    # Get the index of the movie that matches the title
    idx = indices[Name]
    # Get the pairwsie similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get the scores for 19 most similar movies
    sim_scores = sim_scores[0:20]
    # Get the movie indices
    book_indices = [i[0] for i in sim_scores]
    # Return the top 10 most similar movies
    for item in book_indices:
        name_dict["Name"].append(sel['Name'][item])
        name_dict["Genre"].append(sel['Genres'][item])
        name_dict["Description"].append(sel["Description"][item])
    # name_list.append(sel['Name'].iloc[book_indices])
    # return sel['Name'].iloc[book_indices], sel['Genres'].iloc[book_indices], sim_scores


book_name = sys.argv[1]
get_recommendations(book_name, cosine_sim, indices)
# get_recommendations("Floodland", cosine_sim, indices)
print(name_dict['Name'])
json_object = json.dumps(name_dict, indent=4)
print(json_object)


client = MongoClient('localhost', 27017)
db = client['test']
work = db['work_dbs']
x = work.insert_one(name_dict)
