from flask import Flask, render_template, request
import pickle
import pandas as pd
import requests

# Create Flask app
app = Flask(__name__)

# ----------------------------
# Fetch Poster from TMDb
# ----------------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=a1a994767555ab4b6da26c1aa8ef8e3d&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
    except Exception:
        pass
    return "https://via.placeholder.com/500x750?text=No+Poster"

# ----------------------------
# Load Data
# ----------------------------
movies_dict = pickle.load(open("movie_list.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
movies = movies.reset_index(drop=True)
titles_list = movies["title"].tolist()

similarity = pickle.load(open("similarity.pkl", "rb"))
similarity = similarity[: len(movies), : len(movies)]  # ensure alignment

# ----------------------------
# Recommendation Function
# ----------------------------
def recommend(movie):
    try:
        index = movies[movies["title"] == movie].index[0]
    except IndexError:
        return [], []

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1],
    )[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in distances:
        idx = i[0]
        if idx < len(movies):
            movie_id = movies.iloc[idx].movie_id
            recommended_movies.append(movies.iloc[idx].title)
            recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# ----------------------------
# Flask Route
# ----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    selected_movie = None
    movie_data = []

    if request.method == "POST":
        selected_movie = request.form.get("movie")
        if selected_movie:
            recs, posters = recommend(selected_movie)
            movie_data = list(zip(recs, posters))

    return render_template(
        "index.html",
        movies=titles_list,
        selected_movie=selected_movie,
        movie_data=movie_data
    )

if __name__ == "__main__":
    app.run(debug=True)
