import sys
import InstaBotV2


def main():
    hdLess = False
    numberOfProfilesToProcess = 5

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

        v2Bot.l0_Service(numberOfProfilesToProcess)
    except Exception as e:
        print("we have a fail")
        print(e)
        v2Bot.shutDown()


if __name__ == "__main__": main()
