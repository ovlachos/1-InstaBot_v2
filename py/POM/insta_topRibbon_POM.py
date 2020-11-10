from time import sleep
from selenium.webdriver.common.keys import Keys
import auth


class AccountTab:
    ac_xpaths = {
        # "myAvatar": "//img[contains(@alt,'{}')]//..".format(auth.username)
        "myAvatar": "//img[contains(@alt,'{}')]//..//..//span[@class='_2dbep qNELH']".format(auth.username),
        'ownProfile': "//div[contains(text(),'Profile')]",
        'logOutButton': "//div[contains(text(),'Log Out')]",
    }

    def __init__(self, webPage):
        self.page = webPage
        self.driver = self.page.driver

    def navigateToOwnProfile(self):
        from POM import insta_userPage_POM as up

        result = None
        attempts = 4
        while result is None:
            try:
                self.page.getPageElement_tryHard(self.ac_xpaths['myAvatar']).click()
                result = self.page.getPageElement_tryHard(self.ac_xpaths['ownProfile'])
                result.click()
                sleep(1)
                if auth.username in self.page.whichPageAmI():
                    return up.userPage(self.page, auth.username)
            except:
                if attempts == 0:
                    break
                attempts -= 1

        return None

    def logOut(self):
        result = None
        attempts = 4
        while result is None:
            try:
                self.page.getPageElement_tryHard(self.ac_xpaths['myAvatar']).click()
                sleep(1)
                result = self.page.getPageElement_tryHard(self.ac_xpaths['logOutButton'])
                sleep(2)
                result.click()
            except:
                if attempts == 0:
                    break
                attempts -= 1


class SearchField:
    sf_xpaths = {
        "searchBoxInput": "//input[@placeholder='Search']",
        "resultsListFrame": "//div[@class='fuqBx']",
        "resultsList": "//div[@class='fuqBx']/a",
        "clearSearch": "//div[contains(@class,'coreSpriteSearchClear')]",
    }

    def __init__(self, webPage):
        self.page = webPage
        self.driver = self.page.driver

    def clearSearchField(self):
        try:
            self.driver.find_element_by_xpath(self.sf_xpaths['clearSearch']).click()
        except Exception as e:
            print('Cannot Clear search field in top ribbon')

    def navigateToUserPageThroughSearch(self, userName):
        from POM import insta_userPage_POM as up

        # self.clearSearchField()
        attempts = 2
        result = None
        while result is None:
            try:
                self.typeIntoSearchBox(userName)
                sleep(2)

                result = self.driver.find_element_by_xpath("//a[@href='/{}/']".format(userName))
                result.click()

                sleep(2)

                return up.userPage(self.page, userName)
            except Exception as e:
                print(e)
                self.page.sendKey(Keys.ESCAPE)
                self.clearSearchField()
                if attempts == 0:
                    break

                attempts -= 1
                result = None

    def navigateToHashTagPageThroughSearch(self, hashtag):
        self.typeIntoSearchBox('#{}'.format(hashtag))
        self.page.getPageElement_tryHard("//a[@href='/explore/tags/{}/']".format(hashtag)).click()
        sleep(2)

        return self.page  # TODO create a POM of hashtag pages and have it return an instance of that

    def getHashTagPostCountThroughSearch(self, hashtag):
        self.typeIntoSearchBox('#{}'.format(hashtag))
        tagResult = self.page.getPageElement_tryHard(
            "//a[@href='/explore/tags/{}/']//../div[@class='Fy4o8']/span/span".format(hashtag)).text

        self.clearSearchField()

        return int(tagResult.replace(',', ''))

    def getAllSearchResults_List(self, query):
        self.typeIntoSearchBox(query)
        return self.driver.find_elements_by_xpath(self.sf_xpaths["resultsList"])

    def typeIntoSearchBox(self, query):
        self.page.getPageElement_tryHard(self.sf_xpaths["searchBoxInput"]).send_keys(query)
