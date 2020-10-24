import auth


class userPage_base:

    def __init__(self, webPage, user):
        self.page = webPage
        self.driver = self.page.driver
        self.userName = user
        self.type = 0
        if self.iAmInAUserPage():
            self.determineProfileType()
            self.stats = self.getStats_dict()
        else:
            self.type = 0

    def updateUserName(self):
        self.userName = self.driver.find_element_by_xpath("//header//h2").text

    def getAlternativeUserName(self):
        return self.driver.find_element_by_xpath("//header//div[@class='-vDIg']//h1").text

    def getBio(self):
        bioText = ''

        bio = self.driver.find_elements_by_xpath("//header//div[@class='-vDIg']//span")
        for line in bio:
            bioText += line.text

        return bioText

    def iAmInAUserPage(self):
        if self.userName in self.page.whichPageAmI():
            return True
        else:
            return False

    def determineProfileType(self):
        # 10 - Type 1: it's me
        # 20 -  Type 2: it's not me
        # 30 -   Type 2A: It is someone I already follow
        # 40 -   Type 2B: It is someone I do not follow
        # 50 -       Type 2Bi: Their profile is open
        # 60 -       Type 2Bi: Their profile is not open
        # 70 -  Type 3: It's no one (name changed, or profile deleted)

        self.type = 0
        if self.userName == auth.username:
            self.type += 10
            return
        else:
            self.type += 20

        try:
            self.driver.find_element_by_xpath("//header//section//span[@aria-label='Following']")
            self.type += 10
            return
        except Exception as e:
            # print(e)
            self.type += 20

        try:
            self.driver.find_element_by_xpath("//h2[contains(text(),'Private')]")
            self.type += 20
            return
        except Exception as e:
            # print(e)
            self.type += 10

        try:
            self.driver.find_element_by_xpath("//h2[contains(text(),'Sorry')]")
            self.type += 20
            return
        except Exception as e:
            pass

    def profileTypeDescription(self):
        # phrased so that it fits in 'This user BLAH ...'
        description = {
            '10': 'is myself, good job :P',
            '20': 'is not me Sherlock',
            '30': 'is someone I already follow',
            '40': 'is someone I do not follow',
            '50': 'is someone I do not follow and their profile is OPEN',
            '60': 'is someone I do not follow, but their profile is CLOSED',
            '70': 'has either changed handle or deleted their account',
        }
        return description[str(self.type)]

    def getStats_dict(self):
        stats = {
            'posts': '',
            'followers': '',
            'following': ''
        }

        try:
            allItems = self.driver.find_elements_by_xpath("//header//ul//span[@class='g47SY ']")

            if len(allItems) >= 3:
                stats['posts'] = int(allItems[0].text.replace(',', ''))
                stats['followers'] = int(allItems[1].text.replace(',', ''))
                stats['following'] = int(allItems[2].text.replace(',', ''))
        except Exception as ex:
            print(ex)

        return stats


