#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  coletorPuro.py
#  
#  Copyright 2022 tales <tales@DESKTOP-SD20F2N>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import tweepy
import Credenciais
import csv
import Keywords
def escreverDados(arquivo, tweet, texto):
	if tweet["geo"] !=None:
		cx,cy = tweet["geo"]["coordinates"]
	elif tweet["place"]!=None:
		coords = tweet["place"]["bounding_box"]["coordinates"][0]
		cx = 0
		cy= 0
		d = len(coords)
		for i in coords:
			cx+= i[0]
			cy+= i[1]
		cx = cx/d
		cy= cy/d
	else:
		cx,cy = None,None
	if texto[-1] != "…" :
		arquivo.writerow([texto,tweet["id"],tweet["created_at"],cx,cy] )
class tweetStreamer(tweepy.Stream):
	saida = csv.writer(open('outputs/Saida.csv','a+', encoding= 'utf-8'))
	def on_status(self, status):
		if not hasattr(status, "retweeted_status"):
			tweet = status._json
			if hasattr(status, "extended_tweet"):
				tweet_extendido = tweet["extended_tweet"]
				escreverDados(self.saida,tweet, tweet_extendido["full_text"])
			else:
				escreverDados(self.saida,tweet,tweet["text"])
def autenticar():
	auth = tweepy.OAuthHandler(Credenciais.CONSUMER_KEY,Credenciais.CONSUMER_SECRET)
	auth.set_access_token(Credenciais.ACCESS_TOKEN, Credenciais.ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)	
	return api
def main(args):
	listener = tweetStreamer(Credenciais.CONSUMER_KEY,Credenciais.CONSUMER_SECRET,Credenciais.ACCESS_TOKEN, Credenciais.ACCESS_TOKEN_SECRET)
	
	listener.filter(track= Keywords.KEYWORDS, languages = ["en"])
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
