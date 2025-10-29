from stellar_sdk import (
    Server,
    Keypair,
    TransactionBuilder,
    Network,
    Asset,
)

from stellar_sdk.operation import ChangeTrust, Payment

import config

def establish_trustline(asset_name):

    asset = Asset(asset_name, config.GOVERNMENT_P)

    server = Server(horizon_url="https://horizon-testnet.stellar.org")
    government_keypair = Keypair.from_public_key(config.GOVERNMENT_P)
    treasury_keypair = Keypair.from_secret(config.TREASURY_S)

    account_treasury = server.load_account(treasury_keypair.public_key)

    tx_builder = TransactionBuilder(
        source_account=account_treasury,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )

    operation = ChangeTrust(
        asset=asset,
        limit="1000000000"  # Límite de 1 billón de tokens
    )

    tx_builder.append_operation(operation)
    tx = tx_builder.build()
    tx.sign(treasury_keypair)

    server.submit_transaction(tx)

def print_and_fund_tokens(asset_name, amount_to_print):
    asset = Asset(asset_name, config.GOVERNMENT_P)

    server = Server(horizon_url="https://horizon-testnet.stellar.org")

    government_keypair = Keypair.from_secret(config.GOVERNMENT_S)

    account_government = server.load_account(government_keypair.public_key)

    tx_builder = TransactionBuilder(
        source_account=account_government,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )

    operation = Payment(
        destination=config.TREASURY_P,
        asset=asset,
        amount=amount_to_print
    )

    tx_builder.append_operation(operation)
    tx = tx_builder.build()
    tx.sign(government_keypair)

    # Send transaction to network
    response = server.submit_transaction(tx)
    return response

if __name__ == "__main__":
    establish_trustline(config.ASSET_NAME)
    response = print_and_fund_tokens(config.ASSET_NAME, "1000000")
    print(response)