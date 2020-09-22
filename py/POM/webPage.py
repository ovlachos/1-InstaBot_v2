from selenium import webdriver
from selenium.webdriver.firefox.options import Options


# All POMs require a webPage object to be instantiated/initialized.
# The webPage object provides the webdriver and a "what page am I currently browsing" method

class Browser:
    def __init__(self, headless=False):
        # ~~~ setting up a Chrome driver
        # option = webdriver.ChromeOptions()
        # chrome_prefs = {}
        # chrome_prefs["profile.default_content_settings"] = {"images": 2}
        # chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
        # option.experimental_options["prefs"] = chrome_prefs
        # self.browser =  webdriver.Chrome(options=option)
        # ~~~ setting up a Chrome driver

        # ~~~ setting up a Firefox driver
        options = Options()
        if headless:
            options.headless = True
        profile = webdriver.FirefoxProfile()
        profile.set_preference("intl.accept_languages", 'en-us')

        # 1 - Allow all images
        # 2 - Block all images
        # 3 - Block 3rd party images
        profile.set_preference("permissions.default.image", 1)
        profile.update_preferences()
        self.driver = webdriver.Firefox(options=options, firefox_profile=profile)
        self.driver.implicitly_wait(6)
        # ~~~ setting up a Firefox driver


class WebPage:
    instance = Browser()
    driver = instance.driver
    driver.implicitly_wait(6)
    allpages = []

    def __init__(self):
        # append all instances of the WebPage class to check if the same one gets passed around
        WebPage.allpages.append(self)
        self.__anyname = "thatName"

    def whichPageAmI(self):
        name = self.driver.current_url
        print("Session: {0}\n@ {1}".format(self.driver.session_id, name))
        return name
