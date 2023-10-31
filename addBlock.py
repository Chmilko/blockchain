import blockchain
from blockchain import Chain, Block, Transaction
import json
import os

def addNewBlock(path):
    with open(path, 'r') as f:
        chain = json.load(f)

    #get the data from json to chain
    currentChain = Chain()
    for i in range(1, len(chain)):
        newBlock = Block(
            chain[i]['index'],
            chain[i]['timeStamp'],
            [Transaction(tmp['sender'], tmp['receiver'], tmp['amount']) for tmp in chain[i]['transaction']],
            chain[i]['previousHash'],
            chain[i]['nonce']
        )
        newBlock.hash = chain[i]['hash']
        currentChain.chain.append(newBlock)

    while True:
      response = input('Do you want to add a block? (y/n) ')
      if response.lower() == 'y':
        transactions = []
        while True:
          try:
            sender, receiver, amount = input('Enter sender, receiver, and amount (press Enter to stop): ').split()
          except ValueError:
            break
          amount = int(amount)
          transactions.append(Transaction(sender, receiver, amount))
        currentChain.appendBlock(transactions)
      elif response.lower() == 'n':
        break
      else:
            print('Please enter "y" or "n".')
    currentChain.saveToJson(path)



def main():
    path = input('Enter path to chain you want to add block: ')
    if os.path.isfile(path):
        addNewBlock(path)
    else:
        print('Error! File not found.')

if __name__ == '__main__':
    main()
