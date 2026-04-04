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
    Decode encoded email address using shift-1 cipher with punctuation mapping

    Args:
        encoded: Encoded email string

    Returns:
        Decoded email address

    Examples:
        >>> decode_email("bmjdfAxpoefsmboe/fy")
        'alice@wonderland.ex'
    """
    # Punctuation mappings (shift-1 cipher)
    # Note: Based on ASCII shift-1 pattern (char + 1 to encode, char - 1 to decode)
    punct_map = {
        'A': '@',   # Confirmed via testing
        '/': '.',   # Confirmed via testing
        '.': '-',   # Confirmed via testing (hyphen encodes to period)
        '`': '_',   # Likely but unverified (underscore would encode to backtick)
        ',': '+',   # Likely but unverified (plus would encode to comma)
    }

    decoded = []

    for char in encoded:
        # Check explicit punctuation mapping first
        if char in punct_map:
            decoded.append(punct_map[char])
            continue

        # Letters: shift back by 1
        if char.isalpha():
            base = ord('a') if char.islower() else ord('A')
            decoded.append(chr((ord(char) - base - 1) % 26 + base))
            continue

        # Digits: shift back by 1 (with wraparound)
        if char.isdigit():
            decoded.append(str((int(char) - 1) % 10))
            continue

        # Otherwise keep as-is (shouldn't happen if encoding is consistent)
        decoded.append(char)

    return ''.join(decoded)


def get_therapist_profile(profile_url: str, max_retries: int = 2) -> Optional[Dict[str, str]]:
    """
    Extract therapist info from a profile page

    Args:
        profile_url: Full URL to therapist profile (e.g., "https://www.therapie.de/profil/alice/")
        max_retries: Maximum number of retries for rate limit errors (default: 2)

    Returns:
        Dictionary with therapist info if found, None if no email:
        {
            "name": "Dr. Alice Wonderland",
            "email": "alice@example.com",
            "profile_url": "https://...",
            # Future fields: "phone", "address", "specializations", etc.
        }
    """
    retry_delays = [60, 300]  # 1 min, 5 min

    for attempt in range(max_retries + 1):
        try:
            response = requests.get(profile_url, timeout=10)

            # Handle rate limiting
            if response.status_code == 429:
                if attempt < max_retries:
                    wait_time = retry_delays[attempt]
                    print(f"    ⚠️  Rate limited (429). Waiting {wait_time}s before retry {attempt + 1}/{max_retries}...")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"    ✗ Rate limited after {max_retries} retries, skipping")
                    return None

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

            # Extract address
            street = soup.find(itemprop="streetAddress")
            postal = soup.find(itemprop="postalCode")
            city = soup.find(itemprop="addressLocality")
            address = " ".join(
                tag.get_text(strip=True) for tag in [street, postal, city] if tag
            )

            return {
                "name": name,
                "email": decoded_email,
                "address": address,
                "profile_url": profile_url
            }

        except requests.RequestException as e:
            # For non-429 errors, don't retry
            print(f"Error fetching {profile_url}: {e}")
            return None

    return None


def scrape_search_results(
    zip_code: str,
    page: int = 1,
    search_radius: int = None,
    max_retries: int = 2,
    insurance_type: int = None,
    availability: int = None,
    language: int = None,
    therapy_type: int = None,
    focus: int = None,
    gender: int = None,
) -> list[str]:
    """
    Scrape therapist profile URLs from a single search results page

    Args:
        zip_code: German postal code (e.g., "10117")
        page: Page number (default: 1)
        search_radius: Search radius in km. None = therapie.de default (~10km).
                       Use 25 as fallback when default radius yields too few results.
        max_retries: Maximum number of retries for rate limit errors (default: 2)
        insurance_type: abrechnungsverfahren (1=GKV, 2=PKV, 3=self-pay, 6=Kostenerstattung).
        availability: terminzeitraum (1=available now, 2=up to 3 months, 3=over 3 months,
                      4=over 12 months).
        language: sprache (3=English, 26=Persian, etc.).
        therapy_type: therapieangebot (1=individual, 2=family, 3=group, etc.).
        focus: arbeitsschwerpunkt (2=anxiety, 10=depression, 30=ADHD, etc.).
        gender: geschlecht (1=male, 2=female, 4=non-binary).
        All filter params default to None = no filter applied.

    Returns:
        List of full profile URLs from this page
    """
    base_url = "https://www.therapie.de/therapeutensuche/ergebnisse/"
    params = {"ort": zip_code}

    if insurance_type is not None:
        params["abrechnungsverfahren"] = insurance_type
    if availability is not None:
        params["terminzeitraum"] = availability
    if language is not None:
        params["sprache"] = language
    if therapy_type is not None:
        params["therapieangebot"] = therapy_type
    if focus is not None:
        params["arbeitsschwerpunkt"] = focus
    if gender is not None:
        params["geschlecht"] = gender
    if search_radius is not None:
        params["search_radius"] = search_radius
    if page > 1:
        params["page"] = page

    retry_delays = [60, 300]  # 1 min, 5 min

    for attempt in range(max_retries + 1):
        try:
            response = requests.get(base_url, params=params, timeout=10)

            # Handle rate limiting
            if response.status_code == 429:
                if attempt < max_retries:
                    wait_time = retry_delays[attempt]
                    print(f"⚠️  Rate limited (429). Waiting {wait_time}s before retry {attempt + 1}/{max_retries}...")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"✗ Rate limited after {max_retries} retries, skipping page")
                    return []

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
            # For non-429 errors, don't retry
            print(f"Error fetching search results: {e}")
            return []

    return []


def collect_therapists(
    zip_code: str,
    target_count: int = 20,
    max_pages: int = 10,
    delay_seconds: float = 2.5,
    insurance_type: int = None,
    availability: int = None,
    language: int = None,
    therapy_type: int = None,
    focus: int = None,
    gender: int = None,
) -> List[Dict[str, str]]:
    """
    Collect therapist data until target count is reached.

    Starts with the default search radius. If results run out before reaching
    target_count, automatically retries with a 25km radius.

    Args:
        zip_code: German postal code (e.g., "10117")
        target_count: Number of therapists with valid emails to collect
        max_pages: Maximum number of search result pages to process
        delay_seconds: Delay between requests (default: 2.5 seconds)
        insurance_type, availability, language, therapy_type, focus, gender:
            Optional search filters. All default to None (no filter applied).
            See scrape_search_results() for value meanings.

    Returns:
        List of dictionaries containing therapist info:
        [{"name": "...", "email": "...", "profile_url": "..."}, ...]
    """
    collected = []
    seen_urls = set()
    page = 1
    search_radius = None  # None = default radius (therapie.de decides, ~10km)

    print(f"Searching for {target_count} therapists in {zip_code}...")
    print(f"Rate limit: {delay_seconds}s between requests\n")

    while len(collected) < target_count and page <= max_pages:
        print(f"Page {page}: Fetching search results...")
        profile_urls = scrape_search_results(
            zip_code,
            page=page,
            search_radius=search_radius,
            insurance_type=insurance_type,
            availability=availability,
            language=language,
            therapy_type=therapy_type,
            focus=focus,
            gender=gender,
        )

        # Detect when we've exhausted results — all remaining are duplicates or nothing returned
        new_urls = [u for u in profile_urls if u not in seen_urls]

        if not profile_urls:
            # Server returned nothing — truly exhausted this radius
            if search_radius is None:
                print(f"\nNo more results in default radius. Expanding search to 25km...\n")
                search_radius = 25
                page = 1
                continue
            else:
                print(f"No more results found. Stopping.")
                break

        print(f"Found {len(new_urls)} new profiles on page {page}")

        for i, profile_url in enumerate(new_urls, 1):
            if len(collected) >= target_count:
                break

            seen_urls.add(profile_url)

            print(f"  [{i}/{len(new_urls)}] Checking profile...")
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
