import requests
import time
import winsound
from datetime import datetime

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'

def monitor_wallet(wallet_address):
    url = f"https://blockchain.info/rawaddr/{wallet_address}"
    balance = None
    last_timestamp = int(time.time())
    
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                new_balance = data['final_balance'] / 1e8  # Convert balance from satoshis to BTC
                transactions = data['txs']

                if balance is None:
                    balance = new_balance
                elif new_balance != balance:
                    print(f"Triggered: Balance change detected in wallet {wallet_address}!")
                    print(f"Previous balance: {balance} BTC")
                    print(f"Current balance: {new_balance} BTC")
                    balance = new_balance

                # Check incoming and outgoing transactions
                for transaction in transactions:
                    timestamp = transaction['time']
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp
                        tx_hash = transaction['hash']
                        amount = abs(transaction['result']) / 1e8
                        timestamp_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')  # Convert timestamp to string format
                        if transaction['result'] >= 0:
                            print(f"{GREEN}Incoming transaction: {tx_hash}")
                            print(f"Amount: {amount} BTC")
                            print(f"Timestamp: {timestamp_str}{ENDC}")
                        else:
                            print(f"{RED}Outgoing transaction: {tx_hash}")
                            print(f"Amount: {amount} BTC")
                            print(f"Timestamp: {timestamp_str}{ENDC}")
                            
                        # Play a sound
                        winsound.PlaySound("soundfile.wav", winsound.SND_FILENAME)  # Replace "soundfile.wav" with your sound file

            time.sleep(60)  # Check every 60 seconds

        except requests.exceptions.RequestException as e:
            print("An error occurred:", str(e))
            time.sleep(60)  # Retry after 60 seconds if there was an error

wallet_address = input("Enter your Bitcoin wallet address: ")
monitor_wallet(wallet_address)