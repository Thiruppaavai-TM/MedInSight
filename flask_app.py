from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import random
import string
import os

# Import necessary functions from main code
from condition_predict import prediction
from drug_rating import predict_drug_rating
from associated_patientcond_drug_types import efx, check_steroid
from identifying_useful_elements import perform_topic_modeling
from understanding_negative_reviews import visualize_sentiment_for_drug

# Import Google Sheets API client and error handling
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Setup Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'google_sheets_credentials/drug-review-project-627edc2546a8.json'
SPREADSHEET_ID = '1JTygK5cqGdXF4K_KNL-fD30rcrd85BiWdEe2ndmdnKE'
RANGE_NAME = 'Sheet1!A1:E'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)

def get_next_serial_number():
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        ).execute()
        values = result.get('values', [])
        if values:
            last_row = values[-1]
            last_serial = int(last_row[0]) if last_row[0].isdigit() else 0
            return last_serial + 1
        else:
            return 1
    except HttpError as err:
        print(f"An error occurred: {err}")
        return 1

def append_to_sheet(values):
    try:
        body = {
            'values': values
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body=body
        ).execute()
        return result
    except HttpError as err:
        print(f"An error occurred: {err}")
        return None

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def generate_otp():
    return ''.join(random.choices(string.digits, k=4)) # 4-digit OTP

otp_storage = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/index')
def index():
    if 'logged_in' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/perform_task', methods=['POST'])
def perform_task():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    drug_name = request.form.get('drug_name')
    review = request.form.get('review')
    serial_number = get_next_serial_number()

    # Task 1: Predict Condition
    condition_output = prediction(drug_name, review)
    
    # Task 2: Predict Drug Rating
    rating_output = predict_drug_rating(drug_name)
    
    # Task 3: Identify Side Effects 
    side_effects_output = efx(drug_name)
    side_effects_output = side_effects_output.replace('*', ',').replace(',**', ' ').replace(':**', ':')

    
    # Task 4: Identify Dominant Topic from Review
    top_words, topic_distributions, dominant_topic = perform_topic_modeling(review)
    topic_output = (f"<b>Top words for each topic:</b> {top_words}<br>"
                    f"<b>Topic distribution for the review:</b> {topic_distributions}<br>"
                    f"<b>Dominant topic:</b> {dominant_topic}<br>")
    
    # Task 5: Visualize Sentiment for Drug
    img_path = os.path.join('static', 'images', f'{drug_name}_sentiment.png')
    results = visualize_sentiment_for_drug(drug_name, review, save_to=img_path)
    
    # Check if image was generated and convert to base64 if needed
    img_data = None
    if results["visualization_path"]:
        with open(results["visualization_path"], "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')

    # Log results to Google Sheets
    append_to_sheet([
        [serial_number, drug_name, review, 
         f"Condition: {condition_output}, Rating: {rating_output}, Side Effects: {side_effects_output}, "]
    ])
    
    # Prepare result output with HTML formatting
    result_output = (
        f"<h4>Predicted Condition:</h4><p>{condition_output}</p><br>"
        f"<h4>Predicted Rating:</h4><p>{rating_output}</p><br>"
        f"<h4>Side Effects:</h4><p>{side_effects_output}</p><br>"
        f"<h4>Topic Modeling Output:</h4><p>{topic_output}</p><br>"
        f"<h4>Sentiment Analysis:</h4><p>Sentiment score: {results['sentiment_score']:.2f}<br>"
        f"Sentiment category: {results['sentiment_category']}</p><br>"
    )
    
    if results['sentiment_category'] == 'Negative' and results['sentiment_distribution']:
        sentiment_distribution_output = "<h4>Sentiment Distribution:</h4><p>"
        for category, count in results['sentiment_distribution'].items():
            sentiment_distribution_output += (
                f"{category}: {count} "
                f"({count/sum(results['sentiment_distribution'].values())*100:.1f}%)<br>"
            )
        sentiment_distribution_output += "</p>"
        result_output += sentiment_distribution_output
        #if img_data:
            #result_output += f"<h4>Visualization image:</h4><img src='data:image/png;base64,{img_data}'><br>"
    else:
        result_output += results.get("message", "No further analysis was performed.")
    
    return jsonify({'result': result_output, 'image': img_data})

@app.route('/login_otp', methods=['POST','GET'])
def login_otp():
    session['logged_in']=True
    print({'msg': "session has been set successfully"})
    return jsonify({'msg': "session has been set successfully"})
      
if __name__ == '__main__':
    # Ensure the 'static/images' directory exists
    if not os.path.exists('static/images'):
        os.makedirs('static/images')
        
    app.run()
