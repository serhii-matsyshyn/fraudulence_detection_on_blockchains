""" Modified from the source: https://github.com/eltontay/Ethereum-Fraud-Detection """
import logging
import os

import pandas as pd
import requests
from web3 import Web3

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def formQueryString(address, pgNo, offset, api_key):
    return f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&page={pgNo}&offset={offset}&sort=asc&apikey={api_key}"


def get_address_stats_normal_tnx(tag, address):
    response = requests.get(formQueryString(address, 1, 0, os.environ.get("ETHERSCAN_API_KEY")))
    print(response.json()['result'])
    if response.status_code != 200:
        logger.error("Incorrect etherscan code!")
    sample_df = pd.DataFrame(response.json()['result'])
    # Column creation of ETH from Wei
    sample_df['eth value'] = sample_df['value'].apply(lambda x: Web3.from_wei(int(x), 'ether'))

    # Typing of sent and received transactions
    sample_df['txn type'] = sample_df['from'].apply(lambda x: 'sent' if x == address else 'received')

    # Handling of Sent transactions stats
    sample_df_sent = sample_df[sample_df['txn type'] == 'sent']
    sample_df_sent = sample_df_sent.sort_values(by=['timeStamp'])
    sample_df_sent['timeStamp'] = sample_df_sent['timeStamp'].astype('int')

    # Filtering of sent normal transfers to contract addresses
    sample_df_sent_contracts = sample_df[sample_df['contractAddress'] != '']

    # Compilation of normal sent transaction statistics
    core_stats_Sent_tnx = len(sample_df_sent)
    core_stats_MinValSent = sample_df_sent['eth value'].min()
    core_stats_MaxValSent = sample_df_sent['eth value'].max()
    core_stats_AvgValSent = sample_df_sent['eth value'].mean()
    core_stats_MinValueSentToContract = sample_df_sent_contracts['eth value'].min()
    core_stats_MaxValueSentToContract = sample_df_sent_contracts['eth value'].max()
    core_stats_AvgValueSentToContract = sample_df_sent_contracts['eth value'].mean()
    core_stats_TotalEtherSent = sample_df_sent['eth value'].sum()
    core_stats_TotalEtherSent_Contracts = sample_df_sent_contracts['eth value'].sum()
    core_stats_UniqueSentTo_Addresses = len(sample_df_sent['to'].unique())

    # Handling of received transactions stats
    sample_df_received = sample_df[sample_df['txn type'] == 'received']
    sample_df_received = sample_df_received.sort_values(by=['timeStamp'])
    sample_df_received['timeStamp'] = sample_df_received['timeStamp'].astype('int')

    # Compilation of normal received transaction statistics
    core_stats_Received_tnx = len(sample_df_received)
    core_stats_MinValueReceived = sample_df_received['eth value'].min()
    core_stats_MaxValueReceived = sample_df_received['eth value'].max()
    core_stats_AvgValueReceived = sample_df_received['eth value'].mean()
    core_stats_TotalEtherReceived = sample_df_received['eth value'].sum()
    core_stats_UniqueReceivedFrom_Addresses = len(sample_df_received['from'].unique())

    # Handling of remaining normal transaction values
    sample_df['timeStamp'] = sample_df['timeStamp'].astype('int')
    sample_df.sort_values(by=['timeStamp'])
    sample_df['unix time difference'] = sample_df['timeStamp'].diff()
    sample_df_time_dim = sample_df.groupby('txn type')['unix time difference'].sum() / 60

    print(sample_df_time_dim)

    # Compilation of remaining normal transaction statistics
    core_stats_TimeDiffbetweenfirstand_last = ((sample_df['timeStamp'].max()) - (sample_df['timeStamp'].min())) / 60
    core_stats_TotalTransactions = len(sample_df)
    core_stats_NumberofCreated_Contracts = len(sample_df[sample_df['contractAddress'] != ''])

    # Check for division by zero
    if core_stats_Received_tnx != 0:
        core_stats_Avg_min_between_received_tnx = sample_df_time_dim.get('received', 0) / core_stats_Received_tnx
    else:
        core_stats_Avg_min_between_received_tnx = 0

    if core_stats_Sent_tnx != 0:
        core_stats_Avg_min_between_sent_tnx = sample_df_time_dim.get('sent', 0) / core_stats_Sent_tnx
    else:
        core_stats_Avg_min_between_sent_tnx = 0

    core_stats_TotalEtherBalance = core_stats_TotalEtherReceived - core_stats_TotalEtherSent
    compiled_normal_tnx_result = {
        'Address': address, 'tag': tag, 'FLAG': 1,
        'Avg min between sent tnx': core_stats_Avg_min_between_sent_tnx,
        'Avg min between received tnx': core_stats_Avg_min_between_received_tnx,
        'Time Diff between first and last (Mins)': core_stats_TimeDiffbetweenfirstand_last,
        'Sent tnx': core_stats_Sent_tnx, 'Received Tnx': core_stats_Received_tnx,
        'Number of Created Contracts': core_stats_NumberofCreated_Contracts,
        'Unique Received From Addresses': core_stats_UniqueReceivedFrom_Addresses,
        'Unique Sent To Addresses': core_stats_UniqueSentTo_Addresses,
        'min value received': core_stats_MinValueReceived,
        'max value received ': core_stats_MaxValueReceived,
        'avg val received': core_stats_AvgValueReceived,
        'min val sent': core_stats_MinValSent,
        'max val sent': core_stats_MaxValSent,
        'avg val sent': core_stats_AvgValSent,
        'min value sent to contract': core_stats_MinValueSentToContract,
        'max val sent to contract': core_stats_MaxValueSentToContract,
        'avg value sent to contract': core_stats_AvgValueSentToContract,
        'total transactions (including tnx to create contract': core_stats_TotalTransactions,
        'total Ether sent': core_stats_TotalEtherSent,
        'total ether received': core_stats_TotalEtherReceived,
        'total ether sent contracts': core_stats_TotalEtherSent_Contracts,
        'total ether balance': core_stats_TotalEtherBalance}
    return pd.DataFrame([compiled_normal_tnx_result])


