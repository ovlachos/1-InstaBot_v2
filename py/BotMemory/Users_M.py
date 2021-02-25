import json

timeStampFormat = "%m/%d/%Y, %H:%M:%S"


class UserEncoderDecoder(json.JSONEncoder):
    def default(self, us):
        if isinstance(us, User_M):
            userDict = {
                '__user__': 'true',

                '0_Handle': us.handle,
                'Bio': us.bio,
                'AltName': us.altName,
                'Stats': us.statsDict,
                'StatsTime': us.statsDictTimestamp,
                'Past Names': us.listOfPastNames,
                # 'LastVisited': us.dateTimeVisitedLast, #This will be calculated by dict variable and retrieved only by function

                'listOf_followers': us.listOf_followers,
                'listOf_following': us.listOf_following,
                'listOf_HashTagsfollowing': us.listOf_HashTagsfollowing,
                'listOf_HashTagsUsing': us.listOf_HashTagsUsing,

                'dateFollowed_byMe': us.dateFollowed_byMe,
                'dateUnFollowed_byMe': us.dateUnFollowed_byMe,
                'userIgotYouFrom_youWereFollowing': us._userIgotYouFrom_youWereFollowing,

                'markL0': us._markL0,
                'markL1': us._markL1,
                'markL2': us._markL2,

                'dateTimeLovedlast': us._dateTimeLovedlast,
                'dateUnLoved_byMe': us.dateUnLoved_byMe,
                'dailyLove': us._dailyLove,
                'extraLove': us._extraLove
            }
            return userDict
        else:
            return super().default(us)

    def decode_user(dct):
        if "__user__" in dct:
            user = User_M(dct['0_Handle'])
            user.populate_overwrite(dct)
            return user
        if 'followers' in dct:
            return dct


