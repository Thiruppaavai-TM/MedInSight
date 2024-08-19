"""
Original file is located at
    https://colab.research.google.com/drive/1L3atMzEPnXHeTF2sOyWWcXRdLq1QCBQs
"""

import joblib
import pandas as pd
from scipy.sparse import hstack
import numpy as np

def get_reviews_for_drug(df, drug_name):
    return df[df['drugname'] == drug_name]

def preprocess_reviews(reviews):
    reviews['review'] = reviews['review'].fillna('')  # Fill NaN with empty string
    reviews['review'] = reviews['review'].str.lower()  # Convert to lowercase
    return reviews

def transform_text_data(reviews, tfidf):
    return tfidf.transform(reviews['review'])

def combine_features(reviews, scaler, tfidf, numerical_features):
    X_numerical = reviews[numerical_features]  # Ensure the order matches
    X_numerical = X_numerical.replace([np.inf, -np.inf], np.nan).fillna(0)
    X_numerical_scaled = scaler.transform(X_numerical)
    X_text_tfidf = transform_text_data(reviews, tfidf)
    return hstack([X_text_tfidf, X_numerical_scaled])

def predict_drug_rating(drug_name):
    df = pd.read_csv('datasets/drug_data.csv')  # Replace with your dataset path

    # Load the saved model and preprocessing components
    lgb_model = joblib.load('models/lgb_model.pkl')
    tfidf_vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
    scaler = joblib.load('models/scaler.pkl')
    numerical_features = joblib.load('models/numerical_features.pkl')

    # Get reviews for the specified drug
    reviews = get_reviews_for_drug(df, drug_name)

    # Preprocess the reviews
    reviews = preprocess_reviews(reviews)

    # Combine features
    X_combined = combine_features(reviews, scaler, tfidf_vectorizer, numerical_features)

    # Predict ratings
    predictions = lgb_model.predict(X_combined)

    # Return or print the predicted ratings
    return predictions[0]

'''# Example usage:
drug_name = input('Enter the drug name: ')
predicted_ratings = predict_drug_rating(drug_name)
print(f'Predicted ratings for {drug_name}: {predicted_ratings}')
'''


