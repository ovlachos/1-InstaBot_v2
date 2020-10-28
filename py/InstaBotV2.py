import auth
import FileHandlerBot as fh
from datetime import datetime, timedelta, time
from time import sleep
import time
from POM import webPage as wp
from POM import insta_LogInPage_POM as login


class InstaBot:
    datetimeStringFormat_day = '%Y_%m_%d'

    def __init__(self, headless=False):
        self.fileHandler = fh.FileHandlerBot()
        self.webPage = wp.WebPage(headless)

    def logIn(self):
        logInPage = login.InstaLogIn(self.webPage)
        self.mainPage = logInPage.logIn(auth.username, auth.password)

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
                    print("Will follow {}".format(user))
                    if 'OK' in userpage.follow():
                        usersTofollowToday -= 1
                        self.fileHandler.addUserto_the_Love(user, 'dailyLoveCSV')
                        game_frame.iloc[rowIndexOfUser, 6] = dateList[0]  # Mark the date you followed
                        self.fileHandler.CSV_saveFrametoCSVfile('theList_1_fileCSV', game_frame)
                        sleep(25)
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

    def theLoveDaily(self, fileName, numberOflikes=2, percentageOfUsers=1):
        import pandas as pd
        # 'Like' everyone's latest N posts
        # log.error('\n\n~~~ The Love Daily commences ! ~~~\n\n')

        # Sorted by date last checked
        # Least recently checked profiles come first
        lovedOnes_frame = self.fileHandler.CSV_getFrameFromCSVfile(fileName)
        lovedOnes_frame.t_sinceLast = pd.to_datetime(lovedOnes_frame.t_sinceLast)
        lovedOnes_frame = lovedOnes_frame.sort_values(by='t_sinceLast', ascending=True)
        lovedOnes_frame = lovedOnes_frame.reset_index(drop=True)

        # This is what it's all about:
        # Send some love to the users that have new posts
        # sleep(2)
        printMark = 0.0
        loveTotal = lovedOnes_frame['theLoveDaily'].count()
        loveCount = loveTotal

        # loveTotal_dataIntegrityCheck = loveFrame['theLoveDaily'].tolist()
        # loveTotal_dataIntegrityCheck = list(dict.fromkeys(loveTotal_dataIntegrityCheck))
        # if loveTotal != len(loveTotal_dataIntegrityCheck):
        #     diff = int(abs(loveTotal - loveTotal_dataIntegrityCheck))
        #     # log.error('~~~ Missmatch of love counts: {0} users may be duplicates'.format(str(diff)))
        #     return self.tooManyActionsBreakCode

        # log.error('~~~ {0} users to love'.format(loveTotal))

        # Go through the list line by line and like things
        for index, row in lovedOnes_frame.iterrows():

            loveCount -= 1
            if (loveTotal - loveCount) > (loveTotal * percentageOfUsers):
                break

            deltaT = self.theLoveDaily_timeCheck(row)
            if 72 < deltaT <= 13:
                continue

            # Navigate to user's profile
            userPage = self.mainPage.topRibbon_SearchField.navigateToUserPageThroughSearch(row['theLoveDaily'])

            if not userPage:
                continue  # TODO: Handle username changes? Check love lists fro users with more than 72 hours since last check.

            # Check if we have new post since last time
            # Move to next user if there are no new posts since last check
            if row["Post Count"] >= userPage.stats['posts']:
                lovedOnes_frame.iloc[index, 1] = userPage.stats['posts']
                lovedOnes_frame.iloc[index, 2] = datetime.now()  # t_sinceLast
                self.fileHandler.CSV_saveFrametoCSVfile(fileName, lovedOnes_frame)
                sleep(13)
                del userPage
                continue

            # Adjust number of likes to just new posts
            if int(userPage.stats['posts'] - row["Post Count"]) < numberOflikes:
                numberOflikes = int(userPage.stats['posts'] - row["Post Count"])

            # Liking photos
            for i in range(0, numberOflikes):
                post = userPage.navigateTo_X_latestPost(i)
                sleep(1)
                post.like_post()
                sleep(2)
                post.close_post()
                sleep(1)

            lovedOnes_frame.iloc[index, 1] = userPage.stats['posts']
            lovedOnes_frame.iloc[index, 2] = datetime.now()  # t_sinceLast
            self.fileHandler.CSV_saveFrametoCSVfile(fileName, lovedOnes_frame)
            del userPage

        # log.error('\n\n~~~ The Love Daily has ended ! ~~~\n\n')
        return 'OK'

    def theLoveDaily_timeCheck(self, row):
        try:
            lastCheck_Time = row['t_sinceLast']
            now_DateTime = datetime.now()
            # Convert to Unix timestamp
            d1_ts = time.mktime(lastCheck_Time.timetuple())
            d2_ts = time.mktime(now_DateTime.timetuple())
            deltaT = int(d2_ts - d1_ts) / 60 / 60
            print('{0}:  {1} hours since last checked on {2} with {3} posts on record'.format(
                datetime.today(), str(round(deltaT, 2)), row['theLoveDaily'], row["Post Count"]))
            # Skip user if it has been less than X hours since we last checked
            return deltaT
        except Exception as e:
            print(e)
            # add a time to the row by fully going through the
            # love daily for this user
            return 48

    def list_getList_0(self, numberOfProfilesToProcess=3):
        # Get TheList_0: A list of all people following a number of profiles
        old_frame = self.fileHandler.CSV_getFrameFromCSVfile('theList_1_fileCSV')

        # If the name of the source user is already there do not re-examine
        sourceUsersAlreadyExamined = old_frame[old_frame.columns[0]].tolist()
        sourceUsersAlreadyExamined = list(dict.fromkeys(sourceUsersAlreadyExamined))  # Remove duplicates

        # If a source user's follower is already in the list we need not add a duplicate
        usersAlreadyInList = old_frame[old_frame.columns[1]].tolist()
        usersAlreadyInList = list(dict.fromkeys(usersAlreadyInList))  # Remove duplicates

        # Get a list of target source users
        targetuserInput = self.fileHandler.CSV_getFrameFromCSVfile("usersToTargetCSV")  # usersToTarget
        targetuserInputPyList = targetuserInput[targetuserInput.columns[0]].tolist()

        targetuserInputPyList = list(dict.fromkeys(targetuserInputPyList))  # Remove duplicates
        l3 = [x for x in targetuserInputPyList if
              x not in sourceUsersAlreadyExamined]  # Remove source users already examined

        # log.error('{0} users remaining'.format(len(l3)))
        if len(l3) > 0:
            targetuserInputPyList = l3[:numberOfProfilesToProcess]

            for user in targetuserInputPyList:
                # log.error('Updating the List 0 for user: {0}'.format(user))

                # Navigate to user's profile
                userPage = self.mainPage.topRibbon_SearchField.navigateToUserPageThroughSearch(user)

                if userPage:
                    followers_ = userPage.getFollowersList()

                    for follower in followers_:
                        if follower not in usersAlreadyInList:
                            newFrameRow = {old_frame.columns[0]: user,
                                           old_frame.columns[1]: follower,
                                           old_frame.columns[2]: '',
                                           old_frame.columns[3]: '',
                                           old_frame.columns[4]: '',
                                           old_frame.columns[5]: '',
                                           old_frame.columns[6]: '',
                                           old_frame.columns[7]: ''}

                            # append row to the dataframe
                            old_frame = old_frame.append(newFrameRow, ignore_index=True)
                            self.fileHandler.CSV_saveFrametoCSVfile('theList_1_fileCSV', old_frame)

                        # Update list of users already in dataframe so that we may not add a duplicate
                        usersAlreadyInList = old_frame[old_frame.columns[1]].tolist()
                        usersAlreadyInList = list(dict.fromkeys(usersAlreadyInList))  # Remove duplicates

        # log.error('No New users to examine for the list 0')

        return 'OK'

    def list_getList_1(self, processStep=4):
        # TODO cannot really work as there are too many users who have changed their handles
        # in actuall life we need to mark them as drop if we open their page and it gives the
        # broken link error. Let us do a quick fix to make a release and then fix it in the 'user' object

        # Get TheList_1: A list of all people following certain profiles that:
        # a) Do not follow me
        # b) Have less than twice my followers
        ppath = self.paths.theList_1_file
        # Get the list of profiles already examined in the list 1 file on disk
        old_frame = pd.read_csv(ppath)

        # Get a list of profiles sitting on list 0 waiting to be examined
        theList_0_frame = old_frame[
            (old_frame[old_frame.columns[3]] != 'keep') & (old_frame[old_frame.columns[3]] != 'drop')]
        theList_0_users_list = theList_0_frame[self.list_columnHeaders[1]].tolist()
        theList_0_users_list = list(dict.fromkeys(theList_0_users_list))  # Remove duplicates
        random.shuffle(theList_0_users_list)
        theList_0_users_list = theList_0_users_list[:processStep]

        # Get people already following me and remove them
        try:
            self.MyProfile.followersList = self.t1_getUser_Followers(self.username)

            # Check if we have hit Instagrams Action limit and are getting error pages only
            if self.tooManyActionsBreakCode in self.MyProfile.followersList:
                sleep(60 * 4)
                # return self.tooManyActionsBreakCode

            theList_1_list = [x for x in theList_0_users_list if
                              x not in self.MyProfile.followersList]  # Remove people already following me
            sleep(1 * 60)
        except Exception as e:
            log.error('list 1 | Unable to get my followers because: {0}'.format(e))
            # return self.tooManyActionsBreakCode
        # theList_1_list = theList_0_users_list

        try:
            print('Will try getting stats for the following users {}'.format(theList_1_list))
            theList_1_frame = old_frame

            numberOfFails = 0
            user_counter = 0
            for user in theList_1_list:
                user_counter += 1
                rowIndexOfUser = theList_1_frame[theList_1_frame.a1_User == user].index.values[0]

                if self.t0_Open_user_profile(user):
                    dictio = self.currentProfileStats_dict

                    # In case the process fails to retrieve real stats
                    # the value returned for followers is '99999999'
                    # in this case we do not want to write junk to our frame/file
                    # so we skip this user's false stats
                    if dictio['Followers'] == 99999999:
                        numberOfFails += 1
                        if numberOfFails > 0.4 * processStep:
                            return self.tooManyActionsBreakCode

                        continue

                    # Filter out users with more than 500 followers
                    mark = 'keep'
                    if dictio['Followers'] > (2 * len(self.MyProfile.followersList)) or (dictio['Posts'] <= 3):
                        mark = 'drop'
                        print('Droping user: {0} has {1} followers and {2} posts'.format(dictio['user'],
                                                                                         str(dictio['Followers']),
                                                                                         str(dictio['Posts'])))
                    else:
                        print('Keeping user: {0} has {1} followers'.format(dictio['user'], str(dictio['Followers'])))

                    # write new user progress to frame
                    theList_1_frame.iloc[rowIndexOfUser, 2] = int(dictio['Followers'])
                    theList_1_frame.iloc[rowIndexOfUser, 3] = mark
                    # theList_1_frame.columns = self.list_columnHeaders

                    theList_1_frame.to_csv(ppath, index=False, encoding='utf-8')
                    if mark == 'keep':
                        self.t2_getList_2(user, theList_1_frame)

                    log.error('L1-L2: {0} users processed'.format(user_counter))
                else:
                    # In case the page did not open due to
                    # tooManyActionsLimit being hit

                    theList_1_frame.iloc[rowIndexOfUser, 2] = 0
                    theList_1_frame.iloc[rowIndexOfUser, 3] = "drop"
                    theList_1_frame.to_csv(ppath, index=False, encoding='utf-8')

                    numberOfFails += 1
                    HelperBot.sleepForXseconds(self.helper, 30, 40)
                    if numberOfFails > 0.3 * processStep:
                        print('L_1 died on too many actions hit while just opening user profiles')
                        return self.tooManyActionsBreakCode
                    continue

        except Exception as e2:
            print('list 1 | Unable to get user stats because: {0}'.format(e2))
            log.error('list 1 | Unable to get user stats because: {0}'.format(e2))

        return 'OK'

    def list_getList_2(self, user, theList_1_frame):
        # Get TheList_2: A list of people following certain hashTags
        # and/or use certain words in their bio

        rowIndexOfUser = theList_1_frame[theList_1_frame.a1_User == user].index.values[0]
        theList_1_frame.iloc[rowIndexOfUser, 4] = 'drop'
        theList_1_frame.iloc[rowIndexOfUser, 5] = 'drop'

        try:
            hashtags = self.t1_getProfiles_N_tags_followed_By_user(user)
            # hashtags = combinedList[1]
            # following = combinedList[0]
        except Exception as e:
            log.error('List 2 died on user: {0} because {1}'.format(user, e))
            return self.tooManyActionsBreakCode

        # Check if we have hit Instagrams Action limit and are getting error pages only
        if self.tooManyActionsBreakCode in hashtags:
            return self.tooManyActionsBreakCode

        # While we are at it let's get some #tag usage stats
        self.tH_getHashtagFollowership_embededInList2(user, hashtags)

        # Record hashtags followed and word in bio
        if len(hashtags) != 0:
            commonlist = [x for x in hashtags if x in self.targetHashtags_List]
            if len(commonlist) > 0:
                theList_1_frame.iloc[rowIndexOfUser, 4] = 'keep'
                # continue
            for word in self.words:
                for tag in hashtags:
                    if word in tag:
                        theList_1_frame.iloc[rowIndexOfUser, 4] = 'keep'

        for word in self.words:
            if word in self.currentProfileStats_dict['bio']:
                theList_1_frame.iloc[rowIndexOfUser, 4] = 'keep'
                break

            if word in self.currentProfileStats_dict['user']:
                theList_1_frame.iloc[rowIndexOfUser, 4] = 'keep'
                break

        # Get prime candidates
        # if len(following) > 0 and theList_1_frame.iloc[rowIndexOfUser, 4] == 'keep':
        #     follow_overlap = [x for x in following if x in self.MyProfile.followersList]
        #     if len(follow_overlap) > 1:
        #         theList_1_frame.iloc[rowIndexOfUser, 5] = 'keep'

        ppath = self.paths.theList_1_file
        theList_1_frame.to_csv(ppath, index=False, encoding='utf-8')

        return 'OK'
