# Blocks from Mempool
Selects Transactions from a mempool to create a Transaction Block like a Bitcoin Miner.

## Problem Statement

Bitcoin miners construct blocks by selecting a set of transactions from their mempool. Each transaction in the mempool:
 - includes a fee which is collected by the miner if that transaction is included in a block
 - has a weight , which indicates the size of the transaction
 - may have one or more parent transactions which are also in the mempool
The miner selects an ordered list of transactions which have a combined weight below the maximum block weight. Transactions with parent transactions in the mempool may be included in the list, but only if all of their parents appear before them in the list.
Naturally, the miner would like to include the transactions that maximize the total fee.
Your task is to write a program which reads a file mempool.csv, with the format:
```
<txid>,<fee>,<weight>,<parent_txids>
```
 - txid is the transaction identifier
 - fee is the transaction fee
 - weight is the transaction weight
 - parent_txids is a list of the txids of the transaction’s unconfirmed parent transactions (confirmed parent transactions are not included in this list).

The output from the program should be txids, separated by newlines, which make a valid block, maximizing the fee to the miner. Transactions MUST appear in order
(no transaction should appear before one of its parents).

## Solution implemented

The solution implemented here is a variation of the knapsack problem which is an NP Hard problem. The difference between this problem and a regular knapsack problem is that if a transaction has parents, then all its parents must be selected.
To over come this, I have tried to first resolve all parents of a transaction recursively, ie, if a is a parent to b and b is a parent to c, then c is present iff both a and b are present.
Thus, the total weight and fee of c , also includes weight and fee of a and b.

Then, to select the transactions, a sorting based technique is used, where the elements are placed in a heap based on the fee/weight ratio, and then added to the selected_transactions according to fee/weight ratio(if fee/weight ratio of some transactions is similar, then they are taken up in the order of their decreasing weights, ie, the heaviest transaction gets taken up first).

After all the transactions are selected they are sorted in such an order that all parents must come before the children.
Some special cases that are handled include:
 - if a transaction that is being added already has some of its parents selected. (We first check if the fee/weight ratio is still the same or higher as few transactions have already been added. If yes, then in this case, the weight added to the total count is added such that the weight of the parents already present is counted only once. If the ratio is lesser the transaction is moved to a lower density and thus gets processed only after other transactions with higher density have been processed.)

### Time Complexity
For preprocessing, ie, resolving parents, we need to do this for all transactions and in worst case a transaction might have n-1 parents. Thus, the time taken for this O(n<sup>2</sup>). We try to reduce the total time by memoizing all the transactions that have already been resolved so that they dont need to be resolved again while recursing throuugh one of its children.

For selecting the time required to traverse every transaction in a decreasing fee/weight ratio order, a heap is used. Popping an element from the heap takes O(log(n)) time.  And for each transactions, we must check if its parents have already been added to the selected transations or not which takes O(number of parents for this transaction) time. (A Hash map is used to make sure that we take O(1) time to search in the selected transactions). Since in worst case a transaction may have n-1 parents. Worst case Time Complexity for the selection is O(n<sup>2</sup>log(n))
Note: Generally number of parents << n

## Authors

* **Madhur Maurya** - [emem365](https://github.com/emem365)
