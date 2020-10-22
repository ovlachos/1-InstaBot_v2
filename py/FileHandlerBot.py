import os
import BotMemoryFiles as BF


def initializeFolder(targetPath):
    from os import path

    try:
        if not path.exists(targetPath):
            os.makedirs(targetPath)
    except Exception as e:
        print(e)


class MemoryFile():
    def __init__(self, fileName, filepath, extension, columns):
        self.fileName = fileName
        self.filepath = filepath
        self.extension = extension
        self.columns = columns

    def initialize(self, creator):
        creator.getDetails(self.filepath, self.columns)


class FileHandlerBot:
    # Main Directories
    py_files = os.path.dirname(__file__)
    projectFolder = os.path.join(py_files, '../')

    def __init__(self):
        from pathlib import Path

        self.paths = self.getConfig_JSON_paths('paths')
        self.files = self.getConfig_JSON_paths('files')
        self.fileFactoryCreator = BF.fileCreator()

        for val in self.paths.values():
            initializeFolder(Path(self.projectFolder + val))

        for file in self.files:  # TODO: turn this into a factory object for you have many file cases
            if not Path(file['filepath']).is_file():
                mFile = MemoryFile(file['filename'], file['filepath'], file['extension'], file['columns'])
                self.fileFactoryCreator.create(mFile, file['extension'])

    def getConfig_JSON_paths(self, kindOfJSON='paths'):
        import json

        os.chdir(self.projectFolder)
        if kindOfJSON == 'paths':
            fileName = "paths_config.json"
        else:
            fileName = "files_config.json"

        with open(fileName) as json_conf:
            CONF = json.load(json_conf)

        return CONF

    # def addUserto_theDailyLove(self, user):
    #     import pandas as pd
    #     from datetime import datetime
    #     from pathlib import Path
    #
    #     initializeFile(Path(self.files['dailyLoveCSV']))
    #     dailyLove_frame_old = pd.read_csv(self.files['dailyLoveCSV'])
    #
    #     new_row = pd.Series([user, 1, datetime.now(), 0])
    #     row_df = pd.DataFrame([new_row])
    #     row_df.columns = ['theLoveDaily', 'Post Count', 't_sinceLast', 'PostsPerDay']
    #
    #     lovedOnes_frame_new = pd.concat([row_df, dailyLove_frame_old], ignore_index=True)
    #     lovedOnes_frame_new.to_csv(self.paths.theDailyLoveCSV, index=False, encoding='utf-8')
    #     # log.error('User: {} added to the LoveDaily'.format(user))
