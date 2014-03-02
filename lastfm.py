# -*- coding: utf-8 -*-

__module_name__ = "last.fm" 
__module_version__ = "1.1.0"
__module_description__ = "/np for last.fm" 
import xchat
import urllib2
import sys
import time

username = 'KillaB-zilla'
api = 'c9059e92f56e9c41df9e3cb5e2b2278a'
	
def RateLimited(maxPerSecond):
    """Limit speed of network communications."""
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rateLimitedFunction(*args,**kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.clock()
            return ret
        return rateLimitedFunction
    return decorate

@RateLimited(1)
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
# return up to three tags for the song
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
		artist_numtags = min(3, len(artist_json.split('</name>')) - 1)
		for i in range(song_numtags):
			tags = readTag(tags, song_json, i)
		for i in range(artist_numtags - song_numtags):
			tags = readTag(tags, artist_json, i)
	
	if tags != "":
		tags = " (" + tags + ")"
	return tags

def resolveUser(nick):
# return lastfm username for irc nick
# I might use a dictionary for this if I ever add more people
	if (nick == "oranj"):
		return "oranj456"
	else:
	# couldn't find user, just return nick
		return nick

def checkChannel(channel):
# returns true if script can be triggered in channel
	channels = {'#love', '#lucky'}
	for allowed in channels:
		if channel == allowed:
			return True
	return False


def lastfmNp(user):
	# get currently playing song
	np = lastfmApi('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={}&api_key={}'.format(user, api))

	if len(np.split('</name>')) == 1:
		return "no tracks found"
	artist = np.split('</artist>')[0].split('>')[-1]
	song = np.split('</name>')[0].split('>')[-1]
	
	# get song tags
	tags = getTags(artist, song)
	
	# return np text
	return 'np: {} - {}{}'.format(artist, song, tags)


def sendNp(word,word_eol,userdata):
	xchat.command('me {}'.format(lastfmNp(username)))
	return xchat.EAT_ALL

def triggerNp(word, word_eol, userdata):
	nick = word[0].split('!')[0]
	nick = nick.lstrip(':')
	channel = word[2]
	if word[3] == ":!np" and checkChannel(channel) == True:
		xchat.command('timer .1 msg {} [{}] {}'.format(channel, nick, lastfmNp(resolveUser(nick))))
	return xchat.EAT_NONE

xchat.hook_command("np", sendNp, help="/np displays your now playing from last.fm") 
xchat.hook_server("privmsg", triggerNp) 