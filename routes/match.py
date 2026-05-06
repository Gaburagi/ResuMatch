from flask import Blueprint, request, jsonify
import pickle
import numpy as np
import pandas as pd
from preprocessing.cleaner import clean_text
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

match_bp = Blueprint('match', __name__)

with open('models/tfidf_vectorizer.pkl', 'rb') as f:
    tfidf = pickle.load(f)

with open('models/job_vectors.pkl', 'rb') as f:
    job_vectors = pickle.load(f)

sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
job_embeddings = np.load('models/job_embeddings_sbert.npy')

df_jobs = pd.read_csv('data/cleaned_jobs_unique.csv')

@match_bp.route('/match', methods=['POST'])
def match():
    data = request.get_json()
    resume_text = data.get('resume', '')
    model_type = data.get('model', 'tfidf')

    if not resume_text:
        return jsonify({'error': 'No resume text provided'}), 400

    cleaned = clean_text(resume_text)

    if model_type == 'sbert':
        resume_vec = sbert_model.encode([cleaned])
        scores = cosine_similarity(resume_vec, job_embeddings)[0]
    else:
        resume_vec = tfidf.transform([cleaned])
        scores = cosine_similarity(resume_vec, job_vectors)[0]

    top_indices = scores.argsort()[::-1][:5]
    results = []
    for i in top_indices:
        results.append({
            'job_title': df_jobs['Job Title'][i],
            'score': round(float(scores[i]) * 100, 2)
        })

    return jsonify({'matches': results, 'model_used': model_type})
