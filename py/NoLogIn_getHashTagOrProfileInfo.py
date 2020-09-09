import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
from random import randint
import logging
import sys
from os import getpid
from multiprocessing import get_context
import multiprocessing as mp

logProfiles = logging.getLogger("InstaFame")
a = os.path.dirname(__file__)
hdlr = logging.FileHandler(
    '/Users/cortomaltese/Google Drive/10 Projects/1 InstaBot_v2/InstaFame.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logProfiles.addHandler(hdlr)


def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()


def getProfileSoup(handle, delayInSec=2):
    # https://www.instagram.com/9gag, handle = "9gag"
    # browse to profile page
    # return soup object

    option = webdriver.ChromeOptions()
    chrome_prefs = {}
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    option.experimental_options["prefs"] = chrome_prefs

    # return webdriver.Chrome(options=option)

    driver = webdriver.Chrome(options=option)
    sleep(delayInSec)
    try:
        driver.get("https://www.instagram.com/" + handle + "/")
        # driver.find_element_by_tag_name('body').send_keys(Keys.END)
        sleep(4)
        soup = BeautifulSoup(driver.page_source, "html.parser")
    except Exception as e:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        logProfiles.error(e)
        logProfiles.error('no guaranteed profile soup for you: ' + handle)

    driver.quit()
    return soup


def getHashTagSoup(hashtag):
    # https://www.instagram.com/explore/tags/winter2020/
    # browse to hastag page
    # return soup object
    # hashtag = "winter2020"
    driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
    driver.find_element_by_tag_name('body').send_keys(Keys.END)
    sleep(2)
    soup = BeautifulSoup(driver.page_source)
    driver.close()
    return soup


def getSinglePostSoup(postURL):
    # browse to hastag page
    # return soup object
    # hashtag = "winter2020"
    driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    driver.get("https://www.instagram.com" + postURL)
    sleep(2)
    soup = BeautifulSoup(driver.page_source)
    driver.close()
    return soup


def getProfileStatsDict(target, driver=0, externalSoup=False):
    # <a class= "-nal3" href="/finestmemes/followers/">
    #   <span class="g47SY " title="2,348,785">2.3m</span> followers</a>
    tag1 = '-nal3'
    tag2 = 'g47SY'
    profileStats = []
    # logProfiles.error("Fetching stats for {0}, with process {1}".format(target, getpid()))

    try:
        if not externalSoup:
            soup = getProfileSoup(target)
        else:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
    except Exception as e:
        logProfiles.error("Get profile stats function failed to eat soup on " + target)
        return getProfileStatsDict_Fail(target)

    for a in soup.findAll('a', attrs={'class': tag1}):
        try:
            profileStats.append(a.find('span', attrs={'class': tag2}))
            logProfiles.error('I got {}'.format(a))
        except Exception as ex:
            logProfiles.error("getProfileStatsDict: Target profile is {0}".format(target))
            logProfiles.error("getProfileStatsDict: No {0} found".format(tag2), str(ex))
            return getProfileStatsDict_Fail(target)

    if len(profileStats) == 3:
        profileStatsDict = {
            "Posts": int(profileStats[0].contents[0].replace(',', '')),
            "Followers": int(profileStats[1]['title'].replace(',', '')),
            "Following": int(profileStats[2].contents[0].replace(',', '')),
            "user": target
        }
        return profileStatsDict
    else:
        return getProfileStatsDict_Fail(target)


def getProfileStatsDict_Fail(target):
    logProfiles.error("getProfileStatsDict: failure on Target {0}".format(target))
    profileStatsDict = {
        "Posts": 99999999,
        "Followers": 99999999,
        "Following": 99999999,
        "user": 'Κοπερτί',
        "bio": 'IamaΚοπερτί'
    }
    return profileStatsDict


def getProfileStatsDict_multiProc(target):
    # <a class= "-nal3" href="/finestmemes/followers/">
    #   <span class="g47SY " title="2,348,785">2.3m</span> followers</a>
    tag1 = '-nal3'
    tag2 = 'g47SY'
    profileStats = []
    # logProfiles.error("Fetching stats for {0}, with process {1}".format(target, getpid()))
    sleep(randint(2, 7))

    try:
        soup = getProfileSoup(target, randint(20, 34))
    except Exception as e:
        logProfiles.error("Get profile stats function failed to eat soup on " + target)
        return getProfileStatsDict_Fail(target)

    for a in soup.findAll('a', attrs={'class': tag1}):
        try:
            profileStats.append(a.find('span', attrs={'class': tag2}))
        except Exception as ex:
            logProfiles.error("getProfileStatsDict: Target profile is {0}".format(target))
            logProfiles.error("getProfileStatsDict: No {0} found".format(tag2), str(ex))
            return getProfileStatsDict_Fail(target)

    if len(profileStats) == 3:
        profileStatsDict = {
            "Posts": int(profileStats[0].contents[0].replace(',', '')),
            "Followers": int(profileStats[1]['title'].replace(',', '')),
            "Following": int(profileStats[2].contents[0].replace(',', '')),
            "user": target
        }
        return profileStatsDict
    else:
        return getProfileStatsDict_Fail(target)


def getCountOfHashtagPosts(soup):
    tag = 'g47SY'
    sample = -1
    try:
        sample = int(soup.find('span', attrs={'class': tag}).contents[0].replace(',', ''))
    except Exception as ex:
        logProfiles.error("No such tag: {0} found and also :".format(tag), ex)
        return -1

    return sample


def getPostsURLs(soup):
    # 'v1Nh3 kIKUG  _bz0w' is the 'div' class containing the post links
    tag = 'v1Nh3'
    postURLs = []
    for a in soup.findAll('div', attrs={'class': tag}):
        t = 1
        try:
            postURLs.append(a.contents[0]['href'])
        except Exception as ex:
            logProfiles.error("No such tag: {0} found and also :".format('tag'), ex)

    return postURLs


def batchProfileInfo(targetProfilesHandleList):
    targetsArray = []
    for target in targetProfilesHandleList:
        row = []
        row.append(target)
        rowdict = getProfileStatsDict(getProfileSoup(target))
        row.append(rowdict['Followers'])
        row.append(rowdict['Following'])
        row.append(rowdict['Posts'])
        targetsArray.append(row)

    panda = pd.DataFrame({'User,Followers, Following, Posts': targetsArray})
    return panda


def getPostHashtags(postList):
    # button (close post
    # div class = C4VMK
    # <a class=" xil3i" href="/explore/tags/streetart/">#streetart</a>
    tag1 = "C4VMK"
    tag2 = "xil3i"
    tagsList = []
    for a in postList:
        soup = getSinglePostSoup(a)
        try:
            c = soup.find_all('a', attrs={'class': tag2})  # .contents[0]
            for i in c:
                tagsList.append(i.contents[0].strip('#\n'))
        except Exception as ex:
            logProfiles.error("No such tag: {0} found and also :".format('tag'), ex)

    return tagsList
