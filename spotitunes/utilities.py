import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from libpytunes import Library
import unidecode as u
import win32com.client
import os
import calendar
import datetime
import subprocess
from PyInquirer import prompt


itunes = win32com.client.Dispatch("iTunes.Application")
load_dotenv('.env')

def getSongsPl_SP(pl_name=None):

    spotiSongs = []

    auth_manager = SpotifyOAuth(
        scope=os.getenv('SCOPE'),
        username=os.getenv('SPOTIFY_USER_ID'),
        redirect_uri='https://github.com/sintc0nery',
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET')
    )

    sp = spotipy.Spotify(auth_manager=auth_manager)

    result = None

    if pl_name == None:
        iterating_offset = 0
        items = []
        while True:
            result = sp.current_user_saved_tracks(limit=50,offset=iterating_offset)
            if not result['items']:
                break
            items += result['items']
            iterating_offset += 50
    else:
        pls_raw = sp.current_user_playlists(limit=50)
        pls_rawitems = pls_raw['items']
        for pl in pls_rawitems:
            if pl['name'] == pl_name:
                iterating_offset = 0
                items = []
                while True:
                    result = sp.user_playlist_tracks(playlist_id=pl['id'],limit=50,offset=iterating_offset)
                    if not result['items']:
                        break
                    items += result['items']
                    iterating_offset += 50
                break

    if result is None:
        return None

    for item in items:
        almost_clean_name = u.unidecode(item['track']['name'].lower())
        clean_name = almost_clean_name.replace("(","").replace(")","").replace("[","").replace("]","")
        almost_clean_artist = u.unidecode(item['track']['artists'][0]['name'].lower())
        clean_artist = almost_clean_artist.replace("(","").replace(")","").replace("[","").replace("]","")
        clean_artist = clean_artist.split(" & ")[0]
        clean_artist = clean_artist.split(" x ")[0]
        spotiSongs.append([clean_name,clean_artist,item['track']['external_urls']['spotify']])
    
    return spotiSongs

def getDiffPls(songs_SP,songs_iT):
    not_in_sp = songs_iT
    not_in_it = []
    located_song = False

    if not songs_iT:
        not_in_it = songs_SP
        not_in_sp = []
        return not_in_it,not_in_sp

    for i, cancion_sp in enumerate(songs_SP):
        located_song = False
        words_t_sp = cancion_sp[0].split(" ")
        for j, cancion_it in enumerate(songs_iT):
            words_t_it = cancion_it[0].split(" ")
            if (((all(substring in cancion_it[0] for substring in words_t_sp)) or (all(substring in cancion_sp[0] for substring in words_t_it))) and (cancion_sp[1] in cancion_it[1])):
                not_in_sp.pop(j)
                located_song = True
                break

        if not located_song:
            not_in_it.append(cancion_sp)

    return not_in_it,not_in_sp

def getSongsPl_iT(pl_name):

    l = Library(os.getenv('DIR_ITUNES'))

    itunSongs = []

    pl = l.getPlaylist(pl_name)
    if pl is None:
        return None
    
    pl = pl.tracks

    for song in pl:
        almost_clean_name = u.unidecode(song.name.lower())
        clean_name = almost_clean_name.replace("(","").replace(")","").replace("[","").replace("]","").replace(" x "," ")

        clean_artist = 'None'
        if song.artist is not None:
            almost_clean_artist = u.unidecode(song.artist.lower())
            clean_artist = almost_clean_artist.replace("(","").replace(")","").replace("[","").replace("]","").replace(" x "," ")

        itunSongs.append([clean_name, clean_artist])

    return itunSongs

def getiTunesSource():
    itunes_sources = itunes.Sources
    for source in itunes_sources:
        if source.Kind == 1:
            return source

def createPl_iT(pl_name):
    itunes = win32com.client.Dispatch("iTunes.Application")
    itunes.CreatePlaylist(pl_name)

def getiTunesPlCOM(pl_name):
    pls = getiTunesSource().Playlists
    remaining = pls.Count
    while remaining != 0:
        if pls.Item(remaining).Name == pl_name:
            return pls.Item(remaining)
        remaining-=1

def addSongPl_iT(pl_name,songs_path):
    playlist = getiTunesPlCOM(pl_name)
    playlist.AddFile(songs_path)

def downloadAddSongs(pl_name,songsToDownload):
    #TODO list of songs to select
    choices = []
    choices.append({'name': 'Download all songs', 'checked': True})
    for song in songsToDownload:
        choices.append({'name': song[0], 'checked': False})
    questions = [
        {
            'type': 'checkbox',
            'qmark': ' ♪ ',
            'message': 'Select the songs you want to download',
            'name': 'songs',
            'choices': choices,
            'validate': lambda answer: 'You must choose at least one song.' \
                if len(answer) == 0 else True
        }
    ]

    songsSelected = prompt(questions)
    if 'Download all songs' not in songsSelected['songs']:
        toRemove = []
        for i,song in enumerate(songsToDownload):
            if songsToDownload[i][0] not in songsSelected['songs']:
                toRemove.append(songsToDownload[i])
        for s in toRemove:
            songsToDownload.remove(s)

    date = datetime.datetime.utcnow()
    timestamp = str(calendar.timegm(date.utctimetuple()))
    path = "./deemix-"+pl_name+"-"+timestamp+"/"
    if not os.path.exists(path):
        os.makedirs(path)
    urls = []
    urls.append('deemix')
    urls.append('--path')
    urls.append(path)
    for song in songsToDownload: urls.append(song[2])
    proc_deemix = subprocess.Popen(urls)
    print('[INFO] Downloading songs...')
    try:
        proc_deemix.wait()
    except Exception as e:
        print("[ERROR] Some songs could not be downloaded")
    else:
        print("[INFO] Songs downloaded successfully!")
    print("[INFO] Adding it to "+pl_name+"...")
    files = os.listdir(path)
    ext_path = os.path.abspath(path)
    try:
        for file in files: addSongPl_iT(pl_name,ext_path+"\\"+file)
    except Exception as e:
        print("[ERROR] There was an error adding your songs to iTunes")
    else:
        print("[SUCESS] All your songs were downloaded and added to your playlist")
