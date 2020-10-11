#!/usr/local/bin/python3.7

import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# see https://console.cloud.google.com/apis/credentials
APIKEY = open("./api.key", "r").read()

class Youtube:
    def __init__(self):
        self.videos = []
        self.channels = []
        self.playlists = []
    
    def search(self, args):
        api = build('youtube', 'v3', developerKey=APIKEY)

        # starting query
        query_result = api.search().list(q=args.query, part='id,snippet', maxResults=20).execute()

        for result in query_result.get('items', []):
            if result['id']['kind'] == 'youtube#video':
                self.videos.append('%s (%s)' % (result['snippet']['title'], result['id']['videoId']))
            elif result['id']['kind'] == 'youtube#channel':
                self.channels.append('%s (%s)' % (result['snippet']['title'], result['id']['channelId']))
            elif result['id']['kind'] == 'youtube#playlist':
                self.playlists.append('%s (%s)' % (result['snippet']['title'], result['id']['playlistId']))

        print('Videos:\n', '\n'.join(self.videos), '\n')
        print('Channels:\n', '\n'.join(self.channels), '\n')
        print('Playlists:\n', '\n'.join(self.playlists), '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query', help='Query for Videos, Channels or Playlists')

    args = parser.parse_args()

    yt = Youtube()

    try:
        yt.search(args)
    except(HttpError, e):
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
