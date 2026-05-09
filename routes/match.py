from flask import Blueprint, request, jsonify
import pickle
import numpy as np
import pandas as pd
from preprocessing.cleaner import clean_text
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

match_bp = Blueprint('match', __name__)

# ── Load TF-IDF ───────────────────────────────────────
with open('models/tfidf_vectorizer.pkl', 'rb') as f:
    tfidf = pickle.load(f)

with open('models/job_vectors.pkl', 'rb') as f:
    job_vectors = pickle.load(f)

# ── Load SBERT ────────────────────────────────────────
sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
job_embeddings = np.load('models/job_embeddings_sbert.npy')

# ── Load Jobs ─────────────────────────────────────────
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

    return jsonify({
        'matches': results,
        'model_used': model_type
    })

import re as _re

@match_bp.route('/live-jobs', methods=['POST'])
def live_jobs():
    import requests as req

    data = request.get_json()
    resume_text = data.get('resume', '')
    model_type = data.get('model', 'tfidf')

    if not resume_text:
        return jsonify({'error': 'No resume text provided'}), 400

    # Fetch live jobs from Jobicy
    try:
        response = req.get('https://jobicy.com/api/v2/remote-jobs?count=20', timeout=10)
        jobs = response.json().get('jobs', [])
    except Exception as e:
        return jsonify({'error': f'Failed to fetch live jobs: {str(e)}'}), 500

    # Strip HTML from job descriptions
    def strip_html(text):
        return _re.sub(r'<[^>]+>', ' ', text)

    # Clean and vectorize
    job_texts = [clean_text(strip_html(j.get('jobDescription', ''))) for j in jobs]
    cleaned_resume = clean_text(resume_text)

    if model_type == 'sbert':
        job_vecs = sbert_model.encode(job_texts)
        resume_vec = sbert_model.encode([cleaned_resume])
        scores = cosine_similarity(resume_vec, job_vecs)[0]
    else:
        from sklearn.feature_extraction.text import TfidfVectorizer
        live_tfidf = TfidfVectorizer(max_features=5000)
        all_texts = [cleaned_resume] + job_texts
        live_tfidf.fit(all_texts)
        job_vecs = live_tfidf.transform(job_texts)
        resume_vec = live_tfidf.transform([cleaned_resume])
        scores = cosine_similarity(resume_vec, job_vecs)[0]

    top_indices = scores.argsort()[::-1][:5]
    results = []
    for i in top_indices:
        j = jobs[i]
        results.append({
            'job_title': j.get('jobTitle', ''),
            'company': j.get('companyName', ''),
            'industry': j.get('jobIndustry', [''])[0],
            'location': j.get('jobGeo', ''),
            'type': j.get('jobType', [''])[0],
            'url': j.get('url', ''),
            'score': round(float(scores[i]) * 100, 2)
        })

    return jsonify({'matches': results, 'model_used': model_type, 'source': 'live'})