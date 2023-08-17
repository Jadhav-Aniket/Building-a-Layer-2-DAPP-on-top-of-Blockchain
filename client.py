import json
import numpy as np
from web3 import Web3
import networkx as nx
import matplotlib.pyplot as plt
from graph import barabasi_albert_graph, send_amount, plot_graph

# connect to the local ethereum blockchain
provider = Web3.HTTPProvider('http://127.0.0.1:7545')
w3 = Web3(provider)
# check if ethereum is connected
print(w3.is_connected())

# replace the address with your contract address (!very important)
deployed_contract_address = '0x172a4df432552ab07f19a76F6F7302E49e3CdFCc'

# path of the contract json file. edit it with your contract json file
compiled_contract_path = "build/contracts/Payment.json"
with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']
contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)


# call Register user function from solidity and register 100 users
for i in range(100):
    txn_receipt = contract.functions.registerUser(
        i, 'user'+str(i)).transact({'txType': "0x3", 'from': w3.eth.accounts[0], 'gas': 2409638})


edge_list = []
# create graph using barabasi_albert_graph Algorithm
G = barabasi_albert_graph(100, 2)
nx.draw(G, with_labels=True)
plt.savefig('Graph.png')
adj_list = nx.to_dict_of_lists(G)

# Create Joint Accounts for all available edges in above graph
for key, list in adj_list.items():
    for node in list:
        if ((key, node) in edge_list) or ((node, key) in edge_list):
            continue
        edge_list.append((key, node))
        bal = np.random.exponential(10)
        # Since we do not have support for float, we will convert total balance as
        # the closest even number
        bal = int(round(bal))
        if bal % 2 == 1:
            bal += 1
        txn_receipt = contract.functions.createJointAccount(int(key), int(node), int(
            bal)).transact({'txType': "0x3", 'from': w3.eth.accounts[0], 'gas': 2409638})


# fire random 1000 transactions.
for i in range(1000):
    print(i)
    amount, path = send_amount(adj_list)
    txn_receipt = contract.functions.sendAmount(amount, path).transact(
        {'txType': "0x3", 'from': w3.eth.accounts[0], 'gas': 2409638})

# Call TxStatus function to get to know the status of transaction, Failed or not.
Txlist = contract.functions.TXstatus().call()
Txcount = []
for i in range(10):
    success = 0
    for j in range(100):
        ind = (i*100) + j
        success += Txlist[ind]
    Txcount.append(success)

print(Txcount)

# At last close all available accounts
for tuple in edge_list:
    node1 = tuple[0]
    node2 = tuple[1]
    txn_receipt = contract.functions.closeAccount(node1, node2).transact(
        {'txType': "0x3", 'from': w3.eth.accounts[0], 'gas': 2409638})
    edge_list.remove(tuple)

plot_graph(Txcount)
