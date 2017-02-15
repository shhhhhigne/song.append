def get_track_info(track_id):


    track_results = spotify.search(q=user_input, type='track')
    track_items = track_results['tracks']['items']
    tracks = {}
    if len(track_items) > 0:
        for item in track_items:
            tracks[item['id']] = {'id': item['id'],
                                  'name': item['name'],
                                  'artist': item['artist']['name'],
                                  'artist_id': 
                                  'preview': item['preview_url'],
                                  'spotify_url': item['external_urls']['spotify']
                                  'album':
                                  }

        return tracks
    return None



def search(user_input):

    spotify = spotipy.Spotify()


    all_results = {'artists': None,
                   'tracks': None,
                   'playlists': None,
                   'albums': None}


    artist_results = spotify.search(q=user_input, type='artist')
    artist_items = artist_results['artists']['items']
    artists = {}
    if len(artist_items) > 0:
        for item in artist_items:
            artists[item['id']] = item['name']

        all_results['artists'] = artists



    track_results = spotify.search(q=user_input, type='track')
    track_items = track_results['tracks']['items']
    tracks = {}
    if len(track_items) > 0:
        for item in track_items:
            tracks[item['id']] = {'id': item['id'],
                                  'name': item['name'],
                                  'artist': item['artist']['name'],
                                  'artist_id': 
                                  'preview': item['preview_url'],
                                  'spotify_url': item['external_urls']['spotify']
                                  'album':
                                  }

        all_results['tracks'] = tracks


    playlist_results = spotify.search(q=user_input, type='playlist')
    playlist_items = playlist_results['playlists']['items']
    playlists = {}
    if len(playlist_items) > 0:
        for item in playlist_items:
            playlists[item['id']] = item['name']
        
        all_results['playlists'] = playlists


    album_results = spotify.search(q=user_input, type='album')
    album_items = album_results['albums']['items']
    albums = {}
    if len(album_items) > 0:
        for item in album_items:
            albums[item['id']] = item['name']

        all_results['albums'] = albums


    return all_results
    