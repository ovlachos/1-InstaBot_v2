from time import sleep


def love(bot, loveType='extra', numberOfLikes=1, percentageOfUsers=0.501):
    print("\n")
    print("### theLoveDaily ~ Extra ###")
    print("\n")
    # 'Like' everyone's latest N posts
    print(f"### ~~> Now processing the {loveType} list with {numberOfLikes} likes/user going for {(percentageOfUsers * 100)}%")

    bot.mainPage.driver.refresh()

    # Sorted by date last checked
    # Least recently checked profiles come first
    userLoveList = getList(bot, loveType)

    userLoveList = sorted(userLoveList, key=lambda User_M: User_M._dateTimeLovedlast)

    loveTotal = len(userLoveList)
    loveCount = loveTotal
    print(f'#### {int(percentageOfUsers * loveTotal)} of {loveTotal} users to love')

    # Go through the list line by line and like things
    printMark = 0.0
    userNotFound_counter = 0
    for user in userLoveList:
        printMark = printCompletionRate(loveCount, loveTotal, printMark)

        if (loveTotal - loveCount) > (loveTotal * percentageOfUsers):
            break

        if user.printHowLongItHasBeenSinceYouGotAnyLove() <= bot.timeLimitSinceLastLoved:
            continue

        # Navigate to user's profile
        userPage = bot.mainPage.topRibbon_SearchField.navigateToUserPageThroughSearch(user.handle)

        user.updateTimelastLoved()

        if not userPage:
            print(f"###### User {user.handle} cannot be found")
            # bot.memoryManager.userPageCannotBeFound(user)
            #
            # userNotFound_counter += 1
            # if userNotFound_counter > 5:
            #     if bot.internetConnectionLost():
            #         return "No Internet"
            continue

        loveCount -= 1

        # Remove user from love if there is no point in liking his posts (or no access for doing so)
        if user.thereIsNoPointLovingYou(userPage):
            bot.memoryManager.updateUserRecord(user)
            continue

        # Check if we have new post since last time
        # Move to next user if there are no new posts since last check
        if user.getLatestPostCount() >= userPage.stats['posts']:
            user.updateInfoFromLivePage_Landing(userPage)
            bot.memoryManager.updateUserRecord(user)
            continue

        # Adjust number of likes to just new posts
        numberOfLikes = adjustNoOfLikes(numberOfLikes, user, userPage)

        user.updateInfoFromLivePage_Landing(userPage)  # a note on userName changes and fuzzyLookup:
        # If I manage to navigate to a userPage with a similar but not exactly
        # the same usrename as my query, then this new username will ovwrwrite the old
        # one in the db. This could be a mistake as a user that changed his name from Maria.98
        # to blacksofa will get mached to a completely unrelated user (e.g. mar.i.a.97).
        # So maybe a data validation check should be in place: does the new user have roughly the same stats?

        # Liking photos
        response = likeTheXlatestPostsOfAUser(userPage, numberOfLikes)
        if 'busted' in response:
            return 'busted'

        bot.memoryManager.updateUserRecord(user)

        bot.botSleep()

    print("\n### theEnd ###")
    return 'OK'


def likeTheXlatestPostsOfAUser(userPage, numberOfLikes):
    if userPage.infoAccess < 45:
        for i in range(0, numberOfLikes):
            try:
                response = None

                post = userPage.navigateTo_X_latestPost(i)

                if post:
                    sleep(1)
                    response = post.like_post()
                    post.close_post()
                    sleep(1)

                if response:
                    print("#### Like pressed on user {0}".format(userPage.userName))

                    if not isinstance(response, bool):
                        return 'busted'

                elif post and not response:
                    return 'OK'

                sleep(1)
            except Exception as e:
                print(e)
                continue

    return "OK"


def adjustNoOfLikes(numberOfLikes, user, userPage):
    if int(userPage.stats['posts'] - user.getLatestPostCount()) < numberOfLikes:
        numberOfLikes = int(userPage.stats['posts'] - user.getLatestPostCount())
    return numberOfLikes


def printCompletionRate(loveCount, loveTotal, printMark):
    completionRate = round(100 * (1 - (loveCount / loveTotal)), 1)
    if completionRate > printMark:
        print('\n#### ~> {}% of 100% completed\n'.format(printMark))
        printMark += 5

    return printMark


def getList(bot, loveType):
    bot.memoryManager.readMemoryFileFromDrive()

    if "daily" in loveType:
        return bot.memoryManager.getDailyLoveList()
    else:
        bot.memoryManager.redistributeExtraLove()
        return bot.memoryManager.getExtraLoveList()
