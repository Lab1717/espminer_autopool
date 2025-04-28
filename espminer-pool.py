import os
import sys
import requests
import time

# DEFINE MINERS AS A DICTIONARY {IP: [ALIAS, SD?]} # SD or sart difficulty (the integer value) is only used for ZERG_POOL.cfg; leave it out or set to None/empty to skip it.
miners = {
    "192.168.0.118": ["Lucky07_Papi",2222],
    "192.168.0.211": ["Lucky08_Papi",3333], 
    # You can omit SD entirely, as this example: "192.168.0.212": ["WORKER_3"],
    
}

REQUIRED_FIELDS = [
    "stratumURL", "fallbackStratumURL", "stratumPort",
    "fallbackStratumPort", "stratumUser", "fallbackStratumUser"
]

def list_pool_files():
    files = [f for f in os.listdir() if f.endswith(".cfg")]
    if not files:
        print("NO POOL CONFIG FILES FOUND IN THE ROOT DIRECTORY!")
        sys.exit(1)
    return files

def read_pool_config(filename):
    config = {}
    with open(filename, "r") as file:
        for line in file:
            if not line.strip() or line.startswith("#"):
                continue
            key, value = line.strip().split("=", 1)
            config[key.strip()] = value.strip()
    return config

def validate_pool_config(config):
    missing_fields = [f for f in REQUIRED_FIELDS if f not in config]
    if missing_fields:
        raise ValueError(f"MISSING REQUIRED FIELDS: {', '.join(missing_fields)}")

def compose_zerg_password(miner_alias, config):
    # 'c' is required, 'sd' is optional
    if 'c' not in config:
        raise ValueError("Missing ZERG field: c")
    pwd = f"ID={miner_alias}"
    sd_val = config.get('sd')
    if sd_val not in (None, "", 0):
        pwd += f",sd={sd_val}"
    pwd += f",c={config['c']}"
    mc_val = config.get('mc', '').strip()
    if mc_val:
        pwd += f",mc={mc_val}"
    m_val = config.get('m', '').strip()
    if m_val:
        pwd += f",m={m_val}"
    return pwd

def fetch_miner_settings(miner_ip):
    try:
        r = requests.get(f"http://{miner_ip}/api/system/info", timeout=10)
        r.raise_for_status()
        d = r.json()
        return {
            "stratumURL": d.get("stratumURL"),
            "fallbackStratumURL": d.get("fallbackStratumURL"),
            "stratumPort": d.get("stratumPort"),
            "fallbackStratumPort": d.get("fallbackStratumPort"),
            "stratumUser": d.get("stratumUser"),
            "fallbackStratumUser": d.get("fallbackStratumUser"),
        }
    except requests.exceptions.RequestException as e:
        print(f"ERROR FETCHING MINER SETTINGS FROM {miner_ip}: {e}")
        return None

def restart_miner(miner_ip):
    try:
        print(f"RESTARTING MINER AT {miner_ip}...")
        r = requests.post(f"http://{miner_ip}/api/system/restart", timeout=10)
        r.raise_for_status()
        print(f"MINER {miner_ip} RESTARTED SUCCESSFULLY.")
    except requests.exceptions.RequestException as e:
        print(f"ERROR RESTARTING MINER {miner_ip}: {e}")

