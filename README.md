# 🎬 Movie Recommendation System

A **content-based movie recommender system** built using **Flask**, **Streamlit**, and **Jupyter Notebook**.  
It suggests movies similar to a selected title and fetches posters using the TMDb API.

---

## 🚀 Features

- 🔎 **Search box with auto-suggestions** (like Streamlit’s selectbox).
- 🎥 **Recommendations with posters** and bold movie titles.
- 🌐 **Flask Web App** (HTML + CSS + JS frontend).
- 📊 **Streamlit App** for quick interactive UI.
- 📓 **Jupyter Notebook** for experiments and dataset preprocessing.

---

## 🛠️ Tech Stack

- **Backend:** Flask, Streamlit, Pandas, Scikit-learn
- **Frontend:** HTML, CSS, JavaScript (for Flask UI)
- **API:** TMDb API (for posters)
- **Extras:** Jupyter Notebook for dataset exploration

---

## 📂 Project Structure

```
Movie-Recommender/
│── app2.py # Flask app
│── app.py # Streamlit app
│── movie_list.pkl # Movies dataset
│── similarity.pkl # Similarity matrix
│── requirements.txt # Dependencies (Flask + Streamlit + Jupyter)
│── README.md # Project description
│
├── templates/
│ └── index.html # Flask frontend
│
├── notebooks/
│ └── preprocessing.ipynb # Optional: experiments
│
└── static/ # (Optional: CSS/JS files for Flask)
```

---

## 📂 Dataset

You can download the dataset from Kaggle:

https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset

After downloading, preprocess the dataset to create `movie_list.pkl` and `similarity.pkl` locally before running the apps.

---

▶️ Running the Apps

## Run Flask App

python app2.py

## Run Streamlit App

streamlit run app.py
