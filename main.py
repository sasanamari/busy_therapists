"""
main.py - Entry point for busy_therapists

Usage:
    python main.py              — scrape therapists and generate emails
    python main.py --protocol  — generate Kostenerstattung protocol from responses.csv

Reads my_data.csv, scrapes therapists from therapie.de, generates
personalized emails, saves output to output/, and opens emails.html in
the browser for manual sending.
"""

import csv
import shutil
import sys
import urllib.parse
import webbrowser
from datetime import datetime
from pathlib import Path

# Make src/ importable regardless of where the script is called from
sys.path.insert(0, str(Path(__file__).parent / "src"))

from scraper import collect_therapists, save_therapists_to_json
from email_generator import generate_emails_for_therapists, save_emails_to_json
from protocol_generator import generate_protocol


EXAMPLE_ZIP = "12345"
REQUIRED_FIELDS = ["Zip code", "Insurance type", "Insurance company", "Symptoms"]

# Maps human-readable CSV values to therapie.de numeric IDs
LANGUAGE_MAP = {
    "english": 3, "englisch": 3,
    "arabic": 1, "arabisch": 1,
    "french": 5, "französisch": 5,
    "spanish": 19, "spanisch": 19,
    "turkish": 21, "türkisch": 21,
    "russian": 16, "russisch": 16,
    "persian": 26, "farsi": 26, "persisch": 26,
    "italian": 8, "italienisch": 8,
    "polish": 14, "polnisch": 14,
    "portuguese": 15, "portugiesisch": 15,
    "greek": 6, "griechisch": 6,
    "ukrainian": 29, "ukrainisch": 29,
    "dutch": 12, "niederländisch": 12,
}

AVAILABILITY_MAP = {
    "available": 1, "available now": 1, "sofort": 1, "sofort verfügbar": 1,
    "3 months": 2, "up to 3 months": 2, "bis drei monate": 2,
    "6 months": 3, "over 3 months": 3, "über drei monate": 3,
    "12 months": 4, "over 12 months": 4, "über zwölf monate": 4,
}

INSURANCE_MAP = {
    "public": 1, "gesetzlich": 1, "gkv": 1,
    "private": 2, "privat": 2, "pkv": 2,
    "self-pay": 3, "selbstzahler": 3,
    "kostenerstattung": 6,
    "public or kostenerstattung": 7, "kassenleistung oder kostenerstattung": 7,
}

THERAPY_TYPE_MAP = {
    "individual": 1, "einzeltherapie": 1, "einzeln": 1,
    "family": 2, "familientherapie": 2,
    "group": 3, "gruppentherapie": 3,
    "children": 4, "kinder": 4,
    "couples": 5, "paartherapie": 5,
}

FOCUS_MAP = {
    "general": 1, "allgemein": 1, "life counselling": 1,
    "anxiety": 2, "angst": 2, "phobia": 2, "phobie": 2,
    "eating disorder": 3, "essstörung": 3,
    "personality disorder": 4, "persönlichkeitsstörung": 4,
    "crisis": 6, "krise": 6, "notfall": 6,
    "psychosis": 7, "psychose": 7, "schizophrenia": 7, "schizophrenie": 7,
    "ocd": 8, "zwang": 8,
    "psychosomatics": 9, "psychosomatik": 9,
    "depression": 10,
    "sexuality": 12, "sexualität": 12,
    "trauma": 13, "violence": 13, "abuse": 13, "gewalt": 13, "missbrauch": 13,
    "neurology": 14, "neurologie": 14,
    "addiction": 15, "sucht": 15,
    "stress": 18, "burnout": 18, "mobbing": 18,
    "chronic pain": 20, "schmerzen": 20,
    "grief": 21, "trauer": 21,
    "adhd": 30, "adhs": 30,
    "autism": 31, "autismus": 31,
}

GENDER_MAP = {
    "male": 1, "männlich": 1, "man": 1, "mann": 1,
    "female": 2, "weiblich": 2, "woman": 2, "frau": 2,
    "non-binary": 4, "divers": 4, "diverse": 4,
}


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

