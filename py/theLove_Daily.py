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
    print('\n')
    
    try:
        v2Bot = InstaBotV2.InstaBot(hdLess)
        # v2Bot.delayOps()
        v2Bot.getBrowser()
        v2Bot.logIn()

        theDailyResponse = v2Bot.love_Service('daily', noOfLikesToGive, percentageOfUsersToCover)
        if 'busted' in theDailyResponse:
            print("Busted!")
            return

        theExtraResponse = v2Bot.love_Service('extra', noOfLikesToGive, percentageOfUsersToCover)
        if 'busted' in theExtraResponse:
            print("Busted!")
            return
    except:
        # v2Bot.shutDown()
        pass


if __name__ == "__main__": main()
