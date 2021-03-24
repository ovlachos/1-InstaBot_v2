import sys

import InstaBotV2


def main():
    hdLess = False
    numberOfProfilesToProcess = 5
    typeOfList = 'hashtags'
    numberOfTags = 10
    numberOfPostsPerTag = 5

    if len(sys.argv) > 1:
        print(sys.argv)
        if sys.argv[1] == 'True':
            hdLess = True
        try:
            typeOfList = int(sys.argv[2])
            numberOfProfilesToProcess = int(sys.argv[3])
            numberOfTags = int(sys.argv[4])
            numberOfPostsPerTag = int(sys.argv[5])
        except Exception as e:
            print(e)
    else:
        hdLess = False

    print([hdLess, type(hdLess), typeOfList, numberOfProfilesToProcess, type(numberOfProfilesToProcess)], numberOfTags, numberOfPostsPerTag)
    print('\n')

    try:
        v2Bot = InstaBotV2.InstaBot(hdLess)
        # v2Bot.delayOps()
        v2Bot.getBrowser()
        v2Bot.logIn()

        v2Bot.l0_Service(typeOfList, numberOfProfilesToProcess, numberOfTags, numberOfPostsPerTag)
    except Exception as e:
        v2Bot.memoryManager.writeMemoryFileToDrive()
        print("we have a fail")
        print(e)


if __name__ == "__main__": main()