# print(get_address_stats_normal_tnx('', "0x04e3d778e3b7f2cf833ac7adceb02b367bc7ebc6"))
#
# exit()
def get_empty_details_for_address(tag, address):
    compiled_empty_address = {
        'Address': address, 'tag': tag, 'FLAG': 1,
        'Avg min between sent tnx': 0,
        'Avg min between received tnx': 0,
        'Time Diff between first and last (Mins)': 0,
        'Sent tnx': 0, 'Received Tnx': 0,
        'Number of Created Contracts': 0,
        'Unique Received From Addresses': 0,
        'Unique Sent To Addresses': 0,
        'min value received': 0,
        'max value received ': 0,
        'avg val received': 0,
        'min val sent': 0,
        'max val sent': 0,
        'avg val sent': 0,
        'min value sent to contract': 0,
        'max val sent to contract': 0,
        'avg value sent to contract': 0,
        'total transactions (including tnx to create contract': 0,
        'total Ether sent': 0,
        'total ether received': 0,
        'total ether sent contracts': 0,
        'total ether balance': 0
    }
    return pd.DataFrame([compiled_empty_address])


# def get_details_for_address(address):
#     normal_address_stats = get_address_stats_normal_tnx(address)
#     return pd.DataFrame(normal_address_stats, index=pd.Series(1))
df_address_in = pd.read_csv('data/2_data_collected/search_results_out.csv')

with open("data/2_data_collected/addresses_processed.txt", "r") as file:
    all_lines_processed = set([line.rstrip() for line in file.readlines() if len(line.rstrip()) > 0])

print(f"Length before cleanup: {len(df_address_in)}")
# Exclude rows with addresses in the all_lines_processed list
df_address_in = df_address_in[~df_address_in['address'].isin(all_lines_processed)]
print(f"Length after cleanup: {len(df_address_in)}")

write_to_file = 'data/2_data_collected/data_collected_out.csv'
base_df = pd.DataFrame()
total_transactions = 0
for i, row in df_address_in.iterrows():
    tag = row['tag']
    address = row['address']
    # print(address)
    # try:
    cand_df = get_address_stats_normal_tnx(tag=tag, address=address)
    cand_df.to_csv(write_to_file, mode='a', index=False, header=False)
    base_df = pd.concat([base_df, cand_df])
    itxns = cand_df.loc[0, 'total transactions (including tnx to create contract']
    total_transactions = total_transactions + itxns

    logger.info("Address number {}: {} mined! {} retrieved. {} total transactions.".format(i, address, itxns,
                                                                                           total_transactions))
    # except Exception as err:
    #     print(err)
    #     cand_df = get_empty_details_for_address(tag=tag, address=address)
    #     base_df = pd.concat([base_df, cand_df])
    #     cand_df.to_csv(write_to_file, mode='a', index=False, header=False)
    #     logger.info("Address number {}: {} mined! 0 txns retrieved. {} total transactions.".format(i, address, total_transactions))

    with open("data/2_data_collected/addresses_processed.txt", "a") as file:
        print(address, file=file)

base_df = base_df.reset_index(drop=True)
