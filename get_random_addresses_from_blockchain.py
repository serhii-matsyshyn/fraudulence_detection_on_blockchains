import os
import random
import time

from web3 import Web3
from datetime import datetime, timedelta

blastapi_api_key = os.environ['BLASTAPI_API_KEY']
blastapi_url = f'wss://eth-mainnet.blastapi.io/{blastapi_api_key}'
w3 = Web3(Web3.WebsocketProvider(blastapi_url))

end_date = datetime.now()
start_date = end_date - timedelta(days=120)

# Convert dates to Unix timestamps
start_timestamp = int(start_date.timestamp())
end_timestamp = int(end_date.timestamp())

# Open a text file to append addresses
output_file = "data/3_normal_addresses/interacted_addresses.txt"


# Function to get addresses from transactions
def get_addresses_from_transactions(block_number):
    addresses = set()
    block = w3.eth.get_block(block_number, True)  # Retrieve transactions
    transactions = block['transactions']

    for tx in transactions:
        addresses.add(tx['from'])
        addresses.add(tx['to'])

    print(addresses)
    time.sleep(0.500)

    return addresses


random_blocks = random.sample(range(18708785, 19388785), 1000)


# Loop through blocks in the specified date range
for block_number in random_blocks:
    try:
        timestamp = w3.eth.get_block(block_number)['timestamp']
        print(timestamp)

        if start_timestamp <= timestamp <= end_timestamp:
            addresses = get_addresses_from_transactions(block_number)

            # Append addresses to the text file
            with open(output_file, "a") as file:
                for address in addresses:
                    if address:
                        file.write(address.lower() + "\n")
    except:
        pass

print("Addresses appended to", output_file)
