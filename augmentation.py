# augmentation.py
import pandas as pd
import random
from nltk.corpus import wordnet

# Ensure the NLTK wordnet is downloaded
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')

def augment_text(df: pd.DataFrame) -> pd.DataFrame:
    
    def get_synonyms(word):
        """Find synonyms using WordNet."""
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())
        # Remove the word itself from synonyms
        synonyms.discard(word)
        return list(synonyms)

    def augment_text_entry(text):
        """Apply logical augmentations to the text."""
        words = text.split()
        
        # Synonym Replacement: Randomly replace some words with synonyms
        augmented_words = []
        for word in words:
            # Only augment words that are more than 3 characters long to avoid small words
            if len(word) > 3 and random.random() < 0.2:  # 20% chance to augment a word
                synonyms = get_synonyms(word)
                if synonyms:
                    word = random.choice(synonyms)  # Replace with a random synonym
            augmented_words.append(word)
        
        # Random Insertion: Add a filler word randomly
        filler_words = ["actually", "seriously", "definitely", "perhaps", "mainly", "interestingly"]
        if random.random() < 0.15:  # 15% chance to insert a word
            insert_pos = random.randint(0, len(augmented_words))
            augmented_words.insert(insert_pos, random.choice(filler_words))
        
        return " ".join(augmented_words)

    df['Text'] = df['Text'].apply(lambda x: augment_text_entry(x) if isinstance(x, str) else x)
    return df
