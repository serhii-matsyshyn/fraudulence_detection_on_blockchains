# Fraudulence detection on blockchains 

## Dataset creation
### Step 1 - get addresses by tag
Getting all addresses by tag `Fake_Phishing` - `BlockScan_addresses_by_tag_retrival.py`.  
Since BlockScan shares `Fake_Phishing` labels across several blockchains, so you need to find only active addresses on Ethereum - `check_if_address_active.py`.

### Step 2 - collect data about addresses

`collect_data_about_addresses_full.py`


## References
1. https://medium.com/@nusfintech.ml/crypto-fraud-detection-3d99b3298815
2. https://github.com/eltontay/Ethereum-Fraud-Detection
3. https://etherscan.io/