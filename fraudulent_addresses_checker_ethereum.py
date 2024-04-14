import joblib
import numpy as np
import pandas as pd
import xgboost as xgb

from collect_data_about_addresses_full import get_all_data

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


class FraudulentAddressesCheckerEthereum:
    def __init__(self, model_path="data/models/1/xgboost_model_1.json", scaler_path="data/models/1/scaler.gz"):
        # Load the saved model and scaler
        self.model = xgb.Booster()
        self.model.load_model(model_path)

        self.scaler = joblib.load(scaler_path)

        self.columns = [
            # 'Address',
            # 'tag',
            # 'FLAG',
            'Avg min between sent tnx',
            'Avg min between received tnx',
            'Time Diff between first and last (Mins)',
            'Sent tnx',
            'Received Tnx',
            'Number of Created Contracts',
            'Unique Received From Addresses',
            'Unique Sent To Addresses',
            'min value received',
            'max value received ',
            'avg val received',
            # 'min val sent',
            'max val sent',
            'avg val sent',
            'min value sent to contract',
            # 'max val sent to contract',
            'avg value sent to contract',
            'total transactions (including tnx to create contract',
            # 'total Ether sent',
            'total ether received',
            'total ether sent contracts',
            'total ether balance',
            ' Total ERC20 tnxs',
            ' ERC20 total Ether received',
            ' ERC20 total ether sent',
            # ' ERC20 total Ether sent contract',
            ' ERC20 uniq sent addr',
            ' ERC20 uniq rec addr',
            # ' ERC20 uniq sent addr.1',
            # ' ERC20 uniq rec contract addr',
            ' ERC20 avg time between sent tnx',
            ' ERC20 avg time between rec tnx',
            # ' ERC20 avg time between rec 2 tnx',
            # ' ERC20 avg time between contract tnx',
            ' ERC20 min val rec',
            ' ERC20 max val rec',
            ' ERC20 avg val rec',
            # ' ERC20 min val sent',
            # ' ERC20 max val sent',
            ' ERC20 avg val sent',
            # ' ERC20 min val sent contract',
            # ' ERC20 max val sent contract',
            # ' ERC20 avg val sent contract',
            # ' ERC20 uniq sent token name',
            # ' ERC20 uniq rec token name',
            # ' ERC20 most sent token type',
            # ' ERC20_most_rec_token_type',
        ]

    @staticmethod
    def converter(x):
        if isinstance(x, (int, float)):
            return np.log(x) if x > 0 else 0
        return x

    def check_address(self, address) -> float:
        df = get_all_data(address, "")
        df = df.drop(columns=['Address', 'FLAG', 'tag'])

        df = df.fillna(0)
        df = df[self.columns]

        for c in self.columns:
            df[c] = df[c].apply(self.converter)

        # Scaling
        df.rename(columns={'max value received ': 'max value received'}, inplace=True)
        X = self.scaler.transform(df)

        # Use the loaded model for predictions
        predictions = self.model.predict(xgb.DMatrix(X))
        return float(predictions[0])


if __name__ == '__main__':
    checker = FraudulentAddressesCheckerEthereum()

    # Close to 0 - definitely not fraudulent
    # Close to 1 - fraudulent
    print(checker.check_address("0x1fBad35b92bE6B0754EA7b87D6e9072627527672"))  # Fake_Phishing327049
    print(checker.check_address("0xb5d85CBf7cB3EE0D56b3bB207D5Fc4B82f43F511"))  # Coinbase 5
    print(checker.check_address("0xe97C5331bf3ca4f22c76e958872D07c923E0367C"))  # Random addresses
    print(checker.check_address("0x995A014a6D43Ad9F49DddE79803936Cd1111aB8D"))  # Random addresses

