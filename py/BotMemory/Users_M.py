import json
import time
from datetime import datetime
from uuid import uuid4

timeStampFormat = "%m/%d/%Y, %H:%M:%S"
timeStampFormat_old = "%Y_%m_%d"


class UserEncoderDecoder(json.JSONEncoder):
    def default(self, us):
        if isinstance(us, User_M):
            userDict = {
                '__user__': 'true',

                '0_Handle': us.handle,
                'uid': us.uid,
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
        self.uid = str(uuid4())
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

        self.dateFollowed_byMe = None  # The existense of a follow date means that the user has been followed ata some point and could be unfollowed
        self.dateUnFollowed_byMe = None  # The existense of a unfollow date means that the cycle is over. No more follow/unfollow actions for this user
        self._userIgotYouFrom_youWereFollowing = None

        self._markL0 = False  # MarkL0 can turn to MarkL1, MarkL2, or be rejected (all marks are faulse and follow/unfollow dates == None
        self._markL1 = False  # MarkL1 can turn to a follow (marked by the existense of a follow date), or remain as MarkL1
        self._markL2 = False  # MarkL2 will 100% turn to a follow (marked by the existense of a follow date)

        self._dateTimeLovedlast = None
        self.dateUnLoved_byMe = None
        self._dailyLove = False
        self._extraLove = False

    def populate_overwrite(self, dict):

        stats = {"posts": 0, "followers": 0, "following": 0}

        if "__user__" in dict:
            self.handle = dict.get('0_Handle', ' ')
            self.uid = dict.get('uid', str(uuid4()))
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

            self.dateFollowed_byMe = dict.get('dateFollowed_byMe', None)
            self.dateUnFollowed_byMe = dict.get('dateUnFollowed_byMe', None)
            self._userIgotYouFrom_youWereFollowing = dict.get('userIgotYouFrom_youWereFollowing', None)

            self._markL0 = dict.get('markL0', False)
            self._markL1 = dict.get('markL1', False)
            self._markL2 = dict.get('markL2', False)

            self._dateTimeLovedlast = dict.get('dateTimeLovedlast', None)
            self.dateUnLoved_byMe = dict.get('dateUnLoved_byMe', None)
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
        if len(self.listOfPastNames) > 0:
            if handleNew != self.listOfPastNames[0]:
                self.listOfPastNames.insert(0, self.handle)
        else:
            self.listOfPastNames.insert(0, self.handle)

        self.handle = handleNew

    def updateStats(self, statsDictIn):
        from datetime import datetime

        if len(self.statsDict) > 0:
            if statsDictIn != self.statsDict[0]:
                self.statsDict.insert(0, statsDictIn)
                self.statsDictTimestamp.insert(0, datetime.now().strftime(timeStampFormat))
            else:
                self.statsDictTimestamp[0] = datetime.now().strftime(timeStampFormat)
        else:
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

    def updateHashtagsFollwingList(self, newHashtags):
        self.listOf_HashTagsfollowing.extend(newHashtags)
        self.listOf_HashTagsfollowing = list(dict.fromkeys(self.listOf_HashTagsfollowing))  # remove duplicates

    def updateFollowersList(self, listF):
        self.listOf_followers.insert(0, listF)

    def updateFollowingList(self, listF):
        self.listOf_following.insert(0, listF)

    def markUserRejected(self):
        self._markL0 = False
        self._markL1 = False
        self._markL2 = False
        self.dateFollowed_byMe = None
        self.dateUnFollowed_byMe = None

    def addToL0(self, sponsorUser):
        self._markL0 = True
        self._markL1 = False
        self._markL2 = False
        self._userIgotYouFrom_youWereFollowing = sponsorUser

    def addToL1(self):
        if self._markL0:
            self._markL0 = False
            self._markL1 = True
            self._markL2 = False

    def addToL2(self):
        if self._markL1:
            self._markL0 = False
            self._markL1 = False
            self._markL2 = True

    def markTimeFollowed(self):
        from datetime import datetime
        self.dateFollowed_byMe = datetime.now().strftime(timeStampFormat)
        self._markL0 = False
        self._markL1 = False
        self._markL2 = False

    def markDateUnfollowed(self):
        from datetime import datetime

        timestamp = datetime.now().strftime(timeStampFormat)
        self.dateUnFollowed_byMe = timestamp

    def addToLoveDaily(self):
        self._dailyLove = True
        self._dateTimeLovedlast = "01/01/2020, 14:10:04"

        if self.getLatestPostCount() > 0:
            self.statsDict[0]['posts'] -= 2  # This is done to make sure the user gets a like the next time I visit

    def addToLoveExtra(self):
        self._extraLove = True
        self._dateTimeLovedlast = "01/01/2020, 14:10:04"
        print(f"#### {self.handle} added to theLoveExtra")

    def removeFromLoveDaily(self):

        timestamp = datetime.now().strftime(timeStampFormat)
        self._dailyLove = False
        self.dateUnLoved_byMe = timestamp

    def removeFromLoveExtra(self):
        self._extraLove = False
        print(f"#### {self.handle} removed from theLoveExtra")

    def printHowLongItHasBeenSinceYouGotAnyLove(self):

        try:
            lastCheck_Time = datetime.strptime(self._dateTimeLovedlast, timeStampFormat)
            now_DateTime = datetime.now()

            # Convert to Unix timestamp
            d1_ts = time.mktime(lastCheck_Time.timetuple())
            d2_ts = time.mktime(now_DateTime.timetuple())
            deltaT = int(d2_ts - d1_ts) / 60 / 60

            print(
                f'#### {datetime.today()}:  {str(round(deltaT, 2))} hours since last checked on {self.handle} with {self.getLatestPostCount()} posts on record')
            # Skip user if it has been less than X hours since we last checked
            return deltaT
        except Exception as e:
            print(e)
            return 48

    def daysSinceYouGotFollowed_Unfollowed(self, action, verbose=False):

        if "un" in action:
            date = self.dateUnFollowed_byMe
        else:
            date = self.dateFollowed_byMe

        try:
            startingDate = datetime.strptime(date, timeStampFormat)
        except ValueError:
            startingDate = datetime.strptime(date, timeStampFormat_old)
        except Exception as e:
            print(e)
            startingDate = datetime.now()
            time.sleep(2)

        try:
            now_DateTime = datetime.now()

            # Convert to Unix timestamp
            d1_ts = time.mktime(startingDate.timetuple())
            d2_ts = time.mktime(now_DateTime.timetuple())
            deltaT = int(d2_ts - d1_ts) / 60 / 60 / 24

            if verbose:
                print(f'{datetime.today()}:  {str(round(deltaT, 1))} days since I followed {self.handle}')

            return deltaT
        except Exception as e:
            print(e)
            return 1

    def thisUserDeservesDailyLove(self):
        return self._dailyLove

    def thisUserDeservesExtraLove(self):
        return self._extraLove

    def thisUserDeservesAnyKindOfLove(self):
        return self.thisUserDeservesDailyLove() or self.thisUserDeservesExtraLove()

    def removeFromLove(self, name="daily"):
        if 'daily' in name:
            self.removeFromLoveDaily()
        elif 'extra' in name:
            self.removeFromLoveExtra()
        else:
            pass

    def iShouldFollowThisUser(self):
        answer = False

        if self._markL2 and not self.dateFollowed_byMe:
            answer = True

        return answer

    def iShouldUnFollowThisUser(self):
        answer = False

        if self.dateFollowed_byMe and not self.dateUnFollowed_byMe:
            answer = True

        return answer

    def thereIsNoPointLovingYou(self, userPage):
        if userPage.infoAccess > 45 and userPage.followAccess > 65:
            self.removeFromLove("daily")
            self.removeFromLove("extra")
            print(f"No longer will I love {userPage.userName}")
            return True

    def getSponsor(self):
        return self._userIgotYouFrom_youWereFollowing

    def thisUserHasBeenRejected(self):
        response = True
        if self._markL0: response = False
        if self._markL1: response = False
        if self._markL2: response = False

        if self.dateFollowed_byMe: response = False
        if self.dateUnFollowed_byMe: response = False

        return response
