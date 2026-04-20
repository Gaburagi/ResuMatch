"""
Helper Functions
Utility functions for data processing and analysis
"""

import logging

logger = logging.getLogger(__name__)


def load_dataset(file_path, encoding='utf-8'):
    """
    Load CSV dataset
    
    Args:
        file_path (str): Path to CSV file
        encoding (str): File encoding
        
    Returns:
        DataFrame: Loaded data
    """
    import pandas as pd
    try:
        df = pd.read_csv(file_path, encoding=encoding)
        logger.info(f'Dataset loaded: {file_path} ({len(df)} rows)')
        return df
    except UnicodeDecodeError:
        logger.warning(f'Encoding {encoding} failed, trying latin1')
        df = pd.read_csv(file_path, encoding='latin1')
        return df
    except Exception as e:
        logger.error(f'Error loading dataset: {str(e)}')
        raise


def normalize_score(score, min_val=0, max_val=100):
    """
    Normalize score to specified range
    
    Args:
        score (float): Raw score
        min_val (float): Minimum value
        max_val (float): Maximum value
        
    Returns:
        float: Normalized score
    """
    return max(min_val, min(max_val, score))


def format_response(data, status='success'):
    """
    Format standardized API response
    
    Args:
        data (dict): Response data
        status (str): Status message
        
    Returns:
        dict: Formatted response
    """
    return {
        'status': status,
        'data': data
    }
