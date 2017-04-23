'''Containing functions to interact with spotify web api wrapper'''

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import spotipy.util as util
import requests
import datetime

# Constants
USER_NAME = '1112218246'
CLIENT_ID = '21e79949d7714f39b78532e3c27672fc'
CLIENT_SECRET = '8fb9db7204d04075b6e05a296b043136'
SCOPE = "user-library-read playlist-modify-public playlist-modify-private playlist-read-private"

USER_OAUTH = 'BQB4ICipSAi_KI5g8wY_2Gp08WxxhWzmumZKR_H_ryK-BeYLhfKaJD9l1eE3yS3O2RBbdyMt_zTR7zqvaVVAEcGecuA68jp5HcdCvpFvpmmcL5A62AP8GbGLFGY8oZm5fO6G6ZB4UA'

def _get_spotipy_object(user_id):
    '''Return a spotipy object with authentications'''
    token = util.prompt_for_user_token(user_id, SCOPE)
    sp = spotipy.Spotify(auth=token)
    return sp
    pass


def _get_generated_recommendation_tracks(sp_obj, country_code, genre_seed_list, energy_level=0.5):
    '''Returns a result based on a energy level and genre_seed_list and market'''
    #energy attribute was previous
    results = sp_obj.recommendations(seed_genres=genre_seed_list, valence=energy_level, market=country_code, limit=10)
    return results

def _create_public_playlist_and_add_tracks(sp_obj, results, user_name):
    '''Create a public playilist and add tracks to it.'''
    # Creating a public playlist
    sp_obj.trace = False
    playlist_name = datetime.datetime.now().strftime("%H-%M-%S")
    playlists = sp_obj.user_playlist_create(user_name, playlist_name)
    # Find id of the playlist
    playlists = sp_obj.current_user_playlists(limit=10)
    playlists = playlists['items']
    for playlist in playlists:
        if playlist['name'] == playlist_name:
            playlist_id = playlist['id']
            break
    # Adding tracks from results
    tracks_list = results['tracks']
    list_of_track_ids = [track['id'] for track in tracks_list]
    results = sp_obj.user_playlist_add_tracks(user_name, playlist_id, list_of_track_ids)
    return results


def generate_playlist(list_of_genres, country_code, energy_value):
    '''Public function to generate a playlist'''
    sp_obj = _get_spotipy_object(USER_NAME)
    results = _get_generated_recommendation_tracks(sp_obj, country_code, list_of_genres, energy_value)
    print _create_public_playlist_and_add_tracks(sp_obj, results, USER_NAME)


if __name__ == "__main__":
    generate_playlist(['classical', 'rock'], "GB", 0.506)
