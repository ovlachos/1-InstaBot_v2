import pandas as pd
import datetime
import multiprocessing as mp
import glob, os
from selenium import webdriver
import time
from time import sleep
import logging
import math
from bs4 import BeautifulSoup

dirname_of_py_files = os.path.dirname(
    __file__)  # e.g. '/Users/cortomaltese/Google Drive/10 Projects/1 Insta-Fame WebScraper/instaBot/py'
projectFolderPath = os.path.join(dirname_of_py_files, '../')

paths = {
    'root': projectFolderPath,
    'output': projectFolderPath + 'Outputs/HashTagEvaluation/',
    'input': projectFolderPath + 'Inputs/hashTags_EVALUATION/'
}

cutOffvalues = {
    'postLowerCount': 60000,
    'postUpperCOunt': 600000,
    'hastagScoreUpper': 3
}

log = logging.getLogger("InstaFame")
hdlr = logging.FileHandler(paths['root'] + 'HashTag.log')
formatter = logging.Formatter('%(asctime)s %(message)s')
hdlr.setFormatter(formatter)
log.addHandler(hdlr)


def getYourPaths(photoName):
    photoNameOutputDirectory = paths['output'] + photoName + "/"
    research_list_directory = photoNameOutputDirectory + 'research_lists/'
    pathsDict = {
        'photoName_Dir': photoNameOutputDirectory,
        'researchList_Dir': research_list_directory,
        'root': paths['root'],
        'output': paths['output'],
        'input': paths['input']
    }
    return pathsDict


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def addNewRow_toDataFrame(mainDF, newRowList):
    a_row = pd.Series(newRowList)
    newRow_df = pd.DataFrame([a_row])
    newRow_df.columns = list(mainDF.columns)[:len(list(newRow_df.columns))]

    try:
        return mainDF.append([newRow_df], ignore_index=True, sort=False)
    except Exception as e:
        return mainDF


def getHashTagSoup(hashtag, browserType='ff'):
    # https://www.instagram.com/explore/tags/winter2020/
    # browse to hastag page
    # return soup object

    if 'chrome' in browserType:
        option = webdriver.ChromeOptions()
        chrome_prefs = {}
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
        option.experimental_options["prefs"] = chrome_prefs

        # driver = webdriver.Chrome(options=option)
        driver = webdriver.Chrome()
    else:
        profile = webdriver.FirefoxProfile()
        profile.set_preference("intl.accept_languages", 'en-us')
        profile.update_preferences()
        # 1 - Allow all images
        # 2 - Block all images
        # 3 - Block 3rd party images
        profile.set_preference("permissions.default.image", 2)

        driver = webdriver.Firefox(firefox_profile=profile)

        # driver = webdriver.Firefox()

    try:
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        # driver.find_element_by_tag_name('body').send_keys(Keys.END)
        sleep(4)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        return soup
    except Exception as e:
        log.error("Attempt to eat soup " + hashtag + " failed because: {}".format(e))
        driver.quit()
        return -1


def scrapeForSimilarHashTags(hashtag):
    soup = getHashTagSoup(hashtag.strip('#\n'))
    tag = 'LFGs8'
    listOfSimilarHashTags = []
    try:
        for i in soup.find_all('a', attrs={'class': tag}):
            listOfSimilarHashTags.append(i.contents[0].strip("#"))
    except Exception as ex:
        log.error("No such tag: {0} found and also :".format(tag))
        log.error(ex)
        listOfSimilarHashTags.append(hashtag)

    return listOfSimilarHashTags


def batch_getListOfSimilarHashtags(seedList):
    expandedList = []
    processPool0 = mp.Pool(processes=10)
    try:
        list_of_lists_of_similar_hash_tags = processPool0.map(scrapeForSimilarHashTags, seedList)
    except Exception as e:
        log.error(e)
        return expandedList

    for listIn in list_of_lists_of_similar_hash_tags:
        if len(listIn) > 0:
            for tag in listIn:
                expandedList.append(tag)

    expandedList = list(dict.fromkeys(expandedList))
    return expandedList


