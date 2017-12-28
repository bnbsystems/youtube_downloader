import os
import shutil
import logging

class WatchDrive:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


    def get_disk_free_space(self, dir=None):
        dir = "/" if dir==None else dir
        s = os.statvfs(dir)
        return (s.f_bavail * s.f_frsize)

    def get_sorted_files(self, dir):
        all_files = (os.path.join(basedir, filename)
                     for basedir, dirs, files in os.walk(dir)
                     for filename in files
                     if filename.endswith("mp3"))
        return sorted(all_files, key=os.path.getsize)

    def try_to_move(self, dir_from , dir_to):
        if os.path.exists(dir_to):
            for filepath in self.get_sorted_files(dir_from):
                try:
                    filesize = os.path.getsize(filepath)
                    freespace = self.get_disk_free_space(dir_to)
                    if filesize * 2 < freespace:
                        self.logger.info("moving file "+filepath + " to dir " + dir_to)
                        filename = os.path.basename(filepath)
                        dist_filename = os.path.join(dir_to, filename)
                        if not os.path.exists(dist_filename):
                            shutil.move(filepath, dist_filename)
                        else:
                            self.logger.error("File " + filename + "already exist. Removing source file")
                            os.remove(filepath)
                    else:
                        self.logger.info("Not enough free disk space for location "+ dir_to)
                except OSError as err:
                    self.logger.error(err)

if __name__ == "__main__":
    _ = WatchDrive()
    dir_from = '/Users/arekbee/PycharmProjects/PlayerMp3Manager/testit/1'
    dir_to = '/Users/arekbee/PycharmProjects/PlayerMp3Manager/testit/2'
    print(os.path.getsize(dir_to))



    #dir = '/Volumes/SANSA CLIP/AUDIOBOOKS/ds_fin'
    while True:
        _.try_to_move(dir_from, dir_to)