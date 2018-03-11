# -*- coding: utf-8 -*-
"""
    File Name: BattlestationsBot.py
    Author: Ari Madian
    Created: March 9, 2018 11:13 PM
    Python Version: 3.6
    Repo: github.com/akmadian/Machine-Learning
    Twitter: twitter.com/BattlestatBot
"""

import config_secret
import tweepy
import praw
from imguralbum import ImgurAlbumDownloader
from os import path, listdir
from sys import argv

class SubmissionInstance:
    def __init__(self):
        self.


class BotInstance:
    def __init__(self):
        self.redditinstance = self.reddit_authenticate()
        self.twitterinstance = self.twitter_authenticate()

    @staticmethod
    def reddit_authenticate():
        print('Authenticating Reddit...')
        reddit = praw.Reddit(client_id=config_secret.client_id,
                     client_secret=config_secret.client_secret,
                     password=config_secret.password,
                     user_agent=config_secret.user_agent,
                     username=config_secret.username)
        print('Successfully Authenticated Reddit...')
        return reddit

    @staticmethod
    def twitter_authenticate():
        print('Authenticating Twitter...')
        auth = tweepy.OAuthHandler(config_secret.c_key,
                                   config_secret.c_secret)
        auth.set_access_token(config_secret.a_token,
                              config_secret.a_secret)
        api = tweepy.API(auth)
        print('Successfully Authenticated Twitter...')
        return api

    def download_imgur_album(self, album_url, album_id, title):
        downloader = ImgurAlbumDownloader(album_url)
        downloader.save_images(path.os.path.dirname(path.realpath(argv[0])) + '/Downloaded Albums/' + album_id)
        self.tweet_image('None', album_id, title)

    def parse_new_submissions(self):
        subreddit = self.redditinstance.subreddit('battlestations')
        for submission in subreddit.hot(limit=10):
            print(submission.title)
            print(submission.url)
            album_type = submission.url.split('/')[3]
            if album_type == 'a':
                album_id = submission.url.split('/')[4]
                self.download_imgur_album(submission.url, album_id, submission.title)
            elif album_type == 'gallery':
                album_id = submission.url.split('/')[4]
                self.download_imgur_album(submission.url, album_id, submission.title)

    def tweet_image(self, message, album_id, title):
        api = self.twitterinstance
        api.update_with_media(self.get_image_path(album_id), status=title)

    @staticmethod
    def get_image_path(album_id):
        base_path = path.os.path.dirname(path.realpath(argv[0])) + '/Downloaded Albums/' + album_id + '/'
        file_list = listdir(base_path)
        image_name = file_list[0]
        full_path = base_path + image_name
        print(full_path)
        return full_path


botinstance = BotInstance()
botinstance.parse_new_submissions()
'''
subreddit_ = botinstance.redditinstance.subreddit('battlestations')
print(subreddit_)
for submission in subreddit_.hot(limit=10):
    print(submission.title)
    print(submission.url.split('/'))
    # botinstance.download_imgur_album(submission.url)
'''