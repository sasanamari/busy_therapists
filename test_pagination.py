"""
Test script to check if therapists appear on multiple pagination pages
"""
import sys
sys.path.insert(0, '/Users/sasan/spicy_projects/busy_therapists/src')

from scraper import scrape_search_results
import time

# Test with Berlin zip code
zip_code = "10117"

print("Fetching page 1...")
page1_urls = scrape_search_results(zip_code, insurance_type=1, availability=4, page=1)
print(f"Page 1: {len(page1_urls)} profiles")

time.sleep(2.5)  # Rate limit

print("\nFetching page 2...")
page2_urls = scrape_search_results(zip_code, insurance_type=1, availability=4, page=2)
print(f"Page 2: {len(page2_urls)} profiles")

# Check for duplicates
duplicates = set(page1_urls) & set(page2_urls)

print(f"\n{'='*60}")
if duplicates:
    print(f"⚠️  Found {len(duplicates)} duplicate(s) between pages:")
    for url in duplicates:
        print(f"  - {url}")
else:
    print("✓ No duplicates found between page 1 and page 2")

print(f"{'='*60}")

print(f"\nPage 1 first 3: {page1_urls[:3]}")
print(f"Page 2 first 3: {page2_urls[:3]}")
