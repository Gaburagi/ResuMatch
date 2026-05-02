
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words]
    return ' '.join(tokens)

# Load existing jobs
df_jobs = pd.read_csv('data/cleaned_jobs.csv')

# Add a 'Field' column to existing jobs (default to IT)
if 'Field' not in df_jobs.columns:
    df_jobs['Field'] = 'Information Technology'

# Hospitality Jobs Data
hospitality_jobs = [
    {
        'Job Title': 'Hotel Manager',
        'Job Description': 'Lead hotel operations, manage staff, ensure guest satisfaction, oversee budget and revenue management. Requires strong leadership, communication, and hospitality industry experience.',
        'Field': 'Hospitality'
    },
    {
        'Job Title': 'Chef',
        'Job Description': 'Plan and prepare meals, manage kitchen staff, ensure food quality and hygiene standards. Experience with menu planning, food costing, and kitchen management required.',
        'Field': 'Hospitality'
    },
    {
        'Job Title': 'Front Desk Officer',
        'Job Description': 'Greet guests, manage check-ins and check-outs, handle reservations and customer inquiries. Requires excellent customer service and communication skills.',
        'Field': 'Hospitality'
    },
    {
        'Job Title': 'Housekeeping Manager',
        'Job Description': 'Supervise housekeeping staff, ensure rooms meet cleanliness standards, manage supplies and inventory. Leadership and attention to detail required.',
        'Field': 'Hospitality'
    },
    {
        'Job Title': 'Event Coordinator',
        'Job Description': 'Plan and organize events, manage vendor relationships, coordinate logistics and budgets. Requires organizational skills and event planning experience.',
        'Field': 'Hospitality'
    },
    {
        'Job Title': 'Restaurant Manager',
        'Job Description': 'Manage restaurant operations, staff supervision, customer service, revenue management. Experience in food service industry essential.',
        'Field': 'Hospitality'
    },
    {
        'Job Title': 'Waiter/Waitress',
        'Job Description': 'Serve customers, take orders, deliver food and beverages, process payments. Requires excellent customer service and attention to detail.',
        'Field': 'Hospitality'
    },
    {
        'Job Title': 'Bartender',
        'Job Description': 'Prepare and serve drinks, manage bar inventory, interact with customers. Knowledge of drink recipes and bartending techniques required.',
        'Field': 'Hospitality'
    },
    {
        'Job Title': 'Concierge',
        'Job Description': 'Assist guests with information and reservations, arrange services, provide personalized recommendations. Excellent communication and problem-solving skills needed.',
        'Field': 'Hospitality'
    },
    {
        'Job Title': 'Pastry Chef',
        'Job Description': 'Prepare pastries and desserts, create baking recipes, manage pastry kitchen. Creativity and baking expertise required.',
        'Field': 'Hospitality'
    }
]

# Engineering Jobs Data
engineering_jobs = [
    {
        'Job Title': 'Civil Engineer',
        'Job Description': 'Design and supervise construction projects, analyze site conditions, manage project budgets. Knowledge of CAD software and building codes required.',
        'Field': 'Engineering'
    },
    {
        'Job Title': 'Mechanical Engineer',
        'Job Description': 'Design mechanical systems, create technical drawings, oversee manufacturing processes. Proficiency in CAD and mechanical design principles required.',
        'Field': 'Engineering'
    },
    {
        'Job Title': 'Electrical Engineer',
        'Job Description': 'Design electrical systems, develop schematics, test equipment functionality. Strong knowledge of electrical theory and circuit design required.',
        'Field': 'Engineering'
    },
    {
        'Job Title': 'Software Engineer',
        'Job Description': 'Develop and maintain software applications, write clean code, participate in code reviews. Proficiency in multiple programming languages required.',
        'Field': 'Engineering'
    },
    {
        'Job Title': 'Structural Engineer',
        'Job Description': 'Design building structures, perform stress analysis, ensure structural safety. Knowledge of structural design and analysis software required.',
        'Field': 'Engineering'
    },
    {
        'Job Title': 'Chemical Engineer',
        'Job Description': 'Design chemical processing systems, optimize production processes, ensure safety compliance. Knowledge of chemistry and process engineering required.',
        'Field': 'Engineering'
    },
    {
        'Job Title': 'Environmental Engineer',
        'Job Description': 'Design environmental protection systems, manage waste management, ensure regulatory compliance. Knowledge of environmental regulations required.',
        'Field': 'Engineering'
    },
    {
        'Job Title': 'Automotive Engineer',
        'Job Description': 'Design vehicle components, improve performance and safety, conduct testing. Knowledge of automotive systems and CAD required.',
        'Field': 'Engineering'
    },
    {
        'Job Title': 'Aerospace Engineer',
        'Job Description': 'Design aircraft and spacecraft components, perform aerodynamic analysis, ensure safety standards. Advanced knowledge of aerospace principles required.',
        'Field': 'Engineering'
    },
    {
        'Job Title': 'Industrial Engineer',
        'Job Description': 'Optimize manufacturing processes, improve efficiency, reduce costs. Knowledge of lean manufacturing and process optimization required.',
        'Field': 'Engineering'
    }
]

# Create DataFrames
df_hospitality = pd.DataFrame(hospitality_jobs)
df_engineering = pd.DataFrame(engineering_jobs)

# Combine all jobs
df_all_jobs = pd.concat([df_jobs, df_hospitality, df_engineering], ignore_index=True)

# Clean text for new jobs
df_all_jobs['cleaned'] = df_all_jobs['Job Description'].apply(clean_text)

# Remove duplicates based on job title
df_all_jobs_unique = df_all_jobs.drop_duplicates(subset='Job Title').reset_index(drop=True)

# Save the combined dataset
df_all_jobs_unique.to_csv('data/all_jobs_combined.csv', index=False)
df_all_jobs.to_csv('data/all_jobs_full.csv', index=False)

print("✅ Job data successfully added!")
print(f"Total jobs (with duplicates): {len(df_all_jobs)}")
print(f"Total unique jobs: {len(df_all_jobs_unique)}")
print(f"\nBreakdown by field:")
print(df_all_jobs_unique['Field'].value_counts())
print(f"\n✅ Files saved:")
print("   - data/all_jobs_combined.csv (unique jobs)")
print("   - data/all_jobs_full.csv (with duplicates)")
