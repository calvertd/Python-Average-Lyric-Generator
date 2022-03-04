import requests
import musicbrainzngs
import re

def print_menu():
    menu_options = {
        1: 'Average number of words in artists songs',
        2: 'Exit'
    }
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )


def get_artist_songs(input_artist):
    ### initialise app to enable use of API
    musicbrainzngs.set_useragent("cli_python_music_app","0.1","calvo6@hotmail.co.uk")

    try:
        ### search for albums. Have limited the search results to five albums as it may vary from artist to artist
        result = musicbrainzngs.search_releases(artist=input_artist, limit=5)
        if result["release-list"][0]['artist-credit'][0]['name'].lower() == input_artist.lower():

            album_info = set()
            for i in range(len(result["release-list"])):
                album_info.add(result["release-list"][i]['id'])

            for album_id in list(album_info):
            
                #### get songs via album id
                recordings = musicbrainzngs.get_release_by_id(album_id, includes=["recordings"])
                song_list = []
                t = (recordings["release"]["medium-list"][0]["track-list"])
                for x in range(len(t)):
                    song_list.append(t[x]["recording"]["title"])

                print("*** Compiling artist tracks ***")
                print("*** Retrieving the lyrics from each track ***")
                
                lyrics_list = []
                headers = {'content-type': 'application/json'}
                
                ### retrieve lyrics for each song using the other API endpoint
                for s in song_list:
                    url = f'https://api.lyrics.ovh/v1/{input_artist}/{s}'
                    response = requests.get(url, headers=headers)
                    if response.status_code > 201 or response.json() == None:
                        continue
                    lyrics_list.append(response.json())
            
            return lyrics_list

        else:
            print("Cannot find artist specified")
            exit()
    
    except IndexError:
        print("Cannot find artist specified")
        exit()


def find_mean_of_artists_lyrics(list_of_lyrics):
    try:
        lyric_numbers = []
        for i in range(len(list_of_lyrics)):
            lyric_numbers.append(len(re.findall(r'\w+', list_of_lyrics[i]['lyrics'])))
        
        return sum(lyric_numbers) / len(lyric_numbers)

    except ZeroDivisionError:
        print("No songs found for artist")
        return None


while(True):
    print_menu()
    try:
        option = int(input('Enter a number: '))
    except ValueError:
        print('Invalid option. Please enter a number...')

    if option == 1:
        artist_input = input("Enter an artist name: ")
        if artist_input is not None:
            lyrics = get_artist_songs(artist_input)
            print("**************")
            print(f"Average number of words per song for the artist {artist_input} is", find_mean_of_artists_lyrics(lyrics))
            print("**************")
    elif option == 2:
        print('Thanks for using the interface')
        exit()
    else:
        print('Invalid option. Please enter a number between 1 and 2.')