def getCountOfHashtagPosts(hashtag):
    tag = 'g47SY'
    try:
        soup = getHashTagSoup(hashtag.strip('#\n'))
        sample = int(soup.find('span', attrs={'class': tag}).contents[0].replace(',', ''))
    except Exception as ex:
        try:
            sample = int(soup.find('span', attrs={'class': tag}).contents[0].replace(',', ''))
        except Exception as ex2:
            log.error("# # # #{} gets a 0!!".format(hashtag))
            log.error("# # # #{}".format(ex2))
            return 0

    return sample


def batch_getHashTagPostCount(hashTagList, no_of_threads=4):
    # a multithreaded version of "getHashTagPostCount"
    processPool = mp.Pool(processes=no_of_threads)
    try:
        hashCount = processPool.map(getCountOfHashtagPosts, hashTagList)
    except Exception as e:
        log.error('batch_getHashTagPostCount: failed to get counts because {}'.format(e))
        return -1

    # create the dataFrame
    d = datetime.datetime.utcnow()
    d = pd.to_datetime(d)
    dateList = []
    for i in hashCount:
        dateList.append(d)
    df = pd.DataFrame({'hashtag': hashTagList, 'count of posts': hashCount, "Time Stamp": dateList})

    return df


def findAll_TXT_CSV_Files_pathsToList(path, filetype='txt'):
    # navigate to folder where all stored txt files are
    os.chdir(path)
    # create a list with all the .txt file paths
    paths = []
    for file in glob.glob("*." + filetype):
        paths.append(path + file)
    paths.sort()

    return paths


def readHashtagsFromTXTFile(inputFilepath):
    # get input hashtags from a txt file read into a list no matter how they are layed out in the file.
    f = open(inputFilepath, "r")
    hashTag = []
    for line in f:

        if "#" in line:
            a = line.strip('\u2060\n').split(' ')

            for i in a:
                b = i.split("#")
                for j in b:
                    hashTag.append(j.strip("\u2063").strip("\u2060"))
    hashTag = list(filter(lambda x: x != "", hashTag))
    hashTag = list(dict.fromkeys(hashTag))

    return hashTag


def readHashCountFileToDataFrame(filename):
    # get data from csv file to a pandas dataframe
    try:
        data = pd.read_csv(filename, parse_dates=True, dtype={'hashtag': str, 'count of posts': int})
    except Exception as e:
        log.error(e)

    return data


