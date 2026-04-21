"""
main.py - Entry point for busy_therapists

Usage:
    python main.py  — shows interactive menu

Reads my_data.csv, presents a numbered menu, and runs the selected step.
"""

import csv
import shutil
import sys
import urllib.parse
import webbrowser
from datetime import date, datetime
from pathlib import Path

# When frozen by PyInstaller, bundled files live in sys._MEIPASS.
# my_data.csv and output/ always live next to the executable.
def _bundle_dir() -> Path:
    """Path to bundled read-only assets (templates, src, fonts)."""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).parent

def _runtime_dir() -> Path:
    """Path to the executable's directory — where my_data.csv and output/ live."""
    if getattr(sys, "frozen", False):
        exe = Path(sys.executable)
        # Inside a .app bundle the executable is at
        # SomeApp.app/Contents/MacOS/exe — go up to the folder containing the .app
        for parent in exe.parents:
            if parent.suffix == ".app":
                return parent.parent
        return exe.parent
    return Path(__file__).parent

BUNDLE_DIR = _bundle_dir()
RUNTIME_DIR = _runtime_dir()

# Make src/ importable regardless of where the script is called from
sys.path.insert(0, str(BUNDLE_DIR / "src"))

from scraper import collect_therapists, save_therapists_to_json
from email_generator import generate_emails_for_therapists, save_emails_to_json, generate_insurance_email


EXAMPLE_ZIP = "12345"
REQUIRED_FIELDS = ["Zip code", "Your insurance", "Insurance company", "Symptoms"]

# Sentinel — distinguishes "caller didn't pass an override" from "caller explicitly wants None (no filter)"
_UNSET = object()

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

def _cell_to_str(value) -> str:
    """Convert a numbers-parser cell value to a clean string."""
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def read_config(csv_path: Path) -> dict:
    """
    Read my_data into a dict of {field: value}. Skips header row.
    Prefers my_data.numbers (if present) over my_data.csv.
    """
    numbers_path = csv_path.with_suffix(".numbers")
    if numbers_path.exists():
        try:
            from numbers_parser import Document
            doc = Document(str(numbers_path))
            print(f"  Using {numbers_path.name}")
            table = doc.sheets[0].tables[0]
            config = {}
            for i, row in enumerate(table.rows()):
                if i == 0:
                    continue  # skip header row
                if len(row) >= 2 and row[0].value:
                    field = _cell_to_str(row[0].value)
                    value = _cell_to_str(row[1].value)
                    config[field] = value
            return config
        except Exception as e:
            print(f"  WARNING: Could not read {numbers_path.name} ({e}), falling back to {csv_path.name}.")

    config = {}
    print(f"  Using {csv_path.name}")
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        sample = f.read(1024)
        f.seek(0)
        delimiter = ";" if ";" in sample.split("\n")[0] else ","
        reader = csv.reader(f, delimiter=delimiter)
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

    # Availability accepts "yes"/"no" (cascade shortcuts) in addition to specific values
    avail_value = config.get("Availability", "").strip().lower()
    if avail_value and avail_value not in AVAILABILITY_MAP and avail_value not in {"yes", "no"}:
        warnings.append(
            f"'Availability' value '{avail_value}' was not recognised — filter will be ignored. "
            f"Valid options: 'yes', 'no', or a specific value. See docs/therapie_de_filter_params.md."
        )

    optional_filters = [
        ("Therapist insurance",      INSURANCE_MAP),
        ("Foreign therapy language", LANGUAGE_MAP),
        ("Therapy format",           THERAPY_TYPE_MAP),
        ("Focus / topic",            FOCUS_MAP),
        ("Therapist gender",         GENDER_MAP),
    ]
    for field, mapping in optional_filters:
        value = config.get(field, "").strip()
        if value and value.lower() not in mapping:
            warnings.append(
                f"'{field}' value '{value}' was not recognised — filter will be ignored. "
                f"See docs/therapie_de_filter_params.md for valid options."
            )

    return errors, warnings


def _lookup(value: str, mapping: dict):
    """Map a human-readable string to a numeric ID. Returns None if blank or unrecognised."""
    if not value:
        return None
    return mapping.get(value.strip().lower())


