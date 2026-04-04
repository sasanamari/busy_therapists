# Therapy Finder for Kostenerstattung - Implementation Plan

## Project Overview
An automated tool to help people in Germany find therapists and compile the required documentation for Kostenerstattung (cost reimbursement) applications, as recommended by the Bundespsychotherapeutenkammer (BPtK).

## Problem Statement
Finding therapy in Germany is extremely difficult:
- Average wait time: 3+ months for first appointment
- For Kostenerstattung (private therapy paid by public insurance), patients must document contacting 20-30+ therapists and receiving rejections
- This bureaucratic process is especially difficult for mentally unwell people
- therapie.de is the only directory with "Freie Plätze" (available slots) filter

## Solution
A Python-based terminal application that:
1. Searches therapie.de based on user criteria
2. Extracts therapist contact information (especially emails)
3. Generates personalized email templates
4. Sends batch emails with delays
5. Generates required Kostenerstattung protocol documentation

---

## Development Phases

### Phase 1: Core Scraping ✅ MOSTLY COMPLETE (has bugs)
**Goal**: Successfully extract therapist info from therapie.de

**Status**: Basic scraping works. Email decoder has bugs with special characters and numbers. See CONTEXT_FOR_CLAUDE.md for known issues.

#### Tasks:
1. **Analyze therapie.de structure**
   - [x] Visit therapie.de search page
   - [x] Inspect search form parameters
   - [x] Identify important filters: city, insurance type, "Freie Plätze", radius
   - [x] Examine search results HTML structure
   - [x] Check pagination mechanism
   - [x] Test with different search criteria

2. **Build scraper**
   - [x] Set up Python environment with dependencies (conda env: busy_therapists)
   - [x] Implement search request (GET with URL parameters)
   - [x] Parse HTML to extract therapist profile URLs
   - [x] Extract fields: name, email (others: TODO later)
   - [x] Handle pagination (multi-page support implemented)
   - [x] Add delays between requests (2.5s default)
   - [x] Error handling for missing fields
   - [x] Email decoder (has bugs - see known issues)

3. **Test scraper**
   - [x] Test with Berlin, gesetzlich insurance, "Freie Plätze"
   - [ ] Test with different cities
   - [ ] Fix email decoder bugs (-, 8, and possibly other chars)
   - [ ] Fix pagination duplicates
   - [ ] Add retry logic for 429 errors

**Output**: `src/scraper.py` - Command-line script that outputs JSON of therapists

**Example usage**:
```bash
python src/scraper.py --city Berlin --insurance gesetzlich --free-slots
```

**Estimated time**: 2-4 sessions

---

### Phase 2: Email Template System
**Goal**: Generate personalized, customizable emails

#### Tasks:
1. **Create template structure**
   - [ ] Design template with placeholders (therapist name, user name, insurance, etc.)
   - [ ] Create default therapy request template
   - [ ] Create Kostenerstattung-specific template (explicitly mentions documentation need)
   - [ ] Support user customization

2. **Build template engine**
   - [ ] Create `src/email_templates.py`
   - [ ] Load templates from `templates/` directory
   - [ ] Accept user info (name, insurance, symptoms, city, etc.)
   - [ ] Replace placeholders with actual values
   - [ ] Generate one email per therapist

3. **User info collection**
   - [ ] Create `my_data.csv` template (3 columns: Field, Your data, Notes)
   - [ ] Read user data from .csv using built-in `csv` module
   - [ ] Document required fields
   - [ ] Add validation for required fields
   - (Previous approach: `user_config.json` — kept as fallback for technical users)

**Output**: `src/email_templates.py` + template files

**Example usage**:
```bash
python src/email_templates.py --therapists data/therapists.json --user-config user_config.json
```

**Estimated time**: 1-2 sessions

---

### Phase 3: Kostenerstattung Protocol Generator
**Goal**: Auto-generate required documentation for insurance

#### Tasks:
1. **Study BPtK requirements**
   - [ ] Review BPtK PDF (in `docs/` folder)
   - [ ] Note required fields for protocol
   - [ ] Find official format/template if exists

2. **Build protocol generator**
   - [ ] Create `src/protocol_generator.py`
   - [ ] Format therapist contacts with timestamps
   - [ ] Include wait times and rejection info
   - [ ] Calculate statistics (total contacted, average wait time)
   - [ ] Export as formatted text file
   - [ ] (Optional) Export as PDF

3. **Test output**
   - [ ] Generate sample protocol
   - [ ] Verify it matches BPtK guidelines
   - [ ] Check formatting is professional/official

**Output**: `src/protocol_generator.py`

**Example usage**:
```bash
python src/protocol_generator.py --therapists data/therapists.json --output protocol.txt
```

**Estimated time**: 1-2 sessions

---

