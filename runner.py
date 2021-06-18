import mempool_parser
import preprocess_transactions


mempool_list = mempool_parser.parse_mempool_csv('sample_mempool.csv')

# preprocess data

# For each transaction that has parents we replace its weight and fee by
# the total weight and fee of the transaction and all of its parents.

for i in mempool_list:
    print(i)
mempool_list = preprocess_transactions.resolveParents(mempool_list)

print('*********')
for i in mempool_list:
    print(i)



# # fee/weight->list of mempool transactions
# mempool = {}

# for txn in mempool_list:
#     x = txn.fee/txn.weight
#     if(txn.weight in mempool):
#         mempool[x].append(txn)
#     else:
#         mempool[x] = [txn]

# for k, v in mempool.items():
#     mempool[k] = sorted(v, key= lambda x: x.weight, reverse=True)  
# densities = sorted(mempool.keys(), reverse=True)

# max_weight = 4000000
# total_weight = 0
# total_fee = 0
# selected_transactions = []
# i = 0

# # txnid->True\False

# map = {}
# while(i<len(densities)):
#     j = 0
#     vals = mempool[densities[i]]
#     while(j<len(vals)):
#         if(total_weight+vals[j].weight<=max_weight):
#             total_weight+=vals[j].weight
#             total_fee+=vals[j].fee
#             selected_transactions.append(vals[j])
#             map[vals[j].txid] = True
#         j+=1
#     i+=1

# # Find Transactions that don fulfill Parent req

# remove_ids = []
# for i in range(len(selected_transactions)):
#     txn = selected_transactions[i]
#     for txid in txn.parents:
#         if(txid not in map):
#             remove_ids.append(i)
#             break

# print(len(selected_transactions))
# print(remove_ids)
# # Remove Indexes

# # for i in remove_ids:
# #     txn = selected_transactions.pop(i)
# #     map[txn.txid] = False
# #     total_weight-=txn.weight
# #     total_fee-=txn.fee

# # # Fill in Spaces with valid transactions
# # while(i<len(densities)):
# #     j = 0
# #     vals = mempool[densities[i]]
# #     while(j<len(vals)):
# #         if(vals[j] in map):
# #             j+=1
# #             continue
# #         if(total_weight+vals[j].weight<=max_weight):
# #             f = True
# #             for x in vals[j].parents:
# #                 if(x not in map or map[x] == False):
# #                     f = False
# #                     break
# #             if(f):
# #                 total_weight+=vals[j].weight
# #                 total_fee+=vals[j].fee
# #                 selected_transactions.append(vals[j])
# #                 map[vals[j].txid] = True
# #         j+=1
# #     i+=1

