import streamlit as st
import pickle
import pandas as pd
import requests
import os
import zipfile

# ----------------------------
# Google Drive Direct Download
# ----------------------------
ZIP_URL = "https://drive.google.com/uc?export=download&id=1Pkme2TBbZRUagPtJYPImXXqbwIcg3bYY"
ZIP_FILE = "movie_files.zip"

def download_zip():
    st.info("Downloading required data... please wait (only once).")
    r = requests.get(ZIP_URL, stream=True)

    with open(ZIP_FILE, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    st.success("Download complete! Extracting files...")

    with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
        zip_ref.extractall(".")

    st.success("Files extracted successfully!")


# ----------------------------
# Ensure PKL Files Are Ready
# ----------------------------
if not os.path.exists("movie_list.pkl") or not os.path.exists("similarity.pkl"):
    download_zip()


# ----------------------------
# Fetch Poster from TMDb
# ----------------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=a1a994767555ab4b6da26c1aa8ef8e3d&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get("poster_path")
    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"


# ----------------------------
# Load Data
# ----------------------------
movies_dict = pickle.load(open("movie_list.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

# Ensure alignment
movies = movies.reset_index(drop=True)
similarity = similarity[: len(movies), : len(movies)]


# ----------------------------
# Recommendation Function
# ----------------------------
def recommend(movie):
    try:
        index = movies[movies["title"] == movie].index[0]
    except IndexError:
        return [], []

    if index >= similarity.shape[0]:
        return [], []

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1],
    )[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in distances:
        if i[0] < len(movies):
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# ----------------------------
# Streamlit UI
# ----------------------------
st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a movie:",
    movies["title"].values,
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    if not names:
        st.warning("No recommendations available.")
    else:
        cols = st.columns(5)
        for idx, col in enumerate(cols):
            if idx < len(names):
                with col:
                    st.image(posters[idx])
                    st.markdown(f"**{names[idx]}**")
