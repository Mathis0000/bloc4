import algokit_utils as au
import algosdk as sdk
from algokit_utils import AlgorandClient, TransactionParameters
from utils import (
    account_creation,
)
import os
# os.system("algokit compile py --out-dir ./app app.py")
# os.system("algokit generate client app/Eval.arc32.json --output client.py")
import client as cl
import algokit_utils.transactions.transaction_composer as att

# ⚠️ Remplace ta seed phrase ici (NE JAMAIS partager cette phrase publiquement !)
if __name__ == "__main__":
    # Connexion à Algorand TestNet
    algorand = au.AlgorandClient.testnet()

    #créer compte
    mnemonic = "correct dad grape window young trim client retire already piece flower rural maid wool asset code sand gun country tree hamster problem write able mandate"

    private_key = sdk.mnemonic.to_private_key(mnemonic)
    account_address = sdk.account.address_from_private_key(private_key)
    print(f"Adresse du compte: {account_address}")

    mathis = algorand.account.from_mnemonic(mnemonic=mnemonic)





    factory = algorand.client.get_typed_app_factory(
            cl.EvalFactory, default_sender=mathis.address
        )
    app_id = 736038676

    ac = factory.get_app_client_by_id(app_id, default_sender=mathis.address)
    sp = algorand.get_suggested_params()
    send_params=au.SendParams(populate_app_call_resources=True)
    # ac.send.claim_algo(
    #     params=au.CommonAppCallParams(
    #     box_references=[mathis.address],
    #     sender=mathis.address,
    #     signer=mathis.signer
    #     ),
    #     send_params=send_params,
    # )



    # res_asset = algorand.send.asset_create(
    #     au.AssetCreateParams(
    #         sender=mathis.address,
    #         signer=mathis.signer,
    #         total=15,
    #         decimals=0,
    #         default_frozen=False,
    #     )
    # )

    # asset_id = res_asset.confirmation["asset-index"]

    # mbr_pay_txn = algorand.create_transaction.payment(
    #     au.PaymentParams(
    #         sender=mathis.address,
    #         receiver=ac.app_address,
    #         amount=au.AlgoAmount(algo=0.2),
    #         extra_fee=au.AlgoAmount(micro_algo=sp.min_fee),
    #     )
    # )

    # result = ac.send.opt_in_to_asset(
    #     cl.OptInToAssetArgs(
    #         mbr_pay=att.TransactionWithSigner(
    #             mbr_pay_txn,
    #             mathis.signer
    #         ),
    #         asset=asset_id
    #     ),
    #     params=au.CommonAppCallParams(
    #         box_references=[mathis.address],
    #         sender=mathis.address,
    #         signer=mathis.signer,
    #     ),
    #     send_params=send_params
    # )

    # result = ac.send.sum(
    #     cl.SumArgs(
    #         array=bytes([1, 2])
    #     ),
    #     params=au.CommonAppCallParams(
    #         box_references=[mathis.address],
    #         sender=mathis.address,
    #         signer=mathis.signer,
    #     ),
    #     send_params=send_params
    # )

    # result = ac.send.update_box(
    #     cl.UpdateBoxArgs(
    #         value="test"
    #     ),
    #     params=au.CommonAppCallParams(
    #         box_references=[mathis.address],
    #         sender=mathis.address,
    #         signer=mathis.signer,
    #     ),
    #     send_params=send_params
    # )