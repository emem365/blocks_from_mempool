from models import *

def parse_mempool_csv(filename):
    """Parse the CSV file and return a list of MempoolTransactions."""
    with open(filename) as f:
        f.readline()
        return ([MempoolTransaction(*line.strip().split(',')) for line in f.readlines()])

def save_block(transactions, fileName):
    transactions = [x+'\n' for x in transactions]
    with open(fileName, 'w') as f:
        f.writelines(transactions)