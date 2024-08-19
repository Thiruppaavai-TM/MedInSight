# Drug Review Analysis System

This project analyzes drug reviews to predict conditions, drug ratings, side effects, and steroidal information. It also performs topic modeling on reviews and visualizes sentiment data.

## Project Structure

- `condition_predict.py`: Predicts conditions based on drug name and review.
- `drug_rating.py`: Predicts drug ratings based on drug name.
- `associated_patientcond_drug_types.py`: Provides side effects and steroidal information for drugs.
- `identifying_useful_elements.py`: Identifies useful elements in reviews through topic modeling.
- `understanding_negative_reviews.py`: Visualizes sentiment for drugs and searches drugs by condition.

## Installation

To run this project, you need to install the following packages. You can use `pip` to install them:

```bash

pip install pandas numpy scikit-learn lightgbm joblib imbalanced-learn gensim nltk matplotlib seaborn requests google-generativeai google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

#after installing nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

