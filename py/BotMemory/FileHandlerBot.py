import json
import os

import pandas as pd

from BotMemory import BotMemoryFilesFactory as BF


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
    thisFile = os.path.dirname(__file__)
    py_files = os.path.join(thisFile, '../')
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

    def listToFrame(self, inputList):
        return pd.DataFrame(data=inputList)

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

        file = self.getFileFromFilename(kindOfLove)  # e.g. 'dailyLoveCSV'
        if file:
            oldFrame = pd.read_csv(file['filepath'])

            if not user in oldFrame[file['columns'][0]].tolist():
                self.CSV_addNewRowToCSV(kindOfLove, [user])

    def removeUserfrom_the_Love(self, user, kindOfLove):
        file = self.getFileFromFilename(kindOfLove)
        if file:
            oldFrame = pd.read_csv(file['filepath'])
            try:
                rowIndexOfUser = oldFrame[oldFrame[file['columns'][0]] == user].index.values[0]
                self.CSV_removeRowFromCSV(kindOfLove, rowIndexOfUser)
            except Exception as e:
                print("{0}, {1}".format(e, user))

    def readSimpleJSONfiles(self, fileName):

        memoryfile = None
        file = self.getFileFromFilename(fileName)

        if file:
            try:
                with open(file['filepath']) as jUM:
                    memoryfile = json.load(jUM)
            except Exception as e:
                print(f'WARNING: fail in reading {fileName}. Falling back to defaults')

            return memoryfile

    def writeSimpleJSONfiles(self, fileName, fileObj):

        file = self.getFileFromFilename(fileName)['filepath']

        if file:
            with open(file, 'w') as jUM:
                json.dump(fileObj, jUM, sort_keys=True, indent=4)

    def readMemoryFile(self, JSONdecoder):  # JSONdecoder is a function that translates JSON to User_M objects

        file = self.getFileFromFilename('User_Memory')

        if file:
            try:
                with open(file['filepath']) as jUM:
                    memoryfile = json.load(jUM, object_hook=JSONdecoder)
            except:
                memoryfile = []
                print('WARNING: 0 users in memory file! No love can be given.')

            return memoryfile

    def readMemoryFiles(self, JSONdecoder):
        import glob

        directory = self.paths['User_Memory']
        all_files = glob.glob(directory + "/*.json")

        memoryfile = []
        memoryfile1 = []
        for file in all_files:
            with open(file) as jUM:
                memoryfile1.append(json.load(jUM, object_hook=JSONdecoder))

        for item in memoryfile1:
            memoryfile.append(item[0])

        return memoryfile

    def writeToUserMemory(self, userMemory, JSONencoder, file=None):
        # userMemory is a list of python dictionaries each containing a single user's info

        if not file:
            file = self.getFileFromFilename('User_Memory')['filepath']

        if file:
            with open(file, 'w') as jUM:
                json.dump(userMemory, jUM, cls=JSONencoder, sort_keys=True, indent=4)
