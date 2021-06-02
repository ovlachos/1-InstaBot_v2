def homePagePostScrolling(bot, numberOfPosts):
    homePage = bot.mainPage.topRibbon_myAccount.goHomeWhereYouAreSafe_u()

    print(f"I'll just scroll through a few homepage posts, like {numberOfPosts} of them")

    for post in range(0, numberOfPosts):
        homePage.likeCurrentPost()
        homePage.scrollNextPostIntoView()

    print(f"### theEnd ###")


def homePageStoryWatching(bot, numberOfStories):
    homePage = bot.mainPage.topRibbon_myAccount.goHomeWhereYouAreSafe_u()

    print(f"I'll just watch a few stories, like {numberOfStories} of them")

    homePage.startWatchingStories(numberOfStories)

    print(f"### theEnd ###")
