import random
from time import sleep
from selenium.webdriver.common.keys import Keys
from fuzzywuzzy import process
import auth

xpaths = {
    "searchBoxInput": "//input[@placeholder='Search']",
    "resultsListFrame": "//div[@class='fuqBx']",
    "resultsList": "//div[@class='fuqBx']/a",
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

    def noResultsCheck(self):
        try:
            noResults = self.driver.find_element_by_xpath("//div[contains(text(),'No results')]")
            if noResults:
                return True
            return False
        except:
            return False

    def goHomeWhereYouAreSafe_s(self, e):
        try:
            if 'obscures it' in e.msg:
                clickOnObscuringElement(self.driver, e)
        except:
            pass

    def navigateToUserPageThroughSearch(self, userName):
        from POM import insta_userPage_POM as up

        attempts = 3
        result = None
        while result is None:
            try:
                self.page.slowTypeIntoField(xpaths["searchBoxInput"], userName)
                sleep(2)

                if self.noResultsCheck():
                    return None

                fuzzyMatch = self.getFuzzyResults(userName)
                result = self.driver.find_element_by_xpath("//a[@href='/{}/']".format(fuzzyMatch))
                userName = fuzzyMatch

                # used to be result = self.getExactResult(userName)

                if not result:
                    fuzzyMatch = self.getFuzzyResults(userName)
                    result = self.driver.find_element_by_xpath("//a[@href='/{}/']".format(fuzzyMatch))
                    userName = fuzzyMatch

                result.click()

                return up.userPage(self.page, userName)

            except Exception as e:
                attempts -= 1
                result = None
                self.goHomeWhereYouAreSafe_s(e)
                if attempts == 0:
                    break
                if attempts == 1:
                    self.driver.get("https://www.instagram.com/")

    def navigateToHashTagPageThroughSearch(self, hashtag):
        self.page.slowTypeIntoField(xpaths["searchBoxInput"], '#{}'.format(hashtag))
        self.page.getPageElement_tryHard("//a[@href='/explore/tags/{}/']".format(hashtag)).click()
        sleep(2)

        return self.page  # TODO create a POM of hashtag pages and have it return an instance of that

    def getHashTagPostCountThroughSearch(self, hashtag):
        self.page.slowTypeIntoField(xpaths["searchBoxInput"], '#{}'.format(hashtag))
        tagResult = self.page.getPageElement_tryHard(
            "//a[@href='/explore/tags/{}/']//../div[@class='Fy4o8']/span/span".format(hashtag)).text

        return int(tagResult.replace(',', ''))

    def getAllSearchResults_List(self, query):
        sleep(1)
        try:
            return self.driver.find_elements_by_xpath(xpaths["resultsList"])
        except:
            return None

    def getExactResult(self, userName):
        try:
            result = self.driver.find_element_by_xpath("//a[@href='/{}/']".format(userName))
            return result
        except:
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
