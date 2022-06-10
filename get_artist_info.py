import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = ''
client_secret = ''
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret), requests_timeout=5)

artist = sp.artist("artist uri")
# print(artist)
print(artist["genres"])
