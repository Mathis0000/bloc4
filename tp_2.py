import algokit_utils as au
import algosdk as sdk
from utils import (
    account_creation,
    display_info,
)
from algokit_utils import AlgorandClient, Account, AssetCreateParams
import random
#creer l'asset
def generate_test_asset(algorand: AlgorandClient, sender: au.SigningAccount, total: int | None = None) -> int:
    """Create a test asset and return its ID"""
    if total is None:
        total = random.randint(20, 120)

    create_result = algorand.send.asset_create(
        AssetCreateParams(
            sender=sender.address,
            total=15,
            decimals=0,
            default_frozen=False,
            unit_name="Mathis",
            asset_name=f"Test Asset {random.randint(1,100)}",
            url="https://example.com",
            manager=sender.address,
            reserve=sender.address,
            freeze=sender.address,
            clawback=sender.address,
        )
    )

    return int(create_result.confirmation["asset-index"])
algorand = au.AlgorandClient.from_environment()
algod_client = algorand.client.algod
indexer_client = algorand.client.indexer
alice: au.SigningAccount = account_creation(algorand, "ALICE", au.AlgoAmount(algo=10_000))
bob: au.SigningAccount = account_creation(algorand, "BOB", au.AlgoAmount(algo=100))

asset_id = generate_test_asset(algorand, alice)
params = algod_client.suggested_params()
# Bob opts-in to receive the asset
opt_in_txn = sdk.transaction.AssetTransferTxn(
    sender=bob.address,
    sp=params,
    receiver=bob.address,
    amt=0,
    index=asset_id
)

# Sign the opt-in transaction
signed_opt_in_txn = opt_in_txn.sign(bob.private_key)

# Send the opt-in transaction
opt_in_tx_id = algod_client.send_transaction(signed_opt_in_txn)

# Wait for confirmation
sdk.transaction.wait_for_confirmation(algod_client, opt_in_tx_id, 4)

# Create the asset transfer transaction
asset_transfer_txn = sdk.transaction.AssetTransferTxn(
    sender=alice.address,
    sp=params,
    receiver=bob.address,
    amt=1,
    index=asset_id
)

# Sign the transaction
signed_asset_transfer_txn = asset_transfer_txn.sign(alice.private_key)

# Send 1 token from Alice to Bob only if Bob sends 1 algo to Alice
params = algod_client.suggested_params()

# Create a payment transaction from Bob to Alice (1 Algo)
pay_txn_bob_to_alice = sdk.transaction.PaymentTxn(bob.address, params, alice.address, 1000000)

# Create an asset transfer transaction from Alice to Bob (1 token)
asset_transfer_txn = sdk.transaction.AssetTransferTxn(alice.address, params, bob.address, 1, asset_id)

# Group the transactions
gid = sdk.transaction.calculate_group_id([pay_txn_bob_to_alice, asset_transfer_txn])
pay_txn_bob_to_alice.group = gid
asset_transfer_txn.group = gid

# Sign the transactions again with the group ID
signed_txn_bob_to_alice = pay_txn_bob_to_alice.sign(bob.private_key)
signed_asset_transfer_txn = asset_transfer_txn.sign(alice.private_key)

# Send the grouped transactions
signed_group = [signed_txn_bob_to_alice, signed_asset_transfer_txn]
tx_id = algod_client.send_transactions(signed_group)

res = sdk.transaction.wait_for_confirmation(algod_client, tx_id, 4)

print('Transaction confirmed, round: '
    f'{res["confirmed-round"]}')
