import auth


class AccountTab:
    ac_xpaths = {
        "myAvatar": "//img[contains(@alt,'{}')]".format(auth.username),
        'ownProfile': "//div[contains(text(),'Profile')]",
        'logOutButton': "//div[contains(text(),'Log Out')]",
    }

    def __init__(self, webPage):
        self.page = webPage
        self.driver = self.page.driver

    def navigateToOwnProfile(self):
        from POM import insta_userPage_POM as up

        self.driver.find_element_by_xpath(self.ac_xpaths['myAvatar']).click()
        self.driver.find_element_by_xpath(self.ac_xpaths['ownProfile']).click()

        return up.userPage(self.page, auth.username)

    def logOut(self):
        self.driver.find_element_by_xpath(self.ac_xpaths['myAvatar']).click()
        self.driver.find_element_by_xpath(self.ac_xpaths['logOutButton']).click()


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
            self.driver.find_element_by_xpath("//div[contains(@class,'SearchClear')]").click()
        except Exception as e:
            pass

    def navigateToUserPageThroughSearch(self, userName):
        from POM import insta_userPage_POM as up
        from time import sleep
        self.clearSearchField()
        self.typeIntoSearchBox(userName)
        sleep(2)
        try:
            result = self.driver.find_element_by_xpath(
                "//a[@href='/{}/']".format(userName))  # This is the first/top result
            result.click()
            sleep(2)
        except Exception as e:
            print(e)
            self.clearSearchField()

        return up.userPage(self.page, userName)

    def navigateToHashTagPageThroughSearch(self, hashtag):
        from time import sleep
        self.typeIntoSearchBox('#{}'.format(hashtag))
        self.driver.find_element_by_xpath("//a[@href='/explore/tags/{}/']".format(hashtag)).click()
        sleep(2)

        return self.page  # TODO create a POM of hashtag pages and have it return an instance of that

    def getHashTagPostCountThroughSearch(self, hashtag):
        self.typeIntoSearchBox('#{}'.format(hashtag))
        tagResult = self.driver.find_element_by_xpath(
            "//a[@href='/explore/tags/{}/']//../div[@class='Fy4o8']/span/span".format(hashtag)).text

        self.driver.find_element_by_xpath(self.sf_xpaths["clearSearch"]).click()

        return int(tagResult.replace(',', ''))

    def getAllSearchResults_List(self, query):
        self.typeIntoSearchBox(query)
        return self.driver.find_elements_by_xpath(self.sf_xpaths["resultsList"])

    def typeIntoSearchBox(self, query):
        self.driver.find_element_by_xpath(self.sf_xpaths["searchBoxInput"]).send_keys(query)