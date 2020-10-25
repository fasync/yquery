#!/usr/local/bin/python3.7

# BSD 2-Clause License

# Copyright (c) 2020, Florian Büstgens
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from os import system
import argparse, sys, tty, termios
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# see https://console.cloud.google.com/apis/credentials TODO: Use oauth instead
APIKEY = open("./api.key", "r").read()

class Youtube:
    def __init__(self):
        self.api = build('youtube', 'v3', developerKey=APIKEY)
        self.ytprefix = "https://www.youtube.com/watch?v="
        self.videos = {}
        self.channels = []
        self.playlists = []
    
    def search(self, search_string, mres=20, videos=True, channels=False, playlists=False):
        # starting query
        query_result = self.api.search().list(q=search_string, part='id,snippet', maxResults=mres).execute()

        self.videos = {}
        self.channels = []
        self.playlists = []

        for result in query_result.get('items', []):
            if videos:
                if result['id']['kind'] == 'youtube#video':
                    self.videos[result['snippet']['title']] = result['id']['videoId']
                    
            if channels:
                if result['id']['kind'] == 'youtube#channel':
                    self.channels.append('%s [%s]' % (result['snippet']['title'], result['id']['channelId']))
                    
            if playlists:
                if result['id']['kind'] == 'youtube#playlist':
                    self.playlists.append('%s [%s]' % (result['snippet']['title'], result['id']['playlistId']))

    def __rawInput(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def __printPretty(self, iterator):
        if self.videos:
            print('Videos:\n', '\n'.join(list(self.videos)[:iterator]))
            print('---------------------------------------------------------------------------------------')
            print('-> ', list(self.videos)[iterator])
            print('---------------------------------------------------------------------------------------')
            print('\n'.join(list(self.videos)[(iterator + 1):]))
        if self.channels:
            print('Channels:\n', '\n'.join(self.channels), '\n')
        if self.playlists:
            print('Playlists:\n', '\n'.join(self.playlists), '\n')
        
    def choose(self):
        stay = True
        iterator = 0
        while stay:
            system('clear')
            self.__printPretty(iterator)
            keypress = self.__rawInput()
            
            if keypress == 'k':
                if iterator > 0:
                    iterator-=1
                self.__printPretty(iterator)
                
            elif keypress == 'j':
                if iterator + 1 < len(self.videos):
                    iterator+=1
                self.__printPretty(iterator)

            elif keypress == 'l':
                system('clear')
                print('Loading ' + list(self.videos)[iterator] + ' ...')
                system('mpv ' + self.ytprefix + self.videos[list(self.videos)[iterator]])

            elif keypress == 'd':
                system('clear')
                print('Downloading ' + list(self.videos)[iterator] + ' ...')
                system('youtube-dl -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4')

            elif keypress == 'a':
                system('clear')
                print('Loading audio track of ' + list(self.videos)[iterator] + ' ...')
                system('mpv --no-video ' + self.ytprefix + self.videos[list(self.videos)[iterator]])
                
            elif keypress == 'q' or keypress == 'h':
                stay = False
        

class Menu:
    def __init__(self):
        self.yt = Youtube()
        self.stay = True
        self.maxResults = '100'
        self.show_videos = True
        self.show_channels = False
        self.show_playlists = False

        self.main_menu()

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
                self.yt.choose()
                
            elif c == "1":
                self.maxResults = input("maxResults? > ")

            elif c == "2":
                self.show_videos = not self.show_videos

            elif c == "3":
                self.show_channels = not self.show_channels

            elif c == "4":
                self.show_playlists = not self.show_playlists
                
            elif c == "5":
                return
                
            elif c == "6":
                self.stay = False
                
            else:
                print("yquery: command not found")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interactive', help='Start yquery with a interactive menu.', action="store_true")
    parser.add_argument('-q', '--query', help='Query for Videos, Channels or Playlists.')
    parser.add_argument('-n', '--number', help='Maximum number of search results.')
    parser.add_argument('-v', '--videos', help='Search for videos?', action="store_true")
    parser.add_argument('-c', '--channels', help='Search for channels?', action="store_true")
    parser.add_argument('-p', '--playlists', help='Search for playlists?', action="store_true")

    args = parser.parse_args()

    # Menu mode, see Menu class (ugly menu handling, oof)
    if(args.interactive):
        menu = Menu()
    else:
        yt = Youtube()
        try:
            yt.search(args.query, args.number, args.videos, args.channels, args.playlists)
            yt.choose()
        except(HttpError, e):
            print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