class userPage(userPage_base):
    def getFollowersList(self):
        from time import sleep
        if self.type < 55:
            try:
                sleep(3)
                self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format('followers')).click()
                sleep(2)
                followersList = self.__scroll_and_get(targetCount=self.stats['followers'])
                self.driver.find_element_by_xpath("//button[@class='wpO6b ']//*[@aria-label='Close']").click()
                return followersList
            except Exception as e:
                print(e)
                return []
        else:
            print('nahh - no followers access for this user')
            print('User {0} {1}'.format(self.userName, self.profileTypeDescription()))

    def getFollowingList(self):
        from time import sleep
        if self.type < 55:
            try:
                sleep(3)
                self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format('following')).click()
                sleep(2)
                followingList = self.__scroll_and_get(targetCount=self.stats['following'])
                self.driver.find_element_by_xpath("//button[@class='wpO6b ']//*[@aria-label='Close']").click()
                return followingList
            except Exception as e:
                print(e)
                return []
        else:
            print('nahh - no following access for this user')
            print('User {0} {1}'.format(self.userName, self.profileTypeDescription()))

    def getHashtagsFollowingList(self):
        from time import sleep
        if self.type < 55:
            sleep(3)
            try:
                self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format('following')).click()
                sleep(2)
                self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format('hashtag_following')).click()
                sleep(2)
                hashtagList = self.__scroll_and_get('hashTags', "//div[@class='_8zyFd']")
                self.driver.find_element_by_xpath("//button[@class='wpO6b ']//*[@aria-label='Close']").click()
                return hashtagList
            except Exception as e:
                print(e)
                return []
        else:
            print('nahh - no hashtag access for this user')
            print('User {0} {1}'.format(self.userName, self.profileTypeDescription()))

    def navigateTo_X_latestPost(self, numberX):
        from POM import insta_post as post
        # numberX runs from 0 to whatever
        if self.type < 55:
            try:
                # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                posts = self.driver.find_elements_by_xpath("//a[contains(@href,'/p/')]")
                if len(posts) > 0 and len(posts) > numberX:
                    self.driver.execute_script("arguments[0].scrollIntoView();", posts[numberX])
                    self.driver.execute_script("arguments[0].click();", posts[numberX])
            except Exception as e:
                print(e)
                print('Opening post number {} failed'.format(numberX))
            return post.Post(self.page)
        else:
            print('nahh')
            print('User {0} {1}'.format(self.userName, self.profileTypeDescription()))

    def follow(self):
        if self.type > 35:
            try:
                self.driver.find_element_by_xpath("//button[contains(text(),'Follow')]").click()
            except Exception as e:
                print('Cannot find the follow button')

            self.determineProfileType()
            if self.type < 40:
                return 'OK'
            else:
                return 'fail'
        else:
            print('nahh - no follow access for this user')
            print('User {0} {1}'.format(self.userName, self.profileTypeDescription()))
            return 'OK'

    def unfollow(self):
        from time import sleep
        if 10 < self.type < 35:
            self.driver.find_element_by_xpath("//span[@aria-label='Following']").click()
            sleep(1)
            buttons = self.driver.find_element_by_xpath("//*[contains(@class,'-Cab')]")
            if 'follow' in buttons.text:
                buttons.click()
                sleep(2)
                self.driver.refresh()

            self.determineProfileType()
            if self.type > 40:
                return 'OK'
            else:
                return 'fail'
        else:
            print('nahh - no unfollow access for this user')
            print('User {0} {1}'.format(self.userName, self.profileTypeDescription()))
            return 'OK'

    def __scroll_and_get(self, type='users', xpath="//div[@class='isgrP']", targetCount=0):
        from time import sleep
        xpath.strip("'\'")
        sleep(2)
        outputList = []

        try:
            scroll_box = self.driver.find_element_by_xpath(xpath)
        except Exception as e:
            print(e)
            return outputList

        try:
            sugs = self.driver.find_element_by_xpath("//h4[text()='Suggestions')]")
            self.driver.execute_script('arguments[0].scrollIntoView()', sugs)
        except Exception as e:
            sleep(1)

        sleep(2)

        # make sure you scroll to the end of the list
        scrollCount = 0
        while (len(outputList) <= int(0.95 * targetCount)) or scrollCount < 2:
            last_ht, ht = 0, 1
            while last_ht != ht:
                last_ht = ht
                sleep(1)
                dialog = self.driver.find_element_by_xpath("//div[contains(@role, 'dialog')]")
                currentAtags = dialog.find_elements_by_tag_name('a')
                names = currentAtags

                # names = dialog.find_elements_by_tag_name('a')
                for name in names:
                    try:
                        if type == 'users':
                            if len(name.get_attribute('title')) > 0:
                                outputList.append(name.get_attribute('title'))
                                outputList = list(dict.fromkeys(outputList))
                        else:
                            if '#' in name.text: outputList.append(name.text)
                    except Exception as e:
                        print(e)
                        continue

                # print('~~scrolling ' + type)
                ht = self.driver.execute_script(
                    'arguments[0].scrollTo(0, arguments[0].scrollHeight);'
                    'return arguments[0].scrollHeight;',
                    scroll_box)
            scrollCount += 1

        outputList = list(dict.fromkeys(outputList))  # remove duplicates
        return list(outputList)
