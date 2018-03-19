# -*- coding: utf-8 -*-
"""
    File Name: BattlestationsBot.py
    Author: Ari Madian
    Created: March 9, 2018 11:13 PM
    Python Version: 3.6
    Repo: github.com/akmadian/Machine-Learning
    Twitter: twitter.com/BattlestatBot
"""

# TODO: Add support for OP to invoke bot with command like !battlestationsbot
# TODO: Add context provider to give post credit to OP
# TODO: Add method of keeping track of which submissions have already been posted

import config_secret
import tweepy
import praw
from imguralbum import ImgurAlbumDownloader
from os import path, listdir
from sys import argv
from time import sleep


class BotInstance:
    def __init__(self):
        self.redditinstance = self.reddit_authenticate()
        self.twitterinstance = self.twitter_authenticate()

    @staticmethod
    def reddit_authenticate():
        """Returns a Reddit API object"""
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
        """Returns a twitter API object"""
        print('Authenticating Twitter...')
        auth = tweepy.OAuthHandler(config_secret.c_key,
                                   config_secret.c_secret)
        auth.set_access_token(config_secret.a_token,
                              config_secret.a_secret)
        api = tweepy.API(auth)
        print('Successfully Authenticated Twitter...')
        return api




    def parse_new_submissions(self):
        """Parses new submissions from r/battlestations"""

        subreddit = self.redditinstance.subreddit('battlestations')
        print('Parsing Submissions')
        for submission in subreddit.hot(limit=10):
            print("parsing")
            print(submission.url.split('/'))
            '''
            if submission.shortlink in open('already_parsed.txt', 'r').read():
                continue
                '''
            '''
            with open('already_parsed.txt', 'w') as f:
                f.write(str(submission.shortlink))
                '''
            if submission.url.split('/')[2] == 'imgur.com':
                print(0)
                self.tweet_image(submission.url, submission.url.split('/')[3], submission.title)
                self.tweet_context(submission.author, submission.shortlink)
            if submission.url.split('/')[3] == 'a':
                print(1)
                self.tweet_image(submission.url, submission.url.split('/')[4], submission.title)
                self.tweet_context(submission.author, submission.shortlink)
            elif submission.url.split('/')[3] == 'gallery':
                print(2)
                self.tweet_image(submission.url, submission.url.split('/')[4], submission.title)
                self.tweet_context(submission.author, submission.shortlink)
                '''
            print('Parsing Comments')
            for comment in submission.comments:
                if True: # comment.author.name == submission.author.name
                    if True: # comment.body == '!battlestationsbot'
                        with open('already_parsed.txt', 'w') as f:
                            f.write(str(submission.shortlink))
                        if submission.url.split('/')[3] == 'a':
                            self.tweet_image(submission.url, submission.url.split('/')[4], submission.title)
                            self.tweet_context(submission.author, submission.shortlink)
                        elif submission.url.split('/')[3] == 'gallery':
                            self.tweet_image(submission.url, submission.url.split('/')[4], submission.title)
                            self.tweet_context(submission.author, submission.shortlink)
                    break
            '''
    @staticmethod
    def do_image_ops(album_id, album_url):
        """Download images and return the path to the first image in the downloaded album

        :param album_id: id for the downloaded album, same as the album id on imgur
        :param album_url: URL for the album to be downloaded"""
        # Downlaoding and saving the album/ image
        downloader = ImgurAlbumDownloader(album_url)
        downloader.save_images(path.os.path.dirname(path.realpath(argv[0])) + '/Downloaded Albums/' + album_id)

        # Getting the path of the first image in the downloaded album
        base_path = path.os.path.dirname(path.realpath(argv[0])) + '/Downloaded Albums/' + album_id + '/'
        file_list = listdir(base_path)
        image_name = file_list[0]
        full_path = base_path + image_name
        print(full_path)
        return full_path

    def tweet_image(self, album_url, album_id, title):
        """Tweets the image of the battlestation

        :param album_url: see album_url documentation in do_image_ops - this is a pass through
        :param album_id: see album_id documentation in do_image_ops - this is a pass through
        :param title: The title of the reddit submission"""
        print('Posting to twitter')
        api = self.twitterinstance
        api.update_with_media(self.do_image_ops(album_id, album_url), status=title)
        sleep(10)

    def tweet_context(self, OP, submission_link):
        """Tweets who the OP was and provides a link to their post.

        :param OP: The username of the poster of the reddit submission
        :param submission_link: The shortlink to the reddit submission"""
        print('Posting Context')
        latest_tweet_id = self.twitterinstance.user_timeline(972372380315090944)[-1].id
        self.twitterinstance.update_status("Posted by /u/" + str(OP) + " on r/battlestations (" + submission_link + ")",
                                           in_reply_to_status_id = latest_tweet_id)


botinstance = BotInstance()

# The two functions below create a loop where the code pauses for 20 minutes, then restarts the parsing process
def parse_new():
    botinstance.parse_new_submissions()
    start_timer()

def start_timer():
    sleep(1200)
    parse_new()


parse_new()