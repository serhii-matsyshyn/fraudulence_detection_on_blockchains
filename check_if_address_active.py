import os

import requests
from tqdm import tqdm
from web3 import Web3


class EthereumAddressChecker:
    def __init__(self, blastapi_api_key, ethplorer_api_key):
        self.blastapi_url = f'wss://eth-mainnet.blastapi.io/{blastapi_api_key}'
        self.w3 = self.connect_websocket()

        self.ethplorer_api_key = ethplorer_api_key

    def connect_websocket(self):
        w3 = Web3(Web3.WebsocketProvider(self.blastapi_url))
        return w3

    def get_tokens_nft_data(self, address_address):
        response = requests.get(
            f"https://api.ethplorer.io/getAddressInfo/{address_address}?apiKey={self.ethplorer_api_key}")
        return response.json()

    def is_address_active(self, address_address):
        # Check if the address is valid
        if not self.w3.is_address(address_address):
            return False

        address_address = Web3.to_checksum_address(address_address)

        # print((
        #         self.w3.eth.get_transaction_count(address_address),
        #         self.w3.eth.get_balance(address_address),
        #         self.w3.eth.get_code(address_address) != b'',
        #         self.get_tokens_nft_data(address_address).get("tokens"),
        # ))

        if (
                self.w3.eth.get_transaction_count(address_address) or  # Get the nonce
                self.w3.eth.get_balance(address_address) or  # balance
                self.w3.eth.get_code(address_address) != b'' or  # contract
                self.get_tokens_nft_data(address_address).get("tokens")  # any tokens holder
        ):
            return True
        return False


if __name__ == "__main__":
    blastapi_api_key = os.environ['BLASTAPI_API_KEY']
    ethplorer_api_key = os.environ['ETHPLORER_API_KEY']

    address_checker = EthereumAddressChecker(blastapi_api_key, ethplorer_api_key)

    filename = "search_results_all.txt"
    with open(filename, "r") as file:
        all_lines = [line.rstrip() for line in file.readlines() if len(line.rstrip()) > 0]

    with open("search_results_processed.txt", "r") as file:
        all_lines_processed = [line.rstrip() for line in file.readlines() if len(line.rstrip()) > 0]

    print("Len of lines: ", len(all_lines))
    all_lines = list(set(all_lines).difference(set(all_lines_processed)))  # remove duplicates
    print("Len of lines cleaned: ", len(all_lines))

    sorted_addresss = sorted(all_lines, key=lambda x: int(x.split("|")[0][13:]), reverse=True)

    # addresss = [
    #     "0xeFb3729Bc9C0ee64c718185d612C9538C0323306",  # walet with nonce
    #     "0xDef1C0ded9bec7F1a1670819833240f027b25EfF",  # address contract with balance
    #     "0xF57e7e7C23978C3cAEC3C3548E3D615c346e79fF",  # address contract no balance
    #     "0x4F773f3FC89b73B34FB57EBc667a245D5e3812F6",  # has nft
    #     "0x94ffc85CB5B4D6819a99387DAB8b4aD80cc0120c"   # empty
    # ]
    #
    for address_address_to_check in tqdm(sorted_addresss):
        key, address = address_address_to_check.split("|")
        # Check if the address is active
        address_active = address_checker.is_address_active(address)

        with open("search_results_processed.txt", "a") as file:
            print(address_address_to_check, file=file)

        if address_active:
            with open("search_results_out.txt", "a") as file:
                print(address_address_to_check, file=file)
        #    print(f"The address {address_address_to_check} was active on Ethereum blockchain.")
        # else:
        #     print(f"The address {address_address_to_check} was not active on Ethereum blockchain.")
