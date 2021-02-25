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

        try:
            self.driver.get("https://www.instagram.com/")
            if self.page.instance.newSession:
                # Remove WebDriver Flag
                success = self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => false})")
        except Exception as e:
            print(e)

        if not self.alreadyLoggedIn():
            from random import randint
            sleep(randint(1, 4))

            try:
                self.page.getPageElement_tryHard(xpaths['GDPRcookies']).click()
            except Exception as e:
                print(f"Login Accept cookies click:\n{e}")

            self.page.slowTypeIntoField(xpaths['logIn_UserName'], user)
            self.page.slowTypeIntoField(xpaths['logIn_password'], pswd)
            self.page.getPageElement_tryHard(xpaths['submitButton']).click()

            sleep(3)

            try:
                self.page.getPageElement_tryHard(xpaths['notNow']).click()
                sleep(3)
                self.page.getPageElement_tryHard(xpaths['notNow']).click()
            except Exception as e:
                print(f"Login NotNow click:\n{e}")

        return InstaMainPage(self.page)

    def alreadyLoggedIn(self):

        try:
            button = self.page.getPageElement_tryHard(xpaths['logIn_password'])
            if button:
                return False
        except:
            pass

        return True


class InstaMainPage:
    def __init__(self, webPage):
        from POM import insta_topRibbon_POM as topRibbon
        self.page = webPage
        self.driver = self.page.driver
        self.topRibbon_SearchField = topRibbon.SearchField(self.page)
        self.topRibbon_myAccount = topRibbon.AccountTab(self.page)
