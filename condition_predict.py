"""
Original file is located at
    https://colab.research.google.com/drive/1129lV8FGnG-WvmTXiZjSdjZ1ep6Bw-gf
"""
import re
import pandas as pd
import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

'''
# Load the dataset
dataset = pd.read_csv('datasets/modified_file.csv')

pattern=r'[^a-zA-Z\s]'
dataset['review']=dataset['review'].str.replace(pattern,'',regex=True)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    if not isinstance(text, str):
        return ''
    words = word_tokenize(text)
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words and word not in string.punctuation]
    return ' '.join(words)

dataset['cleaned_review'] = dataset['review'].apply(preprocess_text)

# Using only relevant features
X = dataset[['drugName', 'cleaned_review']].copy()
y = dataset['condition']

# Combine drugname and review for vectorization
X.loc[:, 'combined'] = X['drugName'] + ' ' + X['cleaned_review']
vectorizer = CountVectorizer()
X_combined = vectorizer.fit_transform(X['combined'])

X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.2, random_state=42)

# Define RandomForestClassifier
rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the RandomForestClassifier
rf_clf.fit(X_train, y_train)

# Evaluate the model
rf_pred = rf_clf.predict(X_test)
#print("Random Forest Classifier Accuracy:", accuracy_score(y_test, rf_pred))


# Save the trained model as a pickle file
with open('random_forest_classifier.pkl', 'wb') as file:
    pickle.dump(rf_clf, file)

# Save the vectorizer
with open('vectorizer.pkl', 'wb') as file:
    pickle.dump(vectorizer, file)'''

# Function to predict condition based on drugname and review
def predict_condition(drugname, review):
    # Load the trained model and vectorizer
    with open('models/random_forest_classifier.pkl', 'rb') as file:
        rf_clf = pickle.load(file)
    
    with open('models/vectorizer1.pkl', 'rb') as file:
        vectorizer = pickle.load(file)
    
    # Preprocess the input data
    combined_input = drugname + ' ' + review
    transformed_input = vectorizer.transform([combined_input])
    
    # Predict the condition
    prediction = rf_clf.predict(transformed_input)
    
    return prediction[0]


def prediction(drugname, review):
    predicted_condition = predict_condition(drugname, review)
    return predicted_condition
    #print(f"Predicted Condition: {predicted_condition}")

'''drugname='Nitrofurantoin'
review='Macrobid caused me to get really sick and did NOT clear up a urinary tract infection  I will not take this medicine again as it was not right for me Drug: Nitrofurantoin'
print(prediction(drugname,review))'''