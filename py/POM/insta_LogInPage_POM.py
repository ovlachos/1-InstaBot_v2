# All POMs require a webPage object to be instantiated/initialized.
# The webPage object provides the webdriver and a "what page am I currently browsing" method
import random
from time import sleep

xpaths = {
    "GDPRcookies": "//button[contains(text(),'Accept')]",
    "logIn_UserName": "//input[@name=\"username\"]",
    "logIn_password": "//input[@name=\"password\"]",
    "submitButton": "//button[@type='submit']",
    "notNow": "//button[contains(text(), 'Not Now')]",
}


class InstaLogIn:

    def __init__(self, webPage):
        self.page = webPage
        self.driver = self.page.driver

    def logIn(self, user, pswd):
        if self.page.instance.newSession:
            from random import randint
            try:
                self.driver.get("https://www.instagram.com/")
                # Remove WebDriver Flag
                success = self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => false})")
            except Exception as e:
                print(e)

            sleep(randint(2, 6))

            try:
                self.page.getPageElement_tryHard(xpaths['GDPRcookies']).click()
            except Exception as e:
                print(f"Login Accept cookies click:\n{e}")

            self.page.slowTypeIntoField(xpaths['logIn_UserName'], user)
            self.page.slowTypeIntoField(xpaths['logIn_password'], pswd)
            self.page.getPageElement_tryHard(xpaths['submitButton']).click()

            sleep(4)

            try:
                self.page.getPageElement_tryHard(xpaths['notNow']).click()
                sleep(4)
                self.page.getPageElement_tryHard(xpaths['notNow']).click()
            except Exception as e:
                print(f"Login NotNow click:\n{e}")

            sleep(5)

        return InstaMainPage(self.page)


class InstaMainPage:
    def __init__(self, webPage):
        from POM import insta_topRibbon_POM as topRibbon
        self.page = webPage
        self.driver = self.page.driver
        self.topRibbon_SearchField = topRibbon.SearchField(self.page)
        self.topRibbon_myAccount = topRibbon.AccountTab(self.page)
