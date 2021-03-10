def playTheGame(bot):
    print("\n")
    print("### theGame ###")
    print("\n")

    print(f"Follow Mana: {bot.followMana}")

    ### Read User Memory
    bot.memoryManager.readMemoryFileFromDrive()

    gameList = bot.memoryManager.getListOfUsersAlreadyFollowedOnly()

    ### Derive Lists
    mark2_list = bot.memoryManager.getListOfMarkedUsers(2)
    unfollowList = bot.memoryManager.getListOfUsersToUnFollow(bot.daysBeforeIunFollow)
    unLoveList = bot.memoryManager.getListOfUsersToUnLove(bot.daysBeforeIunLove)

    ### Un Love ###
    if unLoveList:
        print(f"### - {len(unLoveList)} users to be un-Loved")
        for user in unLoveList:
            user.removeFromLoveDaily()
            bot.memoryManager.updateUserRecord(user)
    else:
        print(f"### - {0} users to be un-Loved")

    ### Un Follow ###
    if unfollowList:
        print(f"### - {len(unfollowList)} users to be un-Followed")
        for user in unfollowList:
            user.daysSinceYouGotFollowed_Unfollowed('follow', True)

            userPage = bot.mainPage.topRibbon_SearchField.navigateToUserPageThroughSearch(user.handle)

            if not userPage:
                bot.memoryManager.userPageCannotBeFound(user)
                continue

            print(f"Will unfollow user {user.handle}")

            if 'OK' in userPage.unfollow():
                user.markDateUnfollowed()

            bot.memoryManager.updateUserRecord(user)
            if user.dateUnFollowed_byMe:
                bot.botSleep()
    else:
        print(f"### - {0} users to be un-Followed")

    ### Follow Reserves ###
    if mark2_list:
        print(f"### - {len(mark2_list)} reserve users to be Followed")
        for user in mark2_list:
            userPage = bot.mainPage.topRibbon_SearchField.navigateToUserPageThroughSearch(user.handle)

            if not userPage:
                bot.memoryManager.userPageCannotBeFound(user)
                continue

            print(f"Will follow user {user.handle}")

            if user.iShouldFollowThisUser() and bot.followMana > 0:
                if 'OK' in userPage.follow():
                    user.markTimeFollowed()
                    user.addToLoveDaily()
                    bot.followMana = bot.followMana - 1

            bot.memoryManager.updateUserRecord(user)
            if user.dateFollowed_byMe:
                bot.botSleep()
    else:
        print(f"### - {0} reserve users to be Followed")

    print("\n### theEnd ###")
