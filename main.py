import json
from web3 import Web3
import time
import random

# устанавливаем рандомный таймаут между кошельками
time_ot = 50
time_do = 200

# RPCs
polygon_rpc_url = 'https://polygon-rpc.com/'
w3 = Web3(Web3.HTTPProvider(polygon_rpc_url))
# ABI
abi = json.load(open('api.json'))
# NFT contract
contr_polygon_address = w3.to_checksum_address('0x9d5D479a84F3358E8e27Afe056494BD2dA239acD')
nft_contract = w3.eth.contract(address=contr_polygon_address, abi=abi)


with open("privates.txt", "r") as f:
    keys_list = [row.strip() for row in f if row.strip()]
    numbered_keys = list(enumerate(keys_list, start=1))
    random.shuffle(numbered_keys) # перемешивание кошельков, можно закомментить

wallets_prob = []
for wallet_number, PRIVATE_KEY in numbered_keys:
    account = w3.eth.account.from_key(PRIVATE_KEY)
    address = account.address

    print(time.strftime("%H:%M:%S", time.localtime()))
    print(f'[{wallet_number}] - {address}', flush=True)

    try:
        swap_txn = nft_contract.functions.mint(
        ).build_transaction({
            'from': address,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(address),
        })
        signed_swap_txn = w3.eth.account.sign_transaction(swap_txn, PRIVATE_KEY)
        swap_txn_hash = w3.eth.send_raw_transaction(signed_swap_txn.rawTransaction)
        print(f"Transaction: https://polygonscan.com/tx/{swap_txn_hash.hex()}")

        time.sleep(random.randint(time_ot, time_do))
    except Exception as err:
        print(f"Unexpected {err=}")
        wallets_prob.append(address)

if len(wallets_prob) > 0:
    print("Есть проблемки")
    print(wallets_prob)
else:
    print("Закончили без ошибок")

