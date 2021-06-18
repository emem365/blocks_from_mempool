import mempool_parser
import preprocess_transactions
import heapq as heap


mempool_list = mempool_parser.parse_mempool_csv('mempool.csv')

print('Loaded Data')
print('Preprocessing...')

# preprocess data

# For each transaction that has parents we replace its weight and fee by
# the total weight and fee of the transaction and all of its parents.

mempool_list, map, orig_map = preprocess_transactions.resolveParents(mempool_list)

# fee/weight->list of mempool transactions
mempool = {}

for txn in mempool_list:
    x = txn.fee/txn.weight
    if(txn.weight not in mempool):
        mempool[x] = []
    heap.heappush(mempool[x], txn)
            
densities = []

for i in mempool.keys():
    heap.heappush(densities, -i)

print('Preprocessing... Done')
print('Selecting Transactions...')
max_weight = 4000000
total_weight = 0
total_fee = 0
selected_transactions_map = {}  # txid -> txn
i = 0
    


while(len(densities)>0):
    max_density =  -heap.heappop(densities)
    H = mempool[max_density]
    while(len(H)>0):
        txn = heap.heappop(H)
        parents_weight = 0
        parents_fee = 0
        for p in txn.parents:
            if(p in selected_transactions_map):
                parents_weight+=orig_map[p].weight
                parents_fee+=orig_map[p].fee
        if(parents_weight>0):
            # some parents already exist in the selected Transitions. This changes the
            # fee / weight value of this txn
            x = txn.fee/txn.weight
            if(x<max_density):
                if(x not in mempool):
                    mempool[x] = []
                heap.heappush(mempool[x], txn)
                heap.heappush(densities, -x)
                continue
        if(txn.weight+total_weight-parents_weight<=max_weight):
            for p in txn.parents:
                selected_transactions_map[p] = map[p][0]
            selected_transactions_map[txn.txid] = map[txn.txid][0]
            total_weight = total_weight+txn.weight-parents_weight
            total_fee = total_fee+txn.fee-parents_fee

selected_transactions = list(selected_transactions_map.keys())

print('Selecting Transactions...Done')

print('Sorting Transactions')
#txid->True\False
already_occured_map = {}
i = 0
while(i<len(selected_transactions)):
    txn = selected_transactions_map[selected_transactions[i]]
    if(len(txn.parents)>0):
        f = False
        for x in txn.parents:
            if x not in already_occured_map:
                f = True
                break
        if(f):
            x = selected_transactions.pop(i)
            selected_transactions.append(x)
            continue
    already_occured_map[selected_transactions[i]] = True
    i+=1

newFileName = 'block.txt'
print('Sorting Transactions... Done')

print('********************************************')
print('Total Weight: ', total_weight)
print('Total Fee gathered: ', total_fee)
print('********************************************')
mempool_parser.save_block(selected_transactions, newFileName)
print('Transactions Block saved as ', newFileName)
print('********************************************')
print('********************************************')


sum = 0
sum2 = 0
for x in selected_transactions:
    sum+=orig_map[x].weight
    sum2+=orig_map[x].fee
print(sum, sum2)