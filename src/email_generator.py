"""
Email template generator for therapy requests

Generates personalized emails from templates and user configuration.
"""

import json
from pathlib import Path
from typing import Dict, List


def load_user_config(config_path: str = "user_config.json") -> Dict[str, str]:
    """
    Load user configuration from JSON file

    Args:
        config_path: Path to user config file (default: "user_config.json")

    Returns:
        Dictionary with user configuration data
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_template(template_path: str) -> str:
    """
    Load email template from file

    Args:
        template_path: Path to template file

    Returns:
        Template string with placeholders
    """
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def generate_email(therapist: Dict[str, str], user_config: Dict[str, str], template: str) -> Dict[str, str]:
    """
    Generate personalized email for a therapist

    Args:
        therapist: Therapist data (name, email, profile_url)
        user_config: User configuration data
        template: Email template string with placeholders

    Returns:
        Dictionary with email data:
        {
            "to": "therapist@example.com",
            "to_name": "Dr. Alice Wonderland",
            "subject": "Subject line extracted from template",
            "body": "Personalized email body"
        }
    """
    # Extract therapist title from name (e.g., "Dr.", "Dipl.-Psych.")
    # Simple heuristic: if name contains title-like words, use generic salutation only
    name_parts = therapist["name"].split()
    therapist_title = "Frau/Herr"  # Generic salutation for all cases

    # Note: We use generic salutation because the full name already contains
    # any titles (e.g., "Dr. Anna Schmidt"), so we don't need to extract them

    # Prepare placeholders
    placeholders = {
        "therapist_name": therapist["name"],
        "therapist_title": therapist_title,
        **user_config
    }

    # Build diagnosis_sentence from the raw previous_diagnosis input.
    # Templates use {diagnosis_sentence} — never the raw {previous_diagnosis} directly.
    raw_diagnosis = placeholders.get("previous_diagnosis", "")
    if raw_diagnosis:
        is_english = "Subject:" in template or "Dear" in template
        if is_english:
            placeholders["diagnosis_sentence"] = f". I have been previously diagnosed with: {raw_diagnosis}"
        else:
            placeholders["diagnosis_sentence"] = f". Ich habe bereits die Diagnose: {raw_diagnosis}"
    else:
        placeholders["diagnosis_sentence"] = ""

    # Fill template
    filled = template
    for key, value in placeholders.items():
        filled = filled.replace(f"{{{key}}}", value)

    # Extract subject and body
    lines = filled.split('\n')
    subject = ""
    body_start = 0

    for i, line in enumerate(lines):
        if line.startswith("Betreff:"):
            subject = line.replace("Betreff:", "").strip()
            body_start = i + 1
            break
        elif line.startswith("Subject:"):
            subject = line.replace("Subject:", "").strip()
            body_start = i + 1
            break

    body = '\n'.join(lines[body_start:]).strip()

    return {
        "to": therapist["email"],
        "to_name": therapist["name"],
        "subject": subject,
        "body": body
    }


def generate_emails_for_therapists(
    therapists: List[Dict[str, str]],
    user_config: Dict[str, str],
    template_path: str = "templates/therapy_request.txt"
) -> List[Dict[str, str]]:
    """
    Generate personalized emails for all therapists

    Args:
        therapists: List of therapist dictionaries
        user_config: User configuration data
        template_path: Path to email template

    Returns:
        List of email dictionaries ready to send
    """
    template = load_template(template_path)
    emails = []

    for therapist in therapists:
        email = generate_email(therapist, user_config, template)
        emails.append(email)

    return emails


def save_emails_to_json(emails: List[Dict[str, str]], output_path: str = "data/emails.json") -> None:
    """
    Save generated emails to JSON file

    Args:
        emails: List of email dictionaries
        output_path: Path to output JSON file (default: "data/emails.json")
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(emails, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(emails)} emails to {output_path}")


if __name__ == "__main__":
    # Test the email generator
    print("Testing email generator...")

    # Load test data
    with open("data/test_therapists.json", 'r', encoding='utf-8') as f:
        therapists = json.load(f)

    # Create a test user config
    test_config = {
        "patient_name": "Max Mustermann",
        "patient_city": "Berlin",
        "insurance_type": "gesetzlich",
        "insurance_company": "TK (Techniker Krankenkasse)",
        "symptoms": "Depressionen und Angstzustände"
    }

    # Generate emails
    emails = generate_emails_for_therapists(
        therapists[:2],  # Just test with first 2
        test_config,
        "templates/therapy_request.txt"
    )

    # Print first email
    print(f"\nGenerated {len(emails)} emails")
    print(f"\nFirst email:")
    print(f"To: {emails[0]['to_name']} <{emails[0]['to']}>")
    print(f"Subject: {emails[0]['subject']}")
    print(f"\n{emails[0]['body']}")
