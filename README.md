# SpotiTunes
SpotiTunes is a productivity-focused software for DJs or music enthusiasts. Its goal is to compare your desired playlists on your Spotify account and on your iTunes local library on your PC.
## Installation
Before installing, you need to create a Spotify application in order to get the API credentials for querying your Spotify account data. You can do this on the [Spotify developers website](https://developer.spotify.com/dashboard/).

Once you have cloned the repository, build and install the package in the repository folder with:
```
python setup.py install
```
After doing this, create a .env file in the spotitunes package folder and add your Spotify API credentials in the following format:
> CLIENT_ID = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' <br>
> CLIENT_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx' <br>
> SPOTIFY_USER_ID = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx' <br>

Then, add the following scope: <br>

> SCOPE = 'user-library-read user-follow-read playlist-read-private' <br>

Lastly, add the path to your iTunes library xml file, for example:  <br>

> DIR_ITUNES = 'C:/Users/JohnDoe/Music/iTunes/iTunes Music Library.xml' <br>

You also need to set up the deemix Spotify plugin. You can do this by going to the installation directory, which is by default:

> C:/Users/\<username\>/AppData/Roaming/deemix/spotify/config.json

Then, add your Spotify API credentials in JSON format to this file:

```
{
  "clientId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "clientSecret": "xxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "fallbackSearch": true
}
```
Save the file, and the installation of SpotiTunes will be complete.
Refer to the Appendices section for additional information.

## Usage

If everything is set up correctly, you will see the following help section:

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

In short, if you have a Spotify playlist named 'EDM' and an iTunes playlist named 'EDM' as well, you can compare their contents by:

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
|        papaoutai extended mix - stromae          | love is gone feat. dylan matthew alrt remix - slander, dylan matthew |
|  give it to me - full vocal mix - matt sassari   |                                 ---                                  |
| destination calabria - radio edit - alex gaudino |                                 ---                                  |
+--------------------------------------------------+----------------------------------------------------------------------+
? What do you want to do now?  (Use arrow keys)
 ❯ Download and add songs from spotify to iTunes
   Remove songs from iTunes
   Quit
```
<del>If you correctly set up the Deemix plugin and you chose Yes in the previous question, Deemix will download the Spotify songs and SpotiTunes will add it to the iTunes library playlist.
</del>
<br> TODO explanation of menu

# TODO list

- [ ] Improve data collection with threading.
- [ ] Check existing songs in the iTunes library and don't download them.
- [x] Improve the CLI with PyInquirer.
  - [x] Allow song selection for downloading only the ones that you want.
  - [ ] Enable the deletion of songs that the user wants to remove from iTunes/Spotify.
- [ ] Create a GUI.

# Appendages

## OAuth2 Spotipy Process

The first time you use SpotiTunes, the Spotipy Python library needs to perform the OAuth2 process.
- To do this, you need to set a redirect website in your [Spotify Developers Portal Dashboard](https://developer.spotify.com/dashboard/).
Go to Applications and select the application that you are using the credentials for, click "Edit settings" and enter the website you want to be redirected to in "Redirect URIs" (It can be whatever you want, for example: www.github.com) Click Save before closing it.
- Once you have done this, if you run SpotiTunes with the correct parameters, the website that you set in your dashboard will be opened. Then, copy the URL with the query string and enter it on the SpotiTunes CLI.
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
- Now, your environment will be correctly authenticated for querying Spotify data.

## Deemix ARL

The first time you use SpotiTunes, if you want to download songs Deemix will ask you for the ARL cookie of your Deezer account.
You just need to copy it on the SpotiTunes CLI when prompted.