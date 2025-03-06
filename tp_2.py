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


# Send 1 token from Alice to Bob
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

# Send the transaction
tx_id = algod_client.send_transaction(signed_asset_transfer_txn)

# Wait for confirmation
res = sdk.transaction.wait_for_confirmation(algod_client, tx_id, 4)

print('Asset transfer confirmed, round: '
      f'{res["confirmed-round"]}')