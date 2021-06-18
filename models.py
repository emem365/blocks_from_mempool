class MempoolTransaction():
    def __init__(self, txid, fee, weight, parents):
        self.txid = txid
        self.fee = int(fee)
        self.weight = int(weight)
        lis = parents.split(';')
        if(lis == ['']):
            lis = []
        self.parents = lis

    def __str__(self):
        return 'MempoolTransaction('+self.txid+', '+str(self.fee)+', '+str(self.weight)+', '+str(self.parents)+')'

    def copy(self):
        return MempoolTransaction(self.txid, self.fee, self.weight, ';'.join(self.parents))
    
    def __lt__(self, other):
        ''' Based on only Size. A transaction is less if its size is more'''
        return self.weight>other.weight