from flask import Blueprint, request, jsonify
import pickle
import pandas as pd
from preprocessing.cleaner import clean_text
from sklearn.metrics.pairwise import cosine_similarity

match_bp = Blueprint('match', __name__)

# Load models
with open('models/tfidf_vectorizer.pkl', 'rb') as f:
    tfidf = pickle.load(f)

with open('models/job_vectors.pkl', 'rb') as f:
    job_vectors = pickle.load(f)

df_jobs = pd.read_csv('data/cleaned_jobs_unique.csv')

@match_bp.route('/match', methods=['POST'])
def match():
    data = request.get_json()
    resume_text = data.get('resume', '')

    if not resume_text:
        return jsonify({'error': 'No resume text provided'}), 400

    cleaned_resume = clean_text(resume_text)
    resume_vec = tfidf.transform([cleaned_resume])
    scores = cosine_similarity(resume_vec, job_vectors)[0]
    top_indices = scores.argsort()[::-1][:5]

    results = []
    for i in top_indices:
        results.append({
            'job_title': df_jobs['Job Title'][i],
            'field': df_jobs.get('Field', ['Information Technology'] * len(df_jobs)).iloc[i] if 'Field' in df_jobs.columns else 'Information Technology',
            'score': round(scores[i] * 100, 2)
        })

    return jsonify({'matches': results})

@match_bp.route('/match-by-field', methods=['POST'])
def match_by_field():
    """Match resumes to jobs filtered by field"""
    data = request.get_json()
    resume_text = data.get('resume', '')
    field_filter = data.get('field', None)

    if not resume_text:
        return jsonify({'error': 'No resume text provided'}), 400

    cleaned_resume = clean_text(resume_text)
    resume_vec = tfidf.transform([cleaned_resume])
    scores = cosine_similarity(resume_vec, job_vectors)[0]
    
    # Filter by field if specified
    if field_filter:
        field_mask = df_jobs['Field'] == field_filter if 'Field' in df_jobs.columns else [True] * len(df_jobs)
        filtered_indices = [i for i, mask in enumerate(field_mask) if mask]
        
        if not filtered_indices:
            return jsonify({'error': f'No jobs found in field: {field_filter}'}), 400
        
        # Get scores only for filtered jobs
        filtered_scores = [(i, scores[i]) for i in filtered_indices]
        filtered_scores.sort(key=lambda x: x[1], reverse=True)
        top_indices = [i for i, _ in filtered_scores[:5]]
    else:
        top_indices = scores.argsort()[::-1][:5]

    results = []
    for i in top_indices:
        results.append({
            'job_title': df_jobs['Job Title'][i],
            'field': df_jobs.get('Field', ['Information Technology'] * len(df_jobs)).iloc[i] if 'Field' in df_jobs.columns else 'Information Technology',
            'score': round(scores[i] * 100, 2)
        })

    return jsonify({'matches': results, 'field_filter': field_filter})

@match_bp.route('/fields', methods=['GET'])
def get_fields():
    """Get list of available job fields"""
    if 'Field' in df_jobs.columns:
        fields = df_jobs['Field'].unique().tolist()
        field_counts = df_jobs['Field'].value_counts().to_dict()
        return jsonify({'fields': fields, 'job_counts': field_counts})
    else:
        return jsonify({'fields': ['Information Technology'], 'job_counts': {'Information Technology': len(df_jobs)}})