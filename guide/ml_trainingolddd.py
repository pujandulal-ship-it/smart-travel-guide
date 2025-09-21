"""
Travel Guide ML Training Script - COMPLETE WORKING VERSION
Trains a multi-output classifier for travel recommendations
Handles items, places, apps, and tips predictions with proper list handling
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.multioutput import MultiOutputClassifier
import joblib
import os
import sys

def main():
    try:
        # Configuration
        CSV_FILE = 'test_data.csv'  # Change to 'travel_data.csv' after testing
        print(f"Loading dataset: {CSV_FILE}")
        
        # Load the dataset
        data = pd.read_csv(CSV_FILE)
        print(f"Dataset shape: {data.shape}")
        print("\nFirst 5 rows:")
        print(data.head())
        
    except FileNotFoundError:
        print(f"Error: {CSV_FILE} not found. Please ensure it's in the current directory.")
        print("Current directory:", os.getcwd())
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: {CSV_FILE} is empty or malformed.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        sys.exit(1)

    # Data validation
    print("\n" + "="*50)
    print("DATA VALIDATION")
    print("="*50)
    
    # Required columns
    required_columns = ['destination', 'season', 'activity', 'recommended_items']
    optional_columns = ['famous_places', 'recommended_apps', 'tips']
    
    # Check required columns
    for col in required_columns:
        if col in data.columns:
            empty_count = data[col]