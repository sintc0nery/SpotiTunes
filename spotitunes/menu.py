from . import utilities as u
import argparse
from prettytable import PrettyTable
from pyfiglet import Figlet
import os
from PyInquirer import prompt

# MAIN PROGRAM


def main():

    parser = interactiveInitMenu()
    args = parser.parse_args()

    if not os.path.exists('.env'):
        print("[INFO] The credentials file doesn't exists, please create it.")
        quit()

    print("[INFO] Fetching data...")
    if(args.liked):
        songs_SP = u.getSongsPl_SP()
    else:
        songs_SP = u.getSongsPl_SP(args.spl)
        if songs_SP is None:
            parser.error("That spotify playlist doesn't exist")

    print("[INFO] Spotify data was fetched succesfully")

    songs_iT = u.getSongsPl_iT(args.itunes)

    print("[INFO] iTunes data was fetched succesfully")

    if songs_iT is None:
        answers = prompt(questions('createPl'))
        if answers['createPl']:
            u.createPl_iT(args.itunes)
        else:
            quit()

    not_in_it, not_in_sp = u.getDiffPls(songs_SP, songs_iT)

    if not not_in_it and not not_in_sp:
        print("[INFO] This playlists have the same content. All is up to date.")
        quit()

    print("[INFO] Playlists differences found:")
    displayTables(not_in_it, not_in_sp)

    menu_sp_it = prompt(questions('menu_sp_it'))
    if menu_sp_it['menu_sp_it'] == 0:
        u.downloadAddSongs(args.itunes, not_in_it)
    elif menu_sp_it['menu_sp_it'] == 1:
        print('TODO: itunes delete menu')
    else:
        quit()


def displayTables(not_in_it, not_in_sp):
    len_table = max(len(not_in_it), len(not_in_sp))
    aux_not_in_it = []
    counter = len_table
    for songNartist in not_in_it:
        if songNartist:
            aux_not_in_it.append(songNartist[0]+" - "+songNartist[1])
            counter -= 1
    while counter > 0:
        aux_not_in_it.append("---")
        counter -= 1

    aux_not_in_sp = []
    counter = len_table
    for songNartist in not_in_sp:
        if songNartist:
            aux_not_in_sp.append(songNartist[0]+" - "+songNartist[1])
            counter -= 1
    while counter > 0:
        aux_not_in_sp.append("---")
        counter -= 1

    columns = ["IN SPOTIFY BUT NOT IN ITUNES", "IN ITUNES BUT NOT IN SPOTIFY"]
    t = PrettyTable()
    t.add_column(columns[0], aux_not_in_it)
    t.add_column(columns[1], aux_not_in_sp)
    print(t)


def interactiveInitMenu():
    f = Figlet(font='slant')
    print(f.renderText('SpotiTunes'))
    parser = argparse.ArgumentParser(prog='SpotiTunes',
                                     usage='%(prog)s [-l] -s <spotify_playlist_name> -i <itunes_playlist_name>',
                                     description='Compares your provided Spotify playlist with your locally stored iTunes playlist with the same name and shows the differences.\n You can also add to iTunes the missing songs.')

    parser.add_argument('-s', '--spl', metavar='', type=str,
                        help='Your spotify playlist name')
    parser.add_argument('-l', '--liked', action='store_true',
                        help='Set if you want to compare with your Spotify liked songs')
    parser.add_argument('-i', '--itunes', metavar='', type=str,
                        help='Your iTunes playlist name to compare with')

    args = parser.parse_args()

    if(args.spl is None and args.liked is False):
        parser.error(
            "one of the arguments -s/--spl and -l/--liked is required")

    if(args.itunes is None):
        parser.error("the argument -i/--itunes is required")
    return parser

def questions(type):
    if type == 'createPl':
        return [
            {
                'type': 'confirm',
                'message': "That iTunes playlist doesn't exist, do you want to create it now?",
                'name': 'createPl',
                'default': True,
            }
        ]
    if type == 'menu_sp_it':
        return [
            {
                'type': 'list',
                'message': "What do you want to do now?",
                'name': 'menu_sp_it',
                'choices': ['Download and add songs from spotify to iTunes', 'Remove songs from iTunes', 'Quit'],
                'filter': lambda var: ['Download and add songs from spotify to iTunes', 'Remove songs from iTunes', 'Quit'].index(var)
            }
        ]

if __name__ == '__main__':
    main()
