import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


def preprocess_query(query):
    
    #extract :intitle operator
    preprocess, title = remove_intitle_operator(query)
    
    query = ' '.join([preprocess,title])
    #extrat " " operator
    preprocess, exact = extract_exact_phrases(query)
   
    query = ' '.join([preprocess,exact])
    
    # Tokenize the query into individual words
    tokens = word_tokenize(query.lower())  # Convert to lowercase for consistency
    #Check if :intitle operator is used
    
   
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Apply stemming (you can also consider lemmatization)
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]

    # Join the processed tokens back into a string
    processed_query = ' '.join(tokens)
    
    
    return processed_query, exact, title
    
   

def extract_exact_phrases(query):
# Use regular expression to find exact phrases in double quotes
    phrases = re.findall(r'"([^"]*)"', query)
    
    # Remove exact phrases from the query
    query = re.sub(r'"([^"]*)"', '', query)
    
    # Split the remaining query into individual words
    terms = query.split()
    terms = ' '.join(terms)
    phrases = ' '.join(phrases)
    return terms, phrases

def remove_intitle_operator(query):
    # Find phrases enclosed by | |
    phrases = re.findall(r'\|([^|]*)\|', query)
    
    # Remove exact phrases from the query
    query = re.sub(r'\|([^|]*)\|', '', query)
    
    # Split the remaining query into individual words
    terms = query.split()
    terms = ' '.join(terms)
    phrases = ' '.join(phrases)
    return terms, phrases