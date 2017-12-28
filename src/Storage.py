import os
import logging

class Storage:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    def __init__(self, dir):
        self.pathDir =  dir
        self.file_v =   os.path.join(self.pathDir, "v.txt")
        self.file_v_done = os.path.join(self.pathDir, "v_done.txt")

    def get_url_to_download(self):
        with open(self.file_v, "r") as f:
            item = f.readline().rstrip()
            if item: return item

            #region loop to get text
            for i in range(0,10):
                item = f.readline().rstrip()
                if item : break
            return item
            #endregion


    def remove_url_from_download_list(self, item_to_remove, file):
        with open(file, "r") as f:
            vs = [v for v in f.readlines() if v ]
            vs_to_save = [v for v in vs if v.upper().rstrip() != item_to_remove.upper().rstrip()]
            with open(file, "w") as fw:
                fw.seek(0)
                fw.truncate(0)
                fw.writelines(vs_to_save)

    def add_url_to_file(self, url, file):
        with open(file, 'w+') as f:
            f.seek(0, os.SEEK_END)
            f.write(url + "\n")
        return True

    def move_url_from_v_to_done(self, url):
        self.logger.info("moving url "+ url +"to done file")
        if self.add_url_to_file(url, self.file_v_done):
            self.remove_url_from_download_list(url, self.file_v)
        else:
            self.logger.error("Can not add url to done file for location "+self.file_v_done )

if __name__ == '__main__':
    pathDir = "../Data"
    _ = Storage(pathDir)
    for i in range(0,10):
        v = _.get_url_to_download()
        if not v:
            _.remove_url_from_download_list(v, _.file_v)
        _.move_url_from_v_to_done(v)

