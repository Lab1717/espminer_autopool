import os
import sys
import requests
import time

# DEFINE MINERS AS A DICTIONARY {IP: ALIAS}
miners = {
    "192.168.0.1": "Workername1",
    "192.168.0.2": "Workername2",
}

REQUIRED_FIELDS = [
    "stratumURL", "fallbackStratumURL", "stratumPort",
    "fallbackStratumPort", "stratumUser", "fallbackStratumUser"
]

def list_pool_files():
    """LISTS ALL .CFG FILES IN THE CURRENT DIRECTORY."""
    files = [f for f in os.listdir() if f.endswith(".cfg")]
    if not files:
        print("NO POOL CONFIG FILES FOUND IN THE ROOT DIRECTORY!")
        sys.exit(1)
    return files

def read_pool_config(filename):
    """READS STRATUM DETAILS FROM THE SELECTED POOL CONFIG FILE."""
    config = {}
    with open(filename, "r") as file:
        for line in file:
            if not line.strip() or line.startswith("#"):  # SKIP EMPTY LINES OR COMMENTS
                continue
            key, value = line.strip().split("=", 1)
            config[key.strip()] = value.strip()
    return config

def validate_pool_config(config):
    """VALIDATES THAT ALL REQUIRED FIELDS ARE PRESENT IN THE CONFIG."""
    missing_fields = [field for field in REQUIRED_FIELDS if field not in config]
    if missing_fields:
        raise ValueError(f"MISSING REQUIRED FIELDS: {', '.join(missing_fields)}")

def fetch_miner_settings(miner_ip):
    """FETCH MINING SETTINGS FROM THE MINER API."""
    try:
        response = requests.get(f"http://{miner_ip}/api/system/info", timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "stratumURL": data.get("stratumURL"),
            "fallbackStratumURL": data.get("fallbackStratumURL"),
            "stratumPort": data.get("stratumPort"),
            "fallbackStratumPort": data.get("fallbackStratumPort"),
            "stratumUser": data.get("stratumUser"),
            "fallbackStratumUser": data.get("fallbackStratumUser")
        }
    except requests.exceptions.RequestException as e:
        print(f"ERROR FETCHING MINER SETTINGS FROM {miner_ip}: {e}")
        return None

def restart_miner(miner_ip):
    """RESTARTS THE MINER AFTER APPLYING NEW SETTINGS."""
    try:
        print(f"RESTARTING MINER AT {miner_ip}...")
        response = requests.post(f"http://{miner_ip}/api/system/restart", timeout=10)
        response.raise_for_status()
        print(f"MINER {miner_ip} RESTARTED SUCCESSFULLY.")
    except requests.exceptions.RequestException as e:
        print(f"ERROR RESTARTING MINER {miner_ip}: {e}")

def set_system_settings(config):
    """APPLIES NEW STRATUM SETTINGS TO ALL MINERS AND RESTARTS THEM."""
    for miner_ip, miner_alias in miners.items():
        miner_config = config.copy()  # COPY THE CONFIG TO AVOID MODIFYING THE ORIGINAL
        
        # APPEND THE ALIAS TO THE USERS
        miner_config["stratumUser"] = f"{miner_config['stratumUser']}.{miner_alias}"
        miner_config["fallbackStratumUser"] = f"{miner_config['fallbackStratumUser']}.{miner_alias}"

        # ENSURE THE PORTS ARE CORRECTLY SET AS INTEGERS
        try:
            miner_config["stratumPort"] = int(miner_config.get("stratumPort", 0))  # CONVERT TO INTEGER
            miner_config["fallbackStratumPort"] = int(miner_config.get("fallbackStratumPort", 0))  # CONVERT TO INTEGER
        except ValueError:
            print(f"ERROR: INVALID PORT VALUE IN CONFIG FOR {miner_ip}")
            continue  # SKIP THIS MINER IF THERE'S AN ISSUE WITH THE PORT VALUE

        try:
            print(f"APPLYING SETTINGS TO {miner_alias} ({miner_ip})...")
            response = requests.patch(f"http://{miner_ip}/api/system", json=miner_config, timeout=10)
            response.raise_for_status()
            print(f"SETTINGS APPLIED TO {miner_alias} SUCCESSFULLY.")
            time.sleep(2)  # SHORT DELAY BEFORE RESTART
            restart_miner(miner_ip)
        except requests.exceptions.RequestException as e:
            print(f"ERROR APPLYING SETTINGS TO {miner_alias}: {e}")

def main():
    """MAIN EXECUTION FLOW."""
    num_miners = len(miners)
    print("#############################################################################")
    print("########### WELCOME TO THE MINER POOL CONFIGURATION SCRIPT! #################")
    print(f"### FOUND {num_miners} MINER{'S' if num_miners > 1 else ''} WITH YOUR CURRENT SETTINGS ###")
    print("#############################################################################\n")

    # FETCH AND DISPLAY CURRENT SETTINGS FOR ALL MINERS FIRST
    for miner_ip, miner_alias in miners.items():
        miner_settings = fetch_miner_settings(miner_ip)
        if miner_settings:
            print(f"\n[CURRENT POOL SETTINGS FOR {miner_alias} ({miner_ip})]")
            print(f"  > PRIMARY STRATUM: {miner_settings['stratumURL']}:{miner_settings['stratumPort']}")
            print(f"  > FALLBACK STRATUM: {miner_settings['fallbackStratumURL']}:{miner_settings['fallbackStratumPort']}")
            print(f"  > STRATUM USER: {miner_settings['stratumUser']}")
            print(f"  > FALLBACK USER: {miner_settings['fallbackStratumUser']}")

    # LIST AVAILABLE POOL FILES ONCE
    pool_files = list_pool_files()

    print("\n############################################################")
    print(f"  > FOUND {len(pool_files)} POOL CONFIGURATION FILES:\n")

    # ASK USER TO SELECT A POOL FILE
    for i, file in enumerate(pool_files, 1):
        print(f"  {i}. {file}")
    
    while True:
        try:
            choice = int(input("\nSELECT A POOL CONFIG FILE (ENTER NUMBER): ").strip())
            if 1 <= choice <= len(pool_files):
                selected_pool_file = pool_files[choice - 1]
                break
            else:
                print("INVALID SELECTION. TRY AGAIN.")
        except ValueError:
            print("ENTER A VALID NUMBER.")

    print("\n###############################################################")
    print(f"#### LOADING CONFIGURATION FROM {selected_pool_file} ###########")
    print("###############################################################")

    # LOAD AND VALIDATE POOL CONFIG
    pool_config = read_pool_config(selected_pool_file)
    try:
        validate_pool_config(pool_config)
        print(f"\nLOADED POOL CONFIG: {selected_pool_file}")
        for key, value in pool_config.items():
            print(f"  {key}: {value}")

        # CONFIRM BEFORE APPLYING
        apply_choice = input("\nDO YOU WANT TO APPLY THIS CONFIGURATION FOR ALL DEVICES? (YES/NO): ").strip().lower()

        if apply_choice in ["yes", "y"]:
            set_system_settings(pool_config)
            print("\nDONE! GOOD LUCK!") 
            print("\nWANT TO BUY ME A BEER? -> bc1qn7wn5dqc3mu5da7za234nt2h3mav8rh8mgp99e")  
        else:
            print("CONFIGURATION WAS NOT APPLIED.")

    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
