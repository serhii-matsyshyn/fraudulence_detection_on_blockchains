# Fraudulence detection on blockchains 

## Environment preparation

I have used Python 3.9.  
Install the dependencies:
```shell
pip install -r requirements.txt
```

Register the necessary API keys of the external services, and export them as environment variables:  
```shell
export BLASTAPI_API_KEY=...
export ETHPLORER_API_KEY=...
export ETHERSCAN_API_KEY=... 
```

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
I have merged datasets into one.

### Step 5 - dataset preparation
Use `dataset_preparation.ipynb` notebook for dataset cleaning and feature reduction.

### Step 6 - XGBoost model
Use `XGBoost_Model.ipynb` to train the model. It can utilize GPU (and can be used on Google Collab).  

The best XGBoost model parameters found:
```python
params = {
    'max_depth': [7],
    'n_estimators': [1300],
    'learning_rate': [0.1]
}
```

XGBoost model accuracy score: 0.9717.

### Step 7 - manual evaluation
Use FraudulentAddressesCheckerEthereum from `fraudulent_addresses_checker_ethereum.py` to use the model to check if address can be considered fraudulent or no.  
Several ready to use models can be found in `data/models/`.

Example usage:
```python
from fraudulent_addresses_checker_ethereum import FraudulentAddressesCheckerEthereum

checker = FraudulentAddressesCheckerEthereum(model_path="data/models/1/xgboost_model.json", scaler_path="data/models/1/scaler.gz")

# Close to 0 - definitely not fraudulent
# Close to 1 - fraudulent
print(checker.check_address("0x1fBad35b92bE6B0754EA7b87D6e9072627527672"))  # Fake_Phishing327049
print(checker.check_address("0xb5d85CBf7cB3EE0D56b3bB207D5Fc4B82f43F511"))  # Coinbase 5
print(checker.check_address("0xe97C5331bf3ca4f22c76e958872D07c923E0367C"))  # Random addresses
print(checker.check_address("0x995A014a6D43Ad9F49DddE79803936Cd1111aB8D"))  # Random addresses
```

### Step 8 - simple API
You can use `server.py` to run model as an api. It has basic cache (1 minute).    
Example GET HTTP request:
```http request
http://localhost:8080/check_fraudulence?eth_address=0x1fBad35b92bE6B0754EA7b87D6e9072627527672
```
Response:
```http request
{"fraudulent":true,"address_check_result":0.6622717380523682,"message":"This address is potentially fraudulent"}
```

## References
1. https://medium.com/@nusfintech.ml/crypto-fraud-detection-3d99b3298815
2. https://github.com/eltontay/Ethereum-Fraud-Detection
3. https://etherscan.io/