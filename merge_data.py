import csv
import glob



data=[]
files = glob.glob("data/*.csv")

for file in files:

    with open(file, 'r') as f:
        # Read the CSV files
        reader = csv.DictReader(open(file, 'r'))

        # Combine the rows
        for row in reader:
            data.append(row)
        

# Write the combined rows to a new CSV file
fieldnames = ['id', 'energy', 'danceability', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature', 'label']
with open('songs.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)


print("Saved at 'songs.csv'.")
