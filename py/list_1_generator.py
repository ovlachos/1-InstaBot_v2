import sys

import InstaBotV2


def main():
    hdLess = False
    numberOfProfilesToProcess = 7

    if len(sys.argv) > 1:
        print(sys.argv)
        if sys.argv[1] == 'True':
            hdLess = True
        try:
            numberOfProfilesToProcess = int(sys.argv[2])
        except Exception as e:
            print(e)
    else:
        hdLess = False

    print([hdLess, type(hdLess), numberOfProfilesToProcess, type(numberOfProfilesToProcess)])
    print('\n')

    try:
        v2Bot = InstaBotV2.InstaBot(hdLess)
        # v2Bot.delayOps()
        v2Bot.getBrowser()
        v2Bot.logIn()

        response = v2Bot.l1_2_Service(numberOfusersToCheck=numberOfProfilesToProcess, randomArgs=False)
        print(response)
    except Exception as e:
        v2Bot.memoryManager.writeMemoryFileToDrive()
        print("we have a fail")
        print(e)


if __name__ == "__main__": main()
