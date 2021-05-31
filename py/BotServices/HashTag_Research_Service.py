def getHashTagList(bot):
    pass


def getPostCounts(bot, hashtagList):
    countsDict = {}
    for tag in hashtagList:
        count = bot.mainPage.topRibbon_SearchField.getHashTagPostCountThroughSearch(tag)
        print(count)

    return countsDict


def compileCategoryStats():
    pass
