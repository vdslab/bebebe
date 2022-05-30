import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from requests.exceptions import ReadTimeout
import spotify_id as sid

def serch_spotify_url(song_name):
  """
  # Spotify APIから曲名検索を行う
  Args:
    song_name: 曲名
  Returns:
    slug: URLの末尾の文字列。曲が見つからなければ文字列で404を返す。曲名と合致するデータがなければNoneを返す。
  """
  client_id = sid.CLIENT_ID#'your client id'
  client_secret = sid.SECRET_ID#'your secret id'
  sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret), requests_timeout=5)
  results = None
  try:
    results = sp.search(q=song_name, limit=1)
  except ReadTimeout:
    print('ReadTimeout, restart')
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret), requests_timeout=10)
    results = sp.search(q=song_name, limit=20)
  if(not results['tracks']['items']): return "404"
  slug = None
  print(song_name)
  for _,track in enumerate(results['tracks']['items']):
    if(track['name'] == song_name):
      slug = track['href'][track['href'].find('/tracks/')+len('/tracks/'):]
  return slug