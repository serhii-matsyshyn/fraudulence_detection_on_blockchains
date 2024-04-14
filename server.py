from cachetools import TTLCache
from fastapi import HTTPException, FastAPI
from web3 import Web3

from fraudulent_addresses_checker_ethereum import FraudulentAddressesCheckerEthereum

app = FastAPI()

web3 = Web3()
checker = FraudulentAddressesCheckerEthereum(
    model_path="data/models/1/xgboost_model.json",
    scaler_path="data/models/1/scaler.gz"
)
cache = TTLCache(maxsize=1000, ttl=60)  # Cache with 60 seconds life


@app.get("/check_fraudulence")
async def check_fraudulence(eth_address: str):
    if not web3.is_address(eth_address):
        raise HTTPException(status_code=400, detail="Invalid Ethereum address")

    if not (address_check_result := cache.get(eth_address)):
        address_check_result = checker.check_address(eth_address)
        cache[eth_address] = address_check_result

    if address_check_result >= 0.5:
        return {
            "fraudulent": True,
            "address_check_result": address_check_result,
            "message": "This address is potentially fraudulent"
        }
    else:
        return {
            "fraudulent": False,
            "address_check_result": address_check_result,
            "message": "This address is not fraudulent"
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
