from random import randint
import random
from time import sleep

xpaths = {
    'likeButton': "//button[@class='wpO6b  ']//*[contains(@aria-label,'ike')]/..",
    'closePostButton': "//*[@aria-label='Close']",
    'locationElements': "//a[contains(@href,'/explore/locations')]",
    'postDateTime': "//time[@class='_1o9PC Nzb55']",
    'commentElements': "//a[@class='sqdOP yWX7d     _8A5w5   ZIAjV ']",
    'likeLimitMessage_Text': "//div[contains(text(),'community')]",
    'likeLimitMessage_ReportButton': "//button[contains(text(),'Report a Problem')]",
    'likeLimitMessage_OKButton': "//button[contains(text(),'OK')]",
}


class Post:

    def __init__(self, webPage):
        self.page = webPage
        self.driver = self.page.driver
        self.location = ""
        self.datePosted = ""
        self.usersCommented = []

    def like_post(self):
        try:
            sleep(randint(2, 4))
            like_button = None
            try:
                # If it's a picture or
                like_button = self.page.getPageElement_tryHard(xpaths['likeButton'])
            except Exception as e:
                print(e)
                print('Could not find like button!')

            buttonStatus = like_button.find_element_by_class_name('_8-yf5 ').get_attribute('aria-label')
            if buttonStatus == 'Like':
                self.driver.execute_script("arguments[0].click();", like_button)

                sleep(2)

                if self.checkForLikeLimitMessage():
                    self.escapeFromLikeLimitMessage(bool(random.getrandbits(1)))
                    print('### Too many Likes message ###')
                    sleep(randint(4, 10))
                    return 'busted'

                return True

            return False
        except Exception as e:
            print(e)
            sleep(2)

    def close_post(self):
        try:
            sleep(1)
            self.page.getPageElement_tryHard(xpaths['closePostButton']).click()
        except Exception as e:
            print(e)

    def getListOfUsersWhoLiked(self):
        outList = []
        return outList

    def updatePostLocation(self):
        try:
            loc_elements = self.driver.find_elements_by_xpath(xpaths['locationElements'])
            self.location = loc_elements[0].text
            if len(loc_elements) > 1:
                self.location = loc_elements[1].text
        except Exception as e:
            print(e)

    def updatePostDateTime(self):
        try:
            dateElement = self.page.getPageElement_tryHard(xpaths['postDateTime'])
            self.datePosted = dateElement.get_attribute('datetime')
        except Exception as e:
            print(e)

    def updateUsers_commented_underPost(self):
        try:
            elements = self.driver.find_elements_by_xpath(xpaths['commentElements'])
            for element in elements:
                self.usersCommented.append(element.text)

            self.usersCommented = list(dict.fromkeys(self.usersCommented))
        except Exception as e:
            print(e)

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

    def checkForLikeLimitMessage(self):
        try:
            likeLimitMessage = self.driver.find_elements_by_xpath(xpaths['likeLimitMessage_Text'])
            if likeLimitMessage:
                return True
            else:
                return False
        except Exception as e:
            return False
