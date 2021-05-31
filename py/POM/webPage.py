import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


# All POMs require a webPage object to be instantiated/initialized.
# The webPage object provides the webdriver and a "what page am I currently browsing" method


class Browser:

    def __init__(self, headless=False):
        # ~~~ setting up a Firefox driver
        sessionDataFromJSON_ = self.getSessionFromJSON()
        self.newSession = True

        if not self.previousSessionExists(sessionDataFromJSON_):
            self.createNewBrowserSession(headless)
        else:
            try:
                self.driver = self.create_driver_session(sessionDataFromJSON_['session_id'], sessionDataFromJSON_['executor_url'])

                self.driver.session_id = sessionDataFromJSON_['session_id']
                print(f"Got that old browser session with id {sessionDataFromJSON_['session_id']}\n")

                self.driver.implicitly_wait(15)
                self.newSession = False

                print(f"It's final: ReUsing browser session with id {sessionDataFromJSON_['session_id']}")
            except Exception as e:
                try:
                    if self.driver:
                        print('Let me quit the old session first')
                        self.driver.quit()
                        del self.driver
                except Exception as e1:
                    print(e1)

                print(f'Creating new browser session because:\n{e}')

                self.createNewBrowserSession(headless)
                self.newSession = True

    def createNewBrowserSession(self, headless):

        option = webdriver.ChromeOptions()
        option.add_argument('--disable-blink-features=AutomationControlled')
        option.add_argument("window-size=1280,800")
        option.add_argument("--start-maximized")

        option.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

        self.driver = webdriver.Chrome(options=option)
        self.driver.implicitly_wait(15)

        executor_url = self.driver.command_executor._url
        session_id = self.driver.session_id

        print(f"New session with:\n\tsession_id: {session_id}\n\texecutor_url: {executor_url}\n")
        self.writeSessionDataToJSON(session_id=session_id, executor_url=executor_url)

    def writeSessionDataToJSON(self, session_id='0', executor_url='0'):
        import json

        sessionData = {}
        sessionData['session_id'] = session_id
        sessionData['executor_url'] = executor_url

        with open('BrowserSession.json', 'w') as json_conf:
            json.dump(sessionData, json_conf)

    def getSessionFromJSON(self):
        import json

        with open('BrowserSession.json', 'r') as json_conf:
            return json.load(json_conf)

    def previousSessionExists(self, dataFromJSON):
        if dataFromJSON['session_id'] == '0':
            return False

        return True

    # Only needed for Firefox sessions ?
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
        RemoteWebDriver.execute = org_command_execute  # for some reason this no longer happens and all new browsers get the faked response.
        new_driver.implicitly_wait(15)

        return new_driver


class WebPage:

    def __init__(self, headless=False):
        self.instance = Browser(headless)
        self.driver = self.instance.driver
        # self.wait = WebDriverWait(self.driver, 10)

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
                # print(f"getPageElement_tryHard:\n{e}At XPATH:\n{xpath}")
                attempts -= 1
                sleep(1)
                if attempts == 0:
                    break

        return result

    def getPageElements_tryHard(self, xpath):
        attempts = 3
        result = None
        while result is None:
            try:
                result = self.driver.find_elements_by_xpath(xpath)
            except Exception as e:
                # print(f"getPageElement_tryHard:\n{e}At XPATH:\n{xpath}")
                attempts -= 1
                sleep(1)
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

    def sendESC(self):
        from selenium.webdriver.common.keys import Keys
        try:
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.ESCAPE).perform()
            # self.driver.refresh()
        except Exception as e:
            print(f"ESC funciton: {e}")

    def slowTypeIntoField(self, fieldXPATH, query):
        try:

            field = self.getPageElement_tryHard(fieldXPATH)
            field.clear()
            for ch in query:
                sleep(random.uniform(0, 1))
                field.send_keys(ch)
            sleep(1)
        except Exception as e:
            print(e)

    def getListOfAtributeFromWebElementList(self, listOfWebElements, attribute):
        newList = []
        if listOfWebElements:
            for elem in listOfWebElements:
                newList.append(elem.get_attribute(attribute))

        return newList

    def getTitleAttributeFromWebElement(self, webElement):
        return webElement.get_attribute('title')

    def getTextFromWebElement(self, webElement):
        return webElement.text

    def sleepPage(self, secs):
        sleep(secs)
