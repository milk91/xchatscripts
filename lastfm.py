# -*- coding: utf-8 -*-

__module_name__ = "last.fm" 
__module_version__ = "1.0.0" 
__module_description__ = "/np for last.fm" 
import xchat
import urllib2

username = 'KillaB-zilla'
api = 'b25b959554ed76058ac220b7b2e0a026'

def lastfm_get(word,word_eol,userdata):
	# get song
	x = urllib2.urlopen( 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={}&api_key={}'.format(username, api) )
	x = x.read().replace('&amp;','&')
	artist = x.split('</artist>')[0].split('>')[-1]
	song = x.split('</name>')[0].split('<name>')[1]
	
	# get song tags
	fartist = urllib2.quote(artist)
	fsong = urllib2.quote(song)
	x = urllib2.urlopen( 'http://ws.audioscrobbler.com/2.0/?method=track.gettoptags&artist={}&track={}&api_key={}'.format(fartist, fsong, api) )
	x = x.read().replace('&amp;','&')
	numtags = len(x.split('</name>'))
	if numtags > 1:
		tags = x.split('</name>')[0].split('<name>')[1]
		if numtags > 2:
			tags += ", " + x.split('</name>')[1].split('<name>')[1]
		if numtags > 3:
			tags += ", " + x.split('</name>')[2].split('<name>')[1]
		xchat.command('me np: {} - {} ({})'.format(artist, song, tags))
	else:
		x = urllib2.urlopen( 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist={}&api_key={}'.format(fartist, api) )
		x = x.read().replace('&amp;','&')
		numtags = len(x.split('</name>'))
		if numtags > 1:
			tags = x.split('</name>')[0].split('<name>')[1]
			if numtags > 2:
				tags += ", " + x.split('</name>')[1].split('<name>')[1]
			if numtags > 3:
				tags += ", " + x.split('</name>')[2].split('<name>')[1]
			xchat.command('me np: {} - {} ({})'.format(artist, song, tags))
		else:
			xchat.command('me np: {} - {}'.format(artist, song))
	return xchat.EAT_ALL

xchat.hook_command("np", lastfm_get, help="/np displays your now playing from last.fm") 