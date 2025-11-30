import os
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import linear_kernel
from scipy import sparse

class Recommender:
    def __init__(self, artifacts_path=None):
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.artifacts_path = artifacts_path or os.path.join(base, 'data', 'processed')
        self._load_artifacts()

    def _load_artifacts(self):
        if not os.path.exists(self.artifacts_path):
            raise RuntimeError(f"Artifacts path not found: {self.artifacts_path}. Run preprocessing first.")
        movies_csv = os.path.join(self.artifacts_path, 'movies_clean.csv')
        vec_path = os.path.join(self.artifacts_path, 'vectorizer.pkl')
        tfidf_npz = os.path.join(self.artifacts_path, 'tfidf_matrix.npz')

        if not (os.path.exists(movies_csv) and os.path.exists(vec_path) and os.path.exists(tfidf_npz)):
            raise RuntimeError("Missing artifacts. Run preprocessing.py.")

        self.movies = pd.read_csv(movies_csv)
        with open(vec_path, 'rb') as f:
            self.vectorizer = pickle.load(f)
        self.tfidf_matrix = sparse.load_npz(tfidf_npz)

        titles = self.movies['title'].astype(str).str.strip().str.lower().tolist()
        self.title_to_idx = {t: i for i, t in enumerate(titles)}

    def recommend_by_title(self, title, n=5):
        key = title.strip().lower()
        if key not in self.title_to_idx:
            candidates = [t for t in self.title_to_idx.keys() if key in t or t.startswith(key)]
            if not candidates:
                raise ValueError(f"Title '{title}' not found.")
            key = candidates[0]

        idx = self.title_to_idx[key]
        cosine_similarities = linear_kernel(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()
        top_idx = np.argsort(cosine_similarities)[::-1]
        top_idx = [i for i in top_idx if i != idx][:n]
        results = self.movies.iloc[top_idx][['title', 'genres', 'year', 'overview']].to_dict(orient='records')
        return results

    def recommend_by_plot(self, plot_text, n=5):
        if self.vectorizer is None:
            raise RuntimeError("Vectorizer not available.")
        vec = self.vectorizer.transform([plot_text])
        sims = linear_kernel(vec, self.tfidf_matrix).flatten()
        top_idx = np.argsort(sims)[::-1][:n]
        results = self.movies.iloc[top_idx][['title', 'genres', 'year', 'overview']].to_dict(orient='records')
        return results
