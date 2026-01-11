import requests
import time

files = {
    "car.json": "https://lottie.host/5a919e1d-8521-460d-b847-19d4b4a3c104/R3k9j7k1qj.json",
    "login.json": "https://lottie.host/93e62053-5296-410a-8c87-9d7a22026773/rQj9W0q2zE.json",
    "stars.json": "https://lottie.host/4b816331-5513-4318-9698-964196398077/1X9Z0j8j10.json",
    "arrow.json": "https://lottie.host/7e946197-7631-4583-990e-66083577411d/8664327570.json"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

for filename, url in files.items():
    print(f"Downloading {filename}...")
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(r.content)
        print(f"Saved {filename}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
    time.sleep(1)
