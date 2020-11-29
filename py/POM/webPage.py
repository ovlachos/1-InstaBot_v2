from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains


# All POMs require a webPage object to be instantiated/initialized.
# The webPage object provides the webdriver and a "what page am I currently browsing" method

class Browser:

    def __del__(self):
        print("Browser deleted")

    def __init__(self, headless=False):
        # ~~~ setting up a Firefox driver
        sessionDataFromJSON_ = self.getSessionFromJSON()
        self.newSession = True

        if not self.previousSessionExists(sessionDataFromJSON_):
            self.createNewBrowserSession(headless)
        else:
            try:
                self.driver = self.create_driver_session(sessionDataFromJSON_['session_id']
                                                         , sessionDataFromJSON_['executor_url'])
                self.driver.implicitly_wait(6)
                self.newSession = False
                print(f"ReUsing browser session with id {sessionDataFromJSON_['session_id']}")
            except Exception as e:
                self.createNewBrowserSession(headless)
                self.newSession = True
                print('Creating new browser session')

    def createNewBrowserSession(self, headless):
        options = Options()
        options.headless = False
        if headless:
            print("I've got a  a headless browser!!")
            options.headless = True

        profile = webdriver.FirefoxProfile()
        profile.set_preference("intl.accept_languages", 'en-us')

        # disabling caching (but not cookies)
        profile.set_preference('browser.cache.disk.enable', False)
        profile.set_preference('browser.cache.memory.enable', False)
        profile.set_preference('browser.cache.offline.enable', False)

        # 1 - Allow all images
        # 2 - Block all images
        # 3 - Block 3rd party images
        profile.set_preference("permissions.default.image", 1)
        profile.update_preferences()
        self.driver = webdriver.Firefox(options=options, firefox_profile=profile)

        executor_url = self.driver.command_executor._url
        session_id = self.driver.session_id

        print(f"New session with session_id: {session_id}\nexecutor_url: {executor_url}")
        self.writeSessionDataToJSON(session_id=session_id, executor_url=executor_url)

    def writeSessionDataToJSON(self, session_id='0', executor_url='0'):
        import json

        sessionData = {}
        sessionData['session_id'] = session_id
        sessionData['executor_url'] = executor_url

        with open('firefoxSession.json', 'w') as json_conf:
            json.dump(sessionData, json_conf)

    def getSessionFromJSON(self):
        import json

        with open('firefoxSession.json', 'r') as json_conf:
            return json.load(json_conf)

    def previousSessionExists(self, dataFromJSON):
        if dataFromJSON['session_id'] == '0':
            return False

        return True

    def clearCache(self):
        return
        self.driver.get('about:preferences#privacy')

    def create_driver_session(self, session_id, executor_url):
        from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

        # Save the original function, so we can revert our patch
        org_command_execute = RemoteWebDriver.execute

        def new_command_execute(self, command, params=None):
            if command == "newSession":
                # Mock the response
                return {'success': 0, 'value': None, 'sessionId': session_id}
            else:
                return org_command_execute(self, command, params)

        # Patch the function before creating the driver object
        RemoteWebDriver.execute = new_command_execute

        new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
        new_driver.session_id = session_id

        # Replace the patched function with original function
        RemoteWebDriver.execute = org_command_execute

        return new_driver


class WebPage:
    allpages = []

    def __del__(self):
        print("webPage deleted")

    def __init__(self, headless=False):
        self.instance = Browser(headless)
        self.driver = self.instance.driver
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
            except Exception as e:
                # print(e)
                attempts -= 1
                if attempts == 0:
                    break

        return result

    def sendKey(self, key):
        if isinstance(key, str):
            try:
                actions = ActionChains(self.driver)
                actions.send_keys(key)
                actions.perform()
            except Exception as e:
                print(e)
