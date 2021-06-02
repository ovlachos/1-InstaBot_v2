import InstaBotV2


def main():
    hdLess = False

    try:
        v2Bot = InstaBotV2.InstaBot(hdLess)
        # v2Bot.delayOps()
        v2Bot.getBrowser()
        v2Bot.logIn()

        v2Bot.run()
    except Exception as e:
        v2Bot.memoryManager.writeMemoryFileToDrive()
        v2Bot.mainPage.page.sleepPage(10)
        print(f'we have a fail: {e}')


if __name__ == "__main__": main()
