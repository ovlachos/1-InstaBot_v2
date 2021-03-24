def userScraping(bot, userCount):
    print("\n")
    print("### theL1-L2 ###")
    print("\n")

    # Read User Memory
    bot.memoryManager.readMemoryFileFromDrive()
    bot.memoryManager.manuallyAddNewUsersTo_theGame()
    bot.mainPage.driver.refresh()

    # Filter users down to L0
    usersL0 = bot.memoryManager.getListOfMarkedUsers(0)

    # Get people already following me and remove them
    myFollowersCount = 1130  # indicative 2021/03/14
    # try:
    #     myPage = bot.mainPage.topRibbon_myAccount.navigateToOwnProfile()
    #
    #     if not myPage:
    #         raise RuntimeError
    #
    #     myFollowers = myPage.getFollowersList()
    #     myFollowersCount = myPage.stats['followers']  # TODO: Record my latest stats into my profile's memory file
    #
    #     usersL0 = [x for x in usersL0 if x.handle not in myFollowers]
    #
    # except Exception as e:
    #     print(e)

    # Bring users with relevant usernames to the top of the list, that they may be examined first
    usersL01 = [x for x in usersL0 if checkHandle(bot.words, x.handle) or x._markL2]
    usersL0 = moveListOfUsersToTop(usersL0, usersL01)

    # move manual additions to theGame to the top of the list
    fileOfGameParticipants = bot.fileHandler.CSV_getFrameFromCSVfile('addUserTotheGameCSV')['userToAdd'].tolist()  # list of handles
    usersL02 = [x for x in usersL0 if x.handle in fileOfGameParticipants]
    usersL0 = moveListOfUsersToTop(usersL0, usersL02)

    # reduce the number of accounts to be examined, to the first N number of accounts
    print(f"### {len(usersL0)} users still to be examined")
    usersL0 = usersL0[:userCount]

    user_counter = 0
    userNotFound_counter = 0
    for user in usersL0:

        userPage = bot.mainPage.topRibbon_SearchField.navigateToUserPageThroughSearch(user.handle)

        if not userPage:
            bot.memoryManager.userPageCannotBeFound(user)

            userNotFound_counter += 1
            if userNotFound_counter > 5:
                if bot.internetConnectionLost():
                    return "No Internet"
            continue

        user.updateInfoFromLivePage_Landing(userPage)

        ### L1 ###
        user = userHasMoreThan_X_followers(myFollowersCount, user)

        ### L2 ###
        if user._markL1:

            if not user._markL2:
                user = L2(user, userPage, bot.words, bot.targetHashtags_List)

            ### Follow on the spot if the user is an L2 and there's still mana left.
            if user.iShouldFollowThisUser() and bot.followMana > 0:
                if 'OK' in userPage.follow():
                    user.markTimeFollowed()
                    user.addToLoveDaily()
                    bot.followMana = bot.followMana - 1
                    user_counter += 1
                    print(f"#### {user_counter} people followed so far")

        bot.memoryManager.updateUserRecord(user)
        if user.dateFollowed_byMe:
            bot.botSleep()

    print(f"#### {user_counter} people followed this time around")
    print("\n### theEnd ###")
    return 'OK'


def moveListOfUsersToTop(originalList, usersToMove):
    for user in usersToMove:
        originalList.insert(0, originalList.pop(originalList.index(user)))

    return originalList


def userHasMoreThan_X_followers(followerCountLimit, user):
    # Filter out users with more followers than myself - aka L1
    userLatestStats = user.getLatestStats()

    if userLatestStats['followers'] > (1.05 * followerCountLimit):
        wording = 'Dropping'
    elif userLatestStats['followers'] < 100:
        wording = 'Dropping'
    elif userLatestStats['posts'] < 3:
        wording = 'Dropping'
    else:
        wording = 'Keeping'

    if "Dropping" in wording:
        user.markUserRejected()
    else:
        user.addToL1()

    print(f"#### L1 - {wording} user: {user.handle} has {userLatestStats['followers']} followers and {userLatestStats['posts']} posts")

    return user


def L2(user, userPage, words, targetHashtags_List):
    # Check if the user has declared an interest to something
    wording = 'Dropping'

    # Check in the username, alt name and bio
    if checkProfile(words, userPage):
        user.addToL2()
        wording = 'Keeping'

    # Check the hashtags the user follows
    hashtags = []
    hashtagsUsing = []
    try:
        hashtags = userPage.getHashtagsFollowingList()
        user.updateHashtagsFollowingList(hashtags)

        for x in range(0, 3):
            post = userPage.navigateTo_X_latestPost(x)
            post.updateHashTagsUsed()
            hashtagsUsing.extend(post.hashTagsUsed)
            post.page.sleepPage(1)
            post.close_post()

        user.updateHashtagsUsing(hashtagsUsing)
        hashtags.extend(hashtagsUsing)

    except Exception as e:
        print(e)

    if checkHashTags(hashtags, words, targetHashtags_List):
        user.addToL2()
        wording = 'Keeping'

    print(f"#### L2 - {wording} user: {user.handle}")
    return user


def checkHandle(words, hanlde):
    for word in words:
        if word in hanlde:
            return True


def checkProfile(words, userPage):
    for word in words:

        if word in userPage.bio:
            return True

        if word in userPage.userName:
            return True

        if word in userPage.altName:
            return True


def checkHashTags(hashtags, words, targetHashtags_List):
    if hashtags:

        commonlist = [x for x in hashtags if x in targetHashtags_List]

        if len(commonlist) > 0:
            return True

        for word in words:
            for tag in hashtags:
                if word in tag:
                    return True
