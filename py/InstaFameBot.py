# -- "InstaFameBot.py" --
# ~ Gets lists of followers of my Instagram profile and any other larger pool of people.
# ~ Executes follow orders on people I should be following.
# ~ Gets past list of people I ordered to be followed from storage [not programmatically/dynamically].
# ~ Checks which people I followed more than a week ago.
# ~ Uses .py files/modules above to figure out which profiles failed to follow me back within the past week.
# ~ Executes "executeFollowUnfollowOneProfile.py" on the above with a "pleaseUnfollow" argument.

import auth
import glob
import logging
import os
import time
import random
import datetime
import pandas as pd
import NoLogIn_getHashTagOrProfileInfo as noLogin

from selenium import webdriver
from datetime import datetime, timedelta
from random import randint
from time import sleep
from collections import Counter

datetimeStringFormat_day = '%Y_%m_%d'
datetimeStringFormat_minute = '%Y_%m_%d %H-%M'

log = logging.getLogger("InstaFame")
dirname_of_py_files0 = os.path.dirname(
    __file__)
projectFolderPath0 = os.path.join(dirname_of_py_files0, '../')
hdlr = logging.FileHandler(projectFolderPath0 + 'InstaFame.log')
formatter = logging.Formatter('%(asctime)s %(message)s')
hdlr.setFormatter(formatter)
# to avoid logging duplication the below clearance must be made
if (log.hasHandlers()):
    log.handlers.clear()
log.addHandler(hdlr)


class User:
    profileStats_dict = {
        "Posts": 999999,
        "Followers": 999999,
        "Following": 999999,
        "user": 'Κοπερτί',
        "bio": 'IamaΚοπερτί'
    }
    followersList = []
    follow_ingList = []
    hashtags_following_list = []
    postsList = []
    postsTheyLiked = []
    postVelocity = 0
    lastChecked = '2020_01_01'

    def __init__(self, handle):
        self.profileStats_dict['user'] = handle

    def UpdateDict(self, dict):
        self.profileStats_dict['Posts'] = dict['Posts']
        self.profileStats_dict['Followers'] = dict['Followers']
        self.profileStats_dict['Following'] = dict['Following']
        self.profileStats_dict['user'] = dict['user']
        self.profileStats_dict['bio'] = dict['bio']


class post:
    noOfLikes = 0
    location = ''
    post_href = ''
    datePosted = ''
    usersThatLiked = []
    usersCommented = []
    comments = []

    def __init__(self, href, driver, scrolNget):
        self.post_href = href
        self.driver = driver
        self.helper = HelperBot
        self.scroll_and_get = scrolNget
        # Mandatory waiting time to make sure we do not hit any limits
        # 200 profile views pre hour = at least 18secs wait
        self.helper.sleepForXseconds(self.helper, 20, 28)
        try:
            self.driver.get(self.post_href)
            self.updatePostDateTime()
            self.updatePostLocation()
            try:
                self.updateUsers_commented_underPost()
            except Exception as e:
                print(e)
            # self.updateUsers_liked_post_andCount()

        except Exception as e:
            print(e)

    def updateUsers_commented_underPost(self):
        try:
            elements = self.driver.find_elements_by_xpath(
                "//a[@class='sqdOP yWX7d     _8A5w5   ZIAjV ']")
            for element in elements:
                self.usersCommented.append(element.text)

            self.usersCommented = list(dict.fromkeys(self.usersCommented))
        except Exception as e:
            print(e)
            self.usersCommented = []

    def updateUsers_liked_post_andCount(self):
        try:
            sleep(3)
            numberOfLikesElem = self.driver.find_elements_by_xpath("//button[@class='sqdOP yWX7d     _8A5w5    ']")
            if ' others' in numberOfLikesElem[1].text:
                self.noOfLikes = int(numberOfLikesElem[1].text.strip(' others')) + 1
            else:
                self.noOfLikes = int(numberOfLikesElem[1].text.strip(' likes'))
        except Exception as e:
            print(e)
            self.noOfLikes = 0

        try:
            numberOfLikesElem = self.driver.find_elements_by_xpath("//button[@class='sqdOP yWX7d     _8A5w5    ']")
            likesListReveal_button = numberOfLikesElem[1]
            sleep(3)
            likesListReveal_button.click()
            sleep(3)
            self.usersThatLiked = self.scroll_and_get('users', "//div[contains(@style,'overflow')]", self.noOfLikes)
            self.usersThatLiked = list(dict.fromkeys(self.usersThatLiked))
            if len(self.usersThatLiked) != self.noOfLikes:
                diff = self.noOfLikes - len(self.usersThatLiked)
                print('UsersThatLiked: scroll and get fell short by {0}'.format(str(diff)))
        except Exception as e:
            print(e)
            self.usersThatLiked = []

    def updatePostDateTime(self):
        try:
            dateElement = self.driver.find_element_by_xpath("//time[@class='_1o9PC Nzb55']")
            self.datePosted = dateElement.get_attribute('datetime')
        except Exception as e:
            print(e)
            self.datePosted = ""

    def updatePostLocation(self):
        try:
            loc_element_text = self.driver.find_element_by_xpath("//a[contains(@href,'/explore/locations')]").text
            if 'LOCATIONS' in loc_element_text:
                self.location = ""
            self.location = loc_element_text
        except Exception as e:
            print(e)
            self.location = ""


class file_paths:
    # Folders
    dirname_of_py_files = os.path.dirname(
        __file__)  # e.g. '/Users/cortomaltese/Google Drive/10 Projects/1 Insta-Fame WebScraper/instaBot/py'
    projectFolderPath = os.path.join(dirname_of_py_files, '../')
    outputs = os.path.join(projectFolderPath, 'Outputs/')
    inputs = os.path.join(projectFolderPath, 'Inputs/')
    targetuserInput = os.path.join(projectFolderPath, 'Inputs/targetusers/')
    myStats = os.path.join(projectFolderPath, 'Outputs/MyStats/')
    theScum = os.path.join(projectFolderPath, 'Outputs/scumReport/')
    mutineers = os.path.join(projectFolderPath, 'Mutineers/')

    # Files
    myStats_FolowersCSV = outputs + 'myFollowers.csv'
    myStats_FollowingCSV = outputs + 'myFollow_ing.csv'
    fansOnly = outputs + 'fansOnly.csv'

    unfollowListCSV = inputs + 'unfollowList.csv'
    theDailyLoveCSV = inputs + 'theLoveDaily.csv'
    extraLoveCSV = inputs + 'extraLove.csv'
    theScumMainCSV = outputs + 'theScum_Main.csv'
    theScumWhiteListCSV = inputs + 'scumWhitelist.csv'

    targetUserHashtagsCSV = inputs + 'targetUserHashtags.csv'
    hashtagFollowershipStatsCSV = outputs + 'hashtags_followersihp_stats.csv'

    theList_0_file = outputs + 'TheList_0.csv'
    theList_1_file = outputs + 'TheList_1.csv'
    addToTheGame = inputs + "manuallGameAdditions.csv"


