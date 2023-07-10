### Wallet Transaction Monitor
This script monitors a Bitcoin wallet address and notifies the user when there are changes in the balance or new transactions. It provides real-time updates on incoming and outgoing transactions, along with the corresponding amounts and timestamps. Additionally, it can play a sound notification on Windows when a new transaction occurs.

<img src="https://i.ibb.co/6DtVpR3/Screenshot-2023-07-10-101803.png)" alt="Wallet Transaction Monitor">

### Requirements
Python 3.x
requests library: You can install it by running pip install requests.
winsound module: This module is available by default on Windows.


### How to Run
* Make sure you have Python 3.x installed on your system.
* pip install -r requirements.txt
* Clone or download the script file wallet_transaction_monitor.py from this repository.
* Place the sound file (in .wav format) you want to use for the notification in the same directory as the script. Make sure to replace "soundfile.wav" in the script with the actual filename of your sound file.
* Open a terminal or command prompt and navigate to the directory where the script is located.

- Run the script by executing the following command:
``` shell
python wallet_transaction_monitor.py
```

The script will start monitoring the wallet and display updates whenever there are changes in the balance or new transactions. It will also play the specified sound notification on Windows.

### Important Notes
This script is designed to work on Windows due to the use of the winsound module for sound notifications. If you are using a different operating system, you may need to modify the sound-related code or use an alternative method for audio notifications.
The script uses the Blockchain.info API to fetch wallet data. Please ensure you have a stable internet connection for the script to work correctly.
It's recommended to run the script in the background or keep the terminal window open while monitoring the wallet.
