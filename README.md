# **ESP Miner Pool Configuration Script**

This script is designed to automate the process of configuring and managing mining devices running **BitAxe OS** or similar systems, including **jailbroken Lucky Miners**. It allows you to apply pool configuration settings to multiple miners and restart them to implement the changes. The script fetches current miner settings, validates configuration files, and applies new settings to all miners in your network.

## **Features**

- Lists all available pool configuration files in the current directory.
- Fetches current settings from multiple miners via their API.
- Validates pool configuration files to ensure required fields are present.
- Automatically applies new pool configuration settings to all miners and restarts them.
- Supports multiple miners, including jailbroken Lucky Miners, with unique aliases.
- Provides clear error handling for any issues encountered during fetching or applying settings.

## **Requirements**

- Python 3.x
- `requests` library for making HTTP requests to miner APIs.

To install the required dependencies, run:

```bash
pip install requests
How to Run
Download the script: Clone or download the script to your machine.

Add miners: Modify the miners dictionary in the script with your miner's IP addresses and aliases.

Create .cfg files: Create as many .cfg pool configuration files as you want, one for each crypto you wish to mine. Place them in the same directory as the script.

Run the script: Execute the script by running the following command in your terminal:


python miner_pool_config.py
Follow the prompts: The script will display current settings for each miner, list available pool configuration files, and ask you to select a configuration to apply. Confirm your choice, and the script will apply the settings to all miners and restart them.

Configuration File Format
The pool configuration files should follow the .cfg format with key-value pairs like the following example:

ini
Copia
Modifica
stratumURL = stratum+tcp://your-pool-url.com
fallbackStratumURL = stratum+tcp://fallback-url.com
stratumPort = 3333
fallbackStratumPort = 3333
stratumUser = yourusername
fallbackStratumUser = yourusername
Ensure that all required fields are present as defined in the REQUIRED_FIELDS list:

stratumURL

fallbackStratumURL

stratumPort

fallbackStratumPort

stratumUser

fallbackStratumUser

Notes
The script is compatible with BitAxe OS devices and other miners that expose a similar API.

Jailbroken Lucky Miners can also be configured using this script, provided they are running a compatible API.

The miners dictionary should be modified to include the IP addresses and aliases of your mining devices.

Pool configuration settings will be applied to all miners listed in the miners dictionary.