### Phase 4: Documentation & Transparency
**Goal**: Clear, comprehensive documentation with legal/ethical context

#### Tasks:
1. **Write README.md**
   - [ ] Project description
   - [ ] Problem statement
   - [ ] Legal basis (§13 Abs. 3 SGB V)
   - [ ] BPtK endorsement
   - [ ] Installation instructions
   - [ ] Usage guide with examples

2. **Responsible use policy**
   - [ ] State purpose: healthcare access, not spam
   - [ ] Recommend rate limiting
   - [ ] Note this is for personal use (Kostenerstattung documentation)
   - [ ] Disclaimer about legal responsibility

3. **Technical documentation**
   - [ ] Code comments
   - [ ] Architecture overview
   - [ ] Contribution guidelines (if making public)

**Output**: Complete README.md, CODE_OF_CONDUCT.md (optional)

**Estimated time**: 1 session

---

### Phase 5: Email Output (HTML)
**Goal**: Generate a browser-based email viewer so users can send emails from their own email client

#### Tasks:
1. **Build HTML email output**
   - [ ] Create `src/email_html_generator.py`
   - [ ] Generate `emails.html` with all emails displayed
   - [ ] Each email has: therapist name, to address, subject, body, "Open in email app" button (mailto: link)
   - [ ] Open the file automatically in browser after generation

2. **Manual response tracker**
   - [ ] Simple JSON format for tracking responses
   - [ ] CLI command to mark therapists as "responded" / "rejected" / "accepted"
   - [ ] Update protocol with response info

**Output**: `emails.html` file that opens in browser

**Estimated time**: 1 session

**Previous approach (kept as fallback)**: Batch SMTP/OAuth auto-sender with 2-3 min delays between emails. More automated but requires credential setup. See DECISIONS.md for details.

---

## Future Enhancements (Post-MVP)

### Optional Features:
- [ ] **Therapist review mode**: CLI interface to review each therapist before emailing
- [ ] **GUI/Web interface**: Replace terminal with user-friendly web app
- [ ] **Automated response tracking**: Gmail API integration to auto-detect replies
- [ ] **Cover letter generator**: Generate complete insurance application letter
- [ ] **Web deployment**: Host as public web service
- [ ] **Browser extension**: Run directly on therapie.de pages

---

## Project Structure

```
busy_therapists/
├── src/
│   ├── scraper.py              # Phase 1: therapie.de scraping
│   ├── email_templates.py      # Phase 2: Email generation
│   ├── protocol_generator.py   # Phase 3: Kostenerstattung docs
│   ├── email_sender.py         # Phase 5: Batch email sending
│   ├── response_tracker.py     # Phase 5: Manual response logging
│   └── config.py               # Configuration, rate limits
├── templates/
│   ├── therapy_request.txt     # Default email template
│   └── kostenerstattung.txt    # Kostenerstattung-specific template
├── docs/
│   └── BPtK_Ratgeber_Kostenerstattung.pdf  # Official guide
├── data/                       # Runtime data (gitignored)
│   ├── therapists.json         # Scraped therapist data
│   ├── emails.json             # Generated emails
│   └── responses.json          # Response tracking
├── tests/
│   └── test_scraper.py         # Unit tests
├── main.py                     # CLI entry point
├── user_config.json            # User's personal info (gitignored)
├── requirements.txt            # Python dependencies
├── .gitignore
├── README.md                   # Public documentation
├── PROJECT_PLAN.md             # This file
├── DECISIONS.md                # Decision log
├── SETUP.md                    # Getting started guide
└── CONTEXT_FOR_CLAUDE.md       # For future AI assistants
```

---

## Getting Started

1. **Read SETUP.md** for environment setup
2. **Read DECISIONS.md** to understand what's been decided
3. **Start with Phase 1** (scraping is the foundation)
4. **Test each phase** before moving to the next
5. **Commit regularly** to track progress

---

## Success Criteria

### MVP is complete when:
- ✅ Can search therapie.de and extract 30+ therapist emails
- ✅ Can generate personalized email templates
- ✅ Can generate official Kostenerstattung protocol
- ✅ Documentation is clear and professional
- ✅ Can send batch emails with delays

### Ready for public release when:
- ✅ All MVP features working reliably
- ✅ Error handling is robust
- ✅ Documentation is comprehensive
- ✅ Legal/ethical considerations documented
- ✅ Tested by real users
- ✅ Response tracking implemented
- ✅ (Optional) GUI or web interface

---

## Notes

- **Priority**: Scraping > Templates > Protocol > Docs > Email sending
- **Development approach**: Build terminal tool first, add GUI later
- **Tech stack**: Python-first, minimal dependencies
- **Distribution**: GitHub repo, users run locally
- **Legal stance**: Prepare to comply immediately if therapie.de objects
