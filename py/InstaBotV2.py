import sched
import sys
import time
from datetime import datetime
from random import randint, random, choice
from time import sleep

import auth
from BotMemory import BotParams as btprms
from BotMemory import FileHandlerBot as fh
from BotMemory import UserMemoryManager
from BotServices import L0_Service
from BotServices import L1_2_Service
from BotServices import Love_Service
from BotServices import PostBooster_Service
from BotServices import theGame_Service
from BotServices import HomePageServices
from POM import insta_LogInPage_POM as login
from POM import webPage as wp

timeStampFormat = "%m/%d/%Y, %H:%M:%S"


class InstaBot:
    datetimeStringFormat_day = '%Y_%m_%d'

    def __init__(self, headless=False):
        # AUX Objects
        print(sys.version)
        self.fileHandler = fh.FileHandlerBot()
        self.memoryManager = UserMemoryManager.UserMemoryManager()
        self.botParams = btprms.BotParams()

        self.headless = headless

        # Bot Params Default values (that get replaced later on, maybe)
        self.paramsTimeStamp = None
        self.timeUpperBound = 48
        self.timeLowerBound = 34
        self.timeLimitSinceLastLoved = 30
        self.followMana = 50
        self.followManaMax = 100

        ## Game vars Default values (that get replaced later on, maybe)
        self.daysBeforeIunFollow = 20 - 1
        self.daysBeforeIunLove = 5

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
        self.homePage = self.mainPage.topRibbon_myAccount.goHomeWhereYouAreSafe_u()

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
            self.daysBeforeIunLove = params['daysBeforeIunLove']

    def botSleep(self, factor=1, verbose=False):
        time = randint(self.timeLowerBound, self.timeUpperBound)
        time = int(factor * time)
        if verbose: print(f"Sleeping {time}")
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

    def l0_Service(self, numberOfProfilesToProcess=1, numberOfTags=1, numberOfPostsPerTag=1, typeOfList='tag', randomArgs=True):
        if randomArgs:
            numberOfProfilesToProcess = randint(1, 5)
            numberOfTags = randint(1, 3)
            numberOfPostsPerTag = randint(1, 5)

        if 'tag' not in typeOfList:
            return L0_Service.list_getList_0_FromSponsors(self, numberOfProfilesToProcess)
        else:
            return L0_Service.list_getList_0_FromTagedPosts(self, numberOfTags, numberOfPostsPerTag)

    def l1_2_Service(self, numberOfusersToCheck=1, randomArgs=True):
        if randomArgs:
            numberOfusersToCheck = randint(1, 5)

        return L1_2_Service.userScraping(self, numberOfusersToCheck)

    def theGame_Service(self, numberOfusersToCheck=1, randomArgs=True):
        if randomArgs:
            factor = 1.2
            numberOfusersToCheck = int(randint(1, 5) * factor)

        return theGame_Service.playTheGame(self, numberOfusersToCheck)

    def postBoostService(self, hashTagPage=10, numberOfPostsPerTag=5, randomArgs=True):
        if randomArgs:
            hashTagPage = randint(1, 5)
            numberOfPostsPerTag = randint(1, 5)

        return PostBooster_Service.boostLatestPost(self, hashTagPage, numberOfPostsPerTag)

    def homePage_PostsService(self, numberOfPosts=1, randomArgs=True):
        if randomArgs:
            numberOfPosts = randint(1, 8)

        return HomePageServices.homePagePostScrolling(self, numberOfPosts)

    def homePage_StoriesService(self, numberOfStories=1, randomArgs=True):
        if randomArgs:
            numberOfStories = randint(1, 4)

        return HomePageServices.homePageStoryWatching(self, numberOfStories)

    def checkYourLikes(self):
        self.mainPage.topRibbon_myAccount.checkYourLikes()
        sleep(5)
        self.mainPage.topRibbon_myAccount.checkYourLikes()
        sleep(5)
        self.mainPage.topRibbon_myAccount.checkYourLikes()

        # self.homePage_PostsService()

    ### RANDOM RUN ###
    def run(self):

        services = [
            self.l0_Service,
            self.l1_2_Service,
            self.theGame_Service
        ]

        fillers = [
            self.homePage_PostsService,
            self.homePage_StoriesService,
            self.checkYourLikes
        ]

        # Produce a fairly non repeatable list of actions
        actionList, actionList_names = self.produceActionList(fillers, services, actionsNumber=4)
        while self.seq_len_moreThan_1(actionList_names):
            actionList, actionList_names = self.produceActionList(fillers, services, actionsNumber=4)

        # Schedule actions
        s = sched.scheduler(time.time, time.sleep)
        for action in actionList:
            s.enter(10, 1, action)

        # Announce Schedule
        print(f"This time's schedule is:")
        for item in s.queue:
            out = str(item[2]).split("InstaBot.")[1].split(' of <')[0]
            print(out)

        # Execute Schedule
        s.run()

        print(f"This run is complete!")

    def seq_len_moreThan_1(self, seq):
        guess = False
        for i in range(0, len(seq)):
            if i > 0:
                seq = seq[1:]

            if len(seq) >= 4:
                if seq[0:2] == seq[2:4]:
                    guess = True

        return guess

    def produceActionList(self, fillers, services, actionsNumber=4):
        actionList = []
        actionList_names = []
        for i in range(0, actionsNumber):
            actionList.append(choice(services))
            actionList.append(choice(fillers))

        for action in actionList:
            actionList_names.append(str(action).split("InstaBot.")[1].split(' of <')[0])

        return actionList, actionList_names