def form_Hashtag_Research_List_final(photoName):
    # Create root photo directory
    createFolder(getYourPaths(photoName)['photoName_Dir'])
    createFolder(getYourPaths(photoName)['researchList_Dir'])

    # Get Category files
    inputFilepaths_0 = findAll_TXT_CSV_Files_pathsToList(paths['input'])
    categoryCleared = []

    if (len(inputFilepaths_0) > 0) & (len(inputFilepaths_0) > len(categoryCleared)):
        for input_file_path in inputFilepaths_0:
            hashTag_Category = input_file_path[len(paths['input']):len(input_file_path) - 4]
            researchListCSV = getYourPaths(photoName)['researchList_Dir'] + 'researchHashtags_{}.csv'.format(
                hashTag_Category)

            # Create hashTag category sub-directories
            samplesDirectory = getYourPaths(photoName)['photoName_Dir'] + hashTag_Category + "_samples/"
            createFolder(samplesDirectory)

            if os.path.isfile(researchListCSV):
                print("File {} exists".format('researchHashtags_{}.csv'.format(hashTag_Category)))
                categoryCleared.append(input_file_path)
                continue
            else:
                # get seed list and check for duplicates
                seedList = readHashtagsFromTXTFile(input_file_path)
                seedList = list(dict.fromkeys(seedList))  # remove duplicates

                # get first round of similar hastags as per Instagrams suggestions
                log.error('Similars list 1 start for {}'.format(hashTag_Category))

                expandedList = batch_getListOfSimilarHashtags(seedList)
                log.error('Similars list end: ' + str(len(expandedList)) + ' hashTags found')
                grandList = seedList + expandedList
                grandList = list(dict.fromkeys(grandList))  # remove duplicates

                # expandedList2 = batch_getListOfSimilarHashtags(grandList)
                # log.error('Similars list 2 end: ' + str(len(expandedList2)) + ' hashTags found')
                # grandList = grandList + expandedList2
                # grandList = list(dict.fromkeys(grandList))  # remove duplicates

                # PointA: Check Which tags have a post count over, or under
                # a set threshold, remove them from the original df and look for alternatives
                try:
                    log.error('Point A: getting counts for {} hastags'.format(str(len(grandList))))
                    df = batch_getHashTagPostCount(grandList)
                    dfoverThreshold = df[df['count of posts'] > cutOffvalues['postUpperCOunt']]
                except Exception as e:
                    log.error('Research list creation for {0} failed at point A'.format(hashTag_Category))
                    continue

                dfoverThreshold = dfoverThreshold.sort_values(by=['count of posts'], ascending=False)
                dfoverThreshold = dfoverThreshold.head(3)
                df = df[df['count of posts'] < cutOffvalues['postUpperCOunt']]
                df = df[df['count of posts'] > cutOffvalues['postLowerCount']]

                print('{0} df count: {1} '.format(hashTag_Category, str(df['hashtag'].count())))
                try:
                    grandList2 = df['hashtag'].tolist()  # + alternativeHashTags
                    grandList2 = list(dict.fromkeys(grandList2))  # check for duplicates
                except Exception as e:
                    print(e)

                final_DataFrame = pd.DataFrame({'hashtag': grandList2})

                final_DataFrame.to_csv(researchListCSV, index=False, encoding='utf-8')
        return False
    else:
        print('~~Sample List Formation: Huh? Are there any new input files in {0} ?'.format(paths['input']))
        log.error('~~Sample List Formation: Huh? Are there any new input files in {0} ?'.format(paths['input']))
        return False


def getSamples(photoName):
    timestamp = datetime.datetime.now().strftime('%Y_%m_%d %H-%M')
    start_time = time.time()
    waitTime = 0

    # retrieve reasearch material: lists of hashtags to sample
    researchInputDirectory = getYourPaths(photoName)['researchList_Dir']
    researchListFilePaths = findAll_TXT_CSV_Files_pathsToList(researchInputDirectory, 'csv')
    if len(researchListFilePaths) > 1:
        waitTime = 1 * 60

    for csv_file in researchListFilePaths:
        # output location getYourPaths(photoName)['photoName_Dir']
        hashTag_Category = csv_file[(len(researchInputDirectory) + 17):-4]
        sampleOutputDirectory = getYourPaths(photoName)['photoName_Dir'] + hashTag_Category + "_samples/"

        researchList = pd.read_csv(csv_file)['hashtag'].tolist()

        log.error('Getting sample for {0} hashtags in {1}_{2}'.format(str(len(researchList)),
                                                                      photoName,
                                                                      hashTag_Category))

        sample_frame = batch_getHashTagPostCount(researchList)
        sample_frame.to_csv(sampleOutputDirectory + photoName + hashTag_Category + '_{0}.csv'.format(timestamp),
                            index=False,
                            encoding='utf-8')
        log.error(
            'Just got a sample for {0} hashtags in {1}_{2}'.format(str(len(researchList)),
                                                                   photoName,
                                                                   hashTag_Category))

        rate = ((time.time() - start_time) / len(researchList))
        log.error(' at a rate of {} secs/tag'.format(str(round(rate, 2))))
        sleep(waitTime)

    log.error('{} -- Sample Round ended'.format(photoName))
    log.error('------------------------------------------')


