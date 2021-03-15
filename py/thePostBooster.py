import sys
import InstaBotV2


def main():
    hdLess = False
    numberOfTags = 5
    numberOfPostsPerTag = 10

    if len(sys.argv) > 1:
        print(sys.argv)
        if sys.argv[1] == 'True':
            hdLess = True
        try:
            numberOfTags = int(sys.argv[2])
            numberOfPostsPerTag = int(sys.argv[3])
        except Exception as e:
            print(e)

    print([hdLess, type(hdLess), numberOfTags, type(numberOfTags), numberOfPostsPerTag, type(numberOfPostsPerTag)])
    print('\n')

    try:
        v2Bot = InstaBotV2.InstaBot(hdLess)
        # v2Bot.delayOps()
        v2Bot.getBrowser()
        v2Bot.logIn()

        theBoostResponse = v2Bot.postBoostService(numberOfTags, numberOfPostsPerTag)
        if 'busted' in theBoostResponse:
            print("Busted!")
            return

    except Exception as e:
        # v2Bot.shutDown()
        print(e)


if __name__ == "__main__": main()