import json
import os

def readChain(path):

  with open(path, 'r') as file:
      chain = json.load(file)
        
  for block in chain:
      print("Block index:", block['index'])
      print('Timestamp:', block['timeStamp'])
      print('Transactions:')
      for tmp in block['transaction']:
          print('  ', tmp['sender'], '->', tmp['receiver'], '(', tmp['amount'], ')')
      print('Previous hash:', block['previousHash'])
      print('Hash:', block['hash'])
      print('Nonce:', block['nonce'])
      print()

def main():
    path = input('Enter path to chain: ')
    if os.path.isfile(path):
        readChain(path)
    else:
        print('Error! File not found')


if __name__ == '__main__':
    main()