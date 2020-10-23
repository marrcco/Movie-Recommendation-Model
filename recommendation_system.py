import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# Reading data
df = pd.read_csv("imdb_top_800_cleaned.csv")
df.reset_index(inplace=True)
df.rename(columns={"index" : "Id"},inplace=True)
print(df.head())
print(df.dtypes)
print(df.columns)
print(df.shape)

# Features for model
features = ["Title", "Director", "Writers", "Stars", "Keywords", "Genre"]
print(df[features].head().T)

# Function to combine important features into single string
def combine_features(features):
    features_combined = []
    for i in range(features.shape[0]):
        features_combined.append(features["Director"][i] + " " +
                                 features["Writers"][i] + " " +
                                 features["Stars"][i] + " " +
                                 features["Keywords"][i] + " " +
                                 features["Genre"][i].lower())

    return features_combined

df["features"] = combine_features(df)

# Count Vectorizer
cv = CountVectorizer()
vectorized = cv.fit_transform(df["features"])

# Cosine Similarity
cs = cosine_similarity(vectorized)
print(cs)
print(cs.shape)

# User's title of the movie
movie_title = "the godfather "

movie_id = df[df["Title"] == movie_title]["Id"].values[0]
print(movie_id)

# Score
scores = list(enumerate(cs[movie_id]))
sorted_scores = sorted(scores,key = lambda x: x[1], reverse=True)

# Get 5 similar movies with highest cosine similarity
counter = 0
similar_movies = []
for i in sorted_scores:
    similar_movie = df[df["Id"] == i[0]]["Id"].values[0]
    similar_movies.append(similar_movie)
    counter+=1
    if(counter == 6):
        break

# Get more info about similar movies
similar_movies_expanded = []
for id in similar_movies:
    movie_to_append = df[df["Id"] == id][["Title","Genre","Release_Year","Rating"]].values[0]
    similar_movies_expanded.append(movie_to_append)

print(similar_movies_expanded[1][2])


# Printing similar movies
print("Similar movies to the movie '{}' are: "
      "\n1)Title:{} | Genre:{} | Year:{} | Rating: {} "
      "\n2)Title:{} | Genre:{} | Year:{} | Rating: {}"
      "\n3)Title:{} | Genre:{} | Year:{} | Rating: {}"
      "\n4)Title:{} | Genre:{} | Year:{} | Rating: {}"
      "\n5)Title:{} | Genre:{} | Year:{} | Rating: {}".format(movie_title,
          similar_movies_expanded[1][0], similar_movies_expanded[1][1], similar_movies_expanded[1][2], similar_movies_expanded[1][3],
          similar_movies_expanded[2][0], similar_movies_expanded[2][1], similar_movies_expanded[2][2], similar_movies_expanded[2][3],
          similar_movies_expanded[3][0], similar_movies_expanded[3][1], similar_movies_expanded[3][2], similar_movies_expanded[3][3],
          similar_movies_expanded[4][0], similar_movies_expanded[4][1], similar_movies_expanded[4][2], similar_movies_expanded[4][3],
          similar_movies_expanded[5][0], similar_movies_expanded[5][1], similar_movies_expanded[5][2], similar_movies_expanded[5][3],
      ))