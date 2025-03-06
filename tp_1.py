import algokit_utils as au
import algosdk as sdk
from utils import (
    account_creation,
    display_info,
)
from algokit_utils import AlgorandClient, Account, AssetCreateParams
import random
algorand = au.AlgorandClient.from_environment()
algod_client = algorand.client.algod
indexer_client = algorand.client.indexer

print(algod_client.block_info(0))
print(indexer_client.health())
alice: au.SigningAccount = account_creation(algorand, "ALICE", au.AlgoAmount(algo=10_000))
bob: au.SigningAccount = account_creation(algorand, "BOB", au.AlgoAmount(algo=100))
#alice vers bob


sdk.mnemonic.from_private_key(alice.private_key)
params = algod_client.suggested_params()
pay_txn = sdk.transaction.PaymentTxn(alice.address, params, bob.address, 1000000)
signed_txn = pay_txn.sign(alice.private_key)
tx_id = algod_client.send_transaction(signed_txn)
res = sdk.transaction.wait_for_confirmation(algod_client, tx_id, 4)

print('Transaction confirmed, round: '
        f'{res["confirmed-round"]}')

#bob vers alice
params = algod_client.suggested_params()
pay_txn = sdk.transaction.PaymentTxn(bob.address, params, alice.address, 1000000)
signed_txn = pay_txn.sign(bob.private_key)
tx_id = algod_client.send_transaction(signed_txn)
res = sdk.transaction.wait_for_confirmation(algod_client, tx_id, 4)

print('Transaction confirmed, round: '
        f'{res["confirmed-round"]}')