class HelperBot:

    def sleepForXseconds(self, lowerBound=10, upperBound=20, verbose=False, printInterval=0.5):
        sleep_time = randint(lowerBound, upperBound)
        if verbose: log.error('>>>> Start of Sleep {0}s'.format(str(sleep_time)))
        for second in reversed(range(0, sleep_time)):
            sleep(1)
            if (printInterval * sleep_time) <= second < ((printInterval * sleep_time) + 1):
                if verbose: log.error('{0} secs of sleep left'.format(str(second)))
                printInterval = printInterval * 2

        if verbose:  log.error('>>>> end of Sleep {0}s'.format(str(sleep_time)))

    def oneHour_timeDelay(self):
        print('~~~ Catching some Zzzzz')
        sleep(60 * 60 * 1)
        self.helper.sleepForXseconds(self.helper, (60 * 1.5), (60 * 2), 0.5, True)
        print('~~~ JUST wole up')

    def findAlltxtFiles_pathsToList(path):
        # navigate to folder where all stored txt files are
        os.chdir(path)
        # create a list with all the .txt file paths
        paths = []
        for file in glob.glob("*.txt"):
            paths.append(path + file)
        paths.sort()

        return paths

    def readLinesFromTXTFile(inputFilepath):
        f = open(inputFilepath, "r")
        linesList = []
        for line in f:
            linesList.append(line.strip('\n'))

        linesList = list(filter(lambda x: x != "", linesList))
        linesList = list(dict.fromkeys(linesList))

        return linesList

    def addNewRow_toDataFrame(self, mainDF, newRowList):
        a_row = pd.Series(newRowList)
        newRow_df = pd.DataFrame([a_row])
        newRow_df.columns = list(mainDF.columns)[:len(list(newRow_df.columns))]

        try:
            return mainDF.append([newRow_df], ignore_index=True, sort=False)
        except Exception as e:
            return mainDF

    def getFolowershipRowList_byDate(self, frame, date):
        row = frame[frame[frame.columns[0]] == date].values.flatten().tolist()[2:]
        return [x for x in row if str(x) != 'nan']


