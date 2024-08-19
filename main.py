import pandas as pd
import csv
import os
from condition_predict import prediction
from drug_rating import predict_drug_rating
from associated_patientcond_drug_types import efx, check_steroid
from identifying_useful_elements import perform_topic_modeling
from understanding_negative_reviews import visualize_sentiment_for_drug
import joblib

# Function to save input and output to a CSV file
def save_to_csv(task_name, user_input, output):
    file_path = 'task_results.csv'
    
    print(f"Saving results to: {file_path}")  # Debugging line
    
    # Check if file exists
    file_exists = os.path.isfile(file_path)
    
    # Define column names
    fieldnames = ['Task', 'User Input', 'Output']
    
    try:
        # Write to the CSV file
        with open(file_path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # Write the header only if the file is being created
            if not file_exists:
                writer.writeheader()
            
            writer.writerow({'Task': task_name, 'User Input': user_input, 'Output': output})
            print("Results saved successfully.")  # Debugging line
    except Exception as e:
        print(f"Error saving to CSV: {e}")  # Debugging line

# Function to perform all tasks together
def perform_all_tasks(drug_name, review):
    # Task 1: Predict Condition Based on Drug Name and Review
    condition_output = prediction(drug_name, review)
    
    # Task 2: Predict Drug Rating Based on Drug Name
    rating_output = predict_drug_rating(drug_name)
    
    # Task 3: Get Side Effects and Steroidal Information for a Drug
    side_effects = efx(drug_name)
    #steroid_info = check_steroid(drug_name)
    side_effects_output = f"Side Effects: {side_effects}"
    
    # Task 4: Identify Useful Elements in a Review
    top_words, topic_distributions, dominant_topic = perform_topic_modeling(review)
    topic_output = (f"Top words for each topic: {top_words}\n"
                    f"Topic distribution for the review: {topic_distributions}\n"
                    f"Dominant topic: {dominant_topic}\n")
    
    # Task 5: Visualize Sentiment for a Drug
    sentiment_results = visualize_sentiment_for_drug(drug_name, review)
    
    # Handle the sentiment visualization output
    sentiment_output = (
        f"Sentiment score: {sentiment_results['sentiment_score']:.2f}\n"
        f"Sentiment category: {sentiment_results['sentiment_category']}\n"
    )
    if sentiment_results['sentiment_category'] == 'Negative' and sentiment_results['sentiment_distribution']:
        sentiment_distribution_output = "\nSentiment distribution:\n"
        for category, count in sentiment_results['sentiment_distribution'].items():
            sentiment_distribution_output += (
                f"{category}: {count} "
                f"({count/sum(sentiment_results['sentiment_distribution'].values())*100:.1f}%)\n"
            )
        sentiment_output += sentiment_distribution_output
        if sentiment_results["visualization_path"]:
            sentiment_output += f"Visualization saved to: {sentiment_results['visualization_path']}\n"
    else:
        sentiment_output += sentiment_results.get("message", "No further analysis was performed.")
    
    # Combine all results into one output
    combined_output = (f"Predicted Condition: {condition_output}\n"
                       f"Predicted Rating: {rating_output}\n"
                       f"{side_effects_output}\n"
                       f"{topic_output}\n"
                       f"{sentiment_output}")
    
    # Debugging line
    print("Combined Output:")
    print(combined_output)  # Print combined output to check its content
    
    # Save the combined result to CSV
    save_to_csv("All Tasks", f"Drug: {drug_name}, Review: {review}", combined_output)

# Main function to handle user interaction
def main():
    print("Please provide the following details to perform all tasks:")
    
    # Get user input
    drug_name = input("Enter the drug name: ").strip()
    review = input("Enter the review: ").strip()
    
    # Perform all tasks together
    perform_all_tasks(drug_name, review)

# Run the main function
if __name__ == "__main__":
    main()
