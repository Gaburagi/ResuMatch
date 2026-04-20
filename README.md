# ResuMatch

NLP-Based Resume and Job Description Matching System

## Overview

ResuMatch is a comprehensive web application that uses Natural Language Processing (NLP) and machine learning to match resumes against job descriptions. The system analyzes both documents and provides:

- **Match Score**: A percentage-based similarity score between resume and job description
- **Matched Keywords**: Skills and qualifications present in both documents
- **Missing Keywords**: Important skills from the job description not found in the resume
- **Recommendations**: Actionable suggestions to improve resume alignment

## Project Structure

```
ResuMatch/
├── backend/                    # Flask Backend
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt        # Python dependencies
│   ├── routes/                # API route handlers
│   │   ├── __init__.py
│   │   └── matching_routes.py # Matching endpoints
│   ├── models/                # ML Models
│   │   ├── __init__.py
│   │   └── matcher.py         # TF-IDF and similarity logic
│   ├── preprocessing/         # Text preprocessing
│   │   ├── __init__.py
│   │   └── cleaner.py         # Text cleaning and tokenization
│   ├── utils/                 # Helper functions
│   │   ├── __init__.py
│   │   └── helpers.py         # Utility functions
│   └── data/                  # CSV datasets (gitignored)
│       ├── UpdatedResumeDataSet.csv
│       └── job_title_des.csv
│
├── frontend/                   # Frontend (HTML/CSS/JS)
│   ├── index.html             # Main page
│   ├── style.css              # Styling
│   └── script.js              # Client-side logic
│
├── Dataset/                   # Original datasets
│   ├── UpdatedResumeDataSet.csv
│   └── job_title_des.csv
│
├── README.md                  # This file
├── .gitignore                 # Git ignore rules
└── explore.ipynb              # Jupyter notebook for exploration
```

## Technology Stack

### Backend
- **Flask 2.3.3**: Lightweight Python web framework
- **scikit-learn 1.3.0**: Machine learning library (TF-IDF, cosine similarity)
- **pandas 2.0.3**: Data manipulation and analysis
- **nltk 3.8.1**: Natural Language Toolkit for text processing
- **numpy 1.24.3**: Numerical computing
- **Flask-CORS 4.0.0**: Cross-Origin Resource Sharing support

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS Grid and Flexbox
- **Vanilla JavaScript**: Client-side logic (no framework dependencies)

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js (optional, for local server if not using Flask's built-in server)
- pip (Python package manager)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Place your CSV datasets in the `data/` folder:
   - `UpdatedResumeDataSet.csv`
   - `job_title_des.csv`

### Frontend Setup

The frontend is a standalone HTML/CSS/JavaScript application that runs directly in the browser. No build process required!

Simply open `frontend/index.html` in your web browser, or serve it with a local HTTP server:

```bash
# Using Python 3
cd frontend
python -m http.server 8000
# Then visit http://localhost:8000
```

## Running the Application

### Start the Backend Server

```bash
cd backend
python app.py
```

The Flask server will start on `http://localhost:5000`

### Start the Frontend

1. Open `frontend/index.html` in your web browser
2. Or serve it with a local server (see Backend Setup section above)

### Using the Application

1. Paste your resume text in the left textarea
2. Paste the job description in the right textarea
3. Click "Match Resume with Job Description" button
4. View the results:
   - Overall match score (0-100%)
   - Keywords matched between both documents
   - Keywords from job description missing in resume
   - Recommendations to improve alignment

## API Endpoints

### Health Check
- **GET** `/health`
  - Returns: `{"status": "OK", "message": "ResuMatch backend is running"}`

### Match Documents
- **POST** `/api/match`
  - Request body:
    ```json
    {
      "resume": "string",
      "job_description": "string"
    }
    ```
  - Response:
    ```json
    {
      "match_score": 75.5,
      "matched_keywords": ["Python", "Machine Learning", "Flask"],
      "missing_keywords": ["Docker", "Kubernetes"],
      "recommendations": ["Add Docker experience", "Learn Kubernetes"]
    }
    ```

## How It Works

### Matching Algorithm

1. **Text Preprocessing**
   - Convert to lowercase
   - Remove URLs, emails, special characters
   - Tokenize text
   - Remove stopwords

2. **Feature Extraction**
   - TF-IDF (Term Frequency-Inverse Document Frequency) vectorization
   - Converts text into numerical vectors

3. **Similarity Calculation**
   - Cosine similarity between resume and job description vectors
   - Score normalized to 0-100%

4. **Keyword Analysis**
   - Extracts top keywords from both documents
   - Identifies matched and missing keywords

5. **Recommendations**
   - Suggests improvements based on missing keywords
   - Provides actionable feedback

## Development

### Project Workflow

1. **Data Exploration**: Use `explore.ipynb` to analyze datasets
2. **Feature Engineering**: Implement preprocessing in `preprocessing/cleaner.py`
3. **Model Development**: Enhance matching logic in `models/matcher.py`
4. **API Development**: Add routes in `routes/matching_routes.py`
5. **Frontend Enhancement**: Improve UI in `frontend/`

### Future Enhancements

- [ ] Advanced NLP techniques (Word2Vec, BERT embeddings)
- [ ] Batch resume matching against multiple job postings
- [ ] Resume parsing from PDF/DOCX files
- [ ] User authentication and saved profiles
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Resume optimization suggestions
- [ ] Integration with job boards
- [ ] Mobile app version
- [ ] Machine learning model training on datasets

## Configuration

### Environment Variables

Create a `.env` file in the backend folder:

```env
FLASK_ENV=development
FLASK_DEBUG=True
API_HOST=0.0.0.0
API_PORT=5000
```

## Troubleshooting

### "Cannot connect to Flask backend" error
- Ensure Flask server is running on `http://localhost:5000`
- Check firewall settings
- Verify CORS is enabled in `app.py`

### "Module not found" errors
- Make sure you've activated the virtual environment
- Run `pip install -r requirements.txt` in the backend folder

### NLTK data errors
- The application auto-downloads required NLTK data
- If issues persist, manually download:
  ```python
  import nltk
  nltk.download('punkt')
  nltk.download('stopwords')
  ```

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes and commit: `git commit -m 'Add your feature'`
3. Push to the branch: `git push origin feature/your-feature`
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on the project repository.

## Authors

- ResuMatch Development Team

---

**Last Updated**: April 2024

**Version**: 1.0.0

Happy matching! 🚀
