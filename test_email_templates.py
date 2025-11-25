"""Test email templates with different scenarios"""
import sys
sys.path.insert(0, '/Users/sasan/spicy_projects/busy_therapists/src')

from email_generator import generate_emails_for_therapists
import json

# Load test therapist
with open("data/test_therapists.json", 'r', encoding='utf-8') as f:
    therapists = json.load(f)

# Test 1: German therapy request WITHOUT diagnosis
print("=" * 60)
print("TEST 1: German therapy request WITHOUT previous diagnosis")
print("=" * 60)
config1 = {
    "patient_name": "Max Mustermann",
    "patient_city": "Berlin",
    "insurance_type": "gesetzlich",
    "insurance_company": "TK",
    "symptoms": "Depressionen und Angstzustände",
    "previous_diagnosis": ""
}
emails1 = generate_emails_for_therapists([therapists[0]], config1, "templates/therapy_request.txt")
print(f"To: {emails1[0]['to']}")
print(f"Subject: {emails1[0]['subject']}\n")
print(emails1[0]['body'])

# Test 2: German therapy request WITH diagnosis
print("\n" + "=" * 60)
print("TEST 2: German therapy request WITH previous diagnosis")
print("=" * 60)
config2 = {
    "patient_name": "Max Mustermann",
    "patient_city": "Berlin",
    "insurance_type": "gesetzlich",
    "insurance_company": "TK",
    "symptoms": "Depressionen und Angstzustände",
    "previous_diagnosis": "generalisierte Angststörung (F41.1)"
}
emails2 = generate_emails_for_therapists([therapists[0]], config2, "templates/therapy_request.txt")
print(f"To: {emails2[0]['to']}")
print(f"Subject: {emails2[0]['subject']}\n")
print(emails2[0]['body'])

# Test 3: English therapy request WITHOUT diagnosis
print("\n" + "=" * 60)
print("TEST 3: English therapy request WITHOUT previous diagnosis")
print("=" * 60)
config3 = {
    "patient_name": "John Doe",
    "patient_city": "Berlin",
    "insurance_type": "private",
    "insurance_company": "Allianz",
    "symptoms": "depression and anxiety",
    "previous_diagnosis": ""
}
emails3 = generate_emails_for_therapists([therapists[0]], config3, "templates/therapy_request_en.txt")
print(f"To: {emails3[0]['to']}")
print(f"Subject: {emails3[0]['subject']}\n")
print(emails3[0]['body'])

# Test 4: English therapy request WITH diagnosis
print("\n" + "=" * 60)
print("TEST 4: English therapy request WITH previous diagnosis")
print("=" * 60)
config4 = {
    "patient_name": "John Doe",
    "patient_city": "Berlin",
    "insurance_type": "private",
    "insurance_company": "Allianz",
    "symptoms": "depression and anxiety",
    "previous_diagnosis": "Major Depressive Disorder (F33.2)"
}
emails4 = generate_emails_for_therapists([therapists[0]], config4, "templates/therapy_request_en.txt")
print(f"To: {emails4[0]['to']}")
print(f"Subject: {emails4[0]['subject']}\n")
print(emails4[0]['body'])
