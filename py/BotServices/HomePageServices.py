def homePagePostScrolling(bot, numberOfPosts):
    homePage = bot.mainPage.topRibbon_myAccount.goHomeWhereYouAreSafe_u()

    for post in range(0, numberOfPosts):
        homePage.likeCurrentPost()
        homePage.scrollNextPostIntoView()


def homePageStoryWatching(bot, numberOfStories):
    homePage = bot.mainPage.topRibbon_myAccount.goHomeWhereYouAreSafe_u()

    for post in range(0, numberOfStories):
        homePage.startWatchingStories(numberOfStories)
