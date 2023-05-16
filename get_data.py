import spotipy
import config
from spotipy.oauth2 import SpotifyOAuth
import csv
import os
from tqdm import tqdm


client_id = config.SPOTIPY_CLIENT_ID
client_secret = config.SPOTIPY_CLIENT_SECRET
redirect_uri = config.SPOTIPY_REDIRECT_URI

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

try:
    os.mkdir('data')
    print("Created directory 'data'")
except FileExistsError:
    print("Found directory 'data'")

playlist_ids = []
labels = []

# Load the file with the playlist ids and their labels
with open("playlists.csv", "r") as f:
    reader = csv.reader(f)
    # Skip the headers
    next(reader, None)  
    for row in reader:
        playlist_ids.append(row[0])
        labels.append(row[1])


counter_studio = 0
counter_live = 0

for playlist_id, label in zip(playlist_ids, labels):

    if label == 'studio':
        counter_studio += 1
        counter = counter_studio
    else:
        counter_live += 1
        counter = counter_live

    # Get playlist and track IDs
    playlist = sp.playlist(playlist_id)
    total_tracks = playlist["tracks"]["total"]

    # Get audio features for each track
    features = []
    offset = 0
    limit = 100

    with tqdm(total=total_tracks, desc=f"Processing {label} playlist {counter}") as pbar:
        while offset < total_tracks:
            results = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
            tracks = results["items"]
            try:
                track_ids = [track["track"]["id"] for track in tracks]
            except:
                pass

            audio_features = sp.audio_features(track_ids)
            for track in audio_features:
                features.append(track)
                pbar.update(1)

            offset += limit


    # Save features to CSV file
    filename = f"{label}{counter}.csv"
    with open(f"data/{filename}", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "energy", "danceability", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature", "label"])
        for track in features:
            row = [track["id"], track["energy"], track["danceability"], track["key"], track["loudness"], track["mode"], track["speechiness"], track["acousticness"], track["instrumentalness"], track["liveness"], track["valence"], track["tempo"], track["duration_ms"], track["time_signature"], label]
            writer.writerow(row)

    print(f"Features saved to data/{filename}")
