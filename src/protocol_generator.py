"""
Protocol generator for Kostenerstattung applications.

Reads output/responses.csv (filled in by the user) and my_data.csv,
then produces a formal contact protocol document suitable for submission
to the health insurance company under § 13 Abs. 3 SGB V.

Usage (via main.py):
    python main.py --protocol
"""

import csv
from datetime import datetime
from pathlib import Path


def read_responses(csv_path: Path) -> list[dict]:
    """Read the user-filled responses.csv into a list of dicts."""
    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    return rows


def _count_responses(rows: list[dict]) -> tuple[int, int]:
    """Return (total_contacted, total_responded)."""
    total = len(rows)
    responded = sum(
        1 for r in rows
        if r.get("Response received (Yes/No)", "").strip().lower() in ("yes", "ja")
    )
    return total, responded


def generate_protocol(config: dict, responses_path: Path, output_path: Path) -> None:
    """
    Generate the contact protocol text file.

    Args:
        config: Parsed user config from parse_config() in main.py.
        responses_path: Path to the user-filled responses.csv.
        output_path: Where to write the protocol .txt file.
    """
    if not responses_path.exists():
        raise FileNotFoundError(
            f"responses.csv not found at {responses_path}\n"
            "Run the main tool first to generate it, then fill in the response columns."
        )

    rows = read_responses(responses_path)

    if not rows:
        raise ValueError("responses.csv is empty — nothing to generate a protocol from.")

    total_contacted, total_responded = _count_responses(rows)
    today = datetime.now().strftime("%d.%m.%Y")
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Determine how many have a contact date filled in
    dated_contacts = [r for r in rows if r.get("Date contacted", "").strip()]

    lines = []

    def hr(char="=", width=72):
        lines.append(char * width)

    def section(title):
        lines.append("")
        lines.append(title)
        lines.append("-" * len(title))

    hr()
    lines.append("NACHWEIS DER KONTAKTAUFNAHME MIT PSYCHOTHERAPEUTEN")
    lines.append("Gemäß § 13 Abs. 3 SGB V")
    hr()
    lines.append(f"Erstellt am: {generated_at}")

    section("PATIENTENDATEN")
    lines.append(f"Name:          {config['patient_name']}")
    lines.append(f"Wohnort:       {config['patient_city']}")
    lines.append(f"Krankenkasse:  {config['insurance_company']}")
    lines.append(f"Versicherung:  {config['insurance_type']}")
    if config.get("sender_email"):
        lines.append(f"E-Mail:        {config['sender_email']}")

    section("SUCHANFRAGE")
    lines.append(f"Postleitzahl:         {config['zip_code']}")
    lines.append(f"Therapeuten gesucht:  {config['target_count']}")
    lines.append(f"Symptome / Anliegen:  {config['symptoms']}")
    if config.get("previous_diagnosis"):
        lines.append(f"Frühere Diagnose:     {config['previous_diagnosis']}")

    section("ZUSAMMENFASSUNG")
    lines.append(f"Therapeuten kontaktiert:  {total_contacted}")
    lines.append(f"Antworten erhalten:       {total_responded}")
    lines.append(f"Ohne Antwort:             {total_contacted - total_responded}")
    if total_contacted > 0:
        rate = round(total_responded / total_contacted * 100)
        lines.append(f"Antwortquote:             {rate}%")
    if dated_contacts:
        dates = [r["Date contacted"].strip() for r in dated_contacts]
        lines.append(f"Kontaktzeitraum:          {min(dates)} – {max(dates)}")

    section("KONTAKTPROTOKOLL")
    lines.append(
        "Die folgende Liste dokumentiert alle kontaktierten Therapeuten "
        "und deren Rückmeldungen.\n"
    )

    for i, row in enumerate(rows, 1):
        name = row.get("Name", "").strip() or "—"
        email = row.get("Email", "").strip() or "—"
        address = row.get("Address", "").strip() or "—"
        contacted = row.get("Date contacted", "").strip() or "nicht eingetragen"
        responded = row.get("Response received (Yes/No)", "").strip() or "—"
        response_date = row.get("Response date", "").strip() or "—"
        notes = row.get("Notes", "").strip() or "—"

        lines.append(f"{i:02d}. {name}")
        lines.append(f"    E-Mail:           {email}")
        lines.append(f"    Adresse:          {address}")
        lines.append(f"    Kontaktiert am:   {contacted}")
        lines.append(f"    Antwort erhalten: {responded}")
        if responded.lower() in ("yes", "ja"):
            lines.append(f"    Datum der Antwort:{response_date}")
        if notes and notes != "—":
            lines.append(f"    Notizen:          {notes}")
        lines.append("")

    section("ERKLÄRUNG")
    lines.append(
        "Ich bestätige hiermit, dass ich mich persönlich und in gutem Glauben\n"
        "mit den oben aufgeführten Psychotherapeutinnen und Psychotherapeuten\n"
        "in Verbindung gesetzt habe, um einen Therapieplatz mit Kassenzulassung\n"
        "zu erhalten. Aufgrund langer Wartezeiten und fehlender freier Kapazitäten\n"
        "war es mir innerhalb einer zumutbaren Frist nicht möglich, einen\n"
        "Kassentherapieplatz zu finden.\n\n"
        "Dieses Dokument dient als Nachweis gemäß den Empfehlungen der\n"
        "Bundespsychotherapeutenkammer (BPtK) für die Beantragung von\n"
        "Kostenerstattung nach § 13 Abs. 3 SGB V."
    )
    lines.append("")
    lines.append(f"Ort, Datum:    Berlin, {today}")
    lines.append("")
    lines.append("Unterschrift:  _________________________________")
    lines.append("")
    hr()

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved protocol → {output_path}")
    print(f"  Contacts documented: {total_contacted}")
    print(f"  Responses received:  {total_responded}")
