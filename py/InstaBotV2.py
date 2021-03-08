import auth
from random import randint
from datetime import datetime, timedelta
from time import sleep

from BotServices import Love_Service
from BotServices import L0_Service
from BotServices import L1_2_Service
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
        self.timeLimitSinceLastLoved = 1
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

    def clearBrowserData(self):  # This does nothing
        self.webPage.instance.clearCache()
        print('Firefox data cleared')

    def shutDown(self):
        self.logOut()
        sleep(1)
        self.webPage.instance.writeSessionDataToJSON()
        self.webPage.killBrowser()

    def getBrowser(self):
        self.webPage = wp.WebPage(self.headless)

    def botSleep(self):
        sleep(randint(self.timeLowerBound, self.timeUpperBound))

    def delayOps(self, minimum=2, maximum=20):
        sleepTime = randint((minimum * 60), (maximum * 60))
        print(f'Sleeping for {int(sleepTime / 60)} minutes')
        sleep(sleepTime)

    def loveService(self, fileName, numberOfLikes, percentageOfUsers):
        return Love_Service.love(self, fileName, numberOfLikes, percentageOfUsers)

    def l0_Service(self, numberOfProfilesToProcess):
        return L0_Service.list_getList_0(self, numberOfProfilesToProcess)

    def l1_2_Service(self):
        return L1_2_Service.userScraping(self, self.followMana)

    def list_getList_1(self, processStep=70):
        # Get TheList_1: A list of all people following certain profiles that:
        # a) Do not follow me
        # b) Have less than 1.05 times my followers

        print(datetime.today())

        # Get the list of profiles already examined in the list 1 file on disk
        theList_1_frame = self.fileHandler.CSV_getFrameFromCSVfile('theList_1_fileCSV')

        # Get a list of profiles sitting on list 0 waiting to be examined
        theList_0_frame = theList_1_frame[
            (theList_1_frame[theList_1_frame.columns[3]] != 'keep') &
            (theList_1_frame[theList_1_frame.columns[3]] != 'drop')]

        theList_0_users_list = theList_0_frame[theList_0_frame.columns[1]].tolist()
        theList_0_users_list = list(dict.fromkeys(theList_0_users_list))  # Remove duplicates
        theList_1_list = theList_0_users_list

        # Get people already following me and remove them
        try:
            myPage = self.mainPage.topRibbon_myAccount.navigateToOwnProfile()

            if not myPage:
                return "Fail"

            myFollowers = myPage.getFollowersList()
            myFollowersCount = myPage.stats['followers']
            theList_1_list = [x for x in theList_0_users_list if x not in myFollowers]

        except Exception as e:
            print(e)

        theList_1_list = theList_1_list[:processStep]
        print('Will try getting stats for the following {0} users {1}'.format(len(theList_1_list), theList_1_list))

        user_counter = 0
        for user in theList_1_list:
            try:
                rowIndexOfUser = theList_1_frame[theList_1_frame.a1_User == user].index.values[0]

                # Navigate to user's profile
                userPage = self.mainPage.topRibbon_SearchField.navigateToUserPageThroughSearch(user)

                if not userPage:
                    # write new user progress to frame
                    print(f"Dropping user: {user}. No page found (code -666)")
                    theList_1_frame.iloc[rowIndexOfUser, 2] = -666
                    theList_1_frame.iloc[rowIndexOfUser, 3] = "drop"
                    self.fileHandler.CSV_saveFrametoCSVfile('theList_1_fileCSV', theList_1_frame)
                    continue

                dictio = userPage.getStats_dict()
                user_counter += 1

                # Filter out users with more than myself
                mark = 'keep'
                if dictio['followers'] > (1.05 * myFollowersCount) or (dictio['posts'] < 3):
                    mark = 'drop'
                    print('L1 - Dropping user: {0} has {1} followers and {2} posts'.format(user,
                                                                                           str(dictio['followers']),
                                                                                           str(dictio['posts'])))
                else:
                    print('L1 - Keeping user: {0} has {1} followers while I have {2}'.format(user, str(dictio['followers']), myFollowersCount))

                # write new user progress to frame
                theList_1_frame.iloc[rowIndexOfUser, 2] = int(dictio['followers'])
                theList_1_frame.iloc[rowIndexOfUser, 3] = mark
                self.fileHandler.CSV_saveFrametoCSVfile('theList_1_fileCSV', theList_1_frame)

                if mark == 'keep':
                    l2_response = self.list_getList_2(user, theList_1_frame, userPage)
                    if l2_response == 'OK':
                        print(f'L2 - Keeping user: {user}')

                sleep(randint(self.timeLowerBound, self.timeUpperBound))

            except Exception as e2:
                print('list 1 | Unable to get user stats because: {0}'.format(e2))

        print(datetime.today())
        return 'OK'

    def list_getList_2(self, user, theList_1_frame, userPage):
        # Get TheList_2: A list of people following certain hashTags
        # and/or use certain words in their bio

        def checkHashTags():

            if hashtags:

                commonlist = [x for x in hashtags if x in self.targetHashtags_List]

                if len(commonlist) > 0:
                    return True

                for word in self.words:
                    for tag in hashtags:
                        if word in tag:
                            return True

        def checkProfile():

            for word in self.words:

                if word in userPage.bio:
                    return True

                if word in user:
                    return True

                if word in userPage.altName:
                    return True

        response = 'meh'

        rowIndexOfUser = theList_1_frame[theList_1_frame.a1_User == user].index.values[0]
        theList_1_frame.iloc[rowIndexOfUser, 4] = 'drop'
        theList_1_frame.iloc[rowIndexOfUser, 5] = 'drop'

        ## Check the profile first cuse usually it is easier and more obvious
        if checkProfile():
            theList_1_frame.iloc[rowIndexOfUser, 4] = 'keep'
            self.fileHandler.CSV_saveFrametoCSVfile('theList_1_fileCSV', theList_1_frame)
            return 'OK'

        ## Then if it is not that obvious get Hashtags a user follows
        hashtags = []
        try:
            hashtags = userPage.getHashtagsFollowingList()
            # TODO: While we are at it let's get some #tag usage stats
            # self.tH_getHashtagFollowership_embededInList2(user, hashtags)
        except Exception as e:
            print(e)

        if checkHashTags():
            theList_1_frame.iloc[rowIndexOfUser, 4] = 'keep'
            self.fileHandler.CSV_saveFrametoCSVfile('theList_1_fileCSV', theList_1_frame)
            return 'OK'

        return response

    def theGame(self, usersTofollowToday=30):

        print('\n\n')
        # create dateList of dates in datetimeStringFormat_day format
        dateList = []
        for i in range(0, self.daysBeforeIunLove + 5):
            dateList.append((datetime.today() - timedelta(days=i)).strftime(self.datetimeStringFormat_day))
            # if this date formatting changes we are screwed. If so make sure to change it across the board

        # Get theList_1 into a frame
        game_frame = self.fileHandler.CSV_getFrameFromCSVfile('theList_1_fileCSV')

        # Get gameLists
        game_lists = self.theGame_derive_Game_Lists(dateList, game_frame, self.daysBeforeIunFollow,
                                                    self.daysBeforeIunLove)

        # unLove
        if game_lists[3]:
            self.theGame_Unlove(game_lists[3])

        # unFollow
        if game_lists[2]:
            self.theGame_Unfollow(dateList, game_frame, game_lists[2])

        print(f'{len(game_lists[0]) + len(game_lists[1])} users left to follow')
        print(f'{len(game_lists[0])} optimal users left to follow')
        if usersTofollowToday > (len(game_lists[0]) + len(game_lists[1])):
            usersTofollowToday = len(game_lists[0]) + len(game_lists[1])

        # Follow optimal
        while usersTofollowToday > 0 and len(game_lists[0]) > 0:
            usersTofollowToday = self.theGame_Follow(dateList, game_frame, game_lists[0], usersTofollowToday)

        # Follow regular
        # while usersTofollowToday > 0 and len(game_lists[1]) > 0:
        #     usersTofollowToday = self.theGame_Follow(dateList, game_frame, game_lists[1], usersTofollowToday)

        # Final Check of tallied actions
        if usersTofollowToday == 0:
            print('OK_Game')
        else:
            print("Fail_Game: {0}".format(usersTofollowToday))

    def theGame_Unlove(self, game_list):
        dailyLove_list = self.fileHandler.CSV_getFrameFromCSVfile('dailyLoveCSV')['theLoveDaily'].tolist()
        listFinal = [x for x in game_list if x in dailyLove_list]

        print(f"{len(listFinal)} to UnLove")

        for user in listFinal:
            self.fileHandler.removeUserfrom_the_Love(user, 'dailyLoveCSV')

        # Checking if the numbers make sense
        dailyLove_list_1 = self.fileHandler.CSV_getFrameFromCSVfile('dailyLoveCSV')['theLoveDaily'].tolist()
        listFinal_1 = [x for x in game_list if x in dailyLove_list_1]

        if len(listFinal_1) > 0:
            print(f'{len(listFinal_1)} users not removed from the love daily')

    def theGame_Follow(self, dateList, game_frame, game_list, usersTofollowToday):
        if game_list:

            game_list = game_list[:usersTofollowToday]
            if len(game_list) < usersTofollowToday:
                usersTofollowToday = len(game_list)

            for user in game_list:
                rowIndexOfUser = game_frame[game_frame.a1_User == user].index.values[0]

                # follow
                userpage = self.mainPage.topRibbon_SearchField.navigateToUserPageThroughSearch(user)

                if userpage:
                    # add to love daily and record progress
                    print("Will follow {}".format(user))
                    if 'OK' in userpage.follow():
                        usersTofollowToday -= 1
                        self.fileHandler.addUserto_the_Love(user, 'dailyLoveCSV')
                        game_frame.iloc[rowIndexOfUser, 6] = dateList[0]  # Mark the date you followed
                        self.fileHandler.CSV_saveFrametoCSVfile('theList_1_fileCSV', game_frame)
                    sleep(randint(self.timeLowerBound, self.timeUpperBound))
                else:
                    # what happens if a user page does not come up / does not exist
                    # -> mark as followed/unfollowed in the very far future
                    print('User {} not found'.format(user))
                    game_list.remove(user)
                    game_frame.iloc[rowIndexOfUser, 6] = '3000_01_01'  # Mark the date you followed
                    game_frame.iloc[rowIndexOfUser, 7] = '3000_01_02'  # Mark the date you unfollowed
                    self.fileHandler.CSV_saveFrametoCSVfile('theList_1_fileCSV', game_frame)

        return usersTofollowToday

    def theGame_Unfollow(self, dateList, game_frame, game_list):
        print(f"{len(game_list)} to UnFollow")
        numberToUnfollow = len(game_list)

        unLoveListPlus = []

        for user in game_list:
            rowIndexOfUser = game_frame[game_frame.a1_User == user].index.values[0]

            userpage = self.mainPage.topRibbon_SearchField.navigateToUserPageThroughSearch(user)

            if userpage:
                print("UnFollow {}".format(user))
                if 'OK' in userpage.unfollow():
                    game_frame.iloc[rowIndexOfUser, 7] = dateList[0]  # Mark the date you unfollowed
                    self.fileHandler.CSV_saveFrametoCSVfile('theList_1_fileCSV', game_frame)
                    numberToUnfollow -= 1

                    # unlove if unfollowing makes like access impossible
                    if userpage.infoAccess > 45:
                        unLoveListPlus.append(user)
                sleep(randint(self.timeLowerBound, self.timeUpperBound))
            else:
                # what happens if a user page does not come up / does not exist
                # -> then I mark as unfollowed in 1/1/1989 so that I can
                # -> figure out who they are later and they also get auto-removed from love lists
                print('User {} not found'.format(user))
                game_frame.iloc[rowIndexOfUser, 7] = '1989_01_01'  # Mark the date you unfollowed
                self.fileHandler.CSV_saveFrametoCSVfile('theList_1_fileCSV', game_frame)

        self.theGame_Unlove(unLoveListPlus)  # unlove if they did not follow back
        print(f"{numberToUnfollow} left to UnFollow")

    def theGame_derive_Game_Lists(self, dateList, game_frame, howManyDaysBeforeI_unfollow, howManyDaysBeforeI_unlove):
        ## Derive lists of: ##
        #   a) Users to follow (optimal)
        #   b) Users to follow (normal)
        #   c) Users to unFollow
        #   d) Users to unLove

        # (a)
        optimalFutureFollowers_frame = game_frame[game_frame[game_frame.columns[4]] == 'keep']
        optimalFutureFollowers_frame = optimalFutureFollowers_frame[optimalFutureFollowers_frame.iloc[:, 6].isnull()]
        optimalFutureFollowers_list = optimalFutureFollowers_frame.iloc[:, 1].tolist()

        # (b)
        futureFollowers_frame = game_frame[game_frame[game_frame.columns[3]] == 'keep']
        futureFollowers_frame = futureFollowers_frame[futureFollowers_frame[futureFollowers_frame.columns[4]] == 'drop']
        futureFollowers_frame = futureFollowers_frame[futureFollowers_frame.iloc[:, 6].isnull()]
        futureFollowers_list = futureFollowers_frame.iloc[:, 1].tolist()
        futureFollowers_list = [x for x in futureFollowers_list if x not in optimalFutureFollowers_list]

        # (c)
        usersToUnfollow_frame = game_frame[(game_frame.iloc[:, 6] < dateList[howManyDaysBeforeI_unfollow])]
        usersToUnfollow_frame = usersToUnfollow_frame[usersToUnfollow_frame.iloc[:, 7].isnull()]
        usersToUnfollow_list = usersToUnfollow_frame.iloc[:, 1].tolist()

        # (d)
        usersToStopLoving_frame = game_frame[game_frame.iloc[:, 7] < dateList[howManyDaysBeforeI_unlove]]
        usersToStopLoving_list = usersToStopLoving_frame.iloc[:, 1].tolist()

        ##    Lists Ready      ##

        return [optimalFutureFollowers_list, futureFollowers_list, usersToUnfollow_list, usersToStopLoving_list]
