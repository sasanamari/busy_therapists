"""Generate sample emails for documentation"""
import sys
sys.path.insert(0, '/Users/sasan/spicy_projects/busy_therapists/src')

from email_generator import generate_emails_for_therapists

# Fake therapist data
fake_therapist = {
    "name": "Dr. Anna Schmidt",
    "email": "a.schmidt@example.com",
    "profile_url": "https://example.com/therapist/profile"
}

# Sample configs
configs = [
    {
        "name": "sample_therapy_request_de",
        "template": "templates/therapy_request.txt",
        "config": {
            "patient_name": "Max Mustermann",
            "patient_city": "Berlin",
            "insurance_type": "gesetzlich",
            "insurance_company": "TK (Techniker Krankenkasse)",
            "symptoms": "Depressionen und Angstzustände",
            "previous_diagnosis": ""
        }
    },
    {
        "name": "sample_therapy_request_de_with_diagnosis",
        "template": "templates/therapy_request.txt",
        "config": {
            "patient_name": "Max Mustermann",
            "patient_city": "Berlin",
            "insurance_type": "gesetzlich",
            "insurance_company": "TK (Techniker Krankenkasse)",
            "symptoms": "Depressionen und Angstzustände",
            "previous_diagnosis": "generalisierte Angststörung (F41.1)"
        }
    },
    {
        "name": "sample_therapy_request_en",
        "template": "templates/therapy_request_en.txt",
        "config": {
            "patient_name": "John Doe",
            "patient_city": "Berlin",
            "insurance_type": "private",
            "insurance_company": "Allianz",
            "symptoms": "depression and anxiety",
            "previous_diagnosis": ""
        }
    },
    {
        "name": "sample_therapy_request_en_with_diagnosis",
        "template": "templates/therapy_request_en.txt",
        "config": {
            "patient_name": "John Doe",
            "patient_city": "Berlin",
            "insurance_type": "private",
            "insurance_company": "Allianz",
            "symptoms": "depression and anxiety",
            "previous_diagnosis": "Major Depressive Disorder (F33.2)"
        }
    }
]

# Generate all samples
for sample in configs:
    emails = generate_emails_for_therapists(
        [fake_therapist],
        sample["config"],
        sample["template"]
    )

    email = emails[0]
    output_file = f"samples/{sample['name']}.txt"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"To: {email['to_name']} <{email['to']}>\n")
        f.write(f"Subject: {email['subject']}\n\n")
        f.write(email['body'])

    print(f"Created: {output_file}")

print("\nAll sample emails generated successfully!")
