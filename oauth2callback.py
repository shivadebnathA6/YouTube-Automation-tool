import os
import google.auth.transport.requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
import json
from flask import Flask, redirect, request, session, url_for

app = Flask(__name__)
app.secret_key = 'add your api key'

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
UPLOADED_VIDEOS_FILE = "uploaded_videos.txt"
VIDEOS_FILE = "videos.txt"

@app.route('/')
def index():
    if 'credentials' not in session:
        return redirect('authorize')

    credentials = google.oauth2.credentials.Credentials(**session['credentials'])

    youtube = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    session['credentials'] = credentials_to_dict(credentials)
    return redirect(url_for('upload'))

@app.route('/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    session['state'] = state

    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('index'))

@app.route('/upload')
def upload():
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])

    youtube = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    video_details = fetch_video_details_from_file()
    if not video_details:
        return "No new videos to upload."

    request_body = {
        "snippet": {
            "title": video_details["title"],
            "description": video_details["description"],
            "tags": video_details["tags"]
        },
        "status": {
            "privacyStatus": "private"
        }
    }

    media_file = MediaFileUpload(video_details["video_path"], chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if response is not None:
            print(f'Video uploaded successfully. Video ID: {response["id"]}')
            log_uploaded_video(video_details["video_path"])

    session['credentials'] = credentials_to_dict(credentials)
    return "Video uploaded successfully."

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

def fetch_video_details_from_file():
    uploaded_videos = set()
    if os.path.exists(UPLOADED_VIDEOS_FILE):
        with open(UPLOADED_VIDEOS_FILE, 'r', encoding='utf-8') as f:
            uploaded_videos = set(line.strip() for line in f)

    with open(VIDEOS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\\')
            if len(parts) < 2:
                print(f"Skipping invalid line: {line.strip()}")
                continue
            
            video_path = parts[0]
            title = parts[1]
            description = parts[2] if len(parts) > 2 else ""
            tags = parts[3].split(',') if len(parts) > 3 else []

            if video_path not in uploaded_videos:
                return {
                    "video_path": video_path,
                    "title": title,
                    "description": description,
                    "tags": tags
                }

    return None

def log_uploaded_video(video_path):
    with open(UPLOADED_VIDEOS_FILE, 'a') as f:
        f.write(video_path + '\n')

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run('localhost', 8080, debug=True)
