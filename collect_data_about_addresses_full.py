""" Modified from the source: https://github.com/eltontay/Ethereum-Fraud-Detection """
import logging
import os

import pandas as pd
from etherscan import Etherscan
from tqdm import tqdm
from web3 import Web3

assert os.environ.get("ETHERSCAN_API_KEY"), "ETHERSCAN_API_KEY not set"
eth = Etherscan(os.environ.get("ETHERSCAN_API_KEY"))

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_address_stats_normal_tnx(data, address, tag):
    sample_df = pd.DataFrame(data)
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

    # Compilation of remaining normal transaction statistics
    core_stats_TimeDiffbetweenfirstand_last = ((sample_df['timeStamp'].max()) - (sample_df['timeStamp'].min())) / 60
    core_stats_TotalTransactions = len(sample_df)
    core_stats_NumberofCreated_Contracts = len(sample_df[sample_df['contractAddress'] != ''])
    # core_stats_Avg_min_between_received_tnx = sample_df_time_dim['received'] / core_stats_Received_tnx
    # core_stats_Avg_min_between_sent_tnx = sample_df_time_dim['sent'] / core_stats_Sent_tnx

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
        'Address': address, 'tag': tag, 'FLAG': 0,
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
        'total ether balance': core_stats_TotalEtherBalance
    }
    return compiled_normal_tnx_result


def get_address_stats_erc20_tnx(data, address):
    sample_df = pd.DataFrame(data)

    # Column creation of ETH from Wei
    sample_df['eth value'] = sample_df['value'].apply(lambda x: Web3.from_wei(int(x), 'ether'))

    # Typing of sent and received ERC20 transactions
    sample_df['txn type'] = sample_df['from'].apply(lambda x: 'sent' if x == address else 'received')

    # Handling of Sent ERC20 transactions stats
    sample_df_sent = sample_df[sample_df['txn type'] == 'sent']
    sample_df_sent = sample_df_sent.sort_values(by=['timeStamp'])
    sample_df_sent['timeStamp'] = sample_df_sent['timeStamp'].astype('int')

    # Creation of unix time difference column for Sent ERC20 transactions
    sample_df_sent['unix time diff'] = sample_df_sent['timeStamp'].diff()

    # Compilation of ERC20 sent transaction statistics
    core_stats_ERC20TotalEther_Sent = sample_df_sent['eth value'].sum()
    core_stats_ERC20TotalEtherSentContract = len(
        sample_df_sent[sample_df_sent['to'] != sample_df_sent['contractAddress']])
    core_stats_ERC20UniqSent_Addr = len(sample_df_sent['to'].unique())
    core_stats_ERC20AvgTimeBetweenSent_Tnx = (
            (sample_df_sent['unix time diff'].sum() / (len(sample_df_sent) - 1)) / 60) if (
                                                                                                  len(sample_df_sent) - 1) > 0 else 0
    core_stats_ERC20AvgTimeBetweenContract_Tnx = 0
    core_stats_ERC20MinVal_Sent = sample_df_sent['eth value'].min()
    core_stats_ERC20MaxVal_Sent = sample_df_sent['eth value'].max()
    core_stats_ERC20AvgVal_Sent = sample_df_sent['eth value'].mean()
    core_stats_ERC20UniqSentTokenName = len(sample_df_sent['tokenName'].unique())
    core_stats_ERC20MostSentTokenType = [sample_df_sent['tokenName'].mode().tolist()]

    # Handling of received ERC20 transactions stats
    sample_df_received = sample_df[sample_df['txn type'] == 'received']
    sample_df_received = sample_df_received.sort_values(by=['timeStamp'])
    sample_df_received['timeStamp'] = sample_df_received['timeStamp'].astype('int')

    # Creation of unix time difference column for received ERC20 transactions
    sample_df_received['unix time diff'] = sample_df_received['timeStamp'].diff()

    # Compilation of ERC20 received transaction statistics
    core_stats_ERC20TotalEther_Received = sample_df_received['eth value'].sum()
    core_stats_ERC20UniqRec_Addr = len(sample_df_received['from'].unique())
    core_stats_ERC20UniqRecContractAddr = len(sample_df_received['contractAddress'].unique())
    core_stats_ERC20AvgTimeBetweenRec_Tnx = (
            (sample_df_received['unix time diff'].sum() / (len(sample_df_received) - 1)) / 60) if (
                                                                                                          len(sample_df_received) - 1) > 0 else 0
    core_stats_ERC20MinVal_Rec = sample_df_received['eth value'].min()
    core_stats_ERC20MaxVal_Rec = sample_df_received['eth value'].max()
    core_stats_ERC20AvgVal_Rec = sample_df_received['eth value'].mean()
    core_stats_ERC20UniqRecTokenName = len(sample_df_received['tokenName'].unique())
    core_stats_ERC20MostRecTokenType = [sample_df_received['tokenName'].mode().tolist()]

    # Compilation of remaining ERC20 transaction statistics
    core_stats_TotalERC20Tnxs = len(sample_df)
    compiled_ERC20_tnx_result = {
        'Address': address,
        ' Total ERC20 tnxs': core_stats_TotalERC20Tnxs,
        ' ERC20 total Ether received': core_stats_ERC20TotalEther_Received,
        ' ERC20 total ether sent': core_stats_ERC20TotalEther_Sent,
        ' ERC20 total Ether sent contract': core_stats_ERC20TotalEtherSentContract,
        ' ERC20 uniq sent addr': core_stats_ERC20UniqSent_Addr,
        ' ERC20 uniq rec addr': core_stats_ERC20UniqRec_Addr,
        ' ERC20 uniq sent addr.1': 0,
        ' ERC20 uniq rec contract addr': core_stats_ERC20UniqRecContractAddr,
        ' ERC20 avg time between sent tnx': core_stats_ERC20AvgTimeBetweenSent_Tnx,
        ' ERC20 avg time between rec tnx': core_stats_ERC20AvgTimeBetweenRec_Tnx,
        ' ERC20 avg time between rec 2 tnx': 0,
        ' ERC20 avg time between contract tnx': core_stats_ERC20AvgTimeBetweenContract_Tnx,
        ' ERC20 min val rec': core_stats_ERC20MinVal_Rec,
        ' ERC20 max val rec': core_stats_ERC20MaxVal_Rec,
        ' ERC20 avg val rec': core_stats_ERC20AvgVal_Rec,
        ' ERC20 min val sent': core_stats_ERC20MinVal_Sent,
        ' ERC20 max val sent': core_stats_ERC20MaxVal_Sent,
        ' ERC20 avg val sent': core_stats_ERC20AvgVal_Sent,
        ' ERC20 min val sent contract': 0,
        ' ERC20 max val sent contract': 0,
        ' ERC20 avg val sent contract': 0,
        ' ERC20 uniq sent token name': core_stats_ERC20UniqSentTokenName,
        ' ERC20 uniq rec token name': core_stats_ERC20UniqRecTokenName,
        ' ERC20 most sent token type': core_stats_ERC20MostSentTokenType,
        ' ERC20_most_rec_token_type': core_stats_ERC20MostRecTokenType}
    return compiled_ERC20_tnx_result


