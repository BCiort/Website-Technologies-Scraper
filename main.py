import asyncio
import aiohttp
from src.fetcher import fetch_domain_data
from src.analyzer import Analyzer


async def main():
    analyzer = Analyzer()
    test_domains = [
        "shopify.com",
        "wordpress.org",
        "react.dev",
    ]

    print("Start:\n")
    unique_technologies = set()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_domain_data(session, domain) for domain in test_domains]
        results = await asyncio.gather(*tasks)

        for res in results:
            domain = res['domain']

            if res.get("error"):
                print(f"[X] EROARE pentru {domain}: {res['error']}")
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