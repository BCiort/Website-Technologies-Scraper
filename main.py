import asyncio
import os
import aiohttp
from src.fetcher import fetch_domain_data
from src.analyzer import Analyzer


def load_domains(file_path: str) -> list:
    if not os.path.exists(file_path):
        print(f"[!] ERROR: File not found {file_path}")
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


async def main():
    analyzer = Analyzer()

    test_domains = load_domains("domains.txt")

    if not test_domains:
        print("Domains could not be loaded.")
        return

    print(f"Start on {len(test_domains)} domains::\n")
    unique_technologies = set()

    connector = aiohttp.TCPConnector(limit=20)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch_domain_data(session, domain) for domain in test_domains]
        results = await asyncio.gather(*tasks)

        for res in results:
            domain = res['domain']

            if res.get("error"):
                print(f"[X] Error for {domain}: {res['error']}")
                continue

            found_technologies = analyzer.analyze(res)

            if found_technologies:
                print(f"[!] {domain}:")
                for tech in found_technologies:
                    print(f"    -> {tech['name']} ({tech['category']})")
                    unique_technologies.add(tech['name'])
            else:
                print(f"[X] {domain}: No known technologies.")

            print("-" * 40)

    print(f"Unique technologies found: {len(unique_technologies)}")
if __name__ == "__main__":
    asyncio.run(main())