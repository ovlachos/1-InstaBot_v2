import InstaBotV2
from BotMemory import FileHandlerBot as fb
import csv

bot = InstaBotV2.InstaBot()
aProfile = bot.mainPage.topRibbon_SearchField.navigateToUserPageThroughSearch('katsikis')

################################################################################################
################################################################################################

# bot = InstaBotV2.InstaBot()
# myProfile = bot.mainPage.topRibbon_myAccount.navigateToOwnProfile()
# myFollowers = myProfile.getFollowersList()
# myFollowing = myProfile.getFollowingList()

# fileBot = fb.FileHandlerBot()
# dailyList_F = fileBot.CSV_getFrameFromCSVfile('dailyLoveCSV')
# dailyList = dailyList_F[dailyList_F.columns[0]].tolist()
#
# extraList_F = fileBot.CSV_getFrameFromCSVfile('extraLoveCSV')
# extraList = extraList_F[extraList_F.columns[0]].tolist()
#
# listFrame = fileBot.CSV_getFrameFromCSVfile('theList_1_fileCSV')
# listList = listFrame[listFrame.columns[1]].tolist()
# listList2 = listFrame[listFrame.columns[1]].tolist()
# # theList_1_fileCSV
#
# listsOverlap = [[x for x in dailyList if x in extraList]]
# inList = [x for x in listList if x in dailyList]
# notInList = [x for x in dailyList if x not in listList]
#
# inList_f = [inList]
# notInList_f = [notInList]
#
# pathLove = fileBot.projectFolder + fileBot.paths['love']
#
# if 'tattooartwork.kimberlyalvarado' in listList:
#     print('tattooartwork.kimberlyalvarado')
#
# with open(pathLove + "overlap.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerows(listsOverlap)
#
# with open(pathLove + "inList.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerows(inList_f)
#
# with open(pathLove + "NotInList.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerows(notInList_f)
################################################################################################
################################################################################################