def get_empty_details_for_address_NORMAL(address, tag):
    compiled_empty_address = {
        'Address': address, 'tag': tag, 'FLAG':0,
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
    return compiled_empty_address


def get_empty_details_for_address_ERC20(address, tag):
    compiled_empty_address = {
        'Address': address,
        ' Total ERC20 tnxs': 0,
        ' ERC20 total Ether received': 0,
        ' ERC20 total ether sent': 0,
        ' ERC20 total Ether sent contract': 0,
        ' ERC20 uniq sent addr': 0,
        ' ERC20 uniq rec addr': 0,
        ' ERC20 uniq sent addr.1': 0,
        ' ERC20 uniq rec contract addr': 0,
        ' ERC20 avg time between sent tnx': 0,
        ' ERC20 avg time between rec tnx': 0,
        ' ERC20 avg time between rec 2 tnx': 0,
        ' ERC20 avg time between contract tnx': 0,
        ' ERC20 min val rec': 0,
        ' ERC20 max val rec': 0,
        ' ERC20 avg val rec': 0,
        ' ERC20 min val sent': 0,
        ' ERC20 max val sent': 0,
        ' ERC20 avg val sent': 0,
        ' ERC20 min val sent contract': 0,
        ' ERC20 max val sent contract': 0,
        ' ERC20 avg val sent contract': 0,
        ' ERC20 uniq sent token name': 0,
        ' ERC20 uniq rec token name': 0,
        ' ERC20 most sent token type': [[]],
        ' ERC20_most_rec_token_type': [[]]
    }
    return compiled_empty_address


def get_empty_details_for_address(address, tag):
    compiled_empty_address = {
        'Address': address, 'tag': tag, 'FLAG': 0,
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
        'total ether balance': 0,
        ' Total ERC20 tnxs': 0,
        ' ERC20 total Ether received': 0,
        ' ERC20 total ether sent': 0,
        ' ERC20 total Ether sent contract': 0,
        ' ERC20 uniq sent addr': 0,
        ' ERC20 uniq rec addr': 0,
        ' ERC20 uniq sent addr.1': 0,
        ' ERC20 uniq rec contract addr': 0,
        ' ERC20 avg time between sent tnx': 0,
        ' ERC20 avg time between rec tnx': 0,
        ' ERC20 avg time between rec 2 tnx': 0,
        ' ERC20 avg time between contract tnx': 0,
        ' ERC20 min val rec': 0,
        ' ERC20 max val rec': 0,
        ' ERC20 avg val rec': 0,
        ' ERC20 min val sent': 0,
        ' ERC20 max val sent': 0,
        ' ERC20 avg val sent': 0,
        ' ERC20 min val sent contract': 0,
        ' ERC20 max val sent contract': 0,
        ' ERC20 avg val sent contract': 0,
        ' ERC20 uniq sent token name': 0,
        ' ERC20 uniq rec token name': 0,
        ' ERC20 most sent token type': [[]],
        ' ERC20_most_rec_token_type': [[]]
    }
    return pd.DataFrame(compiled_empty_address)


def get_all_data(address, tag):
    try:
        try:
            normal_txn_data = eth.get_normal_txs_by_address(address=address, startblock=0,
                                                            endblock=99999999, sort='asc')
            normal_address_stats = get_address_stats_normal_tnx(normal_txn_data, address, tag=tag)
        except Exception as err:
            # logger.debug("No normal_address_stats")
            normal_address_stats = get_empty_details_for_address_NORMAL(address, tag)

        try:
            erc20_txn_data = eth.get_erc20_token_transfer_events_by_address(address=address, startblock=0,
                                                                            endblock=99999999, sort='asc')
            ERC20_stats = get_address_stats_erc20_tnx(erc20_txn_data, address)
        except Exception as err:
            # logger.debug("No ERC20_stats")
            ERC20_stats = get_empty_details_for_address_ERC20(address, tag)

        final_stats = {}
        final_stats.update(normal_address_stats)
        final_stats.update(ERC20_stats)

        data_manual_aggregate = pd.DataFrame(final_stats)
    except Exception as err:
        logger.critical("Critical: ", err)
        data_manual_aggregate = get_empty_details_for_address(address, tag=tag)
    return data_manual_aggregate


def main():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    # addresss = [
    #     "0xeFb3729Bc9C0ee64c718185d612C9538C0323306",  # walet with nonce
    #     "0xDef1C0ded9bec7F1a1670819833240f027b25EfF",  # address contract with balance
    #     "0xF57e7e7C23978C3cAEC3C3548E3D615c346e79fF",  # address contract no balance
    #     "0x4F773f3FC89b73B34FB57EBc667a245D5e3812F6",  # has nft
    #     "0x94ffc85CB5B4D6819a99387DAB8b4aD80cc0120c"   # empty
    # ]
    #
    # for address_address_to_check in tqdm(addresss):
    #
    #     print(get_all_data(address_address_to_check, "ff"))

    in_data = 'data/4_data_collected_normal_addresses/interacted_addresses_out.csv'
    save_to = 'data/4_data_collected_normal_addresses/interacted_addresses_data_collected_out.csv'
    processed_addresses = "data/4_data_collected_normal_addresses/addresses_processed.txt"

    # in_data = 'data/4_data_collected_normal_addresses/interacted_addresses_out_2.csv'
    # save_to = 'data/4_data_collected_normal_addresses/interacted_addresses_data_collected_out_2.csv'
    # processed_addresses = "data/4_data_collected_normal_addresses/addresses_processed.txt"

    df_address_in = pd.read_csv(in_data)

    with open(processed_addresses, "r") as file:
        all_lines_processed = set([line.rstrip() for line in file.readlines() if len(line.rstrip()) > 0])

    logger.info(f"Length before cleanup: {len(df_address_in)}")
    # Exclude rows with addresses in the all_lines_processed list
    df_address_in = df_address_in[~df_address_in['address'].isin(all_lines_processed)]
    logger.info(f"Length after cleanup: {len(df_address_in)}")

    write_to_file = save_to
    base_df = pd.DataFrame()
    total_transactions = 0
    for i, row in tqdm(df_address_in.iterrows()):
        tag = row['tag']
        address = row['address']

        cand_df = get_all_data(address=address, tag=tag)
        cand_df.to_csv(write_to_file, mode='a', index=False, header=False)
        base_df = pd.concat([base_df, cand_df])
        itxns = cand_df.loc[0, 'total transactions (including tnx to create contract']
        total_transactions = total_transactions + itxns

        logger.info("Address number {}: {} mined! {} retrieved. {} total transactions.".format(i, address, itxns,
                                                                                               total_transactions))

        with open(processed_addresses, "a") as file:
            print(address, file=file)

    # base_df = base_df.reset_index(drop=True)


if __name__ == '__main__':
    main()
