# SpotiTunes
SpotiTunes is a productivity improvement oriented software for DJ's or music passionate.
Its objective is to compare your desired playlists, in your Spotify account and in your iTunes local Library on your PC.
## Installation
Before the installation, you need to create a Spotify Application in order for you to get the API credentials for querying your Spotify account data, you can do it in the [Spotify developers website](https://developer.spotify.com/dashboard/).

Once you cloned the repository, build and install the package in the repository folder with:
```
python setup.py install
```
Done this, create a .env file in the spotitunes package folder and write inside it your Spotify API credentials in this format:
> CLIENT_ID = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' <br>
> CLIENT_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx' <br>
> SPOTIFY_USER_ID = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx' <br>

Then, write the following scope: <br>

> SCOPE = 'user-library-read user-follow-read playlist-read-private' <br>

And the last, your iTunes library xml path, for example: <br>

> DIR_ITUNES = 'C:/Users/JohnDoe/Music/iTunes/iTunes Music Library.xml' <br>

You also need to set up the deemix spotify plugin, you can do it by going to the installation directory, by default:

> C:/Users/\<username\>/AppData/Roaming/deemix/spotify/config.json

And write inside this file your Spotify API credentials in json format:

```
{
  "clientId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "clientSecret": "xxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "fallbackSearch": true
}
```
Save it, and the installation of SpotiTunes will be ready.
Take a look at the Appendages section for extra information.

## Usage

If everything goes right, you will see the following help section:

```
>>> SpotiTunes -h ~$
usage: SpotiTunes [-l] -s <spotify_playlist_name> -i <itunes_playlist_name>

Compares your provided Spotify playlist with your locally stored iTunes playlist with the same name and shows the differences. You can also add to iTunes   
the missing songs.

options:
  -h, --help      show this help message and exit
  -s , --spl      Your spotify playlist name
  -l, --liked     Set if you want to compare with your Spotify liked songs
  -i , --itunes   Your iTunes playlist name to compare with
```

Long story short, if you have a Spotify playlist named 'EDM' and an iTunes playlist named 'EDM' too, you can compare their content by:
```
>>> SpotiTunes -s 'EDM' -i 'EDM' ~$
```
SpotiTunes will fetch and compare all songs and show you a table like the following:
```
[INFO] Fetching data...
[INFO] Spotify data was fetched succesfully
[INFO] iTunes data was fetched succesfully
[INFO] Playlists differences found:
+--------------------------------------------------+----------------------------------------------------------------------+
|           IN SPOTIFY BUT NOT IN ITUNES           |                     IN ITUNES BUT NOT IN SPOTIFY                     |
+--------------------------------------------------+----------------------------------------------------------------------+
|       love is gone - alrt remix - slander        | love is gone feat. dylan matthew alrt remix - slander, dylan matthew |
|  give it to me - full vocal mix - matt sassari   |                                 ---                                  |
| destination calabria - radio edit - alex gaudino |                                 ---                                  |
+--------------------------------------------------+----------------------------------------------------------------------+
[?] Do you want to download and add all songs that are in spotify but not in itunes? (Y/n)
```
If you correctly set up the deemix plugin and you chose Yes in the previous question, deemix will download the Spotify songs and SpotiTunes will add it to the iTunes library playlist.

# TODO list

- [ ] Improve the data collection with threading.
- [ ] Check existing songs in itunes library and don't download them
- [ ] Improve the CLI with PyInquirer.
  - [ ] Let songs selection for downloading just the ones which you want.
  - [ ] Enable the deleting of songs the user wants to remove from iTunes/Spotify.
- [ ] Create a GUI.

# Appendages

## OAuth2 Spotipy Process

The first time you use SpotiTunes, the spotipy python library needs to do the OAuth2 process.
- For doing this you need to set a redirection website in your [Spotify Developers Portal Dashboard](https://developer.spotify.com/dashboard/).
Go to applications and select the application which you are using the credentials, click on "edit settings" and write the website you want to be redirected to in "Redirect URIs" (It can be whatever you want, for example: www.github.com) and click on Save before closing it.
- Done this if you run SpotiTunes with correct parameters, the website that you set in your dashboard will be opened, then, copy the URL with the query string and put it on the CLI of SpotiTunes.
```
   _____             __  _ ______
  / ___/____  ____  / /_(_)_  __/_  ______  ___  _____
  \__ \/ __ \/ __ \/ __/ / / / / / / / __ \/ _ \/ ___/
 ___/ / /_/ / /_/ / /_/ / / / / /_/ / / / /  __(__  )
/____/ .___/\____/\__/_/ /_/  \__,_/_/ /_/\___/____/
    /_/

[INFO] Fetching data...
Enter the URL you were redirected to: 
```
- Now, your PC will be correctly authenticated for querying Spotify data correctly.

## Deemix ARL

The first time you use SpotiTunes, if you want to download songs deemix will ask you for the ARL cookie of your Deezer Account.
You just need to copy it on the SpotiTunes CLI when you were asked.