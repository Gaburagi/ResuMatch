"""
Script to retrain models with combined job data (IT, Hospitality, Engineering)
"""
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing.cleaner import clean_text

# Load the combined jobs data
df_jobs = pd.read_csv('data/all_jobs_combined.csv')

print(f"Loading {len(df_jobs)} unique jobs...")
print(f"\nFields breakdown:")
print(df_jobs['Field'].value_counts())

# Ensure the 'cleaned' column exists
if 'cleaned' not in df_jobs.columns:
    print("\nCleaning job descriptions...")
    df_jobs['cleaned'] = df_jobs['Job Description'].apply(clean_text)

# Load resume data to fit TF-IDF on combined text
df_resumes = pd.read_csv('data/cleaned_resumes.csv')

if 'cleaned' not in df_resumes.columns:
    print("Cleaning resume data...")
    df_resumes['cleaned'] = df_resumes['Resume'].apply(clean_text)

# Fit TF-IDF on combined resumes and jobs
print("\nFitting TF-IDF vectorizer...")
tfidf = TfidfVectorizer(max_features=5000)
all_text = list(df_resumes['cleaned']) + list(df_jobs['cleaned'])
tfidf.fit(all_text)

# Transform jobs
job_vectors = tfidf.transform(df_jobs['cleaned'])

# Save the retrained models
print("\nSaving retrained models...")
with open('models/tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(tfidf, f)

with open('models/job_vectors.pkl', 'wb') as f:
    pickle.dump(job_vectors, f)

# Save the combined jobs data
df_jobs.to_csv('data/cleaned_jobs_unique.csv', index=False)

print("✅ Models retrained successfully!")
print(f"✅ TF-IDF vectorizer: max_features=5000")
print(f"✅ Job vectors shape: {job_vectors.shape}")
print(f"✅ Saved: models/tfidf_vectorizer.pkl")
print(f"✅ Saved: models/job_vectors.pkl")
print(f"✅ Saved: data/cleaned_jobs_unique.csv")
