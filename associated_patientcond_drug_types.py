"""
Original file is located at
    https://colab.research.google.com/drive/1HH113pgpNU3YLd_XE3lDa1C-ijDP45Sb
"""

import pandas as pd
import numpy as np
import google.generativeai as gen_ai



'''side_effect_keywords = [
    'nausea', 'headache', 'dizziness', 'fatigue', 'rash', 'diarrhea',
    'constipation', 'vomiting', 'insomnia', 'dry mouth', 'weight gain',
    'weight loss', 'hair loss', 'anxiety', 'depression', 'sweating',
    'itching', 'irritability', 'muscle pain', 'joint pain', 'weakness',
    'loss of appetite', 'blurred vision', 'abdominal pain', 'back pain','overeating','mood swings',
    'heavy periods'
]'''

'''def extract_side_effects(review):
    if pd.isna(review):
        return np.nan
    review_lower = review.lower()
    side_effects = [keyword for keyword in side_effect_keywords if keyword in review_lower]
    return ', '.join(side_effects) if side_effects else np.nan
df['side_effects'] = df['review'].apply(extract_side_effects)
df.head()'''

def gen_ai1(drugname):
    gen_ai.configure(api_key='AIzaSyDx8OsgbtDS3XBccgggzRvepqQwaCT8DF8')
    try:
        
        prompt = f"""
        Instructions:
        1. list the side effects of {drugname}.
        2. Ensure that the response should be categorized and contains only the names of the category name, such as "pain", "urinary problem", "digestive problem", "skin" etc.
        3. Do not include any other words, phrases, or explanations in the response.
        4. Each side effect should be unique. Do not list any repeated words or phrases.
        5. Exclude words that have the same or similar meanings (e.g., do not list both "fever" and "high temperature"—only include one).
        6. Do not include other side effects in the response
          ### Medicine:

            ### Side Effects:
        """
        # Create a new conversation
        response = gen_ai.chat(messages=prompt)
        # Last contains the model's response:
        q=response.last
        return q
    except:
        return 'API KEY EXHAUSTED'

def predicteffects(drugname):
    predict=gen_ai1(drugname)
    if predict:
        return predict
    else:
        return 'Drug Not found'

def is_steroidal(drugName):
    steroidal_drugs = ['Prednisone', 'Hydrocortisone', 'Dexamethasone', 'Cortisone', 'Fludrocortisone', 'Betamethasone', 'Hydrocortisone', 'Cortisone', 'Prednisone', 'Prednisolone', 'Methylprednisolone', 'Dexamethasone','Betamethasone','Triamcinolone','Fludrocortisone','Budesonide','Testosterone','Nandrolone','Stanozolol','Trenbolone','Medroxyprogesterone acetate','Norethindrone','Levonorgestrel','Etonogestrel','Desogestrel','Drospirenone','Estrogens','Estradiol','Estrone','Estriol','Danazol','Clomiphene','Tamoxifen','Spironolactone','Hydrocortisone', 'Cortisone', 'Prednisone', 'Prednisolone', 'Methylprednisolone', 'Dexamethasone', 'Betamethasone', 'Triamcinolone', 'Budesonide', 'Fluticasone', 'Beclomethasone', 'Mometasone', 'Clobetasol', 'Fluocinonide', 'Desonide', 'Diflorasone','Fludrocortisone', 'Aldosterone','Testosterone', 'Nandrolone', 'Oxandrolone', 'Stanozolol', 'Methandienone', 'Trenbolone', 'Boldenone', 'Oxymetholone', 'Methenolone', 'Drostanolone', 'Mesterolone', 'Fluoxymesterone', 'Tetrahydrogestrinone', 'Clostebol','Medroxyprogesterone acetate', 'Norethindrone', 'Levonorgestrel', 'Etonogestrel', 'Desogestrel', 'Drospirenone', 'Norgestimate', 'Megestrol acetate', 'Chlormadinone acetate', 'Dydrogesterone','Estradiol', 'Estrone', 'Estriol', 'Ethinylestradiol ', 'Mestranol','Androstenedione', 'Dehydroepiandrosterone', 'Cyproterone acetate', 'Spironolactone', 'Flutamide', 'Bicalutamide', 'Nilutamide','Danazol', 'Clomiphene', 'Tamoxifen', 'Mifepristone', 'Eplerenone', 'Finasteride', 'Dutasteride', 'Ketoconazole']
    steroidal_drugs=list(set(steroidal_drugs))
    if drugName in steroidal_drugs:
        return True
    else:
        return False
    
    
def check_steroid(drug_name):
    if is_steroidal(drug_name):
        return 'Steroidal'
    else:
        return 'Non-Steroidal'

def efx(drugname):
  side_effects = predicteffects(drugname)
  return side_effects.title()

'''drugname = input().strip() # Replace with the desired drug name
print(efx(drugname))
print(drugname," is ",check_steroid(drugname))'''