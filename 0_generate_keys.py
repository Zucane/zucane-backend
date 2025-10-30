from stellar_sdk import Keypair

import requests

def create_keypair():
    kp = Keypair.random()
    public_key = kp.public_key
    secret_key = kp.secret

    return public_key, secret_key

def activate_account(public_key):
    url = "https://friendbot.stellar.org"
    response = requests.get(url, params={"addr": public_key})
    return response

if __name__ == "__main__":
    issuer_p, government_s = create_keypair()
    treasury_p, treasury_s = create_keypair()

    status_government = activate_account(issuer_p)
    status_treasury = activate_account(treasury_p)

    if status_government.status_code == 200 and status_treasury.status_code == 200:
        print("-- KEYPAIRS SUCCESSFULY GENERATED (SAVE THIS)--")
        print(f"ISSUER PUBLIC KEY: {issuer_p}")
        print(f"ISSUER SECRET KEY: {government_s}\n")

        print(f"TREASURY PUBLIC KEY: {treasury_p}")
        print(f"TREASURY SECRET KEY: {treasury_s}")