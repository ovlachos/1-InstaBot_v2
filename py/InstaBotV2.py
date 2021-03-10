import auth
from random import randint
from time import sleep

from BotServices import Love_Service
from BotServices import L0_Service
from BotServices import L1_2_Service
from BotServices import theGame_Service
from BotMemory import UserMemoryManager
from BotMemory import FileHandlerBot as fh
from POM import webPage as wp
from POM import insta_LogInPage_POM as login


class InstaBot:
    datetimeStringFormat_day = '%Y_%m_%d'

    def __init__(self, headless=False):
        self.fileHandler = fh.FileHandlerBot()
        self.memoryManager = UserMemoryManager.UserMemoryManager()
        self.headless = headless
        self.timeUpperBound = 48
        self.timeLowerBound = 34
        self.timeLimitSinceLastLoved = 30
        self.followMana = 100
        self.followManaMax = 100

        # Game vars
        self.daysBeforeIunFollow = 14 - 1
        self.daysBeforeIunLove = self.daysBeforeIunFollow + 5

        # List vars
        self.targetHashtags_frame = self.fileHandler.CSV_getFrameFromCSVfile('hashtagsToLookForCSV')
        self.targetHashtags_List = self.targetHashtags_frame[self.targetHashtags_frame.columns[0]].tolist()
        self.words_frame = self.fileHandler.CSV_getFrameFromCSVfile('wordsToLookForInBioCSV')
        self.words = self.words_frame[self.words_frame.columns[0]].tolist()

    def logIn(self):
        logInPage = login.InstaLogIn(self.webPage)
        self.mainPage = logInPage.logIn(auth.username, auth.password)

    def logOut(self):
        self.mainPage.topRibbon_myAccount.logOut()

    def shutDown(self):
        self.logOut()
        sleep(1)
        self.webPage.instance.writeSessionDataToJSON()
        self.webPage.killBrowser()

    def getBrowser(self):
        self.webPage = wp.WebPage(self.headless)

    def botSleep(self, factor=1):
        sleep(randint(factor * self.timeLowerBound, factor * self.timeUpperBound))

    def delayOps(self, minimum=2, maximum=20):
        sleepTime = randint((minimum * 60), (maximum * 60))
        print(f'Sleeping for {int(sleepTime / 60)} minutes')
        sleep(sleepTime)

    def love_Service(self, fileName, numberOfLikes, percentageOfUsers):
        return Love_Service.love(self, fileName, numberOfLikes, percentageOfUsers)

    def l0_Service(self, numberOfProfilesToProcess):
        return L0_Service.list_getList_0(self, numberOfProfilesToProcess)

    def l1_2_Service(self, numberOfusersToCheck):
        return L1_2_Service.userScraping(self, numberOfusersToCheck)

    def theGame_Service(self):
        return theGame_Service.playTheGame(self)
