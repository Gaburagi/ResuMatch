/**
 * ResuMatch Frontend Script
 * Handles API communication with Flask backend and UI interactions
 */

// Configuration
const API_BASE_URL = 'http://localhost:5000/api';
const MATCH_ENDPOINT = '/match';

/**
 * Main function to handle resume-job description matching
 */
async function matchDocuments() {
    const resumeText = document.getElementById('resumeInput').value.trim();
    const jobText = document.getElementById('jobInput').value.trim();

    // Validation
    if (!resumeText || !jobText) {
        showError('Please provide both resume and job description text.');
        return;
    }

    if (resumeText.length < 50 || jobText.length < 50) {
        showError('Please provide longer text for both resume and job description (minimum 50 characters each).');
        return;
    }

    // Show loading state
    showLoadingSpinner(true);
    hideError();
    hideResults();

    try {
        // Make API request to Flask backend
        const response = await fetch(API_BASE_URL + MATCH_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                resume: resumeText,
                job_description: jobText
            })
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        console.error('Error during matching:', error);
        showError(`Error: ${error.message}. Make sure the Flask backend is running on http://localhost:5000`);
    } finally {
        showLoadingSpinner(false);
    }
}

/**
 * Display results from the API response
 * @param {Object} data - API response data
 */
function displayResults(data) {
    const {
        match_score = 0,
        matched_keywords = [],
        missing_keywords = [],
        recommendations = []
    } = data;

    // Update match score
    const scoreValue = Math.round(match_score);
    document.getElementById('matchScore').textContent = scoreValue;
    document.getElementById('scoreBar').style.width = scoreValue + '%';

    // Update matched keywords
    const matchedKeywordsContainer = document.getElementById('matchedKeywords');
    matchedKeywordsContainer.innerHTML = matched_keywords.length > 0
        ? matched_keywords.map(kw => `<span class="keyword">${escapeHtml(kw)}</span>`).join('')
        : '<p style="color: #7f8c8d;">No matched keywords found.</p>';

    // Update missing keywords
    const missingKeywordsContainer = document.getElementById('missingKeywords');
    missingKeywordsContainer.innerHTML = missing_keywords.length > 0
        ? missing_keywords.map(kw => `<span class="keyword missing">${escapeHtml(kw)}</span>`).join('')
        : '<p style="color: #7f8c8d;">No missing keywords identified.</p>';

    // Update recommendations
    const recommendationsList = document.getElementById('recommendations');
    recommendationsList.innerHTML = recommendations.length > 0
        ? recommendations.map(rec => `<li>${escapeHtml(rec)}</li>`).join('')
        : '<li>Your resume is well-matched to this job description!</li>';

    // Show results section
    showResults();
}

/**
 * Reset the form to initial state
 */
function resetForm() {
    document.getElementById('resumeInput').value = '';
    document.getElementById('jobInput').value = '';
    hideResults();
    hideError();
    document.getElementById('resumeInput').focus();
}

/**
 * Show the results section
 */
function showResults() {
    document.getElementById('resultsSection').classList.remove('hidden');
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Hide the results section
 */
function hideResults() {
    document.getElementById('resultsSection').classList.add('hidden');
}

/**
 * Show loading spinner
 * @param {Boolean} show - Whether to show or hide the spinner
 */
function showLoadingSpinner(show) {
    const spinner = document.getElementById('loadingSpinner');
    if (show) {
        spinner.classList.remove('hidden');
    } else {
        spinner.classList.add('hidden');
    }
}

/**
 * Display error message
 * @param {String} message - Error message to display
 */
function showError(message) {
    const errorElement = document.getElementById('errorMessage');
    errorElement.textContent = message;
    errorElement.classList.remove('hidden');
    errorElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Hide error message
 */
function hideError() {
    document.getElementById('errorMessage').classList.add('hidden');
}

/**
 * Escape HTML special characters to prevent XSS
 * @param {String} text - Text to escape
 * @returns {String} - Escaped text
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * Initialize event listeners on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('ResuMatch frontend loaded successfully');
    
    // Optional: Auto-focus resume input
    document.getElementById('resumeInput').focus();
    
    // Optional: Enable Enter key for matching (Ctrl+Enter)
    document.addEventListener('keydown', function(event) {
        if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
            matchDocuments();
        }
    });
});

/**
 * Example function to load sample data for testing
 */
function loadSampleData() {
    document.getElementById('resumeInput').value = `
John Doe
Software Engineer | 5 Years Experience

Skills: Python, JavaScript, React, Flask, SQL, Machine Learning, NLP
Experience: 
- Senior Developer at Tech Company (2021-present)
- Full Stack Developer at StartUp (2019-2021)

Education: Bachelor's in Computer Science
    `.trim();

    document.getElementById('jobInput').value = `
Senior Software Engineer - Full Stack

Job Description:
We are looking for an experienced Software Engineer with expertise in:
- Full Stack Web Development
- Python and JavaScript
- React or Vue.js
- RESTful API Design
- SQL Databases
- Machine Learning (preferred)
- Natural Language Processing (nice to have)

Requirements:
- 5+ years of software development experience
- Strong problem-solving skills
- Experience with agile methodologies
- Bachelor's degree in Computer Science or related field

Benefits: Competitive salary, remote work, health insurance
    `.trim();
}
