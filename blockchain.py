import json
import hashlib
import datetime
import random
import os

clients = ["Alexey", "Vladimir", "Ivan", "Danil", "Matvey",
            "Sofya", "Darya", "Anna", "Mihail", "Vyacheslav",
            "Artem", "Lidiya", "Timofey", "Andrey", "Vladislav",
            "Camilla", "Valeriy", "Iskander", "Gregory", "Stepan"]

# transaction structure
class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __dict__(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount
        }

# block structure
class Block:
    #constructor
    def __init__(self, index, timeStamp, transactions, previousHash=' ', nonce = 0):
        self.index = index
        self.timeStamp = timeStamp
        self.transactions = transactions
        self.previousHash = previousHash
        self.nonce = 0
        self.hash = self.calculateHash()

    # calculating hash based on block data
    def calculateHash(self):
        return hashlib.sha256((str(self.index) + self.previousHash + self.timeStamp +\
                            json.dumps([tmp.__dict__() for tmp in self.transactions]) + str(self.nonce)).encode('utf-8')).hexdigest()

    # mining
    def mineBlock(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculateHash()
        print("Block mined: " + self.hash)

    # class to dictionary
    def __dict__(self):
        return {
            "index": self.index,
            "timeStamp": self.timeStamp,
            "transaction": [tmp.__dict__() for tmp in self.transactions],
            "previousHash": self.previousHash,
            "hash": self.hash,
            "nonce": self.nonce
        }



#blockchain object
class Chain:
    # constructor
    def __init__(self):
        self.chain = [self.createGenesisBlock()]
        self.difficulty = 3

    # generate first block
    def createGenesisBlock(self):
        return Block(0, "04/10/2023", [Transaction("Genesis", "Genesis", 1)], "0", 0)

    def getLatestBlock(self):
        return self.chain[len(self.chain)-1]

    #making chain
    def addBlocks(self):
        transactions = []
        for j in range(random.randint(1, 6)):
            transactions.append(Transaction(clients[random.randint(1, 19)], clients[random.randint(1, 19)],
                                                 random.randint(1, 100)))
        newBlock = Block(len(self.chain), datetime.datetime.now().strftime("%d/%m/%Y"), transactions,
                      self.getLatestBlock().hash, nonce=0)
        newBlock.mineBlock(self.difficulty)
        self.chain.append(newBlock)

    def appendBlock(self, transactions):
        newBlock = Block(len(self.chain), datetime.datetime.now().strftime("%d/%m/%Y"), transactions,
                    self.getLatestBlock().hash, nonce=0)
        newBlock.mineBlock(self.difficulty)
        self.chain.append(newBlock)

    def checkValid(self):
        for i in range (1, len(self.chain)):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i-1]
            if currentBlock.hash != currentBlock.calculateHash():
                return False
            if currentBlock.previousHash != previousBlock.hash:
                return False
        return True
    

    def saveToJson(self, path):
        try:
            os.remove(path)
        except OSError:
            pass

        blocks = []
        for block in self.chain:
            blocks.append(block.__dict__())
        with open("chain.json", "w") as outfile:
            json.dump(blocks, outfile, indent=4)
        print(f"Blockchain saved in {path}")



def main():
    try:
        num = int(input('Enter the number of blocks in the chain:'))
    except ValueError:
        print("Error! Enter an integer.")

    test = Chain()
    for j in range(1, num):
        test.addBlocks()

    print ("Chain is valid?" + str(test.checkValid()))
    path = input('Enter the file name to save to:')
    path = f'{path}.json'
    test.saveToJson(path)
    

if __name__ == '__main__':
    main()