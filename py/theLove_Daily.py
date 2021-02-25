import sys
import InstaBotV2


def main():
    hdLess = False
    noOfLikesToGive = 1
    percentageOfUsersToCover = 0.501

    if len(sys.argv) > 1:
        print(sys.argv)
        if sys.argv[1] == 'True':
            hdLess = True
        try:
            noOfLikesToGive = int(sys.argv[2])
            percentageOfUsersToCover = float(sys.argv[3])
        except Exception as e:
            print(e)

    print([hdLess, type(hdLess), noOfLikesToGive, type(noOfLikesToGive), percentageOfUsersToCover, type(percentageOfUsersToCover)])
    try:
        v2Bot = InstaBotV2.InstaBot(hdLess)
        # v2Bot.delayOps()
        v2Bot.getBrowser()
        v2Bot.logIn()

        theDailyResponse = v2Bot.loveService(fileName='daily', percentageOfUsers=1, numberOfLikes=1)
        if 'busted' in theDailyResponse:
            return
        theExtraResponse = v2Bot.loveService(fileName='extra', percentageOfUsers=1, numberOfLikes=1)
    except:
        # v2Bot.shutDown()
        pass


if __name__ == "__main__": main()
