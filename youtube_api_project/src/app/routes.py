from flask import current_app,Blueprint, render_template, request, jsonify
from googleapiclient.discovery import build
from ..search.rank import rank_videos
from ..query.advance_query import preprocess_query
main = Blueprint('main', __name__)


# Replace 'YOUR_API_KEY' with your actual YouTube Data API key
API_KEY = 'AIzaSyDqM8j3lFdL204293gFFkSCRtW1IeaWKEw'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')

    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400

    try:
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
        quesry, exact, intitle = preprocess_query(query)
        query = quesry
        search_response = youtube.search().list(
            q=query,
            type='video',
            part='id,snippet',
            maxResults=30
        ).execute()
        current_app.logger.info("YouTube API response: %s", search_response)
        
        videos = []
        for search_result in search_response.get('items', []):
            
            videos.append({
                'title': search_result['snippet']['title'],
                'videoId': search_result['id']['videoId'],
                'thumbnail': search_result['snippet']['thumbnails']['default']['url'],
                'description': search_result['snippet']['description'],
                
               
            })
        
        sorted_videos = rank_videos(videos,query)
         # Sort videos based on the order of ranks
        
        if(exact != ""):
            sorted_videos = [video for video in sorted_videos
             if (exact.lower() in video['title'] or
                 exact.lower() in video['description'])]
        
        if(intitle != ""):
            sorted_videos = [video for video in sorted_videos if intitle in video['title']]
            
        # Return only the top 10 videos
        sorted_videos = sorted_videos[:10]
        return jsonify({'videos': sorted_videos})

        

    except Exception as e:
        error_message = str(e)
        print(f"An error occurred: {error_message}")
        return jsonify({'error': str(e)}), 500





