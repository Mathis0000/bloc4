import client as cl
import algokit_utils as au
import algosdk as sdk
from tp_2 import generate_test_asset
from utils import (
    account_creation,
    display_info,
)

algorand = au.AlgorandClient.from_environment()
algod_client = algorand.client.algod
indexer_client = algorand.client.indexer
alice: au.SigningAccount = account_creation(algorand, "ALICE", au.AlgoAmount(algo=10_000))
bob: au.SigningAccount = account_creation(algorand, "BOB", au.AlgoAmount(algo=100))
asset_id = generate_test_asset(algorand, alice)

factory = algorand.client.get_typed_app_factory(
    cl.DigitalMarketplaceFactory, default_sender=alice.address
)
price = 10_000
result, _ = factory.send.create.create_application(
    cl.CreateApplicationArgs(
        asset_id=asset_id, unitary_price=price
    )
)
app_id = result.app_id
ac = factory.get_app_client_by_id(app_id, default_sender=alice.address)