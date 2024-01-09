
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import pandas as pd
import matplotlib.pyplot as plt

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
    
     # Sort videos based on similarity score in descending order
    videos_with_similarity = sorted(zip(videos, similarities[-1][:-1]), key=lambda x: x[1], reverse=True)
   

    # Extract only the videos in ranked order
    ranked_videos = [video for video, _ in videos_with_similarity]
    
    video_titles = [video['title'] for video in ranked_videos]
    similarity_scores = [score for _, score in videos_with_similarity]
    plt.bar(video_titles, similarity_scores, color='blue')
    plt.xlabel('Video Titles')
    plt.ylabel('Cosine Similarity Score')
    plt.title('Video Similarity to Query')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
    return ranked_videos
    


