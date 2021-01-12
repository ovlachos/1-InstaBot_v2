import pandas as pd
from pathlib import Path


class MemoryFileFactory:

    def __init__(self):
        self._creators = {}

    def register_fileType(self, fileType, creator):
        self._creators[fileType] = creator

    def get_fileCreator(self, format):
        creator = self._creators.get(format)
        if not creator:
            raise ValueError(format)
        return creator()


class fileCreator:
    def create(self, memoryFile, fileType):
        specific_creator = factory.get_fileCreator(fileType)
        memoryFile.initialize(specific_creator)
        specific_creator.createFile()


class TXTfiles_creator:
    def __init__(self):
        pass

    def getDetails(self, filepath, columns):
        self.filepath = filepath
        self.columns = columns

    def createFile(self):
        targetFile = Path(self.filepath)
        targetFile.touch()


class CSVlists_creator:
    def __init__(self):
        pass

    def getDetails(self, filepath, columns):
        self.filepath = filepath
        self.columns = columns

    def createFile(self):
        list = pd.DataFrame(columns=self.columns)
        list.to_csv(self.filepath, index=False, encoding='utf-8')


# New single file to replace List_0, 1 and Love daily
class JSON_memoryfile_creator:
    def __init__(self):
        pass

    def getDetails(self, filepath, columns):
        self.filepath = filepath
        self.columns = columns

    def createFile(self):
        list = pd.DataFrame(columns=self.columns)
        list.to_csv(self.filepath, index=False, encoding='utf-8')


factory = MemoryFileFactory()
factory.register_fileType('.csv', CSVlists_creator)
factory.register_fileType('.txt', TXTfiles_creator)
