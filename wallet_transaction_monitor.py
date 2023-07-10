import requests
import time
import winsound
from datetime import datetime

# ANSI escape sequences for color formatting
GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'

def monitor_wallets(wallets, filename):
    while True:
        with open(filename, 'a') as file:
            for wallet in wallets:
                wallet_address = wallet['address']
                wallet_name = wallet['name']
                url = f"https://blockchain.info/rawaddr/{wallet_address}"
                balance = wallet.get('balance', None)
                last_timestamp = wallet.get('last_timestamp', int(time.time()))
                processed_transactions = set()

                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        data = response.json()
                        new_balance = data['final_balance'] / 1e8  # Convert balance from satoshis to BTC
                        transactions = data['txs']

                        if balance is None:
                            balance = new_balance
                            wallet['balance'] = new_balance
                        elif new_balance != balance:
                            print(f"Balance change detected in wallet '{wallet_name}'!")
                            print(f"Previous balance: {balance} BTC")
                            print(f"Current balance: {new_balance} BTC")
                            file.write(f"Balance change detected in wallet '{wallet_name}'!\n")
                            file.write(f"Previous balance: {balance} BTC\n")
                            file.write(f"Current balance: {new_balance} BTC\n")
                            balance = new_balance
                            wallet['balance'] = new_balance

                        # Check incoming and outgoing transactions
                        for transaction in transactions:
                            timestamp = transaction['time']
                            if timestamp > last_timestamp:
                                last_timestamp = timestamp
                                tx_hash = transaction['hash']
                                amount = abs(transaction['result']) / 1e8
                                timestamp_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')  # Convert timestamp to string format
                                if tx_hash not in processed_transactions:  # Check if transaction already processed
                                    if transaction['result'] >= 0:
                                        print(f"{GREEN}Incoming transaction in '{wallet_name}': {tx_hash}")
                                        print(f"Amount: {amount} BTC")
                                        print(f"Timestamp: {timestamp_str}{ENDC}")
                                        file.write(f"Incoming transaction in '{wallet_name}': {tx_hash}\n")
                                        file.write(f"Amount: {amount} BTC\n")
                                        file.write(f"Timestamp: {timestamp_str}\n")
                                    else:
                                        print(f"{RED}Outgoing transaction from '{wallet_name}': {tx_hash}")
                                        print(f"Amount: {amount} BTC")
                                        print(f"Timestamp: {timestamp_str}{ENDC}")
                                        file.write(f"Outgoing transaction from '{wallet_name}': {tx_hash}\n")
                                        file.write(f"Amount: {amount} BTC\n")
                                        file.write(f"Timestamp: {timestamp_str}\n")

                                    # Play a sound
                                    winsound.PlaySound("soundfile.wav", winsound.SND_FILENAME)  # Replace "soundfile.wav" with your sound file

                                    processed_transactions.add(tx_hash)  # Add transaction to processed set

                        wallet['last_timestamp'] = last_timestamp

                except requests.exceptions.RequestException as e:
                    print(f"An error occurred while monitoring wallet '{wallet_name}': {str(e)}")
                    file.write(f"An error occurred while monitoring wallet '{wallet_name}': {str(e)}\n")

        time.sleep(60)  # Check every 60 seconds

# Prompt for wallet information
wallets = []
num_wallets = int(input("Enter the number of wallets you want to monitor: "))
for i in range(num_wallets):
    wallet_address = input(f"Enter Bitcoin wallet address #{i+1}: ")
    wallet_name = input(f"Enter a custom name for wallet #{i+1}: ")
    wallets.append({'address': wallet_address, 'name': wallet_name})

filename = input("Enter a filename for saving the monitoring information: ")

print("Monitoring wallets... (Press Ctrl+C to stop)")
monitor_wallets(wallets, filename)
