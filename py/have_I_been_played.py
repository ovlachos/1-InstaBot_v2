import InstaFameBot
import auth
import pandas as pd
from datetime import datetime, timedelta
import os


def haveIbeenPlayed(today=True, date=0):
    helper = InstaFameBot.HelperBot()

    # Define starting date in case you have missed running this for a day
    startDate = datetime.today()
    if not today:
        startDate = datetime.strptime(date, "%Y_%m_%d")

    dateList = []
    today = 0
    for i in range(0, 8):
        dateList.append((startDate - timedelta(days=i)).strftime("%Y_%m_%d"))

    theScum_mainFrame = pd.read_csv(InstaFameBot.file_paths.theScumMainCSV)
    todaysRow_Scum = helper.getFolowershipRowList_byDate(theScum_mainFrame, dateList[0])
    yesterdaysRow_Scum = helper.getFolowershipRowList_byDate(theScum_mainFrame, dateList[1])

    whoJumpedShip_list = [x for x in todaysRow_Scum if x not in yesterdaysRow_Scum]

    followers_mainFrame = pd.read_csv(InstaFameBot.file_paths.myStats_FolowersCSV)
    past_followers = helper.getFolowershipRowList_byDate(followers_mainFrame, dateList[1]) \
                     + helper.getFolowershipRowList_byDate(followers_mainFrame, dateList[2]) \
                     + helper.getFolowershipRowList_byDate(followers_mainFrame, dateList[3]) \
                     + helper.getFolowershipRowList_byDate(followers_mainFrame, dateList[4])

    past_followers = list(dict.fromkeys(past_followers))

    whoUnfollowed = [z for z in helper.getFolowershipRowList_byDate(followers_mainFrame, dateList[today + 1]) if
                     z not in helper.getFolowershipRowList_byDate(followers_mainFrame, dateList[today])]
    whoJumpedShip_list = [y for y in whoJumpedShip_list if y in past_followers]

    if len(whoUnfollowed) > 0:
        unfollow_report_frame = pd.DataFrame(whoUnfollowed)
        unfollow_report_frame.columns = [dateList[today]]
        unfollow_report_frame.to_csv(InstaFameBot.file_paths.myStats + 'unfollowReport' + dateList[today] + '.csv',
                                     index=False, encoding='utf-8')

    if len(whoJumpedShip_list) > 0:
        overBoard_frame = pd.DataFrame(whoJumpedShip_list)
        overBoard_frame.columns = [dateList[0]]
        overBoard_frame.to_csv(InstaFameBot.file_paths.mutineers + 'mutineers_' + dateList[0] + '.csv',
                               index=False, encoding='utf-8')
        whatTosay = 'yep... {0} suspects to check'.format(len(whoJumpedShip_list))
        return whatTosay
    else:
        return "nah, so far, so good!"


def main():
    haveIbeenPlayed()


if __name__ == '__main__':
    main()
