from datetime import datetime
from random import randint
from time import sleep

import time
import auth

from BotMemory import BotParams as btprms
from BotMemory import FileHandlerBot as fh
from BotMemory import UserMemoryManager
from BotServices import L0_Service
from BotServices import L1_2_Service
from BotServices import Love_Service
from BotServices import theGame_Service
from BotServices import PostBooster_Service
from POM import insta_LogInPage_POM as login
from POM import webPage as wp

timeStampFormat = "%m/%d/%Y, %H:%M:%S"


class InstaBot:
    datetimeStringFormat_day = '%Y_%m_%d'

    def __init__(self, headless=False):
        # AUX Objects
        self.fileHandler = fh.FileHandlerBot()
        self.memoryManager = UserMemoryManager.UserMemoryManager()
        self.botParams = btprms.BotParams()

        self.headless = headless

        # Bot Params
        self.paramsTimeStamp = None
        self.timeUpperBound = 48
        self.timeLowerBound = 34
        self.timeLimitSinceLastLoved = 30
        self.followMana = 50
        self.followManaMax = 100

        ## Game vars
        self.daysBeforeIunFollow = 20 - 1
        self.daysBeforeIunLove = self.daysBeforeIunFollow + 5

        # List vars
        self.targetHashtags_frame = self.fileHandler.CSV_getFrameFromCSVfile('hashtagsToLookForCSV')
        self.targetHashtags_List = self.targetHashtags_frame[self.targetHashtags_frame.columns[0]].tolist()
        self.words_frame = self.fileHandler.CSV_getFrameFromCSVfile('wordsToLookForInBioCSV')
        self.words = self.words_frame[self.words_frame.columns[0]].tolist()

        self.loadParams()
        self.replenishFollowMana()

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

    def replenishFollowMana(self):
        timeStamp = datetime.now().strftime(timeStampFormat)
        if self.timeDiffForManaReplenishment() > 24:
            self.followMana = self.followManaMax
            self.botParams.updateMana(self.followManaMax, timeStamp)  # the only time a new timestamp is recorded on drive
        else:
            self.botParams.updateMana(self.followMana)

    def decrementFolowMana(self, delta):
        timeStamp = datetime.now().strftime(timeStampFormat)
        self.followMana = self.followMana - delta
        self.botParams.updateMana(self.followMana)

    def loadParams(self):
        params = self.botParams.getBotParams()
        if params:
            self.paramsTimeStamp = params['TimeStamp']
            self.timeUpperBound = params['sleepMaxSecs']
            self.timeLowerBound = params['sleepMinSecs']
            self.timeLimitSinceLastLoved = params['timeLimitSinceLastLoved']
            self.followMana = params['manaLeft']
            self.followManaMax = params['manaMax']

            self.daysBeforeIunFollow = params['daysBeforeIunFollow']
            self.daysBeforeIunLove = self.daysBeforeIunFollow + params['daysBeforeIunLove']

    def botSleep(self, factor=1):
        time = randint(self.timeLowerBound, self.timeUpperBound)
        time = int(factor * time)
        # print(f"Sleeping {time}")
        sleep(time)

    def delayOps(self, minimum=2, maximum=20):
        sleepTime = randint((minimum * 60), (maximum * 60))
        print(f'Sleeping for {int(sleepTime / 60)} minutes')
        sleep(sleepTime)

    def internetConnectionLost(self):
        self.mainPage.driver.refresh()
        try:
            myPage = self.mainPage.topRibbon_myAccount.navigateToOwnProfile()
            sleep(1)
            mylatestPost = myPage.navigateTo_X_latestPost(0)

            if mylatestPost:
                mylatestPost.close_post()
                return True
            else:
                return False

        except Exception as e:
            print(e)
            return False

    def timeDiffForManaReplenishment(self):

        try:
            lastCheck_Time = datetime.strptime(self.paramsTimeStamp, timeStampFormat)
            now_DateTime = datetime.now()

            # Convert to Unix timestamp
            d1_ts = time.mktime(lastCheck_Time.timetuple())
            d2_ts = time.mktime(now_DateTime.timetuple())
            deltaT = int(d2_ts - d1_ts) / 60 / 60  # hours

            return deltaT
        except Exception as e:
            print(e)
            return 12

    ### SERVICES ###
    def love_Service(self, fileName, numberOfLikes, percentageOfUsers):
        return Love_Service.love(self, fileName, numberOfLikes, percentageOfUsers)

    def l0_Service(self, typeOfList, numberOfProfilesToProcess, numberOfTags, numberOfPostsPerTag):
        if not 'tag' in typeOfList:
            return L0_Service.list_getList_0_FromSponsors(self, numberOfProfilesToProcess)
        else:
            return L0_Service.list_getList_0_FromTagedPosts(self, numberOfTags, numberOfPostsPerTag)

    def l1_2_Service(self, numberOfusersToCheck):
        return L1_2_Service.userScraping(self, numberOfusersToCheck)

    def theGame_Service(self):
        return theGame_Service.playTheGame(self)

    def postBoostService(self, hashTagPage=10, numberOfPostsPerTag=5):
        return PostBooster_Service.boostLatestPost(self, hashTagPage, numberOfPostsPerTag)
