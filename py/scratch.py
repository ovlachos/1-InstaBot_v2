import random
import time

import pandas as pd
from setuptools.package_index import unique_everseen

import InstaFameBot
import auth
import selenium
import sys
from datetime import datetime
from dateutil.parser import parse

# Cleans Up The Daily love list from those who receive extra love
# extralove = pd.read_csv(InstaFameBot.file_paths.extraLoveCSV)
# extralove_List = extralove['t2_theLoveDaily'].tolist()
#
# regularlove = pd.read_csv(InstaFameBot.file_paths.theDailyLoveCSV)
# regularlove_List = regularlove['t2_theLoveDaily'].tolist()
#
# regularlove_List_clean = [x for x in regularlove_List if x not in extralove_List]
# regularLove_clean = pd.DataFrame(regularlove_List_clean)
# regularLove_clean.columns = ['t2_theLoveDaily']
# regularLove_clean.to_csv(InstaFameBot.file_paths.inputs + 'cleanRegularLove.csv', index=False, encoding='utf-8')


# war_start = '_2011-01-03'
# war_end = '_2013-05-23'
#
# first_attempt_start = datetime.strptime(war_start, '_%Y-%m-%d')
# war_end_dateTime = datetime.strptime(war_end, '_%Y-%m-%d')
# dt_days = war_end_dateTime.date() - first_attempt_start.date()
# tt = 0


# ## PUUUUUURGEEEEE!!!!
# botbot = InstaFameBot.InstaBot(auth.username, auth.password)
# botbot.tH_logIn()
# botbot.t2_purgeUsers()
# botbot.tH_logOut()
# botbot.tH_close_browser()
# # botbot.tH_resetRouter()
#
# import NoLogIn_getHashTagOrProfileInfo
# NoLogIn_getHashTagOrProfileInfo.getProfileStatsDict('myrpap')


# Scraped Hashtag Stats
# outPath = '/Users/cortomaltese/Google Drive/10 Projects/1 Insta-Fame WebScraper/instaBot/Outputs/hashtags_followersihp_stats_FREQ.csv'
# filePath = InstaFameBot.file_paths.hashtagFollowershipStatsCSV
# statsFrame = pd.read_csv(filePath)
# hashList = []
# for i in range(2, 150):
#     hashList.append(statsFrame.iloc[:, i].tolist())
#
# finalList = []
# for li in hashList:
#     for htag in li:
#         if 'nan' not in str(htag):
#             finalList.append(htag)
#
# finalFrame = pd.DataFrame(finalList)
# finalListFreq = pd.crosstab(index=finalFrame.iloc[:, 0], columns="count")
# finalListFreq.to_csv(outPath, index=True, encoding='utf-8')

# to Love MAYBE
# date = datetime.now().strftime('%Y_%m_%d')
# following = pd.read_csv(
#     '/Users/cortomaltese/Google Drive/10 Projects/1 Insta-Fame WebScraper/instaBot/Outputs/MyStats/myFollow_ing{}.csv'.format(
#         date))
# following_list = following[date].tolist()
# loving = pd.read_csv(
#     '/Users/cortomaltese/Google Drive/10 Projects/1 Insta-Fame WebScraper/instaBot/Inputs/theLoveDaily.csv')
# lovingList = loving['theLoveDaily'].tolist()
# intersection = [x for x in following_list if x not in lovingList]
# in_Frame = pd.DataFrame(intersection)
# in_Frame.to_csv('/Users/cortomaltese/Google Drive/10 Projects/1 Insta-Fame WebScraper/instaBot/Inputs/toLoveMaybe.csv',
#                 index=False, encoding='utf-8')
# t = 0

# botbot = InstaFameBot.InstaBot(auth.username, auth.password)
# botbot.tH_close_browser()
# botbot.tH_removeUserFrom_theLoveDaily('katsikis')


