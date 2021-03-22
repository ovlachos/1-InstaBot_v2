from time import sleep


def boostLatestPost(bot, numberOfTags, numberOfPostsPerTag):
    print("\n")
    print("### PostBooster ###")
    print("\n")

    bot.mainPage.driver.refresh()

    myPage = bot.mainPage.topRibbon_myAccount.navigateToOwnProfile()
    sleep(1)
    mylatestPost = myPage.navigateTo_X_latestPost(0)
    sleep(1)
    mylatestPost.updateHashTagsUsed()
    sleep(1)
    hashList = mylatestPost.hashTagsUsed
    sleep(1)
    mylatestPost.close_post()

    if hashList:
        hashList = hashList[:numberOfTags]
        print(f"Today's hashtags are: {hashList}")

    for hashtag in hashList:

        hashPage = bot.mainPage.topRibbon_SearchField.navigateToHashTagPageThroughSearch(hashtag)
        sleep(1)
        bot.mainPage.driver.refresh()
        sleep(1)

        print(f"### HashTag: {hashPage.hashtag}")

        response = likeThe_X_mostRecentPostsUnderHashtag(hashPage, numberOfPostsPerTag, bot.mainPage.page.sendESC)
        if 'busted' in response:
            return 'busted'

        bot.botSleep(1.2)

    print("\n### theEnd ###")
    return 'OK'


def likeThe_X_mostRecentPostsUnderHashtag(hashTagPage, numberOfPostsPerTag, escapeFunc):
    for i in range(0, numberOfPostsPerTag):
        try:
            post = hashTagPage.navigateTo_X_mostRecentPosts(i)

            sleep(1)
            liked = post.like_post()
            postExists = post.close_post()
            sleep(1)

            if liked:
                print("#### Like pressed on hashTag {0}".format(hashTagPage.hashtag))

                if not isinstance(liked, bool):
                    return 'busted'

            elif postExists:
                return 'OK'
            elif not postExists:
                escapeFunc()


        except Exception as e:
            print(e)
            continue

    return "OK"
