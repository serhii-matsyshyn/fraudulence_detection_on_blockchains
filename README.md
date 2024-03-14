# Fraudulence detection on blockchains 

## Dataset creation
### Step 1 - get addresses by tag
Getting all addresses by tag `Fake_Phishing` - `BlockScan_addresses_by_tag_retrival.py`.  
Since BlockScan shares `Fake_Phishing` labels across several blockchains, so you need to find only active addresses on Ethereum - `check_if_address_active.py`.

### Step 2 - collect data about fraudulent addresses

`collect_data_about_addresses_full.py`

### Step 3 - get random addresses from blockchain
As second group of addresses, I have collected addresses that had either incoming or outgoing transactions on the blockchain in last 120 days.  
`get_random_addresses_from_blockchain.py`  
Then, I have prepared them (removed duplicates and addresses that were marked as fraudulent).

### Step 4 - merging dataset
I have merged datasets into one. It may require further postprocessing and normalizing.

## References
1. https://medium.com/@nusfintech.ml/crypto-fraud-detection-3d99b3298815
2. https://github.com/eltontay/Ethereum-Fraud-Detection
3. https://etherscan.io/