def read_config(csv_path: Path) -> dict:
    """Read my_data.csv into a dict of {field: value}. Skips header row."""
    config = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header row (Field, Your data, Notes)
        for row in reader:
            if len(row) >= 2:
                field = row[0].strip()
                value = row[1].strip()
                config[field] = value
    return config


def validate_config(config: dict) -> tuple[list, list]:
    """
    Returns (errors, warnings).
    Errors block execution. Warnings are printed but don't stop the run.
    """
    errors = []
    warnings = []

    for field in REQUIRED_FIELDS:
        if not config.get(field):
            errors.append(f"Required field '{field}' is missing or empty in my_data.csv")

    if config.get("Zip code") == EXAMPLE_ZIP:
        errors.append("'Zip code' is still set to the example value (12345). Update it in my_data.csv.")

    try:
        count = int(config.get("Number of therapists", "20"))
        if count < 1:
            errors.append("'Number of therapists' must be at least 1.")
    except ValueError:
        errors.append("'Number of therapists' must be a whole number (e.g. 20).")

    return errors, warnings


def _lookup(value: str, mapping: dict):
    """Map a human-readable string to a numeric ID. Returns None if blank or unrecognised."""
    if not value:
        return None
    return mapping.get(value.strip().lower())


def parse_config(config: dict) -> dict:
    """Map CSV field names to internal keys used by scraper and email generator."""
    return {
        "patient_name":      config.get("Name", ""),
        "patient_city":      config.get("City", ""),
        "zip_code":          config.get("Zip code", ""),
        "insurance_type":    config.get("Insurance type", ""),
        "insurance_company": config.get("Insurance company", ""),
        "symptoms":          config.get("Symptoms", ""),
        "previous_diagnosis": config.get("Previous diagnosis", ""),
        "sender_email":      config.get("Your email", ""),
        "target_count":      int(config.get("Number of therapists", "20")),
        "email_language":    "en" if config.get("Email language", "").strip().lower() == "english" else "de",
        # Optional scraper filters — None means no filter applied
        "filter_availability": _lookup(config.get("Availability", ""), AVAILABILITY_MAP),
        "filter_insurance":    _lookup(config.get("Insurance filter", ""), INSURANCE_MAP),
        "filter_language":     _lookup(config.get("Foreign therapy language", ""), LANGUAGE_MAP),
        "filter_therapy_type": _lookup(config.get("Therapy format", ""), THERAPY_TYPE_MAP),
        "filter_focus":        _lookup(config.get("Focus / topic", ""), FOCUS_MAP),
        "filter_gender":       _lookup(config.get("Therapist gender", ""), GENDER_MAP),
    }


# ---------------------------------------------------------------------------
# Output: therapist list
# ---------------------------------------------------------------------------

def save_therapists_txt(therapists: list, path: Path) -> None:
    """Save scraped therapist list as a readable text file."""
    lines = [
        "Therapist Contact List",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Total found: {len(therapists)}",
        "=" * 50,
        "",
    ]
    for i, t in enumerate(therapists, 1):
        lines.append(f"{i}. {t['name']}")
        lines.append(f"   Email:   {t['email']}")
        lines.append(f"   Address: {t.get('address', 'N/A')}")
        lines.append(f"   Profile: {t['profile_url']}")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved therapist list → {path}")


# ---------------------------------------------------------------------------
# Output: individual email files
# ---------------------------------------------------------------------------

