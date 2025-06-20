# **ESP Miner Auto-Pool configuration script**

This script is designed to automate the process of configuring and managing pool settings for mining devices running **BitAxe OS** / **[ESP-Miner](https://github.com/bitaxeorg/ESP-Miner)**
including jailbroken devices such as **Lucky Miners**. It allows you to apply pool configuration settings to multiple miners and restart them to implement the changes without doing it manually. 

The script fetches current miner settings, validates configuration files, and applies new settings to all miners in your network.


## **Features**

- Lists all available pool configuration files in the current directory.
- Fetches current settings from multiple miners via their API.
- Validates pool configuration files to ensure required fields are present.
- Automatically applies new pool configuration settings to all miners and restarts them.
- Supports multiple miners along unique aliases, eg: btcaddress.WorkerName <- alias

## **Requirements**

- **Python 3.x**
- **requests** library for making HTTP requests to miner APIs.

To install the required dependencies, run:

```bash
pip install requests
```
## **How to Run:**
**1)** Clone or download the script to your machine.

**2)** Add miners: Modify the miners dictionary in the script with your miner's IP addresses, aliases and start difficulty (only applies if ZERG_POOL.cfg is loaded).

```bash
miners = {
    "192.168.0.1": ["WORKER1",2500],
    "192.168.0.2": ["WORKER2",6000],
    "192.168.0.2": ["WORKER3",11000],
}
```
**3) Create .cfg files:**

Create as many .cfg pool configuration files as you want, one for each crypto you wish to mine. Place them in the same directory as the script.

The pool configuration files should follow the .cfg format with key-value pairs like the following example:

```bash
stratumURL = your-pool-url.com
fallbackStratumURL = your-fallback-url.com
stratumPort = 1234
fallbackStratumPort = 1234
stratumUser = yourusername
fallbackStratumUser = yourusername (DO NOT PUT WORKER NAME HERE, INSTEAD SET WORKERNAME IN THE SCRIPT)

ZERG_POOL.cfg have some custom fields, look inside the config. 
```

Now support ZergPool password concatenation check ZERG_POOL.cfg please read the comments within the code. 

**3)** Execute the script by running the following command in your terminal: **espminer-pool.py**

Follow the prompts: 
The script will display current settings for each miner, list available pool configuration files, and ask you to select a configuration to apply. 

Confirm your choice, and the script will apply the settings to all miners and restart them.


## **Notes**

License

This script is open-source and free to use, modify, and distribute. Feel free to contribute to the project or improve it as you see fit.