class InstaBot:

    def __init__(self, username, pw):
        self.driver = self.tH_getDriver()
        self.username = username
        self.pw = pw
        self.myUser = User(self.username)
        self.paths = file_paths
        self.helper = HelperBot
        self.MyProfile = User(username)
        self.tooManyActionsBreakCode = 'Kopertí'
        self.list_columnHeaders = ['a0_User_a1_follows',
                                   'a1_User',
                                   'a2_Count_of_Followers_of_a1',
                                   'a3_TheList_1_keep_drop',
                                   'a4_TheList_2_keep_drop',
                                   'a5_TheList_3_keep_drop',
                                   'a6_theGame_Follow_Date',
                                   'a7_theGame_UnFollow_Date']
        self.list_column_dTypes = {
            "a0_User_a1_follows": 'str',
            "a1_User": 'str',
            "a2_Count_of_Followers_of_a1": 'int',
            "a3_TheList_1_keep_drop": 'str',
            "a4_TheList_2_keep_drop": 'str',
            "a5_TheList_3_keep_drop": 'str',
            "a6_theGame_Follow_Date": 'str',
            "a7_theGame_UnFollow_Date": 'str'
        }
        self.currentProfileStats_dict = {
            "Posts": 999999,
            "Followers": 999999,
            "Following": 999999,
            "user": 'Κοπερτί',
            "bio": 'IamaΚοπερτί'
        }

        # Read from drive specific hashtags to look for
        self.targetHashtags_frame = pd.read_csv(file_paths.targetUserHashtagsCSV)
        self.targetHashtags_frame.columns = ['HashTags']
        self.targetHashtags_List = self.targetHashtags_frame['HashTags'].tolist()
        self.targetHashtags_List = list(dict.fromkeys(self.targetHashtags_List))  # Remove duplicates

        # Read from drive specific keyWords to look for
        self.words = self.helper.readLinesFromTXTFile(self.paths.inputs + 'words.txt')

    def tH_getDriver(self):
        # setting up a Chrome driver
        option = webdriver.ChromeOptions()
        chrome_prefs = {}
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
        option.experimental_options["prefs"] = chrome_prefs

        # setting up a Firefox driver
        profile = webdriver.FirefoxProfile()
        profile.set_preference("intl.accept_languages", 'en-us')
        profile.update_preferences()
        # 1 - Allow all images
        # 2 - Block all images
        # 3 - Block 3rd party images
        profile.set_preference("permissions.default.image", 1)

        return webdriver.Firefox(firefox_profile=profile)
        # return webdriver.Chrome(options=option)
        # return webdriver.Chrome()

    def tH_close_browser(self):
        self.driver.quit()
        print("Browser closed! Did you log out?")

    def tH_logIn(self):
        self.driver.get("https://www.instagram.com")
        sleep(randint(2, 6))
        try:
            loginButton = self.driver.find_element_by_xpath("//a[contains(text(), 'Log in')]")
            loginButton.click()
        except Exception as e:

            self.driver.get("https://www.instagram.com/accounts/login/")
            print(e)
        sleep(randint(2, 6))
        self.driver.find_element_by_xpath("//input[@name=\"username\"]") \
            .send_keys(self.username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]") \
            .send_keys(self.pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]') \
            .click()
        sleep(4)
        try:
            self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]") \
                .click()
        except Exception as e:
            print(e)

            try:
                # self.driver.find_element_by_xpath('//button[@type="submit"]') \
                #     .click()
                self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]") \
                    .click()
            except Exception as e:
                print(e)
                sleep(1)
        sleep(5)

    def tH_logOut(self):
        print('sleep before logging out')
        sleep(7 * 60)
        if self.t0_Open_user_profile(self.username):
            try:
                # Bring up the full options panel
                self.driver.find_element_by_xpath("//div[@class='AFWDX']").click()
                sleep(3)
            except Exception as e:
                log.error("Log out: {0}".format(e))

            try:
                # Clisk on the log out option
                self.driver.find_element_by_xpath("//button[contains(text(), 'Log Out')]").click()
                sleep(3)
                print("Logged out!")
                return True
            except Exception as e:
                log.error("Log out: {0}".format(e))
        else:
            print('\nCould not log out!\n')
            log.error('\nCould not log out!\n')
            return False

    def tH_checkIfIhit_ActionLimit(self, driver):
        try:
            errorMessagePresent = driver.find_element_by_xpath("//p[contains(text(),'Please wait a few minutes')]").text
        except:
            return False

        if 'wait' in errorMessagePresent:
            return True

    def tH_resetRouter(self):
        try:
            print('%%%%%%%%%%%%% reseting router')
            # sleep(60)
            log.error('%%%%%%%%%%%%% reseting router    ')
            self.driver.get('http://192.168.1.1/')
            sleep(5)
            self.driver.find_element_by_xpath("//a[@id='signin']").click()
            sleep(5)
            self.driver.find_element_by_xpath("//input[@id='srp_password']").send_keys(auth.routerPass)
            sleep(5)
            self.driver.find_element_by_xpath("//div[@id='sign-me-in']").click()
            sleep(6)  # //div[@class='span3']
            gateway = self.driver.find_element_by_xpath("//div[@data-id='gateway-modal']").click()
            sleep(6)
            self.driver.find_element_by_xpath("//div[@id='btn-system-reboot']").click()
            sleep(5)
            self.driver.find_element_by_xpath("//div[@id='ok']").click()
            sleep(7 * 30)
            print('OK!! Router rebooted')
            return 'ok'
        except Exception as e:
            print(e)
            return 'bad'

    def tH_escapeSequence(self):
        self.tH_logOut()
        self.tH_resetRouter()
        self.tH_close_browser()

    def tH_addUserto_theLoveDaily(self, user):
        lovedOnes_frame_old = pd.read_csv(self.paths.theDailyLoveCSV)

        new_row = pd.Series([user, 1, datetime.now(), 0])
        row_df = pd.DataFrame([new_row])
        row_df.columns = ['theLoveDaily', 'Post Count', 't_sinceLast', 'PostsPerDay']

        lovedOnes_frame_new = pd.concat([row_df, lovedOnes_frame_old], ignore_index=True)
        lovedOnes_frame_new.to_csv(self.paths.theDailyLoveCSV, index=False, encoding='utf-8')
        log.error('User: {} added to the LoveDaily'.format(user))

    def tH_removeUserFrom_theLoveDaily(self, user):
        lovedOnes_frame_old = pd.read_csv(self.paths.theDailyLoveCSV)
        plop = lovedOnes_frame_old[lovedOnes_frame_old.theLoveDaily == user]
        if plop.theLoveDaily.size > 0:
            lovedOnes_frame_new = lovedOnes_frame_old[lovedOnes_frame_old['theLoveDaily'] != user]
            lovedOnes_frame_new.to_csv(self.paths.theDailyLoveCSV, index=False, encoding='utf-8')
            log.error('No Longer loving {}'.format(user))

    def tH_queueUp_for_theGame(self, alreadyFollowed=False):
        todayStr = datetime.today().strftime(datetimeStringFormat_day)
        inputListOfUsers = pd.read_csv(self.paths.addToTheGame)
        theList1_frame = pd.read_csv(self.paths.theList_1_file)
        theList1_list = theList1_frame["a1_User"].tolist()

        for index, row in inputListOfUsers.iterrows():
            if row['0'] not in theList1_list:
                newRow = ['koperti', row['0'], 666, 'keep', 'keep', 'keep', '', '']
                if row['alreadyFollowed']:
                    newRow[6] = todayStr
                    self.tH_addUserto_theLoveDaily(row['0'])
                theList1_frame_new = HelperBot.addNewRow_toDataFrame(HelperBot, theList1_frame, newRow)
                theList1_frame_new.to_csv(file_paths.theList_1_file, index=False, encoding='utf-8')

    def tH_UpdateCurrentProfileStatsDict(self, user):
        # getProfileStatsDict(target, driver=0, externalSoup=False):
        self.currentProfileStats_dict['user'] = user
        sleep(3)

        # Get posts count
        try:
            element = self.driver.find_elements_by_xpath("//span[@class='g47SY ']")[0]
            posts = element.text.replace(',', '')
        except Exception as e:
            print('No posts! {}'.format(e))
            self.currentProfileStats_dict['Posts'] = noLogin.getProfileStatsDict_Fail(user)['Posts']

        # Get Followers Count
        try:
            element = self.driver.find_elements_by_xpath("//span[@class='g47SY ']")[1]
            followers = element.get_attribute('title').replace(',', '')
        except Exception as e:
            print('No followers! {} '.format(e))
            self.currentProfileStats_dict['Followers'] = noLogin.getProfileStatsDict_Fail(user)['Followers']

        # Get Following Count
        try:
            element = self.driver.find_elements_by_xpath("//span[@class='g47SY ']")[2]
            following = element.text.replace(',', '')
        except Exception as e:
            print('No following! {}'.format(e))
            self.currentProfileStats_dict['Following'] = noLogin.getProfileStatsDict_Fail(user)['Followers']

        # Get bio
        try:
            bioWebElement = self.driver.find_element_by_xpath("//div[@class='-vDIg']")
            bio = bioWebElement.text
        except Exception as e:
            print('No BIO! {}'.format(e))
            self.currentProfileStats_dict['bio'] = noLogin.getProfileStatsDict_Fail(user)['bio']

        self.currentProfileStats_dict['Posts'] = int(posts)
        self.currentProfileStats_dict['Followers'] = int(followers.strip(','))
        self.currentProfileStats_dict['Following'] = int(following.strip(','))
        self.currentProfileStats_dict['bio'] = bio
        sleep(2)
        return self.currentProfileStats_dict

    # Opens the scrolable list of followers or users following for a given profile
    # Performs check for too many actions
    def t0_open_users(self, handle, user_type):
        try:
            self.t0_Open_user_profile(handle)
        except Exception as e:
            print(e)
            return
        if self.tH_checkIfIhit_ActionLimit(self.driver):
            return False

        sleep(3)
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(user_type)).click()
        sleep(2)
        return True

    # Opens the scrolable list of hashtags a profile follows
    # Performs check for too many actions
    def t0_open_HashtagsFollowedBy(self, handle):
        try:
            self.t0_Open_user_profile(handle)
        except Exception as e:
            return
        if self.tH_checkIfIhit_ActionLimit(self.driver):
            return False
        sleep(3)
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format('following')).click()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format('hashtag_following')).click()
        self.helper.sleepForXseconds(self.helper, 40, 40)
        return True

    # Opens the home page of a given profile
    # Performs check for too many actions
    def t0_Open_user_profile(self, userHandle):

        # Mandatory waiting time to make sure we do not hit any limits
        # 200 profile views pre hour = at least 18secs wait
        # previous bounds: 40~45 (14/07/2020)
        self.helper.sleepForXseconds(self.helper, 30, 45)
        nameOnPage = ''

        try:
            self.driver.get('https://www.instagram.com/' + userHandle)
            sleep(2)
        except Exception as e1:
            log.error('Could not navigate 1 to profile page cause \n{}'.format(e1))
            return False

        try:
            nameOnPage = self.driver.find_element_by_xpath(
                "//*[contains(@class,'_7UhW9')]").text
        except Exception as e2:

            if self.tH_checkIfIhit_ActionLimit(self.driver):
                log.error('Action limit hit opening user page for {0}'.format(userHandle))
                sleep(60 * 12)
                try:
                    self.driver.get('https://www.instagram.com/' + userHandle)
                except:
                    log.error('Could not navigate 2 to profile page cause\n{}'.format(e2))
                    return False
            else:
                log.error("It's an error page for {0}\n{1}".format(userHandle, e2))
                return False

        try:
            sleep(1)
            self.tH_UpdateCurrentProfileStatsDict(userHandle)
            if userHandle == self.username:
                self.MyProfile.UpdateDict(self.currentProfileStats_dict)
        except Exception as e3:
            log.error('Did not update current profile dict cause:\n{}'.format(e3))
            return False

        return True

    def t1_getHastags_followed_By_user(self, user):
        if self.t0_open_HashtagsFollowedBy(user):
            return self.__scroll_and_get('hashTags', "//div[@class='_8zyFd']")
        else:
            return [self.tooManyActionsBreakCode]

    def t1_getUser_Following(self, user):
        if self.t0_open_users(user, 'following'):
            return self.__scroll_and_get(targetCount=self.currentProfileStats_dict['Following'])
        else:
            return [self.tooManyActionsBreakCode]

    def t1_getProfiles_N_tags_followed_By_user(self, user):
        try:
            self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format('following')).click()
            sleep(2)
            # following = self.__scroll_and_get()
            self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format('hashtag_following')).click()
            sleep(2)
            hashtags = self.__scroll_and_get('hashTags', "//div[@class='_8zyFd']")
            return hashtags  # [following, hashtags]
        except Exception as e:
            print(e)
            return [self.tooManyActionsBreakCode]

    def t1_getUser_Followers(self, user):
        if self.t0_open_users(user, 'followers'):
            return self.__scroll_and_get(targetCount=self.currentProfileStats_dict['Followers'])
        else:
            return [self.tooManyActionsBreakCode]

    # Scrolls through a list of users following or followers (provided by the t0_open_users function) and draws all
    # handles into a list
    def __scroll_and_get(self, type='users', xpath="//div[@class='isgrP']", targetCount=0):
        xpath.strip("'\'")
        sleep(2)
        users = []
        driver = self.driver
        dialog = driver.find_element_by_xpath("//div[@class='_1XyCr']//..//..//div[contains(@role, 'dialog')]")
        try:
            scroll_box = driver.find_element_by_xpath(xpath)
        except Exception as e:
            print(e)
            return users

        try:
            sugs = driver.find_element_by_xpath("//h4[text()='Suggestions')]")
            driver.execute_script('arguments[0].scrollIntoView()', sugs)
        except Exception as e:
            sleep(1)
        sleep(2)
        last_ht, ht = 0, 1
        names = []
        # make sure you scroll to the end of the list
        scrollCount = 0
        while (len(users) <= 0.95 * targetCount) or scrollCount < 2:
            last_ht, ht = 0, 1
            while last_ht != ht:
                last_ht = ht
                sleep(2)
                dialog = driver.find_element_by_xpath("//div[contains(@role, 'dialog')]")
                currentAtags = dialog.find_elements_by_tag_name('a')
                names = currentAtags

                # names = dialog.find_elements_by_tag_name('a')
                for name in names:
                    try:
                        if type == 'users':
                            if len(name.get_attribute('title')) > 0:
                                users.append(name.get_attribute('title'))
                                users = list(dict.fromkeys(users))
                        else:
                            if '#' in name.text: users.append(name.text)
                    except Exception as e:
                        print(e)
                        continue

                # print('~~scrolling ' + type)
                ht = driver.execute_script(
                    'arguments[0].scrollTo(0, arguments[0].scrollHeight);'
                    'return arguments[0].scrollHeight;',
                    scroll_box)
            scrollCount += 1

        users = list(dict.fromkeys(users))  # remove duplicates
        return list(users)

    def t1_unfollowUser(self, userHandle):
        # TODO add some sort of verification check on the final outcome before returning "OK"
        if not self.t0_Open_user_profile(userHandle):
            return self.tooManyActionsBreakCode
        else:
            unfollowFlag = True
            try:
                self.driver.find_element_by_xpath(
                    "//span[@aria-label='Following']").click()
                sleep(1)
                buttons = self.driver.find_element_by_xpath("//*[contains(@class,'-Cab')]")
                # for some reason if I switch the focus to another window
                # while the unfollow menu is open the unfollow button cannot be pressed
                if 'follow' in buttons.text:
                    buttons.click()
                    log.error('Bye bye ' + userHandle)
                    sleep(2)
                    self.driver.refresh()
                    unfollowFlag = False
                else:
                    log.error('Cannot unfollow ' + userHandle)
                    log.error('Cause ' + buttons.text)
            except Exception as e:
                if unfollowFlag:
                    log.error('Could not unfollow user: ' + userHandle + ' ...oh plus this error {0}'.format(e))
                    return "problem"
            return 'OK'

    def t1_followUser(self, userHandle, zeroPostsOK=False):
        if self.t0_Open_user_profile(userHandle):
            if not zeroPostsOK and (self.currentProfileStats_dict['Posts'] < 2):
                log.error('Too few posts on user {0}, not authorized to follow'.format(userHandle))
                return 'not enough posts'
            else:
                if self.currentProfileStats_dict['Posts'] >= 2:
                    try:
                        self.driver.find_element_by_xpath(
                            "//button[contains(text(),'Follow')]").click()
                        log.error('Hey ' + userHandle + ' ! I hope you will follow back')
                    except Exception as e:
                        log.error('Could not follow user: ' + userHandle)
                        log.error(e)
                    return 'OK'
        else:
            return self.tooManyActionsBreakCode

    def t1_getListOfUsers_thatDontFollowBack(self, handle):
        if self.t0_open_users(handle, 'followers'):
            sleep(2)
            followers = self.__scroll_and_get()
            self.driver.find_element_by_xpath("//button[@type='button']//*[@aria-label='Close']").click()
            sleep(3)
            self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format('following')).click()
            following = self.__scroll_and_get()
        else:
            return [self.tooManyActionsBreakCode]

        if len(followers) < (self.currentProfileStats_dict['Followers'] - 5) or \
                len(following) < (self.currentProfileStats_dict['Following'] - 5):
            return [self.tooManyActionsBreakCode]

        pigs = [x for x in following if x not in followers]
        grandList = [pigs, followers, following]

        return grandList

    def t1_like_photos_under_userName(self, handle, numberOfLikes=3):
        if self.t0_Open_user_profile(handle):
            sleep(2)

            # gathering photos
            pic_hrefs, unique_photos = self.tH_GatherPhoto_hrefs_ToLike(numberOfLikes)

            # Liking photos
            for pic_href in pic_hrefs:
                self.driver.get(pic_href)
                sleep(2)
                unique_photos = self.tH_like_a_photo(handle, pic_href, unique_photos)
            return 'OK'
        else:
            return 'not'
            # return self.tooManyActionsBreakCode

    def tH_like_a_photo(self, handle, pic_href, unique_photos):
        try:
            sleep(randint(2, 6))
            try:
                # If it's a picture
                like_button = self.driver.find_element_by_xpath(
                    "//button[@class='wpO6b ']//*[contains(@aria-label,'ike')]/..")
            except:
                # If it's a video
                like_button = self.driver.find_element_by_xpath(
                    "//button[@class='wpO6b ']//*[contains(@aria-label,'ike')]/..")

            buttonStatus = like_button.find_element_by_class_name('_8-yf5 ').get_attribute('aria-label')
            if buttonStatus == 'Like':
                like_button.click()
                buttonClicked = True
                log.error('~~~~>> {0}: like pressed on {1} | Sleeping'.format(handle, pic_href))

                if buttonClicked:
                    unique_photos -= 1
                    self.helper.sleepForXseconds(self.helper, 2, 6)

            else:
                unique_photos -= 1
        except Exception as e:
            sleep(2)
            log.error("like a photo, for the very first time".format(e))
            log.error('shait')
        return unique_photos

    def tH_GatherPhoto_hrefs_ToLike(self, numberOfLikes=1000):
        pic_hrefs = []
        if numberOfLikes > self.currentProfileStats_dict['Posts']:
            numberOfLikes = self.currentProfileStats_dict['Posts']

        while len(pic_hrefs) < numberOfLikes:
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)

                # get tags
                hrefs_in_view = self.driver.find_elements_by_tag_name('a')

                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]

                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                if len(pic_hrefs) < 1:
                    break
            except Exception:
                continue
        pic_hrefs = pic_hrefs[:numberOfLikes]
        unique_photos = len(pic_hrefs)
        return pic_hrefs, unique_photos

    def t1_get_UserPosting_Velocity(self, user0, numberOfposts=7):

        if self.t0_Open_user_profile(user0):
            hrefs_list = self.tH_GatherPhoto_hrefs_ToLike(numberOfposts)
            postDateTimes = []
            if len(hrefs_list[0]) > 0:
                for href in hrefs_list[0]:
                    post1 = post(href, self.driver, self.__scroll_and_get)
                    postDateTimes.append(post1.datePosted)

            frameOfDates = pd.DataFrame(list(zip(postDateTimes, hrefs_list[0])), columns=['Dates', 'Link'])
            frameOfDates['Dates'] = pd.to_datetime(frameOfDates['Dates'], format='%Y-%m-%dT%H:%M:%S')
            dt = abs(pd.Series(frameOfDates.Dates).diff().dt.days.values) + \
                 abs(pd.Series(frameOfDates.Dates).diff().dt.components.hours.values / 24)
            dt = dt[pd.np.logical_not(pd.np.isnan(dt))]

            return (numberOfposts / pd.np.percentile(dt, 66))
        else:
            return 0
            # return self.tooManyActionsBreakCode

    def tH_getHashtagFollowership_embededInList2(self, user, hashList):
        # read input/outputFiles from disk
        old_frame = pd.read_csv(file_paths.hashtagFollowershipStatsCSV)
        outPutFrame = old_frame

        rowToAppend_list = []
        rowToAppend_list.append(user)
        rowToAppend_list.append(len(hashList))
        if len(hashList) > 0:
            for tag in hashList:
                rowToAppend_list.append(tag)

        try:
            outPutFrame = self.helper.addNewRow_toDataFrame(self.helper, outPutFrame, rowToAppend_list)
        except Exception as e:
            log.error('Point E_CocoNut: Could not update frame for user {0} because: {1}'.format(user, e))
            print('Point E_CocoNut: Could not update frame for user {0} because: {1}'.format(user, e))
            return

        outPutFrame.to_csv(file_paths.hashtagFollowershipStatsCSV, index=False, encoding='utf-8')

    def t2_getHashtagFollowership(self, numberOfProfilesToProcess=3):
        # read input/outputFiles from disk
        targetUsersDB = pd.read_csv(file_paths.theList_0_file)
        old_frame = pd.read_csv(file_paths.hashtagFollowershipStatsCSV)
        outPutFrame = old_frame

        # remove already examined users from the process
        usersAlreadyExamined = old_frame['a_User'].tolist()
        usersAlreadyExamined = list(dict.fromkeys(usersAlreadyExamined))  # Remove duplicates

        targetUsers_List = targetUsersDB['a1_User'].tolist()
        targetUsers_List = [x for x in targetUsers_List if x not in usersAlreadyExamined]
        targetUsers_List = list(dict.fromkeys(targetUsers_List))  # Remove duplicates

        random.shuffle(targetUsers_List)
        targetUsers_List = targetUsers_List[:numberOfProfilesToProcess]

        for user in targetUsers_List:
            try:
                hashList = self.t1_getHastags_followed_By_user(user)
            except:
                log.error('Point Mango: Could not get hashtags user {0} follows'.format(user))
                print('Point Mango: Could not get hashtags user {0} follows'.format(user))
                continue

            # Check if we have hit Instagrams Action limit and are getting error pages only
            if self.tooManyActionsBreakCode in hashList:
                log.error('GET #tag Followership: Too many Actions Hit')
                sleep(60 * 4)
                # return self.tooManyActionsBreakCode

            rowToAppend_list = []
            rowToAppend_list.append(user)
            rowToAppend_list.append(len(hashList))
            if len(hashList) > 0:
                for tag in hashList:
                    rowToAppend_list.append(tag)

            try:
                outPutFrame = self.helper.addNewRow_toDataFrame(self.helper, outPutFrame, rowToAppend_list)
            except Exception as e:
                log.error('Point CocoNut: Could not update frame for user {0} because: {1}'.format(user, e))
                print('Point CocoNut: Could not update frame for user {0} because: {1}'.format(user, e))
                continue

        outPutFrame.to_csv(file_paths.hashtagFollowershipStatsCSV, index=False, encoding='utf-8')
        return 'OK'

    def t2_getMyStats(self, type):
        if type == 'Followers':
            try:
                myFollowers_list = self.t1_getUser_Followers(self.username)

                # Check if we have hit Instagrams Action limit and are getting error pages only
                if self.tooManyActionsBreakCode in myFollowers_list:
                    log.error('GET MY FOLLOWERS: Too many Actions Hit')
                    sleep(60 * 4)
                    # return self.tooManyActionsBreakCode

                myFollowers_frame = pd.DataFrame(myFollowers_list)
                myFollowers_frame.columns = ['Followers']
                myFollowers_frame.to_csv(file_paths.myStats_FolowersCSV, index=False, encoding='utf-8')
            except Exception as e:
                log.error('Could not get My Followers because: {}'.format(e))
        else:
            try:
                myFollowing_list = self.t1_getUser_Following(self.username)

                # Check if we have hit Instagrams Action limit and are getting error pages only
                if self.tooManyActionsBreakCode in myFollowing_list:
                    log.error('GET MY FOLLOWING: Too many Actions Hit')
                    sleep(60 * 4)
                    # return self.tooManyActionsBreakCode

                myFollowing_frame = pd.DataFrame(myFollowing_list)
                myFollowing_frame.columns = ['Following']
                myFollowing_frame.to_csv(file_paths.myStats_FollowingCSV, index=False, encoding='utf-8')
            except Exception as e:
                log.error('Could not get My Following because: {}'.format(e))

        return 'OK'

    def t2_getList_0(self, numberOfProfilesToProcess=3):
        # Get TheList_0: A list of all people following a number of profiles
        ppath = self.paths.theList_1_file
        # self.paths.theList_1_file
        # The above path is only for testing new method - remember to switch back to final
        old_frame = pd.read_csv(ppath)

        # If the name of the source user is already there do not re-examine
        sourceUsersAlreadyExamined = old_frame[old_frame.columns[0]].tolist()
        sourceUsersAlreadyExamined = list(dict.fromkeys(sourceUsersAlreadyExamined))  # Remove duplicates

        # If a source user's follower is already in the list we need not add a duplicate
        usersAlreadyInList = old_frame[old_frame.columns[1]].tolist()
        usersAlreadyInList = list(dict.fromkeys(usersAlreadyInList))  # Remove duplicates

        # Get a list of target source users
        targetuserInput = HelperBot.findAlltxtFiles_pathsToList(file_paths.targetuserInput)
        targetuserInputPyList = []
        for file in targetuserInput:
            for line in HelperBot.readLinesFromTXTFile(file):
                targetuserInputPyList.append(line)

        targetuserInputPyList = list(dict.fromkeys(targetuserInputPyList))  # Remove duplicates
        l3 = [x for x in targetuserInputPyList if
              x not in sourceUsersAlreadyExamined]  # Remove source users already examined
        # random.shuffle(l3)

        log.error('{0} users remaining'.format(len(l3)))
        if len(l3) > 0:
            targetuserInputPyList = l3[:numberOfProfilesToProcess]

            for user in targetuserInputPyList:
                log.error('Updating the List 0 for user: {0}'.format(user))
                try:
                    followers_ = self.t1_getUser_Followers(user)

                    # Check if we have hit Instagrams Action limit and are getting error pages only
                    if self.tooManyActionsBreakCode in followers_:
                        sleep(60 * 4)
                        return self.tooManyActionsBreakCode

                    for follower in followers_:
                        try:
                            if follower not in usersAlreadyInList:
                                newFrameRow = {self.list_columnHeaders[0]: user,
                                               self.list_columnHeaders[1]: follower,
                                               self.list_columnHeaders[2]: '',
                                               self.list_columnHeaders[3]: '',
                                               self.list_columnHeaders[4]: '',
                                               self.list_columnHeaders[5]: '',
                                               self.list_columnHeaders[6]: '',
                                               self.list_columnHeaders[7]: ''}
                                # append row to the dataframe
                                old_frame = old_frame.append(newFrameRow, ignore_index=True)
                        except TypeError as e:
                            print(e)
                            continue

                    old_frame.to_csv(ppath, index=False, encoding='utf-8')
                    # If a source user's follower is already in the list we need not add a duplicate
                    usersAlreadyInList = old_frame[old_frame.columns[1]].tolist()
                    usersAlreadyInList = list(dict.fromkeys(usersAlreadyInList))  # Remove duplicates
                except TypeError as e:
                    log.error('The List 0 on user {0}, got: {1}'.format(user, e))
                    continue
        else:
            log.error('No New users to examine for the list 0')

        return 'OK'

    def t2_getList_1(self, processStep=4):
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

    def t2_getList_2(self, user, theList_1_frame):
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

    def t2_theGame(self, processStep=5):
        howManyDaysBeforeI_unfollow = 10
        howManyDaysBeforeI_unlove = 4
        dateList = []
        for i in range(0, 21):
            dateList.append((datetime.today() - timedelta(days=i)).strftime(datetimeStringFormat_day))
            # if this date formating changes we are screwed. If so make sure to change it across the board

        # read input/output file
        theList_1_frame = pd.read_csv(file_paths.theList_1_file)  # , dtype=self.list_column_dTypes
        theList_1_frame.columns = self.list_columnHeaders

        # Get List of users to follow
        optimalFutureFollowers_frame = theList_1_frame[theList_1_frame[self.list_columnHeaders[5]] == 'keep']
        optimalFutureFollowers_frame = optimalFutureFollowers_frame[optimalFutureFollowers_frame.iloc[:, 6].isnull()]
        optimalFutureFollowers = optimalFutureFollowers_frame.iloc[:, 1].tolist()

        futureFollowers_frame = theList_1_frame[theList_1_frame[self.list_columnHeaders[4]] == 'keep']
        futureFollowers_frame = futureFollowers_frame[futureFollowers_frame.iloc[:, 6].isnull()]
        futureFollowers = futureFollowers_frame.iloc[:, 1].tolist()

        l3 = [x for x in futureFollowers if x not in optimalFutureFollowers]
        futureFollowers = l3

        # Check if it is time to unfollow anyone yet
        # rows with no dates will not be included in the frame filtering below
        usersToUnfollow_frame = theList_1_frame[(theList_1_frame.iloc[:, 6] < dateList[howManyDaysBeforeI_unfollow])]
        usersToUnfollow_frame = usersToUnfollow_frame[usersToUnfollow_frame.iloc[:, 7].isnull()]
        usersToUnfollow_list = usersToUnfollow_frame.iloc[:, 1].tolist()

        if len(usersToUnfollow_list) > 0:
            log.error(
                '{0} users to stop following. They are: {1}'.format(len(usersToUnfollow_list),
                                                                    usersToUnfollow_list[:len(usersToUnfollow_list)]))

        for user in usersToUnfollow_list:
            rowIndexOfUser = theList_1_frame[theList_1_frame.a1_User == user].index.values[0]
            try:
                unfollowed = self.t1_unfollowUser(user)

                # Check if we have hit Instagrams Action limit and are getting error pages only
                if self.tooManyActionsBreakCode in unfollowed:
                    sleep(60 * 4)
                    # return self.tooManyActionsBreakCode

                # log.error('t2_theGame: Bye bye {0}! sorry about that'.format(user))
            except Exception as e:
                continue

            if 'OK' in unfollowed:
                theList_1_frame.iloc[rowIndexOfUser, 7] = dateList[0]  # Mark the date you unfollowed
                theList_1_frame.to_csv(file_paths.theList_1_file, index=False, encoding='utf-8')
            self.helper.sleepForXseconds(self.helper, (60 * 0.5), (60 * 1), 0.5, True)

        # Check if it is time to remove someone from the love daily (a week after I have unfollowed)
        usersToStopLoving_frame = theList_1_frame[theList_1_frame.iloc[:, 7] < dateList[howManyDaysBeforeI_unlove]]
        usersToStopLoving_list = usersToStopLoving_frame.iloc[:, 1].tolist()

        for user in usersToStopLoving_list:
            try:
                self.tH_removeUserFrom_theLoveDaily(user)
            except:
                continue

        # Determine what is the maximum number of users you can follow before you hit the 2:1 ratio
        if self.t0_Open_user_profile(self.username):
            followsLeftUntil_1over2_Ratio = int(self.currentProfileStats_dict['Followers'] * 2 - \
                                                self.currentProfileStats_dict['Following'])
            log.error('{0} users left before 2:1 ratio reached'.format(str(followsLeftUntil_1over2_Ratio)))

        # Start Following people add them to the love daily etc
        maxFollowsPerDay = processStep

        if len(optimalFutureFollowers) > 0:
            log.error(
                '{0} on the list of optimal. The first {1} are: {2}'.format(len(optimalFutureFollowers),
                                                                            processStep,
                                                                            optimalFutureFollowers[:(processStep + 1)]))

        for user in optimalFutureFollowers:
            if maxFollowsPerDay > 0:
                log.error('Will try to follow: {0}'.format(user))
                rowIndexOfUser = theList_1_frame[theList_1_frame.a1_User == user].index.values[0]
                try:
                    followed = self.t1_followUser(user)

                    # Check if we have hit Instagrams Action limit and are getting error pages only
                    if not 'OK' in followed:
                        continue
                except:
                    continue

                theList_1_frame.iloc[rowIndexOfUser, 6] = dateList[0]  # Mark the date you followed
                theList_1_frame.to_csv(file_paths.theList_1_file, index=False, encoding='utf-8')
                log.error('Ok user ~|| {0} ||~ folowed, now adding to LoveDaily'.format(user))
                self.tH_addUserto_theLoveDaily(user)
                maxFollowsPerDay -= 1
                self.helper.sleepForXseconds(self.helper, (60 * 0.3), (60 * 0.75), 0.5, True)

        if len(futureFollowers) > 0:
            log.error(
                '{0} on the list of regular. The first {1} are: {2}'.format(len(futureFollowers),
                                                                            maxFollowsPerDay,
                                                                            futureFollowers[:(maxFollowsPerDay)]))
        for user in futureFollowers:
            if maxFollowsPerDay > 0:
                rowIndexOfUser = theList_1_frame[theList_1_frame.a1_User == user].index.values[0]
                log.error('Will try to follow: {0}'.format(user))
                try:
                    followed = self.t1_followUser(user)

                    # Check if we have hit Instagrams Action limit and are getting error pages only
                    if self.tooManyActionsBreakCode in followed:
                        sleep(6 * 4)
                        # return self.tooManyActionsBreakCode
                    if not 'OK' in followed:
                        continue
                except:
                    log.error('Could not follow: {0}'.format(user))
                    continue

                theList_1_frame.iloc[rowIndexOfUser, 6] = dateList[0]  # Mark the date you followed
                theList_1_frame.to_csv(file_paths.theList_1_file, index=False, encoding='utf-8')
                log.error('Ok user ~|| {0} ||~ folowed, now adding to LoveDaily'.format(user))
                self.tH_addUserto_theLoveDaily(user)
                maxFollowsPerDay -= 1
                self.helper.sleepForXseconds(self.helper, (60 * 0.5), (60 * 0.75), 0.5, True)

        return 'OK'

    def t2_purgeUsers(self):
        users = pd.read_csv(self.paths.unfollowListCSV)
        users_list = users['unfollow'].tolist()
        users_list = list(dict.fromkeys(users_list))  # remove duplicates

        for scumuser in users_list:
            try:
                unfollowed = self.t1_unfollowUser(scumuser)

                # Check if we have hit Instagrams Action limit and are getting error pages only
                if self.tooManyActionsBreakCode in unfollowed:
                    sleep(60 * 4)
                    # return self.tooManyActionsBreakCode

            except Exception as e:
                log.error('Scum puerger: {0}'.format(e))
                continue
            try:
                self.tH_removeUserFrom_theLoveDaily(scumuser)
            except Exception as e:
                log.error('purged but maybe not in love daily\ncouldbebecause: {}'.format(e))
                continue

        return 'OK'

    def t2_theLoveDaily(self, numberOflikes=2, listFile=file_paths.theDailyLoveCSV, percentageOfUsers=1):
        # 'Like' everyone's latest N posts
        log.error('\n\n~~~ The Love Daily commences ! ~~~\n\n')

        # Sorted by date last checked
        # Least recently checked profiles come first
        lovedOnes_frame = pd.read_csv(listFile)
        lovedOnes_frame.t_sinceLast = pd.to_datetime(lovedOnes_frame.t_sinceLast)
        lovedOnes_frame = lovedOnes_frame.sort_values(by='t_sinceLast', ascending=True)
        lovedOnes_frame = lovedOnes_frame.reset_index(drop=True)

        # This is what it's all about:
        # Send some love to the users that have new posts
        sleep(2)
        failCounter = 0
        printMark = 0.0
        loveTotal = lovedOnes_frame['theLoveDaily'].count()
        loveCount = loveTotal
        loveTotal_dataIntegrityCheck = lovedOnes_frame['theLoveDaily'].tolist()
        loveTotal_dataIntegrityCheck = list(dict.fromkeys(loveTotal_dataIntegrityCheck))
        if loveTotal != len(loveTotal_dataIntegrityCheck):
            diff = int(abs(loveTotal - loveTotal_dataIntegrityCheck))
            log.error('~~~ Missmatch of love counts: {0} users may be duplicates'.format(str(diff)))
            return self.tooManyActionsBreakCode

        log.error('~~~ {0} users to love'.format(loveTotal))

        for index, row in lovedOnes_frame.iterrows():
            loveCount -= 1
            if (loveTotal - loveCount) > (loveTotal * percentageOfUsers):
                break

            completionrate = round(100 * (1 - (loveCount / loveTotal)), 1)
            if completionrate > printMark:
                log.error('~~~~~~~ {0} % Done || {1}/{2} users'.format(printMark, loveCount, loveTotal))
                printMark += 5

            try:
                try:
                    # is this good enough? do I need to convert again? Is it not already a date time object?
                    lastCheck_Time = row['t_sinceLast']
                    now_DateTime = datetime.now()

                    # Convert to Unix timestamp
                    d1_ts = time.mktime(lastCheck_Time.timetuple())
                    d2_ts = time.mktime(now_DateTime.timetuple())

                    deltaT = int(d2_ts - d1_ts) / 60 / 60
                    print('{0}:  {1} hours since last checked on {2} with {3} posts on record'.format(
                        datetime.today(), str(round(deltaT, 2)),
                        row['theLoveDaily'],
                        row["Post Count"]))
                    # Skip user if it has been less than X hours since we last checked
                    if deltaT <= 13:
                        continue
                except Exception as e:
                    log.error('no time yet on {0}'.format(e))

                # Navigate to user's profile
                if self.t0_Open_user_profile(row['theLoveDaily']):
                    ## Get fresh count from Instagram
                    stats = self.currentProfileStats_dict

                    # Check if we have new post since last time
                    # Move to next user if there are no new posts since last check
                    if row["Post Count"] >= stats['Posts']:
                        lovedOnes_frame.iloc[index, 1] = stats['Posts']
                        lovedOnes_frame.iloc[index, 2] = datetime.now()  # t_sinceLast
                        lovedOnes_frame.to_csv(listFile, index=False, encoding='utf-8')
                        self.helper.sleepForXseconds(self.helper, 7, 19)
                        continue

                    # Adjust number of likes to just new posts
                    if int(stats['Posts'] - row["Post Count"]) < numberOflikes:
                        numberOflikes = int(stats['Posts'] - row["Post Count"])

                    # gathering photos
                    pic_hrefs, unique_photos = self.tH_GatherPhoto_hrefs_ToLike(numberOflikes)

                    # Liking photos
                    for pic_href in pic_hrefs:
                        self.driver.get(pic_href)
                        sleep(2)
                        unique_photos = self.tH_like_a_photo(row['theLoveDaily'], pic_href, unique_photos)

                    lovedOnes_frame.iloc[index, 1] = stats['Posts']
                    lovedOnes_frame.iloc[index, 2] = datetime.now()  # record new time
                    lovedOnes_frame.to_csv(listFile, index=False, encoding='utf-8')
                else:
                    failCounter += 1
                    fail_ratio = 100 * round(failCounter / loveTotal)
                    log.error('love died on {0}'.format(row['theLoveDaily']))
                    log.error('Current fail levels at {0}'.format(str(fail_ratio)))

                    if fail_ratio > 0.025:
                        log.error('Love has ended suddenly: too Many actions in fail counter {}'.format(
                            row['theLoveDaily']))
                        return self.tooManyActionsBreakCode

                    continue
            except Exception as e:
                log.error('This love is a great one: {0}'.format(e))
                continue

        log.error('\n\n~~~ The Love Daily has ended ! ~~~\n\n')
        return 'OK'

    def t2_fansOnly(self, numberOfposts=3, user0=None):
        if user0 is None:
            user0 = self.username

        if self.t0_Open_user_profile(user0):
            hrefs_list = self.tH_GatherPhoto_hrefs_ToLike(numberOfposts)
            postLikedBy = []
            if len(hrefs_list[0]) > 0:
                for href in hrefs_list[0]:
                    post1 = post(href, self.driver, self.__scroll_and_get)
                    post1.updateUsers_liked_post_andCount()
                    if len(post1.usersThatLiked) > 0:
                        postLikedBy.append(post1.usersThatLiked)

                myFollowers = self.t1_getUser_Followers(self.username)
                postLikedBy_flat = [item for sublist in postLikedBy for item in sublist]
                counterDict = Counter(postLikedBy_flat)
                fans = pd.DataFrame(columns=['User', 'TotalLikes', 'LikesPerPost', 'IsAFollower'])
                for user0 in list(counterDict):
                    fans_line = []
                    fans_line.append(user0)
                    fans_line.append(counterDict[user0])
                    fans_line.append(counterDict[user0] / len(postLikedBy))
                    if user0 in myFollowers:
                        fans_line.append('Yes')
                    else:
                        fans_line.append('No')
                    fans = self.helper.addNewRow_toDataFrame(self.helper, fans, fans_line)

                fans.to_csv(self.paths.fansOnly, index=False, encoding='utf-8')
