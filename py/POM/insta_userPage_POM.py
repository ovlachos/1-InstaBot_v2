import time
from datetime import datetime
import random
from random import randint

from selenium.webdriver.common.keys import Keys
from time import sleep
import auth

xpaths = {
    'likeLimitMessage_Text': "//div[contains(text(),'community')]",
    'likeLimitMessage_ReportButton': "//button[contains(text(),'Report a Problem')]",
    'likeLimitMessage_OKButton': "//button[contains(text(),'OK')]",
}


class userPage_base:

    def __init__(self, webPage, user):
        self.page = webPage
        self.driver = self.page.driver
        self.userName = user

        self.followAccess = 0
        self.infoAccess = 0
        self.determineLevelOfFollowAccess()
        self.determineLevelOfInfoAccess()
        # self.printProfileTypeDescription()

        if self.iAmInAUserPage():
            self.altName = self.getAltname()
            self.bio = self.getBio()
            self.stats = self.getStats_dict()

    def updateUserName(self):
        self.userName = self.page.getPageElement_tryHard("//header//h2").text

    def getAltname(self):
        try:
            return self.page.getPageElement_tryHard("//h1[@class='rhpdm']").text
        except Exception as e:
            # print("No altname cause: {}".format(e))
            return ''

    def getPageElement_tryHard1(self, xpath):
        pass

    def getAlternativeUserName(self):
        return self.page.getPageElement_tryHard("//header//div[@class='-vDIg']//h1").text

    def getBio(self):
        bioText = ''
        try:
            bio = self.driver.find_elements_by_xpath("//header//div[@class='-vDIg']//span")
            for line in bio:
                bioText += line.text
        except Exception as e:
            print("No bio cause: {}".format(e))

        return bioText

    def iAmInAUserPage(self):
        if self.userName in self.page.whichPageAmI():
            return True
        else:
            return False

    def determineLevelOfFollowAccess(self):

        # Follow Access:
        # 0  -  A: It is me
        # 20 -  B: It's someone I'm following currently
        # 40 -  C: It's someone I've requested to follow (and they have not yet replied)
        # 60 -  D: It's someone I do not follow
        # 70 -  E: It's someone I unfollowed and he still follows
        # 80 -  F: It's someone I unfollowed but he did NOT follow back

        sleep(1)
        self.followAccess = 0
        if self.userName == auth.username:
            return
        else:
            self.followAccess += 20  # @20

        # Ok so it is NOT me.
        # One step further away from me are people I am following. Check for that
        try:
            # @20
            self.driver.find_element_by_xpath("//header//section//span[@aria-label='Following']")
            return
        except Exception as e:
            self.followAccess += 20  # @40

        # Ok so it is NOT someone I am following.
        # One step further away from me are people I have requested to follow. Check for that
        try:
            # @40
            self.driver.find_element_by_xpath("//div[@class='nZSzR']//button[contains(text(),'Requested')]")
            return
        except Exception as e:
            self.followAccess += 20  # @60

        # If we get to this point it turns out to be someone I am not following at all,
        # and neither have requested to follow. Do THEY follow me though?
        try:
            # @60
            self.driver.find_element_by_xpath("//div[@class='nZSzR']//button[contains(text(),'Follow Back')]")
            return
        except Exception as e:
            self.followAccess += 10  # @70

        try:
            # @70
            self.driver.find_element_by_xpath("//div[@class='nZSzR']//button[contains(text(),'Follow')]")
            return
        except Exception as e:
            self.followAccess += 10  # @80

        # but it could also be an error page. Let's check
        try:
            self.driver.find_element_by_xpath("//h2[contains(text(),'Sorry')]")
            self.followAccess = 100
            self.infoAccess = 100
        except Exception as e:
            pass

    def determineLevelOfInfoAccess(self):

        # Info/lists Access:
        # 0  - 01: It is me
        # 25 - 02: It is an open profile. I have access to info/lists/posts
        # 50 - 03: It is a private profile. Limited access

        self.infoAccess = 0
        sleep(1)
        if self.userName == auth.username:
            return
        else:
            self.infoAccess += 25  # @25

        # If it's not me it could either be an open or private profile. Let us check for that.
        try:
            self.driver.find_element_by_xpath("//h2[contains(text(),'Private')]")
            self.infoAccess += 25  # @50
        except Exception as e:
            pass
            # self.infoAccess = 100

    def get_profileTypeDescription(self):
        # phrased so that it fits in 'This user BLAH ...'
        descriptionInfoAccess = {
            '0': 'full access since this is myself! good job finding me :P',
            '25': 'full access',
            '50': 'limited access to just the basics',
            '100': 'no access. Is this an error page?',
        }

        descriptionFollowAccess = {
            '0': 'cannot follow myself i.e.',
            '20': 'am already following',
            '40': 'have requested to follow',
            '60': 'am not following, but I am being followed by',
            '70': 'am not following',
            '100': 'no access. Is this an error page?',
        }
        return f"I {descriptionFollowAccess[str(self.followAccess)]} user {self.userName} and I have {descriptionInfoAccess[str(self.infoAccess)]}"  # description[str(self.type)]

    def printProfileTypeDescription(self):
        print('~~> {0}'.format(self.get_profileTypeDescription()))

    def getStats_dict(self):
        stats = {
            'posts': 0,
            'followers': 0,
            'following': 0
        }

        try:
            allItems = self.driver.find_elements_by_xpath("//header//ul//span[@class='g47SY ']")

            if len(allItems) >= 3:
                stats['posts'] = int(allItems[0].text.replace(',', ''))
                stats['followers'] = int(allItems[1].get_attribute("title").replace(',', ''))
                stats['following'] = int(allItems[2].text.replace(',', ''))
        except Exception as ex:
            print(ex)

        return stats


