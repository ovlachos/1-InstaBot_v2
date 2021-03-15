from time import sleep


def boostLatestPost(bot, numberOfTags, numberOfPostsPerTag):
    print("\n")
    print("### PostBooster ###")
    print("\n")

    myPage = bot.mainPage.topRibbon_myAccount.navigateToOwnProfile()

    mylatestPost = myPage.navigateTo_X_latestPost(0)
    mylatestPost.updateHashTagsUsed()
    hashList = mylatestPost.hashTagsUsed
    mylatestPost.close_post()

    if hashList:
        hashList = hashList[:numberOfTags]

    for hashtag in hashList:

        hashPage = bot.mainPage.topRibbon_SearchField.navigateToHashTagPageThroughSearch(hashtag)

        print(f"### HashTag: {hashPage.hashtag}")

        response = likeThe_X_mostRecentPostsUnderHashtag(hashPage, numberOfPostsPerTag)
        if 'busted' in response:
            return 'busted'

        bot.botSleep()

    print("\n### theEnd ###")
    return 'OK'


def likeThe_X_mostRecentPostsUnderHashtag(hashTagPage, numberOfPostsPerTag):
    for i in range(0, numberOfPostsPerTag):
        try:
            post = hashTagPage.navigateTo_X_mostRecentPosts(i)
            sleep(1)
            response = post.like_post()
            post.close_post()
            sleep(1)

            if response:
                print("#### Like pressed on hashTag {0}".format(hashTagPage.hashtag))

                if not isinstance(response, bool):
                    return 'busted'

        except Exception as e:
            print(e)
            continue

    return "OK"
