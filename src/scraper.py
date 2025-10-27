"""
Therapist data scraper for therapie.de

Scrapes therapist contact information from therapie.de based on search criteria.
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, List
import time
import json
from pathlib import Path


def decode_email(encoded: str) -> str:
    """
    Decode encoded email address

    Args:
        encoded: Encoded email string

    Returns:
        Decoded email address

    Examples:
        >>> decode_email("bmjdfAxpoefsmboe/fy")
        'alice@wonderland.ex'
    """
    decoded = []

    for char in encoded:
        if char == 'A':
            decoded.append('@')
        elif char == '/':
            decoded.append('.')
        elif char.isalpha():
            # Shift back by 1 in the alphabet
            if char.islower():
                decoded.append(chr((ord(char) - ord('a') - 1) % 26 + ord('a')))
            else:
                decoded.append(chr((ord(char) - ord('A') - 1) % 26 + ord('A')))
        else:
            # Keep other characters as-is
            decoded.append(char)

    return ''.join(decoded)


def get_therapist_profile(profile_url: str) -> Optional[Dict[str, str]]:
    """
    Extract therapist info from a profile page

    Args:
        profile_url: Full URL to therapist profile (e.g., "https://www.therapie.de/profil/alice/")

    Returns:
        Dictionary with therapist info if found, None if no email:
        {
            "name": "Dr. Alice Wonderland",
            "email": "alice@example.com",
            "profile_url": "https://...",
            # Future fields: "phone", "address", "specializations", etc.
        }
    """
    try:
        response = requests.get(profile_url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'lxml')

        # Find the contact button with encoded email
        contact_button = soup.find('button', id='contact-button')

        if not contact_button or not contact_button.get('data-contact-email'):
            return None

        # Extract email
        encoded_email = contact_button['data-contact-email']
        decoded_email = decode_email(encoded_email)

        # Extract name (usually in <h1> tag)
        name_tag = soup.find('h1')
        name = name_tag.get_text(strip=True) if name_tag else "Unknown"

        return {
            "name": name,
            "email": decoded_email,
            "profile_url": profile_url
        }

    except requests.RequestException as e:
        print(f"Error fetching {profile_url}: {e}")
        return None


def scrape_search_results(zip_code: str, insurance_type: int = 1, availability: int = 4, page: int = 1) -> list[str]:
    """
    Scrape therapist profile URLs from a single search results page

    Args:
        zip_code: German postal code (e.g., "10117")
        insurance_type: 1 = gesetzlich (statutory), 2 = privat (private)
        availability: 4 = Freie Plätze (free slots available)
        page: Page number (default: 1)

    Returns:
        List of full profile URLs from this page
    """
    base_url = "https://www.therapie.de/therapeutensuche/ergebnisse/"
    params = {
        "ort": zip_code,
        "abrechnungsverfahren": insurance_type,
        "terminzeitraum": availability,
    }

    if page > 1:
        params["seite"] = page

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'lxml')

        # Find all profile links
        # Profile links are in format: <a href="/profil/username/">
        profile_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/profil/') and href.endswith('/'):
                full_url = f"https://www.therapie.de{href}"
                if full_url not in profile_links:  # Avoid duplicates
                    profile_links.append(full_url)

        return profile_links

    except requests.RequestException as e:
        print(f"Error fetching search results: {e}")
        return []


def collect_therapists(
    zip_code: str,
    target_count: int = 20,
    insurance_type: int = 1,
    availability: int = 4,
    max_pages: int = 10,
    delay_seconds: float = 2.5
) -> List[Dict[str, str]]:
    """
    Collect therapist data until target count is reached

    Args:
        zip_code: German postal code (e.g., "10117")
        target_count: Number of therapists with valid emails to collect
        insurance_type: 1 = gesetzlich (statutory), 2 = privat (private)
        availability: 4 = Freie Plätze (free slots available)
        max_pages: Maximum number of search result pages to process
        delay_seconds: Delay between requests (default: 2.5 seconds)

    Returns:
        List of dictionaries containing therapist info:
        [{"name": "...", "email": "...", "profile_url": "..."}, ...]
    """
    collected = []
    page = 1

    print(f"Searching for {target_count} therapists in {zip_code}...")
    print(f"Filters: insurance_type={insurance_type}, availability={availability}")
    print(f"Rate limit: {delay_seconds}s between requests\n")

    while len(collected) < target_count and page <= max_pages:
        print(f"Page {page}: Fetching search results...")
        profile_urls = scrape_search_results(zip_code, insurance_type, availability, page)

        if not profile_urls:
            print(f"No more results found on page {page}. Stopping.")
            break

        print(f"Found {len(profile_urls)} profiles on page {page}")

        for i, profile_url in enumerate(profile_urls, 1):
            if len(collected) >= target_count:
                break

            print(f"  [{i}/{len(profile_urls)}] Checking profile...")
            time.sleep(delay_seconds)

            therapist_info = get_therapist_profile(profile_url)

            if therapist_info:
                collected.append(therapist_info)
                print(f"    ✓ Found: {therapist_info['name']} - {therapist_info['email']} (Total: {len(collected)}/{target_count})")
            else:
                print(f"    ✗ No email found, skipping")

        page += 1
        if len(collected) < target_count and page <= max_pages:
            print(f"\nMoving to page {page}...\n")

    print(f"\nCollection complete: {len(collected)} therapists with valid emails")
    return collected


def save_therapists_to_json(therapists: List[Dict[str, str]], output_path: str = "data/therapists.json") -> None:
    """
    Save collected therapist data to JSON file

    Args:
        therapists: List of therapist dictionaries from collect_therapists()
        output_path: Path to output JSON file (default: "data/therapists.json")
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(therapists, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(therapists)} therapists to {output_path}")


if __name__ == "__main__":
    # Test the email decoder
    # "alice@wonderland.ex" encoded is "bmjdfAxpoefsmboe/fy"
    test_encoded = "bmjdfAxpoefsmboe/fy"
    test_decoded = decode_email(test_encoded)
    print(f"Encoded: {test_encoded}")
    print(f"Decoded: {test_decoded}")
    print(f"Expected: alice@wonderland.ex")
    print(f"Match: {test_decoded == 'alice@wonderland.ex'}")
    print()

    # Test profile scraping
    print("Testing profile scraper...")
    test_url = "https://www.therapie.de/profil/alice/"  # Non-existent profile for testing
    profile_info = get_therapist_profile(test_url)
    print(f"Profile info: {profile_info}")
    print()

    # Uncomment to test search results scraping (makes real HTTP request)
    # print("Testing search results scraper...")
    # profile_urls = scrape_search_results("10117", insurance_type=1, availability=4, page=1)
    # print(f"Found {len(profile_urls)} profiles on page 1")
    # if profile_urls:
    #     print(f"First 3 profiles: {profile_urls[:3]}")
    # print()

    # Uncomment to test complete collection workflow (makes many real HTTP requests)
    # print("Testing complete collection workflow...")
    # therapists = collect_therapists(
    #     zip_code="10117",
    #     target_count=20,  # Default recommended count
    #     insurance_type=1,
    #     availability=4,
    #     delay_seconds=2.5
    # )
    # print(f"\nCollected therapists:")
    # for t in therapists:
    #     print(f"  - {t['name']}: {t['email']}")