def runHastagStats(photoName):
    averageNewPostsRateLowerThreshold = 0.01
    start_time = time.time()

    researchInputDirectory = getYourPaths(photoName)['researchList_Dir']
    researchLists = findAll_TXT_CSV_Files_pathsToList(researchInputDirectory, 'csv')

    hashTag_Categories = []
    for researchList in researchLists:
        hashTag_Categories.append(
            researchList[(len(getYourPaths(photoName)['researchList_Dir']) + 17):len(researchList) - 4])

    # create a dataframe with all samples
    for category in hashTag_Categories:
        directoryOfSamples = getYourPaths(photoName)['photoName_Dir'] + category + "_samples/"
        samplesLists = findAll_TXT_CSV_Files_pathsToList(directoryOfSamples, 'csv')
        samplesLists.sort()

        # Do not bother with this category if there are no samples
        if samplesLists == 0:
            continue

        tags_List = pd.read_csv(samplesLists[0])['hashtag'].tolist()
        tagMasterFrame = pd.DataFrame(columns=["hashtag", "count of posts", "Time Stamp"])
        outputFrame = pd.DataFrame(
            columns=["hashtag", "count_of_posts", "Posts_per_Minute", "HashTag_Saturation", "HashTag_Score"])

        # Compose a masterFrame containing all the samples gathered
        for listCSV in samplesLists:
            CSVfileFrame = pd.read_csv(listCSV)
            tagMasterFrame = pd.concat([tagMasterFrame, CSVfileFrame])

        tagMasterFrame['Time Stamp'] = pd.to_datetime(tagMasterFrame['Time Stamp'])

        # Calculate per tag metrics and form a new row to append to the outputFrame
        for tag in tags_List:
            subFrame = tagMasterFrame[tagMasterFrame['hashtag'] == tag]

            # if for some reason a tag has less posts than the
            # minimum number at the latest sample (iloc[-1]) then skip it
            if subFrame['count of posts'].iloc[-1] < cutOffvalues['postLowerCount']:
                continue

            subFrame.set_index('Time Stamp', inplace=True)

            # Calculate posts per minute metric
            dtBase = pd.Series(subFrame.index).diff().dt.components
            dt = (dtBase.seconds.values / 60) + dtBase.minutes.values + \
                 (dtBase.hours.values * 60) + \
                 (dtBase.days.values * 60 * 24)
            dC = subFrame["count of posts"].diff()
            dCdt = dC.div(dt, axis=0)
            avg_dCdt = dCdt.mean()  # this is the final product

            # Compose row list to append to outputFrame
            tagRow_list = []
            tagRow_list.append('#' + tag)  # [0]hashtag
            tagRow_list.append(subFrame["count of posts"].iloc[-1])  # [1]count
            tagRow_list.append(avg_dCdt)  # [2]ppm
            # (1 - (countUpperThreshold - outputDF['count of posts']) / (countUpperThreshold))
            tagRow_list.append(
                1 - (cutOffvalues['postUpperCOunt'] - tagRow_list[1]) / cutOffvalues[
                    'postUpperCOunt'])  # [3]saturation
            if tagRow_list[2] > 0:
                tagRow_list.append(tagRow_list[3] - math.sqrt(tagRow_list[2]))
            else:
                tagRow_list.append(0)

            # Update output frame with new row data
            outputFrame = addNewRow_toDataFrame(outputFrame, tagRow_list)

        outputFrame = outputFrame.sort_values(by=['HashTag_Score'], ascending=False)
        # full output Frame
        fullStatsPath = getYourPaths(photoName)['photoName_Dir'] + 'fullStats/'
        createFolder(fullStatsPath)
        outputFrame.to_csv(fullStatsPath + category + "_statsFull.csv",
                           index=False, encoding='utf-8')

        # strict output Frame
        outputFrame = outputFrame[outputFrame["Posts_per_Minute"] < 0.25]
        outputFrame = outputFrame[outputFrame["HashTag_Score"] > 0.1]
        outputFrame.to_csv(getYourPaths(photoName)['photoName_Dir'] + category + "_statsStrict.csv",
                           index=False, encoding='utf-8')
        print('Stats for {0} done'.format(category))

    elapsed_time = time.time() - start_time
    print('Stats for {0} done: Elapsed time is {1} secs'.format(photoName, elapsed_time))
