"""
ResuMatch - Flask Backend
Main application entry point for the Resume and Job Description Matching System
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

# Import route blueprints
# from routes import matching_routes

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Register blueprints
# app.register_blueprint(matching_routes.bp)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'OK', 'message': 'ResuMatch backend is running'}), 200


@app.route('/api/match', methods=['POST'])
def match_resume_job():
    """
    Main matching endpoint
    Expects JSON with 'resume' and 'job_description' keys
    Returns match score and analysis
    """
    try:
        data = request.get_json()
        
        if not data or 'resume' not in data or 'job_description' not in data:
            return jsonify({'error': 'Missing resume or job_description'}), 400
        
        resume = data['resume']
        job_description = data['job_description']
        
        # TODO: Implement matching logic using models
        # from models import matcher
        # match_result = matcher.calculate_match_score(resume, job_description)
        
        match_result = {
            'match_score': 75.5,
            'matched_keywords': [],
            'missing_keywords': [],
            'recommendations': []
        }
        
        return jsonify(match_result), 200
    
    except Exception as e:
        logger.error(f'Error in match endpoint: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
