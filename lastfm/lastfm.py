#!/usr/bin/env python3

__module_name__ = "last.fm" 
__module_version__ = "1.2.1"
__module_description__ = "/np for last.fm" 

from xchat import hook_command, command, EAT_ALL
#from stdout import hook_command, command, EAT_ALL
import sys
import time
import urllib.request
from urllib.error import HTTPError
from urllib.parse import quote
import socket
import json

# Edit this line to your own username.
username = 'KillaB-zilla'

url_base = 'http://ws.audioscrobbler.com/2.0/'
api_key = 'c9059e92f56e9c41df9e3cb5e2b2278a'

# we must limit the frequency of api calls to one per second
delay = 1000
last_req = 0

def fetch(method, args):
	global last_req
	url = "%s?method=%s&%s&api_key=%s&format=json" % (url_base, method, '&'.join(["%s=%s" % (k_v[0], quote(str(k_v[1]).encode('utf-8'))) for k_v in iter(args.items())]), api_key)

	while time.time() < last_req + 1:
		time.sleep(0.1)

	for retries in range(2, -1, -1):
		try:
			opener = urllib.request.build_opener()
			opener.addheaders = [('User-agent', 'Mozilla/5.0')]
			response = opener.open(url)
			url_data = response.read()
			url_data = url_data.decode('utf-8')

			break
		except HTTPError as e:
			url_data = e.read()
		except socket.error as e:
			errno, errstr = sys.exc_info()[:2]
			if not retries:
				return False
		except Exception as e:	 # <urlopen error timed out>
			if not retries:
				return False

	last_req = time.time()

	return json.JSONDecoder().decode(url_data)

def getTags(artist, track):
# return up to three tags for the track
	try:
		track_tags = fetch('track.getTopTags', {'artist': artist, 'track': track})['toptags']['tag']
		if type(track_tags) == dict:
			track_tags = [track_tags]
	except Exception:
		track_tags = []

	try:
		artist_tags = fetch('artist.getTopTags', {'artist': artist})['toptags']['tag']
		if type(artist_tags) == dict:
			artist_tags = [artist_tags]
	except Exception:
		artist_tags = []

	tags = track_tags + artist_tags
	tags = sorted(tags, key=lambda tag: -int(tag['count']))[:6]
	
	# remove dupes
	seen = set()
	seen_add = seen.add
	tags = [tag for tag in tags if tag['name'] not in seen and not seen_add(tag['name'])]

	tags = ', '.join(map(lambda tag: tag['name'], tags[:3]))
	if tags != '':
		tags = '({})'.format(tags)

	return tags

def np(user):
	# get currently playing song
	recent = fetch('user.getRecentTracks', {'user' : username, 'limit': '1', 'extended': '1'})['recenttracks']['track']

	if type(recent) == list:
		recent = recent[0]

	try:
		artist = recent['artist']['name']
		track  = recent['name']
		loved  = '♥' if recent['loved'] == '1' else ''
	except Exception as e:
		try:
			return recent['error']
		except:
			return e

	# get song tags
	tags = getTags(artist, track)
	
	# return np text
	return 'np: {} - {} {} {}'.format(artist, track, tags, loved)


def np_hook(word,word_eol,userdata):
	command('me {}'.format(np(username)))
	return EAT_ALL

hook_command('np', np_hook, help='/np displays your now playing from last.fm') 
