from __future__ import unicode_literals
import youtube_dl
import os
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MyLogger(object):
    def debug(self, msg):
        logger.info(msg)

    def warning(self, msg):
        logger.warn(msg)

    def error(self, msg):
        logger.error(msg)


def my_hook(d):
    if d['status'] == 'finished':
        logger.info('Done downloading, now converting ...')




class Downloader:
    def __init__(self, pathToDownload):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
        }],
            'outtmpl': os.path.join(pathToDownload, '%(title)s-%(id)s.%(ext)s'),
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
            'nooverwrites':True
        }

    def download(self, url):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([url])


if __name__ == '__main__':
    pathToDownload = '/Users/arekbee/PycharmProjects/PlayerMp3Manager/testit/1'
    url = 'https://www.youtube.com/user/UczelniaASBIRO/'
    url = 'https://www.youtube.com/user/PiestoDaniel/videos'
    _ = Downloader(pathToDownload)
    _.download(url)
