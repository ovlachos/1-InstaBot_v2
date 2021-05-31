from time import sleep


def boostLatestPost(bot, numberOfTags, numberOfPostsPerTag):
    print("\n")
    print("### PostBooster ###")
    print("\n")

    bot.mainPage.driver.refresh()

    myPage = bot.mainPage.topRibbon_myAccount.navigateToOwnProfile()
    sleep(2)
    mylatestPost = myPage.navigateTo_X_latestPost(0)
    sleep(2)
    mylatestPost.updateHashTagsUsed()
    sleep(2)
    hashList = mylatestPost.hashTagsUsed
    sleep(2)
    mylatestPost.close_post()

    if hashList:
        hashList = hashList[:numberOfTags]
        print(f"Today's hashtags are: {hashList}")

    for hashtag in hashList:

        hashPage = bot.mainPage.topRibbon_SearchField.navigateToHashTagPageThroughSearch(hashtag)

        if not hashPage:
            continue

        sleep(3)

        print(f"### HashTag: {hashPage.hashtag}")

        response = likeThe_X_mostRecentPostsUnderHashtag(hashPage, numberOfPostsPerTag, bot.mainPage.page.sendESC, bot)
        if 'busted' in response:
            return 'busted'

        bot.botSleep(1.2)

    print("\n### theEnd ###")
    return 'OK'


def likeThe_X_mostRecentPostsUnderHashtag(hashTagPage, numberOfPostsPerTag, escapeFunc, bot):
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

                bot.botSleep()
            elif postExists:
                return 'OK'
            elif not postExists:
                escapeFunc()


        except Exception as e:
            print(f"Like the {i}th post failed: {e}")
            continue

    return "OK"
