class User_M:
    def __init__(self, handle, jsonInput_fromDrive):
        self.handle = handle
        # self.userID = ''
        self.bio = ''
        self.altName = ''
        self.statsDict = []
        self.listOfPastNames = []
        self.listOfPastNames.append(handle)

        self.listOf_followers = []
        self.listOf_following = []
        self.listOf_HashTagsfollowing = []
        self.listOf_HashTagsUsing = []

        self.dateTimeVisitedLast = ''
        self.dateFollowed_byMe = ''
        self.dateUnFollowed_byMe = ''
        self.userIgotYouFrom_youWereFollowing = ''

        self.markL0 = False
        self.markL1 = False
        self.markL2 = False

        self.dateTimeLovedlast = ''
        self.dateUnLoved_byMe = ''
        self.dailyLove = False
        self.extraLove = False

    def initializeFromJSONdata(self, jsonInput_fromDrive):
        import json
        pass

    def serializeTo_JSON(self):
        import json
        return json.dumps(self.__dict__)

    def updateInfoFromLivePage_Landing(self, userPagePOM):
        from datetime import datetime
        self.updateHandle(userPagePOM.user)
        self.updateStats(userPagePOM.stats)
        self.bio = userPagePOM.bio
        self.altName = userPagePOM.altName
        self.dateTimeVisitedLast = datetime.now()

    def updateTimelastLoved(self):
        from datetime import datetime
        self.dateTimeLovedlast = datetime.now()

    def updateHandle(self, handleNew):
        if not handleNew in self.listOfPastNames[0]:
            self.listOfPastNames.insert(0, self.handle)

        self.handle = handleNew

    def updateStats(self, statsDict):
        self.statsDict.insert(0, dict)

    def getLatestStats(self):
        if self.statsDict:
            return self.statsDict[0]

    def updateFollowersList(self, listF):
        self.listOf_followers.insert(0, listF)

    def getLatestFollowersList(self):
        if self.listOf_followers:
            return self.listOf_followers[0]

    def updateFollowingList(self, listF):
        self.listOf_following.insert(0, listF)

    def getLatestFollowersList(self):
        if self.listOf_following:
            return self.listOf_following[0]

    def addToL0(self, sponsorUser):
        self.markL0 = True
        self.userIgotYouFrom_youWereFollowing = sponsorUser

    def addToL1(self):
        self.markL1 = True

    def addToL2(self):
        self.markL2 = True
