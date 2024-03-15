# For data analysis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Loading the Spotify dataset
spotify=pd.read_csv("archive\\spotify-2023.csv", encoding='ISO-8859-1')

# Removing NaN values from all columns
spotify_cleaned = spotify.dropna()

print(spotify_cleaned.head())

spotify_cleaned= spotify_cleaned.rename(columns= ({'artist(s)_name':'artists_name'}))

# artists having most songs in top streamed songs
Top_artists=spotify_cleaned[['track_name','artists_name']]
Top_artists = spotify_cleaned['artists_name'].value_counts()
Top_artists.head(10).plot(kind= 'bar') 
plt.xlabel('Singer')
plt.ylabel('Count')
plt.title('Most frequently appearing artists in top streams')
plt.show()

#top streamed songs up untill 2023
Top_songs = spotify_cleaned[['track_name', 'streams']].copy()
# Convert 'streams' column to numeric, handling errors gracefully
Top_songs['streams'] = pd.to_numeric(Top_songs['streams'], errors='coerce')
# Select top 10 songs based on the highest number of streams
Top = Top_songs[['track_name', 'streams']].sort_values(by='streams', ascending=False).head(10)
print(Top)
plt.figure(figsize=(15,5))
plt.xlabel('Streams')
plt.ylabel('Songs')
plt.title('Most Streamed Songs on Spotify')
plt.show()