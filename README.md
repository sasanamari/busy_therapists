# Therapy Finder for Kostenerstattung

> **Status**: Early development / MVP phase
>
> This project is currently under active development. Core scraping functionality is being implemented.

---

## Overview

An automated tool to help people in Germany find therapists and compile the required documentation for **Kostenerstattung** (cost reimbursement) applications.

### The Problem

Finding therapy in Germany is extremely difficult:
- Average wait time: 3+ months for first appointment
- For Kostenerstattung (getting public insurance to pay for private therapy), patients must document contacting 20-30+ therapists and receiving rejections
- This bureaucratic process is especially challenging for people with mental health issues

### The Solution

This tool automates the process by:
1. Searching therapist directories based on your criteria
2. Extracting therapist contact information
3. Generating personalized email templates
4. Automating batch email sending (with respectful delays)
5. Producing the required documentation for insurance applications

---

## Legal Basis

This tool implements the process **officially recommended** by the Bundespsychotherapeutenkammer (BPtK) for applying for Kostenerstattung under **§13 Absatz 3 SGB V**.

See [`docs/BPtK_Ratgeber_Kostenerstattung.pdf`](docs/BPtK_Ratgeber_Kostenerstattung.pdf) for the official guide.

---

## Features (Planned)

- [x] Project structure and documentation
- [ ] **Phase 1**: Search and scrape therapist data
- [ ] **Phase 2**: Generate personalized email templates
- [ ] **Phase 3**: Auto-generate Kostenerstattung protocol
- [ ] **Phase 4**: Complete documentation
- [ ] **Phase 5**: Batch email sending with delays

---

## Installation

**Prerequisites**: Python 3.8+

```bash
# Clone the repository
git clone <repository-url>
cd busy_therapists

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

> **Note**: Full usage instructions will be added as features are implemented.

### Phase 1: Search for Therapists (In Development)

```bash
python src/scraper.py --city Berlin --insurance gesetzlich --free-slots
```

---

## Project Structure

```
busy_therapists/
├── src/                  # Python source code
├── templates/            # Email templates
├── docs/                 # Reference documents
├── data/                 # Runtime data (gitignored)
├── tests/                # Unit tests
└── main.py              # CLI entry point
```

---

## Development

See [`SETUP.md`](SETUP.md) for development setup and [`PROJECT_PLAN.md`](PROJECT_PLAN.md) for the implementation roadmap.

---

## Responsible Use

This tool is intended for:
- ✅ Personal use in applying for Kostenerstattung
- ✅ Documenting therapy search as required by insurance
- ✅ Legitimate healthcare access

Please use responsibly:
- Respect rate limits (built into the tool)
- Send personalized, genuine therapy requests
- Do not abuse or spam therapist inboxes
- This is for personal healthcare access, not commercial use

---

## Legal & Ethical Considerations

- **Legal basis**: §13 Absatz 3 SGB V (German social insurance code)
- **Official endorsement**: Process recommended by BPtK (Federal Chamber of Psychotherapists)
- **Purpose**: Healthcare access, not commercial scraping
- **Rate limiting**: Built-in delays to respect server resources
- **Compliance**: Prepared to modify or remove if requested by data sources

---

## Contributing

This project is currently in early development. Contributions, suggestions, and feedback are welcome once the MVP is complete.

---

## License

TBD

---

## Disclaimer

This tool is provided as-is for educational and personal healthcare access purposes. Users are responsible for complying with all applicable laws and using the tool ethically and responsibly.

---

## Contact

For questions or concerns, please open an issue on GitHub.

---

**Current Status**: Implementing Phase 1 (scraping functionality)

Last updated: October 2025
