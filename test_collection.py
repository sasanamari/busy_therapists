"""
Test the complete collection workflow with a small sample
"""
import sys
sys.path.insert(0, '/Users/sasan/spicy_projects/busy_therapists/src')

from scraper import collect_therapists, save_therapists_to_json

# Test with a small sample - 5 therapists
print("Testing complete collection workflow (5 therapists)...\n")

therapists = collect_therapists(
    zip_code="10117",
    target_count=5,  # Small sample for testing
    insurance_type=1,
    availability=4,
    delay_seconds=2.5
)

print(f"\n{'='*60}")
print(f"Collection results:")
print(f"{'='*60}")
for i, t in enumerate(therapists, 1):
    print(f"{i}. {t['name']}")
    print(f"   Email: {t['email']}")
    print(f"   URL: {t['profile_url']}")
    print()

# Save to JSON
if therapists:
    save_therapists_to_json(therapists, "data/test_therapists.json")
    print("\nTest successful! Ready for larger runs.")
else:
    print("\nNo therapists collected. Check for errors above.")
