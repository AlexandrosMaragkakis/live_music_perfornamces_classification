import spotipy
import config
from spotipy.oauth2 import SpotifyOAuth
import csv


client_id = config.SPOTIPY_CLIENT_ID
client_secret = config.SPOTIPY_CLIENT_SECRET
redirect_uri = config.SPOTIPY_REDIRECT_URI

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

# Get playlist ID from user input
playlist_id = "4YcKV5lHyR8Aj8Lrn09U9S"


# Get playlist and track IDs
playlist = sp.playlist(playlist_id)
total_tracks = playlist["tracks"]["total"]


# Get audio features for each track
features = []
offset = 0
limit = 100

while offset < total_tracks:
    results = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
    tracks = results["items"]
    track_ids = [track["track"]["id"] for track in tracks]

    audio_features = sp.audio_features(track_ids)
    for track in audio_features:
        features.append(track)

    offset += limit

# Save features to CSV file
filename = "studio.csv"
with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "energy", "danceability", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature", "class"])
    for track in features:
        label = 'studio'
        row = [track["id"], track["energy"], track["danceability"], track["key"], track["loudness"], track["mode"], track["speechiness"], track["acousticness"], track["instrumentalness"], track["liveness"], track["valence"], track["tempo"], track["duration_ms"], track["time_signature"], label]
        writer.writerow(row)

print(f"Features saved to {filename}")