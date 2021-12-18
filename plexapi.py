from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from pprint import pprint
import math
baseurl = 'http://192.168.0.100:32400'
token = 'zDRKmQs5PYzVvsqbjQjh'
plex = PlexServer(baseurl, token)
shows = plex.library.section('TV Shows')
episode = shows.get("Star Trek: Discovery").episode(None, 1, 1)
pprint(episode)
for marker in episode.markers:
    if(marker.type == "intro"):
        pprint(marker)
        pprint(marker.type)
        seconds = marker.start/1000
        second = seconds % 60
        minute = math.floor(seconds/60)
        print( str(minute) + ":" + str(second))
        pprint(marker.start)
        pprint(marker.end)
