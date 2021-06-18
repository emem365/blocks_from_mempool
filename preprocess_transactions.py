from models import *


def _resolveParentsForTxn(txn: MempoolTransaction, map: dict, orig_map: dict):
    total_weight = txn.weight
    total_fee = txn.fee
    setg = set(txn.parents)

    for parent in txn.parents:
        if(map[parent][1] == False and len(map[parent][0].parents) > 0):
            _resolveParentsForTxn(map[parent][0], map)
        parentTxn = map[parent][0]
        st = set(parentTxn.parents)
        setg = setg.union(st)

    for p in setg:
        total_weight += orig_map[p].weight
        total_fee += orig_map[p].fee

    txn.weight = total_weight
    txn.fee = total_fee
    txn.parents = list(setg)
    map[txn.txid] = (txn, True)


def resolveParents(lis: list):
    ''' For each transaction that has parents we replace its weight and fee by
        the total weight and fee of the transaction and all of its parents. '''
    map = {}
    orig_map = {}

    for txn in lis:
        map[txn.txid] = (txn, False)
        orig_map[txn.txid] = txn.copy()

    for txn in lis:
        tup = map[txn.txid]
        if(tup[1] == False and len(txn.parents) > 0):
            _resolveParentsForTxn(txn, map, orig_map)

    newLis = [x[0] for x in map.values()]
    return newLis