def _build_availability_stages(raw_value: str) -> list:
    """
    Convert the Availability CSV field to an ordered list of (availability_id, radius) stages.

    The scraper works through stages in sequence — moving to the next only when
    the current one is exhausted. This cascades from tighter to looser filters
    so we always try to find the most relevant therapists first.

    Each tuple is (availability_id, search_radius):
      - availability_id: None = no filter, or a therapie.de terminzeitraum value
      - search_radius:   None = therapie.de default (~10km), 25 = explicit 25km

    "yes"  — want available therapists (personal search, option 1):
             try available-now locally → up to 3 months locally →
             available-now at 25km → up to 3 months at 25km
    "no"   — want busy therapists (documentation search, option 3):
             try over-12-months locally → over-3-months locally →
             same two at 25km (radius matters less here, but included for completeness)
    other  — a specific single value (e.g. "available now"); tries default
             radius first then expands to 25km as fallback
    blank  — no availability filter; tries default radius then 25km
    """
    v = raw_value.strip().lower() if raw_value else ""

    if v == "yes":
        # Cascade from strictest (available now, local) to most relaxed (3 months, 25km)
        return [
            (AVAILABILITY_MAP["available now"],  None),  # available now, local
            (AVAILABILITY_MAP["up to 3 months"], None),  # up to 3 months, local
            (AVAILABILITY_MAP["available now"],  25),    # available now, 25km
            (AVAILABILITY_MAP["up to 3 months"], 25),    # up to 3 months, 25km
        ]
    elif v == "no":
        # Cascade from longest waits first (most useful for documentation)
        return [
            (AVAILABILITY_MAP["over 12 months"], None),  # over 12 months, local
            (AVAILABILITY_MAP["over 3 months"],  None),  # over 3 months, local
            (AVAILABILITY_MAP["over 12 months"], 25),    # over 12 months, 25km
            (AVAILABILITY_MAP["over 3 months"],  25),    # over 3 months, 25km
        ]
    else:
        # Single specific value or blank — try default radius, expand to 25km if needed
        availability_id = _lookup(v, AVAILABILITY_MAP)  # returns None if blank or unrecognised
        return [(availability_id, None), (availability_id, 25)]


def parse_config(config: dict) -> dict:
    """Map CSV field names to internal keys used by scraper and email generator."""
    return {
        "patient_name":           config.get("Name", ""),
        "patient_city":           config.get("City", ""),
        "zip_code":               config.get("Zip code", ""),
        "insurance_type":         config.get("Your insurance", ""),
        "insurance_company":      config.get("Insurance company", ""),
        "symptoms":               config.get("Symptoms", ""),
        "previous_diagnosis":     config.get("Previous diagnosis", ""),
        "sender_email":           config.get("Your email", ""),
        "target_count":           int(config.get("Number of therapists", "20")),
        "email_language":         "en" if config.get("Email language", "").strip().lower() == "english" else "de",
        "therapy_language_label": config.get("Foreign therapy language", "").strip(),
        # Scraper filters — availability is stored as a stage list (see _build_availability_stages)
        "filter_availability_stages": _build_availability_stages(config.get("Availability", "")),
        "filter_insurance":           _lookup(config.get("Therapist insurance", ""), INSURANCE_MAP),
        "filter_language":        _lookup(config.get("Foreign therapy language", ""), LANGUAGE_MAP),
        "filter_therapy_type":    _lookup(config.get("Therapy format", ""), THERAPY_TYPE_MAP),
        "filter_focus":           _lookup(config.get("Focus / topic", ""), FOCUS_MAP),
        "filter_gender":          _lookup(config.get("Therapist gender", ""), GENDER_MAP),
        # Insurance letter fields (all optional — stay as {placeholder} if empty)
        "insurance_number":       config.get("Insurance number", ""),
        "insurance_email":        config.get("Insurance email", ""),
        "application_date":       config.get("Application date", ""),
        "followup_date":          config.get("Follow-up date", ""),
        "rejection_date":         config.get("Rejection date", ""),
    }


# ---------------------------------------------------------------------------
# Output: therapist list + individual email files
# ---------------------------------------------------------------------------

def save_therapists_txt(therapists: list, path: Path) -> None:
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


def save_email_files(emails: list, output_dir: Path) -> None:
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
# Output: contact tracking CSV
# ---------------------------------------------------------------------------

