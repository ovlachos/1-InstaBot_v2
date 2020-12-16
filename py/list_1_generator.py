import sys
import InstaBotV2


def main():
    hdLess = False
    numberOfProfilesToProcess = 20

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

    v2Bot = InstaBotV2.InstaBot(hdLess)
    # v2Bot.delayOps()
    v2Bot.getBrowser()
    v2Bot.logIn()

    v2Bot.list_getList_1(numberOfProfilesToProcess)
    # del v2Bot


if __name__ == "__main__": main()
