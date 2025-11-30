import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import sparse
import re

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RAW_CSV = os.path.join(BASE, 'data', 'raw', 'movies.csv')
PROCESSED_DIR = os.path.join(BASE, 'data', 'processed')
os.makedirs(PROCESSED_DIR, exist_ok=True)

def load_raw():
    if not os.path.exists(RAW_CSV):
        raise FileNotFoundError(f"Place movies.csv at {RAW_CSV}")
    df = pd.read_csv(RAW_CSV, quotechar='"', encoding='utf-8')
    return df

def clean_and_prepare(df):
    df = df.copy()

    # Fill missing genres
    if 'genres' not in df.columns:
        df['genres'] = ''
    else:
        df['genres'] = df['genres'].fillna('')

    # Fill missing overview
    if 'overview' not in df.columns:
        df['overview'] = df['title'].fillna('') + ' ' + df['genres']
    else:
        df['overview'] = df['overview'].fillna('') + ' ' + df['genres']

    # Extract year from title if exists
    if 'year' not in df.columns:
        def extract_year(title):
            match = re.search(r'\((\d{4})\)$', str(title))
            return int(match.group(1)) if match else None
        df['year'] = df['title'].apply(extract_year)

    # Remove year from title
    df['title'] = df['title'].astype(str).str.replace(r'\s*\(\d{4}\)$','', regex=True).str.strip()

    # Ensure all columns exist
    df['title'] = df['title'].fillna('Unknown')
    df['overview'] = df['overview'].astype(str)
    df['genres'] = df['genres'].astype(str)

    return df[['title','genres','year','overview']]

def build_and_save(max_features=20000):
    df = load_raw()
    if df.empty:
        print("Raw CSV is empty. Add some movies to continue.")
        return
    df_clean = clean_and_prepare(df)
    
    if df_clean.empty:
        print("Cleaned DataFrame is empty. Check your raw CSV formatting.")
        return

    # Save cleaned CSV
    clean_csv_path = os.path.join(PROCESSED_DIR, 'movies_clean.csv')
    df_clean.to_csv(clean_csv_path, index=False)
    print(f"Cleaned CSV saved to {clean_csv_path} ({len(df_clean)} rows)")

    # Build TF-IDF
    tfidf = TfidfVectorizer(stop_words='english', max_features=max_features)
    tfidf_matrix = tfidf.fit_transform(df_clean['overview'].values)

    # Save vectorizer and matrix
    with open(os.path.join(PROCESSED_DIR,'vectorizer.pkl'),'wb') as f:
        pickle.dump(tfidf,f)
    sparse.save_npz(os.path.join(PROCESSED_DIR,'tfidf_matrix.npz'), tfidf_matrix)

    print("TF-IDF matrix and vectorizer saved to", PROCESSED_DIR)

if __name__ == "__main__":
    build_and_save()