class User_M:
    def __init__(self, handle):
        # self.userID = ''
        self.handle = handle
        self.bio = ''
        self.altName = ''
        self.statsDict = []  # contains statsDicts
        self.statsDictTimestamp = []  # contains strings of datetime objects
        self.listOfPastNames = []
        # self.dateTimeVisitedLast = '' #This will be calculated by dict variable and retrieved only by function

        self.listOf_followers = []
        self.listOf_following = []
        self.listOf_HashTagsfollowing = []
        self.listOf_HashTagsUsing = []

        self.dateFollowed_byMe = ''
        self.dateUnFollowed_byMe = ''
        self._userIgotYouFrom_youWereFollowing = ''

        self._markL0 = False
        self._markL1 = False
        self._markL2 = False

        self._dateTimeLovedlast = ''
        self.dateUnLoved_byMe = ''
        self._dailyLove = False
        self._extraLove = False

    def populate_overwrite(self, dict):
        from datetime import datetime
        stats = {"posts": 0, "followers": 0, "following": 0}

        if "__user__" in dict:
            self.handle = dict.get('0_Handle', ' ')
            self.bio = dict.get('Bio', ' ')
            self.altName = dict.get('AltName', ' ')
            self.statsDict = dict.get('Stats', [stats])  # contains statsDicts
            self.statsDictTimestamp = dict.get('StatsTime', [])  # contains strings of datetime objects
            self.listOfPastNames = dict.get('Past Names', [])
            # self.dateTimeVisitedLast = dict['LastVisited'] #This will be calculated by dict variable and retrieved only by function

            self.listOf_followers = dict.get('listOf_followers', [])
            self.listOf_following = dict.get('listOf_following', [])
            self.listOf_HashTagsfollowing = dict.get('listOf_HashTagsfollowing', [])
            self.listOf_HashTagsUsing = dict.get('listOf_HashTagsUsing', [])

            self.dateFollowed_byMe = dict.get('dateFollowed_byMe', ' ')
            self.dateUnFollowed_byMe = dict.get('dateUnFollowed_byMe', ' ')
            self._userIgotYouFrom_youWereFollowing = dict.get('userIgotYouFrom_youWereFollowing', ' ')

            self._markL0 = dict.get('markL0', False)
            self._markL1 = dict.get('markL1', False)
            self._markL2 = dict.get('markL2', False)

            self._dateTimeLovedlast = dict.get('dateTimeLovedlast', ' ')
            self.dateUnLoved_byMe = dict.get('dateUnLoved_byMe', ' ')
            self._dailyLove = dict.get('dailyLove', False)
            self._extraLove = dict.get('extraLove', False)

    def serializeTo_JSON(self, format=False):
        if not format:
            return json.dumps(self, cls=UserEncoderDecoder)
        return json.dumps(self, cls=UserEncoderDecoder, sort_keys=True, indent=4)

    def updateInfoFromLivePage_Landing(self, userPagePOM):

        # TODO: need to create a routine that compares new userPage stats to old ones
        # in case the userPage belongs to a different user with similar handle (fuzzy matchup and handle changes).
        # this way the new random user will not take the place of an existing entry.
        # The questions is: how  do you handle the case of the above happening? Flash a warning? Does this need manual intervention?

        self.updateHandle(userPagePOM.userName)
        self.updateStats(userPagePOM.stats)
        self.bio = userPagePOM.bio
        self.altName = userPagePOM.altName
        # self.dateTimeVisitedLast = timestamp #This will be calculated by dict variable and retrieved only by function

    def updateTimelastLoved(self):
        from datetime import datetime
        self._dateTimeLovedlast = datetime.now().strftime(timeStampFormat)

    def updateHandle(self, handleNew):
        if self.listOfPastNames:
            if not handleNew in self.listOfPastNames[0]:
                self.listOfPastNames.insert(0, handleNew)

        self.handle = handleNew

    def updateStats(self, statsDictIn):
        from datetime import datetime
        self.statsDict.insert(0, statsDictIn)
        self.statsDictTimestamp.insert(0, datetime.now().strftime(timeStampFormat))

    def getTimeLastVisited(self):
        try:
            return self.statsDictTimestamp[0]
        except Exception as e:
            return "01/01/1989, 00:01:01"

    def getLatestStats(self):
        try:
            return self.statsDict[0]
        except Exception as e:
            stats = {
                'posts': 0,
                'followers': 0,
                'following': 0
            }
            return stats

    def getLatestPostCount(self):
        try:
            latestStats = self.getLatestStats()
            return latestStats['posts']
        except:
            return 0

    def updateFollowersList(self, listF):
        self.listOf_followers.insert(0, listF)

    def updateFollowingList(self, listF):
        self.listOf_following.insert(0, listF)

    def addToL0(self, sponsorUser):
        self._markL0 = True
        self._userIgotYouFrom_youWereFollowing = sponsorUser

    def addToL1(self):
        self._markL1 = True

    def addToL2(self):
        self._markL2 = True

    def addToLoveDaily(self):
        self._dailyLove = True

    def addToLoveExtra(self):
        self._extraLove = True

    def removeFromLoveDaily(self):
        from datetime import datetime

        timestamp = datetime.now().strftime(timeStampFormat)
        self._dailyLove = False
        self.dateUnLoved_byMe = timestamp

    def removeFromLoveExtra(self):
        from datetime import datetime

        timestamp = datetime.now().strftime(timeStampFormat)
        self._extraLove = False
        self.dateUnLoved_byMe = timestamp

    def markDateUnfollowed(self):
        from datetime import datetime

        timestamp = datetime.now().strftime(timeStampFormat)
        self.dateUnFollowed_byMe = timestamp

    def printHowLongItHasBeenSinceYouGotAnyLove(self):
        from datetime import datetime
        import time
        try:
            lastCheck_Time = datetime.strptime(self._dateTimeLovedlast, timeStampFormat)
            now_DateTime = datetime.now()

            # Convert to Unix timestamp
            d1_ts = time.mktime(lastCheck_Time.timetuple())
            d2_ts = time.mktime(now_DateTime.timetuple())
            deltaT = int(d2_ts - d1_ts) / 60 / 60

            print(
                f'{datetime.today()}:  {str(round(deltaT, 2))} hours since last checked on {self.handle} with {self.getLatestPostCount()} posts on record')
            # Skip user if it has been less than X hours since we last checked
            return deltaT
        except Exception as e:
            print(e)
            return 48

    def thisUserDeservesDailyLove(self):
        return self._dailyLove

    def thisUserDeservesExtraLove(self):
        return self._extraLove

    def thisUserDeservesAnyKindOfLove(self):
        return self.thisUserDeservesDailyLove() or self.thisUserDeservesExtraLove()

    def removeFromLove(self, name):
        if 'daily' in name:
            self.removeFromLoveDaily()
        elif 'extra' in name:
            self.removeFromLoveExtra()
        else:
            pass

    def thereIsNoPointLovingYou(self, userPage):
        if userPage.infoAccess > 45 and userPage.followAccess > 65:
            self.removeFromLove()
            print(f"No longer will I love {userPage.userName}")
            return True
