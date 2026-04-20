"""
Text Cleaning and Preprocessing
Handles text normalization, tokenization, and feature extraction
"""

import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import logging

logger = logging.getLogger(__name__)

# Download required NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class TextCleaner:
    """Handles text cleaning and preprocessing"""
    
    def __init__(self):
        """Initialize the text cleaner"""
        self.stop_words = set(stopwords.words('english'))
    
    def clean_text(self, text):
        """
        Clean and normalize text
        
        Args:
            text (str): Raw text to clean
            
        Returns:
            str: Cleaned text
        """
        try:
            # Convert to lowercase
            text = text.lower()
            
            # Remove URLs
            text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
            
            # Remove email addresses
            text = re.sub(r'\S+@\S+', '', text)
            
            # Remove special characters and digits
            text = re.sub(r'[^a-zA-Z\s]', '', text)
            
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            
            return text
        except Exception as e:
            logger.error(f'Error cleaning text: {str(e)}')
            raise
    
    def tokenize(self, text):
        """
        Tokenize text into words
        
        Args:
            text (str): Text to tokenize
            
        Returns:
            list: List of tokens
        """
        try:
            tokens = word_tokenize(text)
            # Remove stopwords
            tokens = [token for token in tokens if token not in self.stop_words]
            return tokens
        except Exception as e:
            logger.error(f'Error tokenizing text: {str(e)}')
            raise
    
    def preprocess(self, text):
        """
        Complete preprocessing pipeline
        
        Args:
            text (str): Raw text
            
        Returns:
            list: Preprocessed tokens
        """
        cleaned = self.clean_text(text)
        tokens = self.tokenize(cleaned)
        return tokens


# Instantiate default cleaner
cleaner = TextCleaner()
