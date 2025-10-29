#RUN ONLY ONCE TO GENERATE GOVERNMENT AND TREASURY KEYS
# IMPORTANT -- > Copy and paste them into config.py

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
    GOVERNMENT_PK, GOVERNMENT_SS = create_keypair()
    TREASURY_PK, TREASURY_SS = create_keypair()

    status_government = activate_account(GOVERNMENT_PK)
    status_treasury = activate_account(TREASURY_PK)

    if status_government.status_code == 200 and status_treasury.status_code == 200:
        print("-- KEYPAIRS SUCCESSFULY GENERATED (SAVE THIS)--")
        print(f"GOVERNMENT_PK: {GOVERNMENT_PK}")
        print(f"GOVERNMENT_SS: {GOVERNMENT_SS}\n")
        print(f"TREASURY_PK: {TREASURY_PK}")
        print(f"TREASURY_SS: {TREASURY_SS}")




