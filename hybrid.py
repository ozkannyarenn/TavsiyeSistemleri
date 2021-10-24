import pandas as pd


def create_user_movie_df():
    import pandas as pd
    movie = pd.read_csv(r'C:\Users\Hp\Desktop\movie\movie.csv')
    rating = pd.read_csv(r'C:\Users\Hp\Desktop\rating\rating.csv')
    df = movie.merge(rating, how="left", on="movieId")
    comment_counts = pd.DataFrame(df["title"].value_counts())
    rare_movies = comment_counts[comment_counts["title"] <= 1000].index
    common_movies = df[~df["title"].isin(rare_movies)]
    user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
    return user_movie_df

user_movie_df = create_user_movie_df()

def item_based_recommender(movie_name, user_movie_df):
    movie_name = user_movie_df[movie_name]
    return user_movie_df.corrwith(movie_name).sort_values(ascending=False).head(10)
random_user = 108170
random_user_df = user_movie_df[user_movie_df.index == random_user]
movies_watched = random_user_df.columns[random_user_df.notna().any()].tolist()

movies_watched_df = user_movie_df[movies_watched]
movies_watched_df.head()
movies_watched_df.shape

user_movie_count = movies_watched_df.T.notnull().sum()

user_movie_count = user_movie_count.reset_index()

user_movie_count.columns = ["userId", "movie_count"]

perc = len(movies_watched) * 60 / 100
users_same_movies = user_movie_count[user_movie_count["movie_count"] > perc]["userId"]

final_df = pd.concat([movies_watched_df[movies_watched_df.index.isin(users_same_movies)],
                     random_user_df[movies_watched]])

final_df.shape

final_df.T.corr()

corr_df = final_df.corr().unstack().sort_values().drop_duplicates()
corr_df = pd.DataFrame(corr_df, columns=["corr"])
corr_df.index.names = ["user_id_1", "user_id_2"]
corr_df = corr_df.reset_index()

top_users = corr_df[(corr_df["user_id_1"] != random_user) & (corr_df["corr"] >= 0.65)][
    ["user_id_2", "corr"]].reset_index(drop=True)

top_users = top_users.sort_values(by='corr', ascending=False)
top_users.rename(columns={"user_id_2": "userId"}, inplace=True)

rating = pd.read_csv(r'C:\Users\Hp\Desktop\rating\rating.csv')

top_users_ratings = top_users.merge(rating[["userId", "movieId", "rating"]], how='inner')
top_users_ratings['weighted_rating'] = top_users_ratings['corr'] * top_users_ratings['rating']

