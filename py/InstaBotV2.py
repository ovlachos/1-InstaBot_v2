import auth
import os
from time import sleep
from POM import webPage as wp
from POM import insta_LogInPage_POM as login
import FileHandlerBot as fh


class InstaBot:
    def __init__(self):
        self.fileHandler = fh.FileHandlerBot()
