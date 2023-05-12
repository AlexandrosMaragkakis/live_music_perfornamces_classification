import csv
import random

# Read the CSV files
live_csv = csv.DictReader(open('live.csv'))
studio_csv = csv.DictReader(open('studio.csv'))

# Combine the rows
rows = []
for row in live_csv:
    row['label'] = 'live'
    rows.append(row)
for row in studio_csv:
    row['label'] = 'studio'
    rows.append(row)

# Shuffle the rows
random.shuffle(rows)

# Write the combined rows to a new CSV file
fieldnames = ['id', 'energy', 'danceability', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature', 'label']
with open('songs.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Combined and shuffled CSV file saved as 'songs.csv'")
