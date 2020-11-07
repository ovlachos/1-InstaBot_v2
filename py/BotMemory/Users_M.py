class User_M:
    def __init__(self, handle, jsonInput_fromDrive):
        self.handle = handle
        self.userID = ''
        self.timeLovedlast = ''
        self.bio = ''
        self.altName = ''
        self.dateFollowed_byMe = ''
        self.dateUnFollowed_byMe = ''
        self.dateUnLoved_byMe = ''
        self.userIgotYouFrom = ''
        self.statsDict = {}
        self.listOfPastNames = []
        self.listOf_followers = []
        self.listOf_following = []
        self.listOf_HashTagsfollowing = []
        self.listOf_HashTagsUsing = []
        self.listOf_statsHistory = []

        self.initializeFromJSON(jsonInput_fromDrive)

    def initializeFromJSON(self, jsonInput_fromDrive):
        pass

    def updateTimelastLoved(self):
        pass

    def updateStatsFrom_POM(self, userPage):
        # do something and then:
        self.updateStatsHistory()

    def serializeTo_JSON(self):
        pass

    def updateStatsHistory(self):
        self.listOf_statsHistory.append(self.statsDict)
