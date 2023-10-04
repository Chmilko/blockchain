import json
import hashlib

# block structure
class Block:
    #constructor
    def __init__(self, index, timeStamp, data,  previousHash=' '):
        self.index = index
        self.timeStamp = timeStamp
        self.data = data
        self.previousHash = previousHash
        self.hash = self.calculateHash()

    def calculateHash(self):
        return hashlib.sha256((str(self.index) + self.previousHash + self.timeStamp + self.data).encode('utf-8')).hexdigest()

    def __dict__(self):
        return {
            "index": self.index,
            "timeStamp": self.timeStamp,
            "data": self.data,
            "previousHash": self.previousHash,
            "hash": self.hash,
        }

    def printBlock(self):
        print ("Block #"+ str(self.index))
        print ("TimeStamp: " + str(self.timeStamp))
        print ("Data: " + self.data)
        print ("Block Hash: " + str(self.hash))
        print ("Block Previous Hash: " + str(self.previousHash))



#blockchain object
class Chain:
    def __init__(self):
        self.chain = [self.createGenesisBlock()]

    def createGenesisBlock(self):
        return Block(0, "04/10/2023", "Genesis Block", "0")

    def getLatestBlock(self):
        return self.chain[len(self.chain)-1]

    def addBlock(self, newBlock):
        newBlock.previousHash = self.getLatestBlock().hash
        newBlock.hash = newBlock.calculateHash()
        self.chain.append(newBlock)

    def checkValid(self):
        for i in range (1, len(self.chain)):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i-1]
            # проверка валидности
            if currentBlock.hash != currentBlock.calculateHash():
                return False
            if currentBlock.previousHash != previousBlock.hash:
                return False
        return True

    def printBlockChain(self):
        for i in range(1, len(self.chain)):
            self.chain[i].printBlock()

    def saveToJson(self):
      with open("chain.json", "w") as outfile:
          for i in range(1, len(self.chain)):
            json.dump(self.chain[i].__dict__(), outfile)
          



test = Chain()
test.addBlock(Block(1, "03/10/2023", "block_1"))
test.addBlock(Block(2, "04/10/2023", "block_2"))

test.printBlockChain()
print ("Chain is valid?" + str(test.checkValid()))
test.saveToJson()

