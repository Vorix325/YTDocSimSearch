import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from googleapiclient.discovery import build
import pandas as pd

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
    
videose = [
    {'videoId': '1', 'title': 'Introduction to Python', 'description': 'Learn the basics of Python programming.', 'tags': ['programming', 'Python','data']},
    {'videoId': '2', 'title': 'Web Development with Flask', 'description': 'Build web applications using Flask framework Python dataset.', 'tags': ['web development', 'Flask']},
    {'videoId': '3', 'title': 'Machine Learning Fundamentals', 'description': 'Explore the fundamentals of machine learning.', 'tags': ['machine learning', 'fundamentals']},
    {'videoId': '4', 'title': 'Data Visualization with Matplotlib', 'description': 'Create visualizations using Matplotlib library.', 'tags': ['data visualization', 'Matplotlib']},
    {'videoId': '5', 'title': 'Introduction to Natural Language Processing', 'description': 'An introduction to NLP techniques and applications.', 'tags': ['NLP', 'natural language processing']},
    # Add more videos as needed
]
   


 



# Function to rank videos based on similarity to the user's query
def rank_videos(videos, query):
    documents = [f"{video['title']} {video.get('description', '')}{' '.join(video.get('tags', []))}" for video in videos]
    
    # Combine the search query with the documents
    documents.append(query)
    
   
    # TF-IDF Vectorization
    count_vectorizer = CountVectorizer(stop_words='english')
    X = count_vectorizer.fit_transform(documents)
    df = pd.DataFrame(
    X.todense(),
    columns=count_vectorizer.get_feature_names_out(),
    index=[f"video_{i}" for i in range(len(videos))] + ["query"])
    # Compute cosine similarity between the query and each document
    similarities = cosine_similarity(df, df)
    print(df)

    print(similarities)
     # Sort videos based on similarity score in descending order
    videos_with_similarity = sorted(zip(videos, similarities[-1][:-1]), key=lambda x: x[1], reverse=True)
    # Filter out videos with cosine similarity 0 or lower
    videos_with_similarity = [(video, similarity) for video, similarity in videos_with_similarity if similarity > 0]

    # Extract only the videos in ranked order
    ranked_videos = [video for video, _ in videos_with_similarity]
    
    
    return ranked_videos
    





# Replace 'YOUR_API_KEY' with your actual YouTube Data API key
API_KEY = 'AIzaSyDqM8j3lFdL204293gFFkSCRtW1IeaWKEw'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def search(query):
   
    try:
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
        quesry, exact, intitle = preprocess_query(query)
        query = quesry
        
        search_response = youtube.search().list(
            q=query,
            type='video',
            part='id,snippet',
            maxResults=5
        ).execute()
       
        
        videos = []
        for search_result in search_response.get('items', []):
            
            videos.append({
                'title': search_result['snippet']['title'],
                'videoId': search_result['id']['videoId'],
                'thumbnail': search_result['snippet']['thumbnails']['default']['url'],
                'description': search_result['snippet']['description'],
                'tags': search_result['snippet'].get('tags', []),
               
            })
        print(exact)
        sorted_videos = rank_videos(videos,query)
         # Sort videos based on the order of ranks
        
        if(exact != ""):
            sorted_videos = [video for video in sorted_videos
             if (exact in video['title'] or
                 exact in video['description'])]
        
        if(intitle != ""):
            sorted_videos = [video for video in sorted_videos if intitle in video['title']]
            
        # Return only the top 10 videos
        sorted_videos = sorted_videos[:10]
        return videos

        

    except Exception as e:
        error_message = str(e)
        print(f"An error occurred: {error_message}")
      

print(search('Donbrother'))