def save_email_files(emails: list, output_dir: Path) -> None:
    """Save each email as a numbered .txt file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for i, email in enumerate(emails, 1):
        safe_name = "".join(
            c if c.isalnum() or c in " -_" else "_"
            for c in email["to_name"]
        ).strip()[:50]
        filename = output_dir / f"{i:02d}_{safe_name}.txt"
        content = (
            f"To: {email['to_name']} <{email['to']}>\n"
            f"Subject: {email['subject']}\n\n"
            f"{email['body']}"
        )
        filename.write_text(content, encoding="utf-8")
    print(f"Saved {len(emails)} email files → {output_dir}/")


# ---------------------------------------------------------------------------
# Output: response tracking CSV
# ---------------------------------------------------------------------------

def save_response_tracking_csv(therapists: list, path: Path) -> None:
    """
    Generate a CSV for the user to track therapist responses.
    Pre-filled with therapist details; user fills in response columns manually.
    Can be submitted to insurance as proof of contact.
    """
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Name", "Email", "Address",
            "Date contacted", "Response received (Yes/No)", "Response date", "Notes"
        ])
        for t in therapists:
            writer.writerow([
                t["name"],
                t["email"],
                t.get("address", ""),
                "",  # Date contacted — user fills in
                "",  # Response received
                "",  # Response date
                "",  # Notes
            ])

    print(f"Saved response tracking sheet → {path}")


# ---------------------------------------------------------------------------
# Output: emails.html
# ---------------------------------------------------------------------------

def _build_mailto(email: dict) -> str:
    """Build a mailto: URL pre-filled with subject and body."""
    subject = urllib.parse.quote(email["subject"])
    body = email["body"]
    # mailto: body has a ~2000 char limit in many email clients
    if len(body) > 1800:
        body = body[:1800] + "\n\n[Text gekürzt — vollständigen Text in der E-Mail-Datei lesen]"
    body = urllib.parse.quote(body)
    return f"mailto:{email['to']}?subject={subject}&body={body}"


def generate_html(emails: list, path: Path) -> None:
    """Generate a browser-viewable HTML file with one card per email."""
    cards = []
    for i, email in enumerate(emails, 1):
        mailto = _build_mailto(email)
        body_escaped = (
            email["body"]
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        cards.append(f"""
    <div class="card">
      <div class="card-header">
        <span class="count">{i} / {len(emails)}</span>
        <strong class="name">{email['to_name']}</strong>
        <span class="addr">&lt;{email['to']}&gt;</span>
        <a class="btn" href="{mailto}">Open in email app</a>
      </div>
      <div class="subject"><strong>Subject:</strong> {email['subject']}</div>
      <pre class="body">{body_escaped}</pre>
    </div>""")

    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Therapist Emails ({len(emails)})</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      max-width: 860px; margin: 40px auto; padding: 0 20px;
      background: #f4f4f4; color: #222;
    }}
    h1 {{ font-size: 1.4rem; color: #2E4057; margin-bottom: 4px; }}
    .subtitle {{ color: #666; margin: 0 0 28px; font-size: 0.9rem; }}
    .card {{
      background: white; border-radius: 8px; padding: 20px;
      margin-bottom: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }}
    .card-header {{
      display: flex; align-items: baseline; gap: 10px;
      flex-wrap: wrap; margin-bottom: 10px;
    }}
    .count {{
      background: #2E4057; color: white; border-radius: 12px;
      padding: 2px 9px; font-size: 0.8rem; white-space: nowrap;
    }}
    .name {{ font-size: 1rem; }}
    .addr {{ color: #888; font-size: 0.88rem; flex: 1; }}
    .btn {{
      margin-left: auto; background: #2E4057; color: white;
      padding: 6px 14px; border-radius: 6px; text-decoration: none;
      font-size: 0.85rem; white-space: nowrap;
    }}
    .btn:hover {{ background: #1a2d3d; }}
    .subject {{ color: #555; margin-bottom: 12px; font-size: 0.93rem; }}
    pre.body {{
      white-space: pre-wrap; font-family: inherit; font-size: 0.9rem;
      background: #f9f9f9; border-left: 3px solid #ddd;
      padding: 14px; margin: 0; border-radius: 0 4px 4px 0; line-height: 1.6;
    }}
  </style>
</head>
<body>
  <h1>Therapy Email Outreach</h1>
  <p class="subtitle">
    {len(emails)} emails generated &mdash;
    click <strong>Open in email app</strong> to send each one from your email client.
    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
  </p>
  {''.join(cards)}
</body>
</html>"""

    path.write_text(html, encoding="utf-8")
    print(f"Saved emails.html → {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    base_dir = Path(__file__).parent
    csv_path = base_dir / "my_data.csv"
    output_dir = base_dir / "output"
    emails_dir = output_dir / "emails"

    # --- 1. Read config ---
    print("=" * 50)
    print("Therapy Finder — Kostenerstattung Tool")
    print("=" * 50)

    if not csv_path.exists():
        print("\nERROR: my_data.csv not found.")
        print("Make sure it is in the same folder as main.py and try again.")
        sys.exit(1)

    print("\nReading my_data.csv...")
    raw_config = read_config(csv_path)
    errors, warnings = validate_config(raw_config)

    for w in warnings:
        print(f"  WARNING: {w}")
    if errors:
        print()
        for e in errors:
            print(f"  ERROR: {e}")
        print("\nPlease fix the errors above in my_data.csv and run again.")
        sys.exit(1)

    config = parse_config(raw_config)
    print(f"  Name:      {config['patient_name']}")
    print(f"  Location:  {config['patient_city']} ({config['zip_code']})")
    print(f"  Insurance: {config['insurance_type']} — {config['insurance_company']}")
    print(f"  Target:    {config['target_count']} therapists")

    # --- 2. Scrape ---
    print(f"\nSearching for therapists near {config['zip_code']}...")
    print("This will take a few minutes — please leave the window open.\n")

    output_dir.mkdir(parents=True, exist_ok=True)
    data_dir = output_dir / ".data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Clear individual email files from previous run
    if emails_dir.exists():
        shutil.rmtree(emails_dir)

    therapists = collect_therapists(
        zip_code=config["zip_code"],
        target_count=config["target_count"],
        delay_seconds=2.5,
        insurance_type=config["filter_insurance"],
        availability=config["filter_availability"],
        language=config["filter_language"],
        therapy_type=config["filter_therapy_type"],
        focus=config["filter_focus"],
        gender=config["filter_gender"],
    )

    if not therapists:
        print("\nNo therapists found. Check your zip code and try again.")
        sys.exit(1)

    save_therapists_to_json(therapists, str(data_dir / "therapists.json"))
    save_therapists_txt(therapists, output_dir / "therapists.txt")

    # --- 3. Generate emails ---
    print(f"\nGenerating {len(therapists)} emails...")

    user_config = {
        "patient_name":      config["patient_name"],
        "patient_city":      config["patient_city"],
        "insurance_type":    config["insurance_type"],
        "insurance_company": config["insurance_company"],
        "symptoms":          config["symptoms"],
        "previous_diagnosis": config["previous_diagnosis"],
    }

    emails = generate_emails_for_therapists(
        therapists,
        user_config,
        str(base_dir / "templates" / ("therapy_request_en.txt" if config["email_language"] == "en" else "therapy_request.txt")),
    )

    save_emails_to_json(emails, str(data_dir / "emails.json"))
    save_email_files(emails, emails_dir)
    save_response_tracking_csv(therapists, output_dir / "responses.csv")

    # --- 4. HTML output ---
    html_path = output_dir / "emails.html"
    generate_html(emails, html_path)

    # --- 5. Open in browser ---
    print(f"\nOpening emails.html in your browser...")
    webbrowser.open(html_path.as_uri())

    print("\nDone!")
    print(f"  Therapist list:    output/therapists.txt")
    print(f"  Email files:       output/emails/")
    print(f"  Email viewer:      output/emails.html")
    print(f"  Response tracker:  output/responses.csv")


def protocol_mode():
    """Generate the Kostenerstattung protocol from a filled-in responses.csv."""
    base_dir = Path(__file__).parent
    csv_path = base_dir / "my_data.csv"
    output_dir = base_dir / "output"

    print("=" * 50)
    print("Therapy Finder — Protocol Generator")
    print("=" * 50)

    if not csv_path.exists():
        print("\nERROR: my_data.csv not found.")
        sys.exit(1)

    raw_config = read_config(csv_path)
    errors, _ = validate_config(raw_config)
    if errors:
        for e in errors:
            print(f"  ERROR: {e}")
        sys.exit(1)

    config = parse_config(raw_config)
    responses_path = output_dir / "responses.csv"
    protocol_path = output_dir / "protocol.txt"

    print(f"\nReading responses from {responses_path}...")
    try:
        generate_protocol(config, responses_path, protocol_path)
    except (FileNotFoundError, ValueError) as e:
        print(f"\nERROR: {e}")
        sys.exit(1)

    print("\nDone! Submit output/protocol.txt with your Kostenerstattung application.")


if __name__ == "__main__":
    if "--protocol" in sys.argv:
        protocol_mode()
    else:
        main()