class userPage(userPage_base):
    def getFollowersList(self):

        if self.infoAccess < 45:
            try:
                sleep(3)
                self.page.getPageElement_tryHard("//a[contains(@href,'/{}')]".format('followers')).click()
                sleep(2)
                followersList = self.__scroll_and_get_limitedTo1200(targetCount=self.stats['followers'])
                self.page.getPageElement_tryHard("//button[@class='wpO6b ']//*[@aria-label='Close']").click()
                return followersList
            except Exception as e:
                print(e)
                return []
        else:
            print('nahh - no followers access for this user because:')
            self.printProfileTypeDescription()

    def getFollowingList(self):

        if self.infoAccess < 45:
            try:
                sleep(3)
                self.page.getPageElement_tryHard("//a[contains(@href,'/{}')]".format('following')).click()
                sleep(2)
                followingList = self.__scroll_and_get_limitedTo1200(targetCount=self.stats['following'])
                self.page.getPageElement_tryHard("//button[@class='wpO6b ']//*[@aria-label='Close']").click()
                return followingList
            except Exception as e:
                print(e)
                return []
        else:
            print('nahh - no following access for this user because:')
            self.printProfileTypeDescription()

    def getHashtagsFollowingList(self):

        if self.infoAccess < 45:
            sleep(3)
            try:
                self.page.getPageElement_tryHard("//a[contains(@href,'/{}')]".format('following')).click()
                sleep(2)
                self.page.getPageElement_tryHard("//a[contains(@href,'/{}')]".format('hashtag_following')).click()
                sleep(2)
                hashtagList = self.__scroll_and_get_limitedTo1200('hashTags', "//div[@class='_8zyFd']")
                self.driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
                self.page.getPageElement_tryHard("//div[@class='QBdPU ']//*[@aria-label='Close']").click()
                return hashtagList
            except Exception as e:
                print('{} . Returning an empty hashtag list'.format(e))
                return []
        else:
            print('nahh - no hashtag access for this user because:')
            self.printProfileTypeDescription()

    def navigateTo_X_latestPost(self, numberX):
        from POM import insta_post as post
        # numberX runs from 0 to whatever
        if self.infoAccess < 45:
            try:
                # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                posts = self.driver.find_elements_by_xpath("//a[contains(@href,'/p/')]")
                if len(posts) > 0 and len(posts) > numberX:
                    self.driver.execute_script("arguments[0].scrollIntoView();", posts[numberX])
                    self.driver.execute_script("arguments[0].click();", posts[numberX])
            except Exception as e:
                print(e)
                print('Opening post number {} failed'.format(numberX))
            return post.Post(self.page)
        else:
            print('nahh cannot navigate to a post because:')
            self.printProfileTypeDescription()

    def follow(self):

        self.determineLevelOfFollowAccess()
        if self.followAccess > 45:
            try:
                self.page.getPageElement_tryHard(
                    "//button[contains(text(),'Follow')]").click()

                self.actionsLimitHit()

            except Exception as e:
                print('Cannot find the follow button')

            sleep(2)
            self.determineLevelOfFollowAccess()

            if self.followAccess < 45:
                print('OK followed {}'.format(self.userName))
                return 'OK'
            else:
                return 'fail'
        else:
            print('nahh - no follow access for this user because:')
            self.printProfileTypeDescription()
            return 'OK'

    def unfollow(self):

        self.determineLevelOfFollowAccess()
        if 45 > self.followAccess > 5:
            if self.followAccess < 25:
                # if following
                self.page.getPageElement_tryHard("//span[@aria-label='Following']").click()
                sleep(1)
                buttons = self.page.getPageElement_tryHard("//*[contains(@class,'-Cab')]")
                if 'follow' in buttons.text:
                    buttons.click()
                    sleep(2)

                    self.actionsLimitHit()

                    self.driver.refresh()
            else:
                # if requested
                self.page.getPageElement_tryHard("//button[contains(text(),'Requested')]").click()
                sleep(1)
                buttons = self.page.getPageElement_tryHard("//*[contains(@class,'-Cab')]")
                if 'follow' in buttons.text:
                    buttons.click()
                    sleep(2)

                    self.actionsLimitHit()

                    self.driver.refresh()

            self.determineLevelOfFollowAccess()
            self.printProfileTypeDescription()
            if self.followAccess > 45:
                print('OK UNfollowed {}'.format(self.userName))
                return 'OK'
            else:
                return 'fail'
        else:
            print('nahh - no unfollow access for this user because:')
            self.printProfileTypeDescription()
            return 'OK'

    def actionsLimitHit(self):
        if self.checkForLikeLimitMessage():
            self.escapeFromLikeLimitMessage(bool(random.getrandbits(1)))
            print('### Too many Actions message ###')
            sleep(randint(4, 10))

    def checkForLikeLimitMessage(self):
        try:
            likeLimitMessage = self.driver.find_elements_by_xpath(xpaths['likeLimitMessage_Text'])
            if likeLimitMessage:
                return True
            else:
                return False
        except Exception as e:
            return False

    def escapeFromLikeLimitMessage(self, isitok=True):
        okButton = self.page.getPageElement_tryHard(xpaths['likeLimitMessage_OKButton'])
        reportAProblemButton = self.page.getPageElement_tryHard(xpaths['likeLimitMessage_ReportButton'])

        buttonToClick = reportAProblemButton
        if isitok: buttonToClick = okButton

        if buttonToClick:
            self.driver.execute_script("arguments[0].click();", buttonToClick)
            if self.checkForLikeLimitMessage():
                self.escapeFromLikeLimitMessage()
            else:
                return True

    def __scroll_and_get_limitedTo1200(self, itemType='users', xpath="//div[@class='isgrP']", targetCount=10):

        if targetCount > 1200:
            targetCount = 1200

        xpath.strip("'\'")
        scrollCount = 0
        s = 0
        sleepTimeBetweenScrolls = 2
        maxTimeDeltaAllowed = 1.05 * sleepTimeBetweenScrolls * targetCount / 10
        outputList = []

        sleep(1)

        try:
            scroll_box = self.page.getPageElement_tryHard(xpath)
        except Exception as e:
            print(e)
            return outputList

        print(f'Max time allowed for scrolling  is {maxTimeDeltaAllowed}s')
        startTime = datetime.now()

        while scrollCount < 10:
            last_ht, ht = 0, 1
            while last_ht != ht:
                last_ht = ht

                sleep(sleepTimeBetweenScrolls)

                s += 12
                delta = int(time.mktime(datetime.now().timetuple()) - time.mktime(startTime.timetuple()))
                # print(f"{datetime.now()}:: ht is {ht} items are approx {s} || delta is: {delta}")

                ##### BREAKER OF TIME DELTA
                if delta > maxTimeDeltaAllowed:
                    # print(f'Scroll Count is {scrollCount} delta is {delta}s, which is greater than {maxTimeDeltaAllowed}s')
                    break

                try:
                    ht = self.driver.execute_script(
                        'arguments[0].scrollTo(0, arguments[0].scrollHeight);'
                        'return arguments[0].scrollHeight;',
                        scroll_box)
                except Exception as e:
                    scrollCount = 666
                    # print(f'scrollCount is {scrollCount} by some scrolling error')
                    break

            # print(f"### {datetime.now()}:: Output has approx {s} items || delta is: {delta}\t {scrollCount}")

            scrollCount += 1

        # Out of the Wile loops
        try:
            if itemType == 'users':
                names = self.page.driver.find_elements_by_xpath("//a[@class='FPmhX notranslate  _0imsa ']")
                outputList = list(map(self.page.getTitleAttributeFromWebElement, names))
                print(f"~~~### {datetime.now()}:: Output has {len(outputList)} users out of the expected {targetCount} || delta is: {delta}")
            else:
                tags = self.page.driver.find_elements_by_xpath("//a[@class='hI7cq  xil3i']")
                outputList = list(map(self.page.getTextFromWebElement, tags))
                print(f"~~~### {datetime.now()}:: Output has {len(outputList)} #tags || delta is: {delta}")
        except Exception as e:
            print(e)

        outputList = list(dict.fromkeys(outputList))  # remove duplicates
        return list(outputList)
