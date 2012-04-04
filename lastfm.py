# -*- coding: utf-8 -*-

__module_name__ = "last.fm" 
__module_version__ = "1.1.0"
__module_description__ = "/np for last.fm" 
import xchat
import urllib2

username = 'KillaB-zilla'
api = 'b25b959554ed76058ac220b7b2e0a026'
	
def lastfmApi(url):
# get a page of json from lastfm 'url'
	myjson = urllib2.urlopen(url)
	return myjson.read().replace('&amp;','&')

def readTag(tags, json, num):
# add 'num'th tag from 'json' to 'tags'
	if (tags == ""):
		return json.split('</name>')[num].split('<name>')[1]
	else:
		return tags + ", " + json.split('</name>')[num].split('<name>')[1]

def getTags(artist, song):
	tags = ""
	fartist = urllib2.quote(artist)
	fsong = urllib2.quote(song)
	song_json = lastfmApi('http://ws.audioscrobbler.com/2.0/?method=track.gettoptags&artist={}&track={}&api_key={}'.format(fartist, fsong, api))
	song_numtags = len(song_json.split('</name>')) - 1
	if song_numtags >= 3:
	# song has 3 or more tags, artist tags not needed
		for i in range(3):
			tags = readTag(tags, song_json, i)
	else:
		# get artist tags
		artist_json = lastfmApi('http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist={}&api_key={}'.format(fartist, api))
		artist_numtags = min(3, len(artist_json.split('</name>')) + 1)
		for i in range(song_numtags):
			tags = readTag(tags, song_json, i)
		for i in range(artist_numtags - song_numtags):
			tags = readTag(tags, artist_json, i)
			
	return tags

def lastfmNp(word,word_eol,userdata):
	# get currently playing song
	np = lastfmApi('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={}&api_key={}'.format(username, api))
	artist = np.split('</artist>')[0].split('>')[-1]
	song = np.split('</name>')[0].split('<name>')[1]
	
	# get song tags
	tags = getTags(artist, song)
	
	# print np text
	if (tags == ""):
		xchat.command('me np: {} - {}'.format(artist, song))
	else:
		xchat.command('me np: {} - {} ({})'.format(artist, song, tags))

	return xchat.EAT_ALL

xchat.hook_command("np", lastfmNp, help="/np displays your now playing from last.fm") 