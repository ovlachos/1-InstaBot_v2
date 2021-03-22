def list_getList_0(bot, numberOfProfilesToProcess=5):
    print("\n")
    print("### theL0 ###")
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
            bot.memoryManager.userPageCannotBeFound(user)

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
    import time

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
