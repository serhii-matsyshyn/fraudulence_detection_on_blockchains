# Fraudulence detection on blockchains 

## Dataset creation
### Step 1 - get addresses by tag
Getting all addresses by tag `Fake_Phishing` - `BlockScan_addresses_by_tag_retrival.py`.  
Since BlockScan shares `Fake_Phishing` labels across several blockchains, so you need to find only active addresses on Ethereum - `check_if_address_active.py`.

### Step 2 - collect data about addresses
