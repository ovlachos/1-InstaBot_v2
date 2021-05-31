import random
from time import sleep

from fuzzywuzzy import process
from selenium.webdriver.common.keys import Keys

import auth

xpaths = {
    "searchBoxInput": "//input[@placeholder='Search']",
    "resultsListFrame": "//div[@class='fuqBx']",
    "resultsList": "//a[contains(@href,'/')]//..//..//div[contains(@role,'none')]",
    "noResults": "//div[contains(text(),'No results found.')]",
    "clearSearch": "//div[contains(@class,'coreSpriteSearchClear')]",
    "logo": "//a[@href='/']",
    "cancelUnfollow": "//button[contains(text(),'Cancel')]",
    "myAvatar": "//img[contains(@alt,'{}')]//..//..//span[@class='_2dbep qNELH']".format(auth.username),
    'ownProfile': "//div[contains(text(),'Profile')]",
    'logOutButton': "//div[contains(text(),'Log Out')]",
}


def clickOnObscuringElement(driver, e):
    try:  # Maybe we are stuck on unfollow
        driver.find_element_by_xpath(xpaths["cancelUnfollow"]).click()
        return
    except Exception as ex:
        print(f" In click obscuring 0 elem")

    try:  # Click on it
        typeOfElement = '*'
        classOfelement = e.msg.split("another element <")[1].split("> obscures it")[0].split("class=")[1].strip('\"')
        xpath_0 = f"//{typeOfElement}[@class='{classOfelement}']"
        driver.find_element_by_xpath(xpath_0).click()
        driver.find_element_by_xpath(xpath_0).click()
        driver.find_element_by_xpath(xpath_0).click()
    except Exception as ex:
        print(f" In click obscuring 1 elem")

    try:  # Click on body element
        el = driver.find_element_by_tag_name('body')

        action = driver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(el, 5, 5)
        action.click()
        action.perform()
    except Exception as ex:
        print(f" In click obscuring 2 elem")


class AccountTab:

    def __init__(self, webPage):
        self.page = webPage
        self.driver = self.page.driver

    def navigateToOwnProfile(self):
        from POM import insta_userPage_POM as up

        result = None
        attempts = 4
        while result is None:
            try:
                self.page.getPageElement_tryHard(xpaths['myAvatar']).click()
                result = self.page.getPageElement_tryHard(xpaths['ownProfile'])
                result.click()
                sleep(1)
                if auth.username in self.page.whichPageAmI():
                    return up.userPage(self.page, auth.username)
            except Exception as e:
                attempts -= 1
                self.goHomeWhereYouAreSafe_u(e)
                if attempts == 0:
                    break

        return None

    def logOut(self):
        result = None
        attempts = 4
        while result is None:
            try:
                self.page.getPageElement_tryHard(xpaths['myAvatar']).click()
                sleep(1)
                result = self.page.getPageElement_tryHard(xpaths['logOutButton'])
                sleep(2)
                result.click()
            except Exception as e:
                attempts -= 1
                self.goHomeWhereYouAreSafe_u(e)
                if attempts == 0:
                    break

    def goHomeWhereYouAreSafe_u(self, e):

        # if 'obscures it' in e.msg:
        #     clickOnObscuringElement(self.driver, e)

        # if not obscured
        try:
            self.driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
            logo = self.page.getPageElement_tryHard(xpaths['logo'])
            try:
                logo.click()
            except Exception as e:
                # print(e)
                pass
        except Exception as e:
            # print('ET cannot go home cause: {0}'.format(e))
            pass


class SearchField:

    def __init__(self, webPage):
        self.page = webPage
        self.driver = self.page.driver

    def goHomeWhereYouAreSafe_s(self, e):
        try:
            if 'obscures it' in e.msg:
                clickOnObscuringElement(self.driver, e)
        except Exception:
            pass

    def navigateToUserPageThroughSearch(self, userName):
        from POM import insta_userPage_POM as up

        attempts = 3
        result = None
        while result is None:
            try:
                self.page.slowTypeIntoField(xpaths["searchBoxInput"], userName)
                sleep(2)

                if self.noResults():
                    return None

                fuzzyMatch = self.getFuzzyResults(userName)
                result = self.driver.find_element_by_xpath("//a[contains(@href,'{}')]".format(fuzzyMatch))  # //a[contains(@href,'hd35mm')]
                if len(fuzzyMatch) > 0:
                    userName = fuzzyMatch

                result.click()

                sleep(2)

                return up.userPage(self.page, userName)

            except Exception as e:
                attempts -= 1
                result = None
                if attempts == 1:
                    self.driver.get("https://www.instagram.com/")
                if attempts == 0:
                    break

    def navigateToHashTagPageThroughSearch(self, hashtag):
        from POM import insta_HashTagPage_POM as hp
        hashtag = hashtag.replace("#", "")

        self.page.slowTypeIntoField(xpaths["searchBoxInput"], '#{}'.format(hashtag))
        sleep(1)

        if self.noResults():
            return None

        fuzzyMatch = self.getFuzzyResults(hashtag).replace("#", "")
        result = self.page.getPageElement_tryHard("//a[@href='/explore/tags/{}/']".format(fuzzyMatch))

        if result:
            try:
                self.driver.execute_script("arguments[0].click();", result)
            except Exception as e:
                if "stale" in e:
                    return None

        sleep(4)

        HTpage = hp.HashTagPage(self.page, hashtag)
        if HTpage.verifyHashtagHeading():
            return hp.HashTagPage(self.page, hashtag)

        return None

    def getHashTagPostCountThroughSearch(self, hashtag):
        tagResult = -1

        hashtag = hashtag.replace("#", "")
        self.page.slowTypeIntoField(xpaths["searchBoxInput"], '#{}'.format(hashtag))
        tagResult = self.page.getPageElement_tryHard("//a[@href='/explore/tags/{}/']//span//span".format(hashtag))

        if tagResult:
            tagResult = tagResult.text.replace(',', '')

        return int(tagResult)

    def getAllSearchResults_List(self, query):
        sleep(1)
        try:
            return self.driver.find_elements_by_xpath(xpaths["resultsList"])
        except Exception:
            return None

    def getExactResult(self, userName):
        try:
            result = self.driver.find_element_by_xpath("//a[@href='/{}/']".format(userName))
            return result
        except Exception:
            return None

    def getFuzzyResults(self, userName):
        searchResults = self.getAllSearchResults_List(userName)
        if not searchResults:
            return None

        userHandles = []

        if len(searchResults) > 0:
            for item in searchResults:
                userHandles.append(item.text.split("\n")[0])

            highest = process.extractOne(userName, userHandles)
            fuzzyMatch = highest[0]
            return fuzzyMatch

        return None

    def typeIntoSearchBox(self, query):
        try:
            self.page.getPageElement_tryHard(xpaths["searchBoxInput"]).clear()
            for ch in query:
                sleep(random.uniform(0, 1))
                self.page.getPageElement_tryHard(xpaths["searchBoxInput"]).send_keys(ch)
            sleep(1)
        except Exception as e:
            print(e)

    def noResults(self):
        try:
            noResults = self.driver.find_element_by_xpath(xpaths['noResults'])
            return noResults
        except Exception:
            return None
