import os
import pandas as pd

import BotMemoryFilesFactory as BF


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

        # Make sure the files and folders mentioned
        # in the JSON configs are in existence
        for val in self.paths.values():
            initializeFolder(Path(self.projectFolder + val))

        for file in self.files:
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

    def getFileFromFilename(self, filename):
        fileFound = 0
        for file in self.files:
            if filename in file['filename']:
                return file

    def CSV_getFrameFromCSVfile(self, filename):
        frame = pd.DataFrame([])
        file = self.getFileFromFilename(filename)
        if file:
            frame = pd.read_csv(file['filepath'])

        return frame

    def CSV_saveFrametoCSVfile(self, filename, frame):
        file = self.getFileFromFilename(filename)
        frame.to_csv(file['filepath'], index=False, encoding='utf-8')

    def CSV_removeRowFromCSV(self, filename, row_index):
        file = self.getFileFromFilename(filename)
        if file:
            oldframe = self.CSV_getFrameFromCSVfile(filename)
            oldframe = oldframe.drop(oldframe.index[row_index])
            oldframe.to_csv(file['filepath'], index=False, encoding='utf-8')

    def CSV_addNewRowToCSV(self, filename, row):
        file = self.getFileFromFilename(filename)
        if file:
            oldFrame = pd.read_csv(file['filepath'])

            if len(file['columns']) == len(row):
                new_row = pd.Series(row)
                row_df = pd.DataFrame([new_row])
                row_df.columns = file['columns']

                frame_new = pd.concat([row_df, oldFrame], ignore_index=True)
                frame_new.to_csv(file['filepath'], index=False, encoding='utf-8')

    def addUserto_the_Love(self, user, kindOfLove):
        from datetime import datetime

        file = self.getFileFromFilename(kindOfLove)  # e.g. 'dailyLoveCSV'
        if file:
            oldFrame = pd.read_csv(file['filepath'])

            if not user in oldFrame[file['columns'][0]].tolist():
                self.CSV_addNewRowToCSV(kindOfLove, [user, 1, datetime.now(), 0])

    # TODO: Write integrity / duplicates check method for all the CSV files that get manual input

    def removeUserfrom_the_Love(self, user, kindOfLove):
        file = self.getFileFromFilename(kindOfLove)
        if file:
            oldFrame = pd.read_csv(file['filepath'])
            try:
                rowIndexOfUser = oldFrame[oldFrame[file['columns'][0]] == user].index.values[0]
                self.CSV_removeRowFromCSV(kindOfLove, rowIndexOfUser)
            except Exception as e:
                print("{0}, {1}".format(e, user))
