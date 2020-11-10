from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains


# All POMs require a webPage object to be instantiated/initialized.
# The webPage object provides the webdriver and a "what page am I currently browsing" method

class Browser:
    def __init__(self, headless=False):
        # ~~~ setting up a Firefox driver
        options = Options()
        options.headless = False
        if headless:
            print("I've got a  a headless browser!!")
            options.headless = True
        profile = webdriver.FirefoxProfile()
        profile.set_preference("intl.accept_languages", 'en-us')

        # 1 - Allow all images
        # 2 - Block all images
        # 3 - Block 3rd party images
        profile.set_preference("permissions.default.image", 1)
        profile.update_preferences()
        self.driver = webdriver.Firefox(options=options, firefox_profile=profile)
        # ~~~ setting up a Firefox driver


class WebPage:
    allpages = []

    def __init__(self, headless=False):
        self.instance = Browser(headless)
        self.driver = self.instance.driver
        self.driver.implicitly_wait(6)
        # append all instances of the WebPage class to check if the same one gets passed around
        WebPage.allpages.append(self)

    def killBrowser(self):
        self.driver.quit()

    def whichPageAmI(self, verbose=False):
        currentPageURL = self.driver.current_url

        if verbose:
            print("Session: {0}\n@ {1}".format(self.driver.session_id, currentPageURL))

        return currentPageURL

    def tH_checkIfIhit_ActionLimit(self):
        try:
            errorMessagePresent = self.driver.find_element_by_xpath(
                "//p[contains(text(),'Please wait a few minutes')]").text
        except:
            return False

        if 'wait' in errorMessagePresent:
            return True

    def getPageElement_tryHard(self, xpath):
        attempts = 3
        result = None
        while result is None:
            try:
                result = self.driver.find_element_by_xpath(xpath)
            except:
                if attempts == 0: break
                attempts -= 1
        return result

    def sendKey(self, key):
        if isinstance(key, str):
            try:
                actions = ActionChains(self.driver)
                actions.send_keys(key)
                actions.perform()
            except Exception as e:
                print(e)