def set_system_settings(config, pool_filename):
    for miner_ip, md in miners.items():
        # safe unpack: alias mandatory, sd optional
        miner_alias = md[0]
        miner_sd = md[1] if len(md) > 1 else None

        miner_cfg = config.copy()
        # inject per-miner sd only if provided
        if miner_sd not in (None, "", 0):
            miner_cfg['sd'] = miner_sd

        if pool_filename == "ZERG_POOL.cfg":
            miner_cfg["stratumPassword"] = compose_zerg_password(miner_alias, miner_cfg)
        else:
            miner_cfg["stratumUser"] = f"{miner_cfg['stratumUser']}.{miner_alias}"
            miner_cfg["fallbackStratumUser"] = f"{miner_cfg['fallbackStratumUser']}.{miner_alias}"

        try:
            miner_cfg["stratumPort"] = int(miner_cfg.get("stratumPort", 0))
            miner_cfg["fallbackStratumPort"] = int(miner_cfg.get("fallbackStratumPort", 0))
        except ValueError:
            print(f"ERROR: INVALID PORT VALUE IN CONFIG FOR {miner_ip}")
            continue

        try:
            print(f"APPLYING SETTINGS TO {miner_alias} ({miner_ip})...")
            r = requests.patch(f"http://{miner_ip}/api/system", json=miner_cfg, timeout=10)
            r.raise_for_status()
            print(f"SETTINGS APPLIED TO {miner_alias} SUCCESSFULLY.")
            time.sleep(2)
            restart_miner(miner_ip)
        except requests.exceptions.RequestException as e:
            print(f"ERROR APPLYING SETTINGS TO {miner_alias}: {e}")

def main():
    num = len(miners)
    print("#############################################################################")
    print("########### WELCOME TO THE MINER POOL CONFIGURATION SCRIPT! #################")
    print(f"### FOUND {num} MINER{'S' if num>1 else ''} WITH YOUR CURRENT SETTINGS ###")
    print("#############################################################################\n")

    for ip, md in miners.items():
        alias = md[0]
        s = fetch_miner_settings(ip)
        if s:
            print(f"\n[CURRENT POOL SETTINGS FOR {alias} ({ip})]")
            print(f"  > PRIMARY STRATUM: {s['stratumURL']}:{s['stratumPort']}")
            print(f"  > FALLBACK STRATUM: {s['fallbackStratumURL']}:{s['fallbackStratumPort']}")
            print(f"  > STRATUM USER: {s['stratumUser']}")
            print(f"  > FALLBACK USER: {s['fallbackStratumUser']}")

    pool_files = list_pool_files()
    print("\n############################################################")
    print(f"  > FOUND {len(pool_files)} POOL CONFIGURATION FILES:\n")
    for i, f in enumerate(pool_files, 1):
        print(f"  {i}. {f}")

    while True:
        try:
            choice = int(input("\nSELECT A POOL CONFIG FILE (ENTER NUMBER): ").strip())
            if 1 <= choice <= len(pool_files):
                sel = pool_files[choice-1]
                break
            print("INVALID SELECTION. TRY AGAIN.")
        except ValueError:
            print("ENTER A VALID NUMBER.")

    print("\n###############################################################")
    print(f"#### LOADING CONFIGURATION FROM {sel} ###########")
    print("###############################################################")

    cfg = read_pool_config(sel)
    try:
        validate_pool_config(cfg)
        print(f"\nLOADED POOL CONFIG: {sel}")
        for k,v in cfg.items():
            print(f"  {k}: {v}")

        if sel == "ZERG_POOL.cfg":
            print("\nYOUR ZERGPOOL GENERATED STRATUM PASSWORDS WILL BE:")
            for ip, md in miners.items():
                alias = md[0]
                sd = md[1] if len(md)>1 else None
                tmp = cfg.copy()
                if sd not in (None, "", 0):
                    tmp['sd'] = sd
                pwd = compose_zerg_password(alias, tmp)
                print(f"  {alias}: {pwd}")

        ans = input("\nDO YOU WANT TO APPLY THIS CONFIGURATION FOR ALL DEVICES? (YES/NO): ").strip().lower()
        if ans in ("yes","y"):
            set_system_settings(cfg, sel)
            print("\nDONE! GOOD LUCK!")
            print("\nWant to buy me beer? -> BTC: bc1qn7wn5dqc3mu5da7za234nt2h3mav8rh8mgp99e or DGB: DEqnipmHmcuTwFRUHPxVpVsZgNMnBEm6x4")
        else:
            print("CONFIGURATION WAS NOT APPLIED.")

    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
