# 🎬 Flask Movie Recommendation Engine

A full-featured Movie Recommendation System using:

- **Flask** (Backend API + UI route)
- **Content-Based Filtering**
- **TF-IDF Vectorizer**
- **Cosine Similarity**
- **MovieLens dataset**
- **Front-end HTML/CSS/JS UI**

---

## 🚀 Features

### 🔹 Content-Based Filtering

Recommends movies based on:

- Plot similarity
- TF-IDF embeddings
- Cosine similarity scores

### 🔹 API Endpoints

| Endpoint                     | Method | Purpose                             |
| ---------------------------- | ------ | ----------------------------------- |
| `/recommend?title=Inception` | GET    | Recommend movies using title        |
| `/recommend_text`            | POST   | Recommend using raw plot text       |
| `/ui`                        | GET    | Front-end movie selection interface |

---
