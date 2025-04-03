# **ESP Miner Auto-Pool configuration script**

This script is designed to automate the process of configuring and managing mining devices running **BitAxe OS** or similar systems, including **Lucky Miners**. It allows you to apply pool configuration settings to multiple miners and restart them to implement the changes without doing it manually. 

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

**2)** Add miners: Modify the miners dictionary in the script with your miner's IP addresses and aliases.

```bash
miners = {
    "192.168.0.1": "BitAxe01",
    "192.168.0.2": "LuckyLV08",
    "192.168.0.3": "Ultra01",
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
```

**3)** Execute the script by running the following command in your terminal: **espminer-pool.py**

Follow the prompts: 
The script will display current settings for each miner, list available pool configuration files, and ask you to select a configuration to apply. Confirm your choice, and the script will apply the settings to all miners and restart them.


## **Notes**

License

This script is open-source and free to use, modify, and distribute. Feel free to contribute to the project or improve it as you see fit.
