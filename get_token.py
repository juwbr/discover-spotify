import spotipy
from spotipy.oauth2 import SpotifyOAuth
from credentials import CLIENT_ID, CLIENT_SECRET

scope = ['ugc-image-upload', 'user-read-playback-state', 'user-modify-playback-state', 'user-read-currently-playing', 'app-remote-control', 'streaming', 'playlist-read-private', 'playlist-read-collaborative', 'playlist-modify-private', 'playlist-modify-public', 'user-follow-modify', 'user-follow-read', 'user-read-playback-position', 'user-top-read', 'user-read-recently-played', 'user-library-modify', 'user-library-read', 'user-read-email', 'user-read-private']

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,                                                          
                                                redirect_uri="http://localhost",
                                                scope=scope))

token = sp.auth_manager.get_access_token(as_dict=False)

with open('token.txt', 'w') as f:
    f.write(token)
