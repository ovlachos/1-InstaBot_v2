from datetime import datetime, timedelta
from time import sleep
from POM import webPage as wp
from POM import insta_LogInPage_POM as login
import FileHandlerBot as fh


class InstaBot:
    datetimeStringFormat_day = '%Y_%m_%d'

    def __init__(self, headless=False):
        self.fileHandler = fh.FileHandlerBot()
        self.webPage = wp.WebPage(headless)

    def logIn(self):
        logInPage = login.InstaLogIn(self.webPage)
        self.mainPage = logInPage.logIn()

    def logOut(self):
        self.mainPage.topRibbon_myAccount.logOut()

    def shutDown(self):
        self.logOut()
        self.webPage.killBrowser()

    def theGame(self, processStep=30):
        # Setup parameters
        howManyDaysBeforeI_unfollow = 10
        howManyDaysBeforeI_unlove = howManyDaysBeforeI_unfollow + 4
        usersTofollowToday = processStep

        # create dateList of dates in datetimeStringFormat_day format
        dateList = []
        for i in range(0, 21):
            dateList.append((datetime.today() - timedelta(days=i)).strftime(self.datetimeStringFormat_day))
            # if this date formating changes we are screwed. If so make sure to change it across the board

        # Get theList_1 into a frame
        game_frame = self.fileHandler.CSV_getFrameFromCSVfile('theList_1_fileCSV')

        # Get gameLists
        game_lists = self.derive_Game_Lists(dateList, game_frame, howManyDaysBeforeI_unfollow,
                                            howManyDaysBeforeI_unlove)

        # unLove
        if game_lists[3]:
            dailyLove_list = self.fileHandler.CSV_getFrameFromCSVfile('dailyLoveCSV')['theLoveDaily'].tolist()
            listFinal = [x for x in game_lists[3] if x in dailyLove_list]
            for user in listFinal:
                self.fileHandler.removeUserfrom_the_Love(user, 'dailyLoveCSV')

        # unFollow
        if game_lists[2]:
            for user in game_lists[2]:
                rowIndexOfUser = game_frame[game_frame.a1_User == user].index.values[0]

                userpage = self.mainPage.topRibbon_SearchField.navigateToUserPageThroughSearch(user)

                if userpage:
                    if 'OK' in userpage.unfollow():
                        game_frame.iloc[rowIndexOfUser, 7] = dateList[0]  # Mark the date you unfollowed
                        self.fileHandler.CSV_saveFrametoCSVfile('theList_1_fileCSV', game_frame)
                        sleep(25)
                        print("UnFollow {}".format(user))
                else:
                    # what happens if a user page does not come up / does not exist
                    # -> mark as unfollowed today
                    print('User {} not found'.format(user))
                    game_frame.iloc[rowIndexOfUser, 7] = dateList[0]  # Mark the date you unfollowed
                    self.fileHandler.CSV_saveFrametoCSVfile('theList_1_fileCSV', game_frame)

        # Follow optimal
        usersTofollowToday = self.theGame_Follow(dateList, game_frame, game_lists[0], usersTofollowToday)

        # Follow regular
        if usersTofollowToday > 0:
            usersTofollowToday = self.theGame_Follow(dateList, game_frame, game_lists[1], usersTofollowToday)

        # Final Check of tallied actions
        if usersTofollowToday == 0:
            print('OK_Game')
        else:
            print("Fail_Game")

    def theGame_Follow(self, dateList, game_frame, game_list, usersTofollowToday):
        if game_list:
            game_list = game_list[:usersTofollowToday]
            for user in game_list:
                rowIndexOfUser = game_frame[game_frame.a1_User == user].index.values[0]

                # follow
                userpage = self.mainPage.topRibbon_SearchField.navigateToUserPageThroughSearch(user)

                if userpage:
                    # add to love daily and record progress
                    if 'OK' in userpage.follow():
                        usersTofollowToday -= 1
                        self.fileHandler.addUserto_the_Love(user, 'dailyLoveCSV')
                        game_frame.iloc[rowIndexOfUser, 6] = dateList[0]  # Mark the date you followed
                        self.fileHandler.CSV_saveFrametoCSVfile('theList_1_fileCSV', game_frame)
                        sleep(25)
                        print("Will follow {}".format(user))
                else:
                    # what happens if a user page does not come up / does not exist
                    # -> mark as followed/unfollowed in the very far future
                    print('User {} not found'.format(user))
                    game_frame.iloc[rowIndexOfUser, 6] = '3000_01_01'  # Mark the date you followed
                    game_frame.iloc[rowIndexOfUser, 7] = '3000_01_02'  # Mark the date you unfollowed
                    self.fileHandler.CSV_saveFrametoCSVfile('theList_1_fileCSV', game_frame)

        return usersTofollowToday

    def derive_Game_Lists(self, dateList, game_frame, howManyDaysBeforeI_unfollow, howManyDaysBeforeI_unlove):
        ## Derive lists of: ##
        #   a) Users to follow (optimal)
        #   b) Users to follow (normal)
        #   c) Users to unFollow
        #   d) Users to unLove

        # (a)
        optimalFutureFollowers_frame = game_frame[game_frame[game_frame.columns[5]] == 'keep']
        optimalFutureFollowers_frame = optimalFutureFollowers_frame[optimalFutureFollowers_frame.iloc[:, 6].isnull()]
        optimalFutureFollowers_list = optimalFutureFollowers_frame.iloc[:, 1].tolist()

        # (b)
        futureFollowers_frame = game_frame[game_frame[game_frame.columns[4]] == 'keep']
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