### Compare Two followers/following cvs files
# dateCol1 = '2020_06_26'
# dateCol2 = '2020_06_16'
# type = 'myFollowers'  # 'myFollowers', 'myFollow_ing'
#
# followersPath1 = '/Users/cortomaltese/Google Drive/10 Projects/1 Insta-Fame WebScraper/instaBot/Outputs/MyStats/{0}{1}.csv'.format(
#     type, dateCol1)
# followersPath2 = '/Users/cortomaltese/Google Drive/10 Projects/1 Insta-Fame WebScraper/instaBot/Outputs/MyStats/{0}{1}.csv'.format(
#     type, dateCol2)
#
# fdf1 = pd.read_csv(followersPath1)
# fdf2 = pd.read_csv(followersPath2)
# fdf1_list = fdf1[dateCol1].tolist()
# fdf2_list = fdf2[dateCol2].tolist()
# answer = [x for x in fdf2_list if x not in fdf1_list]
# print(answer)


# Only Fans
# bot = InstaFameBot.InstaBot(auth.username, auth.password)
# bot.tH_logIn()
# bot.t2_fansOnly(90)
# t = 0

### Manually add people to theGame
# 1) Get a list of profiles
# 2) add a new row to theList_1 csv file for each user with a follow date of today

### Manually remove people from the loveDaily
# bot = InstaFameBot.InstaBot(auth.username, auth.password)
# list = ['annsophievanderschueren', 'nickk1253']
# for user in list:
#     bot.tH_removeUserFrom_theLoveDaily(user)


## Testing post Velocity
# noOfLatestPosts = 2
# start = 2
# end = 50
#
# bot = InstaFameBot.InstaBot(auth.username, auth.password)
# bot.tH_logIn()
# lovedOnes_frame_old2 = pd.read_csv(InstaFameBot.file_paths.theDailyLoveCSV)
# lovedOnes_list = lovedOnes_frame_old2['theLoveDaily'].tolist()
# listOfVelocity = []
# lovedOnes_list = lovedOnes_list[start:end]
#
# for love in lovedOnes_list:
#     rowIndexOfUser = lovedOnes_frame_old2[lovedOnes_frame_old2.theLoveDaily == love].index.values[0]
#     vel = bot.t1_get_UserPosting_Velocity(love, noOfLatestPosts)
#     if vel == bot.tooManyActionsBreakCode:
#         vel = 666
#     print('{0} posts p/d for user {1}'.format(str(vel), love))
#     lovedOnes_frame_old2.iloc[rowIndexOfUser, 3] = vel
#     listOfVelocity.append([love, vel])
#
# print(listOfVelocity)
# lovedOnes_frame_old2.to_csv(InstaFameBot.file_paths.theDailyLoveCSV, index=False, encoding='utf-8')
# t = 0


## Migrating to full dataframe usage - Merge L-0 and L-1
# l1_csv = pd.read_csv(
#     '/Users/cortomaltese/Google Drive/10 Projects/1 Insta-Fame WebScraper/instaBot/Outputs/TheList_1.csv')
# l0_csv = pd.read_csv(
#     '/Users/cortomaltese/Google Drive/10 Projects/1 Insta-Fame WebScraper/instaBot/Outputs/TheList_0.csv')
# print("Given Dataframe 1:\n\n", l1_csv)
# print("Given Dataframe 0:\n\n", l0_csv)
#
# l1_a1_list = l1_csv['a1_User'].tolist()
# for index, row in l0_csv.iterrows():
#     # print('~~ {0}'.format(row["a1_User"]))
#     if row["a1_User"] not in l1_a1_list:
#         print('User {0} is going in!'.format(row["a1_User"]))
#         new_row = {'a0_User_a1_follows': row["a0_User_a1_follows"],
#                    'a1_User': row["a1_User"],
#                    'a2_Count_of_Followers_of_a1': '',
#                    'a3_TheList_1_keep_drop': '',
#                    'a4_TheList_2_keep_drop': '',
#                    'a5_TheList_3_keep_drop': '',
#                    'a6_theGame_Follow_Date': '',
#                    'a7_theGame_UnFollow_Date': ''}
#         # append row to the dataframe
#         l1_csv = l1_csv.append(new_row, ignore_index=True)
#
# l1_csv = l1_csv.drop_duplicates(subset='a1_User')
# l1_csv = l1_csv.sort_values('a0_User_a1_follows', ascending=True)  # f = df.sort_values('Age', ascending=False)
# l1_csv.to_csv(
#     '/Users/cortomaltese/Google Drive/10 Projects/1 Insta-Fame WebScraper/instaBot/Outputs/TheList_1_to_be.csv',
#     index=False, encoding='utf-8')
# t = 0