from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")

def get_token():
    """Getting access to Spotify token"""

    auth_string=client_id + ":" + client_secret
    auth_bytes=auth_string.encode("utf-8")
    auth_base64=str(base64.b64encode(auth_bytes), "utf-8")

    url="https://accounts.spotify.com/api/token"
    headers={
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data={"grant_type":"client_credentials"}
    result= post(url,headers=headers, data=data)
    json_result=json.loads(result.content)
    token=json_result["access_token"]
    return token

def get_auth_header(token):
    """Authorization header for future requests"""

    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    """Function that searches for artist of a specific name"""

    url="https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    #after type you write everything that you are looking for, after limit, number of answers
    query=f"q={artist_name}&type=artist&limit=1"
    query_url=url+"?"+query

    result=get(query_url,headers=headers)
    json_result=json.loads(result.content)["artists"]["items"]
    if len(json_result)==0:
        print('No result, sorry')
        return None
    return json_result[0]

def get_songs_by_artist(token, artist_id, country):
    """Gets top songs from specifit artist in given country"""

    url=f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country={country}"
    headers = get_auth_header(token)
    result=get(url,headers=headers)
    json_result=json.loads(result.content)["tracks"]
    return json_result

def get_artist_albums(token, artist_id):
    """Gets given artists albums"""

    url=f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    result=get(url,headers=headers)
    json_result=json.loads(result.content)["items"]
    return json_result

def print_artist_songs(token, artist_name, country_id):
    """Prints the most popular songs for given artist in given country"""

    result=search_for_artist(token, str(artist_name))
    artist_id=result["id"]
    songs=get_songs_by_artist(token, artist_id, str(country_id))

    for idx, song in enumerate(songs):
        print(f"{idx+1}. {song['name']}")
    
    input("Ready to go ahead? Click enter..")

def print_artist_albums(token,artist_name):
    """Prints artists albums"""

    result=search_for_artist(token, str(artist_name))
    artist_id=result["id"]
    
    albums=get_artist_albums(token, artist_id)
    for idx, album in enumerate(albums):
        print(f"{idx+1}. {album['name']}")

    print("do you want additional data?")
    decision=str(input("Y/N? "))

    if decision.upper()=="Y" or decision.upper()=="YES":
        for idx, album in enumerate(albums):
            print(f"{idx+1}. {album['name']}, \n\tdate of release: {album['release_date']}, \n\tnumber of tracks: {album['total_tracks']}")

    input("Ready to go ahead? Click enter..")

#def music_analysis(spotify):


def welcome_message():
    """Welcome message for user"""

    print("\nWelcome!\n")
    print("This is a specialized data analysis tool for Spotify using Spotify Web Api\n")

def main_menu(token):
    """Main functionality stereo"""

    print("\nWhat function do you want to use?\n")
    print("Basic features:")
    print("\t0. Quit")
    print("\t1. Find most popular songs from given artist")
    print("\t2. Find given artist's albums")
    print("\t3. Your spotify day - what happened on your birthday day?\n") # TO DO
    print("Advanced features:")
    print("\t3. Get artist recommendation.") # TO DO
    print("\t4. Get tracks recommendation.") # TO DO
    print("\t5. Analyze artists popularity in 2 countries.") # TO DO
    print("\t6. Compare 2 tracks.") # TO DO

    functionality=int(input())

    match functionality:
        case 1:
            artist_name=input("Type artist name: ")
            country=input("Type country code: ")
            print_artist_songs(token, artist_name, country)
            return True
        case 2:
            artist_name=input("Type artist name: ")
            print_artist_albums(token,artist_name)
            return True
        case 0:
            print("Thank you for using!")
            return False
        case _:
            print("Typo? Try again")
            return True

# Loading Spotify token
token=get_token()
welcome_message()

while main_menu(token):
    pass
