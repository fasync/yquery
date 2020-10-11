#!/usr/local/bin/python3.7

from os import system
import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# see https://console.cloud.google.com/apis/credentials TODO: Use oauth instead
APIKEY = open("./api.key", "r").read()

class Youtube:
    def __init__(self):
        self.videos = []
        self.channels = []
        self.playlists = []
    
    def search(self, search_string, mres=20, videos=True, channels=False, playlists=False):
        api = build('youtube', 'v3', developerKey=APIKEY)

        # starting query
        query_result = api.search().list(q=search_string, part='id,snippet', maxResults=mres).execute()

        for result in query_result.get('items', []):
            if videos:
                if result['id']['kind'] == 'youtube#video':
                    self.videos.append('%s [%s]' % (result['snippet']['title'], result['id']['videoId']))
                    
            if channels:
                if result['id']['kind'] == 'youtube#channel':
                    self.channels.append('%s [%s]' % (result['snippet']['title'], result['id']['channelId']))
                    
            if playlists:
                if result['id']['kind'] == 'youtube#playlist':
                    self.playlists.append('%s [%s]' % (result['snippet']['title'], result['id']['playlistId']))

        if videos:
            print('Videos:\n', '\n'.join(self.videos), '\n')
        if channels:
            print('Channels:\n', '\n'.join(self.channels), '\n')
        if playlists:
            print('Playlists:\n', '\n'.join(self.playlists), '\n')

class Menu:
    def __init__(self):
        self.yt = Youtube()
        self.stay = True
        self.maxResults = '20'
        self.show_videos = True
        self.show_channels = False
        self.show_playlists = False

        self.main_menu()

    def parse_bool(self,res):
        if(res.lower() in ['true', '1', 't', 'y', 'yes']):
            return True
        else:
            return False

    def main_menu(self):
        while self.stay:
            system('clear')
            print("-* MAIN *-\n0: query\n1: exit\n")
            c = input("> ")

            if c == "0":
                self.query_menu()
                
            elif c == "1":
                self.stay = False
                
            else:
                print("yquery: command not found")

    def query_menu(self):
        while self.stay:
            system('clear')
            print("-* QUERY *-\n0: search [STRING]\n1: max nr of search results [" + self.maxResults + "]\n2: search videos [" + str(self.show_videos) + "]\n3: search channels [" + str(self.show_channels) +"]\n4: search playlists [" + str(self.show_playlists) + "]\n5: back\n6: exit\n")
            c = input("> ")

            if c == "0":
                search_string = input("Search? > ")
                self.yt.search(search_string, self.maxResults, self.show_videos, self.show_channels, self.show_playlists)
                input("Press Enter to continue...")
                
            elif c == "1":
                self.maxResults = input("maxResults? > ")

            elif c == "2":
                self.show_videos = self.parse_bool(input("search videos? > "))

            elif c == "3":
                self.show_channels = self.parse_bool(input("search channels? > "))

            elif c == "4":
                self.show_playlists = self.parse_bool(input("search playlists? > "))
                
            elif c == "5":
                self.main_menu()
                
            elif c == "6":
                self.stay = False
                
            else:
                print("yquery: command not found")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interactive', help='Start yquery with a interactive menu.', action="store_true")
    parser.add_argument('-q', '--query', help='Query for Videos, Channels or Playlists.')
    parser.add_argument('-n', '--number', help='Query for Videos, Channels or Playlists.')
    parser.add_argument('-v', '--videos', help='Query for Videos, Channels or Playlists.')
    parser.add_argument('-c', '--channels', help='Query for Videos, Channels or Playlists.')
    parser.add_argument('-p', '--playlists', help='Query for Videos, Channels or Playlists.')

    args = parser.parse_args()

    # Menu mode, see Menu class (ugly menu handling, oof)
    if(args.interactive):
        menu = Menu()
    else:
        yt = Youtube()
        try:
            yt.search(args.query)
        except(HttpError, e):
            print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
