import time


#### SPONSORS ####

def list_getList_0_FromSponsors(bot, numberOfProfilesToProcess=5):
    print("\n")
    print("### theL0 - Sponsors ###")
    print("\n")
    bot.mainPage.driver.refresh()

    # Get users marked as L0: A list of all people following a number of profiles

    # If a source user's follower is already in the list we need not add a duplicate
    bot.memoryManager.readMemoryFileFromDrive()
    usersAlreadyInList = bot.memoryManager.getListOfAllUserHandles()

    # Get a list of target source users
    targetuserInput = bot.fileHandler.CSV_getFrameFromCSVfile("usersToTargetCSV")  # usersToTarget
    targetuserInputPyList = targetuserInput[targetuserInput.columns[0]].tolist()
    targetuserInputPyList = list(dict.fromkeys(targetuserInputPyList))  # Remove duplicates

    # If the name of the source user is already there do not re-examine
    sponsorsAlreadyExamined = bot.memoryManager.getListOfSponsorHandles()
    l3 = [x for x in targetuserInputPyList if x not in sponsorsAlreadyExamined]
    makeSureSponsorsAlreadyHaveAMemoryRecord(bot, l3)

    targetUsers = bot.memoryManager.filterByListOfHandles(l3)  # get a list of user objects whose names are on the list provided: l3

    if not len(targetUsers) > 0:
        return 'OK'

    targetUsers = targetUsers[:numberOfProfilesToProcess]

    userNotFound_counter = 0
    for sponsorUser in targetUsers:  # a list of user memory objects

        # Navigate to user's profile
        userPage = bot.mainPage.topRibbon_SearchField.navigateToUserPageThroughSearch(sponsorUser.handle)

        if not userPage:
            bot.memoryManager.userPageCannotBeFound(sponsorUser)

            userNotFound_counter += 1
            if userNotFound_counter > 5:
                if bot.internetConnectionLost():
                    return "No Internet"

            continue

        print(f"#### User {sponsorUser.handle} has {userPage.stats['followers']} followers")

        followers_ = userPage.getFollowersList()  # a list of handles as strings
        sponsorUser.updateInfoFromLivePage_Landing(userPage)

        if len(followers_) > 0:
            sponsorUser.updateFollowersList(followers_)
            usersAlreadyInList = addSponsorsFollowersToUserMemory(followers_, sponsorUser.handle, usersAlreadyInList, bot)

        bot.memoryManager.updateUserRecord(sponsorUser)

        bot.botSleep()

    print("\n### theEnd ###")
    return 'OK'


def addSponsorsFollowersToUserMemory(followers_, sponsorUser, usersAlreadyInList, bot):
    for follower in followers_:
        if follower not in usersAlreadyInList:
            start = time.time()

            bot.memoryManager.addUserToMemory(follower)

            # Get the newly created memory object of the new user
            newFollower = bot.memoryManager.retrieveUserFromMemory(follower)
            newFollower.addToL0(sponsorUser)
            bot.memoryManager.updateUserRecord(newFollower)

            # Update list of users already in memory so that we do not bother adding a duplicate
            usersAlreadyInList.append(follower)

            end = time.time()
            print(f"##### {round((end - start), 1)} | User {follower} added to memory")

    return usersAlreadyInList


def makeSureSponsorsAlreadyHaveAMemoryRecord(bot, inputSponsorHandles):
    for sponsor in inputSponsorHandles:
        bot.memoryManager.addUserToMemory(sponsor)


#### HASHTAGS ####

def list_getList_0_FromTagedPosts(bot, numberOfTags, numberOfPostsPerTag):
    import random

    print("\n")
    print("### theL0 - Taged Posts ###")
    print("\n")

    bot.mainPage.driver.refresh()
    bot.memoryManager.readMemoryFileFromDrive()

    # myPage = bot.mainPage.topRibbon_myAccount.navigateToOwnProfile()
    # bot.mainPage.sleepPage(1)
    # mylatestPost = myPage.navigateTo_X_latestPost(0)
    # bot.mainPage.sleepPage(1)
    # mylatestPost.updateHashTagsUsed()
    # bot.mainPage.sleepPage(1)
    # hashList = mylatestPost.hashTagsUsed
    # bot.mainPage.sleepPage(1)
    # mylatestPost.close_post()

    hashList = bot.targetHashtags_List
    random.shuffle(hashList)

    if hashList:
        hashList = hashList[:numberOfTags]
        print(f"Today's hashtags are: {hashList}")

    userHandles = []

    for hashtag in hashList:
        hashPage = bot.mainPage.topRibbon_SearchField.navigateToHashTagPageThroughSearch(hashtag)
        bot.mainPage.page.sleepPage(1)
        bot.mainPage.driver.refresh()
        bot.mainPage.page.sleepPage(1)

        print(f"### HashTag: {hashPage.hashtag}")

        userHandles.extend(getUserHandles(hashPage, numberOfPostsPerTag, bot.mainPage.page.sendESC, bot))

        bot.botSleep(1.2)

    addUsersTaggingToUserMemory(userHandles, bot)

    print("\n### theEnd ###")
    return 'OK'


def getUserHandles(hashTagPage, numberOfPostsPerTag, escapeFunc, bot, toLike=True):
    usersToReturn = []
    for i in range(0, numberOfPostsPerTag):
        try:
            post = hashTagPage.navigateTo_X_mostRecentPosts(i)

            bot.mainPage.page.sleepPage(2)

            if toLike:
                liked = post.like_post()

            usersToReturn.append(post.getPostingUsersHandle())

            bot.mainPage.page.sleepPage(2)
            postExists = post.close_post()

            if liked:
                if not isinstance(liked, bool):
                    return 'busted'

                bot.botSleep()
            if not postExists:
                escapeFunc()

        except Exception as e:
            print(e)
            continue

    return usersToReturn


def addUsersTaggingToUserMemory(users, bot):
    users = list(dict.fromkeys(users))
    for user in users:
        start = time.time()

        bot.memoryManager.addUserToMemory(user)

        # Get the newly created memory object of the new user
        newFollower = bot.memoryManager.retrieveUserFromMemory(user)
        newFollower.addToL0('hashtag')
        newFollower.addToL2()

        bot.memoryManager.updateUserRecord(newFollower)

        end = time.time()
        print(f"##### {round((end - start), 1)} | User {user} added to memory")

    return "OK"
