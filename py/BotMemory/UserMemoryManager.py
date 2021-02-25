from BotMemory import FileHandlerBot as fh
from BotMemory import Users_M as UM
import json


class UserMemoryManager:
    def __init__(self):
        self.memoryFileHandler = fh.FileHandlerBot()
        self.listOfUserMemory = []

    ### Memory level
    def writeMemoryFileToDrive(self):
        self.memoryFileHandler.writeToUserMemory(self.listOfUserMemory, UM.UserEncoderDecoder)

    def readMemoryFileFromDrive(self):  # JSONdecoder is a function that translates JSON to User_M objects
        JSONdecoder = UM.UserEncoderDecoder.decode_user
        self.listOfUserMemory = self.memoryFileHandler.readMemoryFile(JSONdecoder)

    def getMemoryFile(self):
        return self.listOfUserMemory

    def getDailyLoveList(self):
        daily = [x for x in self.listOfUserMemory if x.thisUserDeservesDailyLove()]
        return daily

    def getExtraLoveList(self):
        extra = [x for x in self.listOfUserMemory if x.thisUserDeservesExtraLove()]
        return extra

    ### User level
    def userExistsInMemory(self, handle):
        flag = False
        for u in self.listOfUserMemory:
            if u.handle == handle:
                flag = True
                break

        return flag

    def retrieveUserFromMemory(self, handle):
        if self.userExistsInMemory(handle):
            userObj = [x for x in self.listOfUserMemory if x.handle == handle][0]
            return userObj
        else:
            return None

    def addUserToMemory(self, handleOfNewUser):
        if not self.userExistsInMemory(handleOfNewUser):
            userM = UM.User_M(handleOfNewUser)
            self.listOfUserMemory.append(userM)
            self.writeMemoryFileToDrive()

    def updateUserRecord(self, userObj):
        if self.userExistsInMemory(userObj.handle):
            # remove old
            oldUserObj = [x for x in self.listOfUserMemory if x.handle == userObj.handle][0]
            del self.listOfUserMemory[self.listOfUserMemory.index(oldUserObj)]

            # add new
            self.listOfUserMemory.append(userObj)
            self.writeMemoryFileToDrive()
        else:
            # add new
            self.listOfUserMemory.append(userObj)
            self.writeMemoryFileToDrive()

    # def writeToIndividualUserMemory(self, userM):
    #     JSONencoder = UM.UserEncoderDecoder.decode_user
    #     file = self.memoryFileHandler.paths['User_Memory'] + userM.handle + '.json'
