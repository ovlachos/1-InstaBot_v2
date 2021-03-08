def userScraping(bot, userCount):
    # Get User Memory
    bot.memoryManager.readMemoryFileFromDrive()

    # Filter users down to L0
    usersL0 = bot.memoryManager.getListOfMarkedUsers(0)

    # Get people already following me and remove them
    myFollowersCount = 1000  # indicative
    try:
        myPage = bot.mainPage.topRibbon_myAccount.navigateToOwnProfile()

        if not myPage:
            return "Fail"

        myFollowers = myPage.getFollowersList()
        myFollowersCount = myPage.stats['followers']

        usersL0 = [x for x in usersL0 if x.handle not in myFollowers]

    except Exception as e:
        print(e)

    usersL0 = usersL0[:userCount]

    user_counter = 0
    for user in usersL0:

        userPage = bot.mainPage.topRibbon_SearchField.navigateToUserPageThroughSearch(user.handle)

        if not userPage:
            print(f"Dropping user: {user}. No page found (code -666)")
            user.markUserRejected()
            bot.memoryManager.updateUserRecord(user)
            continue

        user_counter += 1
        user.updateInfoFromLivePage_Landing(userPage)

        ### L1 ###
        user = L1(myFollowersCount, user)

        ### L2 ###
        user = L2(user, userPage, bot.words, bot.targetHashtags_List)

        ### Follow on the spot if the user is an L2 and there's still mana left.
        if user.iShouldFollowThisUser() and bot.followMana > 0:
            if 'OK' in userPage.follow():
                user.markTimeFollowed()
                user.addToLoveDaily()
                bot.followMana = bot.followMana - 1

        bot.memoryManager.updateUserRecord(user)
        bot.botSleep()

    return 'OK'


def L1(myFollowersCount, user):
    # Filter out users with more followers than myself - aka L1
    userLatestStats = user.getLatestStats()

    if userLatestStats['followers'] > (1.05 * myFollowersCount) or (userLatestStats['posts'] < 3):
        user.markUserRejected()
        wording = 'Dropping'
    else:
        user.addToL1()
        wording = 'Keeping'

    print(f"L1 - {wording} user: {user.handle} has {userLatestStats['followers']} followers and {userLatestStats['posts']} posts")

    return user


def L2(user, userPage, words, targetHashtags_List):
    # Check if the user has declared an interest to something

    # Check in the username, alt name and bio
    if checkProfile(words, userPage):
        user.addToL2()
        return user

    # Check the hashtags the user follows
    hashtags = []
    try:
        hashtags = userPage.getHashtagsFollowingList()
        user.updateHashtagsFollwingList(hashtags)
    except Exception as e:
        print(e)

    if checkHashTags(hashtags, words, targetHashtags_List):
        user.addToL2()

    return user


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
