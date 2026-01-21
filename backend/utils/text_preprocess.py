import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')

nltk.download('stopwords')
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