def save_contact_csv(therapists: list, path: Path) -> None:
    """
    Append new therapists to a contact CSV, skipping duplicates by email.
    Creates the file with a header if it doesn't exist yet.
    """
    header = ["Name", "Email", "Address", "Date contacted", "Response received (Yes/No)", "Response date", "Notes"]

    existing_emails = set()
    if path.exists():
        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_emails.add(row.get("Email", "").strip().lower())

    new_entries = [t for t in therapists if t["email"].strip().lower() not in existing_emails]

    write_header = not path.exists()
    with open(path, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        for t in new_entries:
            writer.writerow([
                t["name"],
                t["email"],
                t.get("address", ""),
                "",  # Date contacted — user fills in
                "",  # Response received
                "",  # Response date
                "",  # Notes
            ])

    if new_entries:
        print(f"Added {len(new_entries)} new therapists → {path}")
    else:
        print(f"No new therapists to add (all already present) → {path}")


# ---------------------------------------------------------------------------
# Output: HTML viewers
# ---------------------------------------------------------------------------

def _build_mailto(email: dict) -> str:
    subject = urllib.parse.quote(email["subject"])
    body = email["body"]
    if len(body) > 1800:
        body = body[:1800] + "\n\n[Text gekürzt — vollständigen Text in der E-Mail-Datei lesen]"
    body = urllib.parse.quote(body)
    to = email.get("to", "")
    return f"mailto:{to}?subject={subject}&body={body}"


_SHARED_CSS = """
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      max-width: 860px; margin: 40px auto; padding: 0 20px;
      background: #f4f4f4; color: #222;
    }
    h1 { font-size: 1.4rem; color: #2E4057; margin-bottom: 4px; }
    .subtitle { color: #666; margin: 0 0 28px; font-size: 0.9rem; }
    .card {
      background: white; border-radius: 8px; padding: 20px;
      margin-bottom: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }
    .card-header {
      display: flex; align-items: center; gap: 10px;
      flex-wrap: wrap; margin-bottom: 10px;
    }
    .btn {
      background: #2E4057; color: white;
      padding: 6px 14px; border-radius: 6px; text-decoration: none;
      font-size: 0.85rem; white-space: nowrap; border: none; cursor: pointer;
    }
    .btn:hover { background: #1a2d3d; }
    .subject { color: #555; margin-bottom: 12px; font-size: 0.93rem; }
    pre.body {
      white-space: pre-wrap; font-family: inherit; font-size: 0.9rem;
      background: #f9f9f9; border-left: 3px solid #ddd;
      padding: 14px; margin: 0; border-radius: 0 4px 4px 0; line-height: 1.6;
    }
"""


def generate_html(emails: list, path: Path) -> None:
    """Multi-card HTML for therapist outreach emails (options 1–4)."""
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
        <a class="btn" href="{mailto}" style="margin-left:auto">Open in email app</a>
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
{_SHARED_CSS}
    .count {{
      background: #2E4057; color: white; border-radius: 12px;
      padding: 2px 9px; font-size: 0.8rem; white-space: nowrap;
    }}
    .name {{ font-size: 1rem; }}
    .addr {{ color: #888; font-size: 0.88rem; flex: 1; }}
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
    print(f"Saved emails HTML → {path}")


def generate_insurance_html(email: dict, path: Path, attachments_note: str = None) -> None:
    """Single-card HTML for insurance letters (options 5–8)."""
    mailto = _build_mailto(email)
    body_escaped = (
        email["body"]
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    to_display = (
        f"{email['to_name']} &lt;{email['to']}&gt;"
        if email.get("to")
        else email["to_name"]
    )

    attachments_html = ""
    if attachments_note:
        attachments_html = f'<div class="attachments"><strong>Attachments to include:</strong> {attachments_note}</div>'

    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{email['subject']}</title>
  <style>
{_SHARED_CSS}
    .to {{ color: #555; font-size: 0.93rem; flex: 1; }}
    .btn-copy {{ background: #555; }}
    .btn-copy:hover {{ background: #333; }}
    .attachments {{
      margin-top: 16px; padding: 12px 16px;
      background: #fff8e1; border-left: 3px solid #f9a825;
      border-radius: 0 4px 4px 0; font-size: 0.88rem; color: #555;
    }}
  </style>
  <script>
    function copyBody() {{
      const text = document.getElementById('email-body').innerText;
      navigator.clipboard.writeText(text).then(() => {{
        const btn = document.getElementById('copy-btn');
        btn.textContent = 'Copied!';
        setTimeout(() => btn.textContent = 'Copy text', 2000);
      }});
    }}
  </script>
</head>
<body>
  <h1>{email['subject']}</h1>
  <p class="subtitle">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
  <div class="card">
    <div class="card-header">
      <span class="to"><strong>To:</strong> {to_display}</span>
      <a class="btn" href="{mailto}">Open in email app</a>
      <button class="btn btn-copy" id="copy-btn" onclick="copyBody()">Copy text</button>
    </div>
    <div class="subject"><strong>Subject:</strong> {email['subject']}</div>
    <pre class="body" id="email-body">{body_escaped}</pre>
    {attachments_html}
  </div>
</body>
</html>"""

    path.write_text(html, encoding="utf-8")
    print(f"Saved HTML → {path}")


# ---------------------------------------------------------------------------
# CSV picker — select a specific therapist from an output CSV
# ---------------------------------------------------------------------------

def pick_from_csv(path: Path, label: str) -> tuple[str, str] | tuple[None, None]:
    """
    Show a numbered list of entries from a contact CSV and let the user pick one.
    Option 0 allows the user to enter name and email manually (for therapists found outside the tool).
    Returns (name, email) tuple, or (None, None) if skipped.
    """
    entries = []
    if path.exists():
        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                entries.append(row)

    print(f"\nSelect the {label} for this email:")
    print(f"  0. Enter name and email manually (or leave blank to fill in later)")
    if entries:
        for i, entry in enumerate(entries, 1):
            print(f"  {i}. {entry['Name']}  <{entry['Email']}>")
    else:
        print(f"  (No entries found in {path.name} — run option 4 first, or enter manually)")
    print()

    while True:
        max_choice = len(entries)
        choice = input(f"Enter number (0–{max_choice}): ").strip()
        try:
            idx = int(choice)
            if idx == 0:
                name = input("Therapist name (or press Enter to leave as placeholder): ").strip()
                email = input("Therapist email (or press Enter to leave as placeholder): ").strip()
                return (name or None, email or None)
            if 1 <= idx <= max_choice:
                entry = entries[idx - 1]
                return (entry["Name"], entry["Email"])
        except ValueError:
            pass
        print("  Invalid choice, try again.")


# ---------------------------------------------------------------------------
# Shared flow helpers
# ---------------------------------------------------------------------------

def generate_responses_pdf(csv_path: Path, output_path: Path, patient_name: str) -> bool:
    """Generate a formatted PDF of responses.csv for insurance submission.
    Returns True if successful, False if the CSV is missing or empty."""
    try:
        from fpdf import FPDF
    except ImportError:
        print("ERROR: fpdf2 is not installed. Run: pip install fpdf2")
        return False

    if not csv_path.exists():
        print(f"ERROR: {csv_path.name} not found. Run options 1 and/or 3 first to build your contact list.")
        return False

    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    if not rows:
        print(f"ERROR: {csv_path.name} is empty.")
        return False

    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_margins(12, 12, 12)
    font_dir = BUNDLE_DIR / "src" / "fonts"
    pdf.add_font("DejaVu", style="", fname=str(font_dir / "DejaVuSans.ttf"))
    pdf.add_font("DejaVu", style="B", fname=str(font_dir / "DejaVuSans-Bold.ttf"))

    # Title
    pdf.set_font("DejaVu", "B", 13)
    pdf.cell(0, 8, "Therapist Contact Log - Kostenerstattung Application", ln=True)
    pdf.set_font("DejaVu", "", 9)
    pdf.cell(0, 5, f"Patient: {patient_name}    Generated: {date.today().strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(3)

    # Table header
    cols = [
        ("Name",             52),
        ("Email",            52),
        ("Address",          52),
        ("Date contacted",   25),
        ("Response",         18),
        ("Response date",    25),
        ("Notes",            42),
    ]
    csv_keys = ["Name", "Email", "Address", "Date contacted", "Response received (Yes/No)", "Response date", "Notes"]

    pdf.set_font("DejaVu", "B", 8)
    pdf.set_fill_color(220, 220, 220)
    for label, w in cols:
        pdf.cell(w, 6, label, border=1, fill=True)
    pdf.ln()

    # Rows
    line_h = 5
    pdf.set_font("DejaVu", "", 8)
    fill = False
    for row in rows:
        x0 = pdf.get_x()
        y0 = pdf.get_y()

        # First pass: measure how tall each cell needs to be
        row_h = line_h
        for (_, w), key in zip(cols, csv_keys):
            h = pdf.multi_cell(w, line_h, str(row.get(key, "")), dry_run=True, output="HEIGHT")
            row_h = max(row_h, h)

        # Add a page if the row won't fit
        if y0 + row_h > pdf.page_break_trigger:
            pdf.add_page()
            x0 = pdf.get_x()
            y0 = pdf.get_y()

        # Second pass: draw background + border rect, then text
        x = x0
        for (_, w), key in zip(cols, csv_keys):
            if fill:
                pdf.set_fill_color(245, 245, 245)
                pdf.rect(x, y0, w, row_h, style="F")
            pdf.rect(x, y0, w, row_h, style="D")
            pdf.set_xy(x, y0)
            pdf.multi_cell(w, line_h, str(row.get(key, "")), border=0, fill=False)
            x += w

        pdf.set_y(y0 + row_h)
        fill = not fill

    pdf.output(str(output_path))
    print(f"Saved contact log PDF → {output_path}")
    return True


# ---------------------------------------------------------------------------

def _build_user_config(config: dict) -> dict:
    """Build the user_config dict passed to generate_emails_for_therapists."""
    lang_label = config["therapy_language_label"]
    if lang_label:
        therapy_language_question = f"Do you offer therapy in {lang_label.capitalize()}?"
    else:
        therapy_language_question = "Do you offer therapy in German and English?"

    return {
        "patient_name":              config["patient_name"],
        "patient_city":              config["patient_city"],
        "insurance_type":            config["insurance_type"],
        "insurance_company":         config["insurance_company"],
        "symptoms":                  config["symptoms"],
        "previous_diagnosis":        config["previous_diagnosis"],
        "therapy_language_question": therapy_language_question,
    }


def run_scraper_option(
    config: dict,
    base_dir: Path,
    output_dir: Path,
    data_dir: Path,
    emails_dir: Path,
    template_name: str,
    csv_path: Path,
    html_path: Path,
    warnings: list,
    insurance_override=_UNSET,
    stages_override=_UNSET,
    language_override=_UNSET,
    focus_override=_UNSET,
    therapy_type_override=_UNSET,
    gender_override=_UNSET,
):
    """Shared flow for scraper-based options (1–4)."""
    # Stale CSV warning
    if csv_path.exists():
        print(f"\n{'=' * 50}")
        print(f"  HEADS UP: {csv_path.name} already exists.")
        print(f"  New therapists will be appended to it.")
        print(f"  If this is a fresh start, delete it from output/ first.")
        print("=" * 50)

    output_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    if emails_dir.exists():
        shutil.rmtree(emails_dir)

    # Use override if explicitly provided by the menu option, otherwise fall back to config
    insurance    = config["filter_insurance"]           if insurance_override    is _UNSET else insurance_override
    stages       = config["filter_availability_stages"] if stages_override       is _UNSET else stages_override
    language     = config["filter_language"]            if language_override     is _UNSET else language_override
    focus        = config["filter_focus"]               if focus_override        is _UNSET else focus_override
    therapy_type = config["filter_therapy_type"]        if therapy_type_override is _UNSET else therapy_type_override
    gender       = config["filter_gender"]              if gender_override       is _UNSET else gender_override

    print(f"\nSearching for therapists near {config['zip_code']}...")
    print("This will take a few minutes — please leave the window open.\n")

    therapists = collect_therapists(
        zip_code=config["zip_code"],
        target_count=config["target_count"],
        delay_seconds=2.5,
        search_stages=stages,
        insurance_type=insurance,
        language=language,
        therapy_type=therapy_type,
        focus=focus,
        gender=gender,
    )

    if not therapists:
        print("\nNo therapists found. Check your filters and try again.")
        return

    save_therapists_to_json(therapists, str(data_dir / "therapists.json"))
    save_therapists_txt(therapists, output_dir / "therapists.txt")

    template_path = base_dir / "templates" / (
        f"{template_name}_en.txt" if config["email_language"] == "en" else f"{template_name}.txt"
    )
    print(f"\nGenerating {len(therapists)} emails...")
    emails = generate_emails_for_therapists(therapists, _build_user_config(config), str(template_path))

    save_emails_to_json(emails, str(data_dir / "emails.json"))
    save_email_files(emails, emails_dir)
    save_contact_csv(therapists, csv_path)
    generate_html(emails, html_path)

    print(f"\nOpening {html_path.name} in your browser...")
    webbrowser.open(html_path.as_uri())

    print("\nDone!")
    print(f"  Therapist list:   output/therapists.txt")
    print(f"  Email files:      {emails_dir.relative_to(base_dir)}/")
    print(f"  Email viewer:     {html_path.relative_to(base_dir)}")
    print(f"  Contact tracker:  {csv_path.relative_to(base_dir)}")

    if warnings:
        print("\nWarnings (filters ignored):")
        for w in warnings:
            print(f"  WARNING: {w}")


def run_insurance_option(
    config: dict,
    base_dir: Path,
    output_dir: Path,
    template_name: str,
    html_path: Path,
    extra_fields: dict = None,
    attachments_note: str = None,
):
    """Shared flow for insurance letter options (5–8)."""
    output_dir.mkdir(parents=True, exist_ok=True)

    merged = dict(config)
    if extra_fields:
        merged.update(extra_fields)

    template_path = base_dir / "templates" / (
        f"{template_name}_en.txt" if config["email_language"] == "en" else f"{template_name}.txt"
    )

    email = generate_insurance_email(merged, str(template_path))
    generate_insurance_html(email, html_path, attachments_note=attachments_note)

    print(f"\nOpening {html_path.name} in your browser...")
    webbrowser.open(html_path.as_uri())

    print("\nDone!")
    print(f"  Email viewer: {html_path.relative_to(base_dir)}")


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------

MENU = """
  #   Step                                   What you need
  ─────────────────────────────────────────────────────────────────────────
  1   Search for therapists + send           my_data.csv
      outreach emails
  2   Find a private therapist               my_data.csv
      (Kostenerstattung)
  3   Request probationary sessions          my_data.csv
      (to get PTV11 + urgency note)
  4   Contact public therapists for          my_data.csv
      insurance documentation
  5   Apply for reimbursement                my_data.csv + private_therapists.csv
                                             (run option 2 first)
  6   Follow up — no response from           my_data.csv
      insurance                              (Application date field filled in)
  7   Appeal a rejection                     my_data.csv + private_therapists.csv
                                             (Rejection date field filled in)
  8   Threat of legal action —               my_data.csv
      being ignored
                                             (Application date + Follow-up date)
  ─────────────────────────────────────────────────────────────────────────
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    base_dir = BUNDLE_DIR
    csv_path = RUNTIME_DIR / "my_data.csv"
    output_dir = RUNTIME_DIR / "output"
    data_dir = output_dir / ".data"

    print("=" * 60)
    print("  Therapy Finder — Kostenerstattung Tool")
    print("=" * 60)

    numbers_path = csv_path.with_suffix(".numbers")
    if not csv_path.exists() and not numbers_path.exists():
        print("\nERROR: my_data.csv not found.")
        print("Copy my_data.csv.example → my_data.csv, fill it in, and run again.")
        sys.exit(1)

    config_file = numbers_path.name if numbers_path.exists() else csv_path.name
    print(f"\nReading {config_file}...")
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
    print(f"  Your insurance: {config['insurance_type']} — {config['insurance_company']}")

    print(MENU)
    choice = input("Enter a number (1–8): ").strip()

    if choice == "1":
        # Free-form search — all CSV filters (availability, therapist insurance, etc.) apply
        run_scraper_option(
            config, base_dir, output_dir, data_dir,
            emails_dir=output_dir / "emails",
            template_name="therapy_request",
            csv_path=output_dir / "busy_therapists.csv",
            html_path=output_dir / "emails.html",
            warnings=warnings,
        )

    elif choice == "2":
        # Private therapist search — always kostenerstattung insurance, "yes" availability
        # cascade (available now → up to 3 months, expanding to 25km if needed).
        # Language, focus, format, gender respected from CSV.
        run_scraper_option(
            config, base_dir, output_dir, data_dir,
            emails_dir=output_dir / "private_emails",
            template_name="private_inquiry",
            csv_path=output_dir / "private_therapists.csv",
            html_path=output_dir / "private_emails.html",
            warnings=warnings,
            insurance_override=INSURANCE_MAP["kostenerstattung"],
            stages_override=_build_availability_stages("yes"),
        )

    elif choice == "3":
        # Probationary sessions — always public insurance, no availability filter.
        # Language, focus, format, gender respected from CSV.
        run_scraper_option(
            config, base_dir, output_dir, data_dir,
            emails_dir=output_dir / "probationary_emails",
            template_name="probationary_request",
            csv_path=output_dir / "probationary_therapists.csv",
            html_path=output_dir / "probationary_emails.html",
            warnings=warnings,
            insurance_override=INSURANCE_MAP["public"],
            stages_override=[(None, None), (None, 25)],
        )

    elif choice == "4":
        # Documentation search — always public insurance, long wait times cascade.
        # Language, focus, format, gender intentionally ignored: the goal is to
        # document as many contacts as possible, not find the ideal therapist.
        run_scraper_option(
            config, base_dir, output_dir, data_dir,
            emails_dir=output_dir / "emails",
            template_name="therapy_request",
            csv_path=output_dir / "busy_therapists.csv",
            html_path=output_dir / "emails.html",
            warnings=warnings,
            insurance_override=INSURANCE_MAP["public"],
            stages_override=_build_availability_stages("no"),
            language_override=None,
            focus_override=None,
            therapy_type_override=None,
            gender_override=None,
        )

    elif choice == "5":
        print("\n" + "=" * 60)
        print("  Before you proceed, make sure you have these documents")
        print("  ready to attach to the email:")
        print()
        print("    1. Contact log — this tool will generate output/contact_log.pdf")
        print("       automatically when you press Enter below.")
        print("    2. PTV11 form with urgency label (from probationary sessions)")
        print("    3. Written confirmation from your private therapist")
        print("    4. Medical certificate of necessity (from your doctor)")
        print()
        print("  You will need to attach these manually after opening the email.")
        print("=" * 60)
        input("\n  Press Enter when you're ready to continue... ")

        therapist_name, therapist_email = pick_from_csv(
            output_dir / "private_therapists.csv",
            label="private therapist",
        )
        extra = {}
        if therapist_name:
            extra["private_therapist_name"] = therapist_name
        if therapist_email:
            extra["private_therapist_email"] = therapist_email
        pdf_path = output_dir / "contact_log.pdf"
        pdf_ok = generate_responses_pdf(
            csv_path=output_dir / "busy_therapists.csv",
            output_path=pdf_path,
            patient_name=config["patient_name"],
        )
        run_insurance_option(
            config, base_dir, output_dir,
            template_name="insurance_application",
            html_path=output_dir / "insurance_application.html",
            extra_fields=extra if extra else None,
            attachments_note=(
                f"{'output/contact_log.pdf' if pdf_ok else 'output/busy_therapists.csv (PDF generation failed — attach CSV instead)'}, "
                "PTV11 form with urgency note, "
                "confirmation from private therapist, "
                "medical certificate of necessity"
            ),
        )

    elif choice == "6":
        run_insurance_option(
            config, base_dir, output_dir,
            template_name="insurance_followup",
            html_path=output_dir / "insurance_followup.html",
        )

    elif choice == "7":
        therapist_name, therapist_email = pick_from_csv(
            output_dir / "private_therapists.csv",
            label="private therapist",
        )
        extra = {}
        if therapist_name:
            extra["private_therapist_name"] = therapist_name
        if therapist_email:
            extra["private_therapist_email"] = therapist_email
        run_insurance_option(
            config, base_dir, output_dir,
            template_name="appeal_rejection",
            html_path=output_dir / "appeal_rejection.html",
            extra_fields=extra if extra else None,
            attachments_note="Original application with all supporting documents",
        )

    elif choice == "8":
        run_insurance_option(
            config, base_dir, output_dir,
            template_name="appeal_ignored",
            html_path=output_dir / "appeal_ignored.html",
        )

    else:
        print(f"\nInvalid choice '{choice}'. Please run again and enter a number 1–8.")
        sys.exit(1)


if __name__ == "__main__":
    main()
