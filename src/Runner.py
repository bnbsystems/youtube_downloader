from Storage import Storage as S
from Downloader  import Downloader as D
from WatchDrive import WatchDrive as WD
import time
import logging
from sys import argv

from pydub import AudioSegment


class Runner:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    wd = WD()


    def __init__(self, dir_data, dir_download, dir_to_move, sleepInSeconds= None):
        self.s = S(dir_data)
        self.d = D(dir_download)
        self.dir_to_move = dir_to_move
        self.dir_download = dir_download
        self.sleepInSeconds = sleepInSeconds if sleepInSeconds is not None else 1
        self.logger.info("Data dir with list of videos is "+dir_data)
        self.logger.info("Downloaded mp3 are here " + dir_download)
        self.logger.info("Here will be move all mp3 " + dir_to_move + " (if dir exist)")

    def download_next(self):
        try:
            self.logger.info("checking next")
            v = self.s.get_url_to_download()
            if v:
                self.d.download(v)
                self.s.move_url_from_v_to_done(v)
            self.wd.try_to_move(self.dir_download, self.dir_to_move)
        except Exception as err:
            self.logger.error(err)


    def download_loop(self):
        while True:
            self.download_next()
            time.sleep(self.sleepInSeconds)



if __name__ == '__main__':
    #argsv[0] is py script name
    dir_to_move = argv[1] if len(argv) > 1 else "../testit/2"
    dir_download = argv[2] if len(argv) > 2 else "../testit/1"
    dir_data = argv[3] if len(argv) > 3 else "../Data"
    sleepInSeconds = argv[4] if len(argv) > 4 else None

    #'/Volumes/SANSA CLIP/AUDIOBOOKS/ds_fin'
    _ = Runner(dir_data, dir_download, dir_to_move, sleepInSeconds)
    _.download_loop()


