#!/usr/bin/env python3

import praw
import re
import imgurpython

def main():
	"""Parses posts from /u/imgurtranscriber and posts if successful a regenerated picture as a reply to each."""

	config = open('.config', 'r')

	line = config.readline()
	while (len(line) > 0):
		if line.startswith('reddit_login'):
			reddit_login = re.search('\'(.*)\'\n', line).group(1)
		elif line.startswith('reddit_password'):
			reddit_password = re.search('\'(.*)\'\n', line).group(1)
		elif line.startswith('client_id'):
			client_id = re.search('\'(.*)\'\n', line).group(1)
		elif line.startswith('client_secret'):
			client_secret = re.search('\'(.*)\'\n', line).group(1)
		else:
			raise SyntaxError('Illegal line in config file')
		
		line = config.readline()

	r = praw.Reddit(user_agent='Imgur Cisscriber 0.2 by /u/Tularion')
	r.login(reddit_login, reddit_password)
	
	try:
		client = imgurpython.ImgurClient(client_id, client_secret)
	except ImgurClientError as e:
		print(e.error_message)
		print(e.status_code)
		exit()

	user = r.get_redditor('imgurtranscriber')
	comments = user.get_comments(sort='new', time='month')
	
	for comment in comments:
		meme_type = re.search('#\*\*\*(.*)\*\*\*\s*', comment.body).group(1)
		post_title = re.search('Title:\*\*\*  \*(.*)\*\s*', comment.body).group(1)
	
		search = re.search('Top:\*\*\*  \*(.*)\*\s*', comment.body)
		if search is not None:
			top = search.group(1)
	
		search = re.search('Bottom:\*\*\*  \*(.*)\*\s*', comment.body)
		if search is not None:
			bottom = search.group(1)
	
		url = upload_meme(generate_meme(meme_type, post_title, top, bottom), client)
	
		if url is not None:
			comment.reply("Here is what the transcribed meme looks like in case you can't read:\n\n[New Link^1](" + url + ")")

def generate_meme(meme_type, post_title, top, bottom):
	"""Returns a URL for the meme generated by the parameters. The generation may fail, then returns a URL for the failed generation.
	
	Currently uses APIMeme."""

	if top is not None:
		top = top.replace(" ", "+")
	if bottom is not None:
		bottom = bottom.replace(" ", "+")

	return r'http://apimeme.com/meme?meme=' + meme_type.replace(" ", "+") + r'&top=' + top + r'&bottom=' + bottom

def upload_meme(url, client):
	"""Uploads an image anonymously to Imgur and returns a direct link. Returns None if upload failed."""
	
	try:
		upload = client.upload_from_url(url)
	except imgurpython.helpers.error.ImgurClientError:
		return None
	else:
		return upload['link']

main()
