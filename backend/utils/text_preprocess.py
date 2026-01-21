import nltk
import os

# Download NLTK data only if not already present (with error handling)
def download_nltk_data():
    """Download NLTK data with error handling for deployment environments."""
    try:
        nltk_data_path = os.path.join(os.path.expanduser('~'), 'nltk_data')
        if not os.path.exists(nltk_data_path):
            os.makedirs(nltk_data_path, exist_ok=True)
        
        # Download with quiet=True to reduce logs, and only if not present
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
        
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            nltk.download('punkt_tab', quiet=True)
        
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet', quiet=True)
        
        try:
            nltk.data.find('corpora/omw-1.4')
        except LookupError:
            nltk.download('omw-1.4', quiet=True)
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
    except Exception as e:
        # Log but don't fail - data might already be available
        print(f"Note: NLTK data download issue (may already be present): {e}")

# Download NLTK data on import
download_nltk_data()

from nltk.corpus import stopwords

from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import string
import pandas as pd


# ps = PorterStemmer()
# lemmatizer = WordNetLemmatizer()


def transform_text(text):
  text = text.lower() #lowercase converter
  text = nltk.word_tokenize(text) #tokenizes the text

  y = []
  for i in text:
    if i.isalnum(): # removes special chars like ! ?
      y.append(i)

  text = y[:]
  y.clear()

  for i in text:
    if i not in stopwords.words('english') and i not in string.punctuation:
      y.append(i) #Stopwords and punctuations removed

#   text = y[:]
#   y.clear()

#   for i in text:
#     y.append(lemmatizer.lemmatize(i))  # Lemmatization

#   for i in text:
#     y.append(ps.stem(i)) #Stemming e.g.: loves --> love (root word)

  return " ".join(y) # this returns the list 'y' in a string format