# preprocessing.py
import pandas as pd
import re

def preprocess_text(df: pd.DataFrame) -> pd.DataFrame:
    def clean_text(text):
        # Remove special characters and extra spaces, convert to lowercase
        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        return text.lower()  # Convert to lowercase
    
    df['Text'] = df['Text'].apply(lambda x: clean_text(x) if isinstance(x, str) else x)
    return df
