# Project Decisions Log

This document tracks all decisions made during project planning and development.

## Legend
- ✅ **DECIDED** - Decision made and confirmed
- ⏸️ **PENDING** - To be decided later
- 🤔 **UNDER CONSIDERATION** - Currently discussing

---

## Architecture Decisions

### ✅ Tech Stack
- **Language**: Python (primary language for all core functionality)
- **Scraping**: requests + BeautifulSoup (start simple, switch to Selenium if needed)
- **Data format**: JSON files (simple, readable, no database needed for MVP)
- **Interface**: Command-line/terminal (start here, add GUI later)

**Rationale**: You're comfortable with Python, terminal tool is simplest MVP, can add GUI later.

---

### ✅ Development Approach
- **Phased development**: Terminal tool first → GUI later
- **MVP-first**: Build core features, then iterate
- **Testing strategy**: Manual testing during development, unit tests later

**Rationale**: Get working MVP quickly, iterate based on real use.

---

### ✅ Project Structure
```
busy_therapists/
├── src/              # Python modules
├── templates/        # Email templates
├── docs/            # Reference documents
├── data/            # Runtime data (gitignored)
└── tests/           # Unit tests
```

**Rationale**: Clear separation of concerns, standard Python project layout.

---

## Feature Decisions

### ✅ Email Sending Method
**Decision**: User clicks "Send All" once → app sends all emails with automatic 2-3 minute delays

**Alternatives considered**:
- User clicks "Send" for each email individually (too tedious)
- No delays (legally risky, spam-like)

**Rationale**: Best balance of automation and legal safety. User authorizes batch, app handles timing.

---

### ✅ Rate Limiting
**Decision**: 2-3 minutes between each email, user keeps app/browser running

**Details**:
- Total time for 30 emails: ~60-90 minutes
- User doesn't need to babysit (can walk away)
- No need to return every hour

**Rationale**: Respectful to servers, user-friendly, legally defensible.

---

### ✅ Therapist Review Mode
**Decision**: Start with auto-send only (no review), add optional review mode later

**Current implementation**: Auto-send to all matching therapists
**Future enhancement**: Toggle between "review each" vs "auto-send all"

**Rationale**: Auto-send is core use case for Kostenerstattung (collecting rejections). Review mode is nice-to-have for people genuinely choosing a therapist.

---

### ✅ Response Tracking
**Decision**: Manual logging for MVP, note automated tracking (Gmail API) for future

**Current implementation**:
- JSON file with therapist status
- CLI command to mark responses: `track-response --therapist "Dr. X" --status rejected`

**Future enhancement**: Gmail API integration to auto-detect replies

**Rationale**: Manual is simpler and privacy-respecting. Automated is complex but good for portfolio showcase.

---

### ✅ Data Storage Between Steps
**Decision**: JSON files (no database for MVP)

**Files**:
- `data/therapists.json` - Scraped therapist data
- `data/emails.json` - Generated emails
- `data/responses.json` - Response tracking
- `user_config.json` - User's personal info

**Rationale**: Simple, human-readable, easy to edit/debug, no setup required.

---

### ✅ User Info Collection
**Decision**: User edits a `user_config.json` file with their details

**Fields**:
```json
{
  "name": "Max Mustermann",
  "insurance": "gesetzlich",
  "insurance_company": "TK",
  "city": "Berlin",
  "symptoms": "depression, anxiety",
  "previous_diagnosis": "optional field",
  "email": "user@example.com"
}
```

**Rationale**: Easy to edit, reusable, no interactive prompts needed.

---

## Scraping Decisions

### ✅ Scraping Library
**Decision**: Start with requests + BeautifulSoup, switch to Selenium if site requires JavaScript

**Rationale**: BeautifulSoup is simpler and faster. Only use Selenium if necessary (adds complexity, requires browser driver).

---

### ✅ Respect robots.txt
**Decision**: Yes, follow robots.txt rules

**From analysis**:
- Main pages allowed
- Avoid `/psychotherapie/-ergebnisse-/` and video session pages
- No crawl delay specified, but we'll add 2-3 seconds between requests

**Rationale**: Shows good faith, ethically correct, legally safer.

---

### ✅ Data to Extract
**Priority fields**:
1. Name
2. Email (critical - only contact therapists with email)
3. Wait time / "Freie Plätze" status
4. Specializations (optional but useful)
5. Address/city (for verification)
6. Phone (backup if email fails)

**Rationale**: Email is essential for automation. Wait time is critical for Kostenerstattung documentation.

---

## Email Decisions

### ⏸️ Email Sending Method (TO BE DECIDED)
**Options**:
1. **SMTP** - User provides Gmail username + app-specific password
2. **OAuth** - User grants app permission via Google OAuth
3. **Email service API** - SendGrid, Mailgun, etc.

**To decide**: After scraping works, research and choose based on:
- Security
- Ease of setup for users
- Reliability

---

### ✅ Email Templates
**Decision**: Provide default templates, user can customize

**Templates**:
1. `templates/therapy_request.txt` - General therapy request
2. `templates/kostenerstattung.txt` - Explicit mention of documentation need

**Template format**: Simple text with `{placeholders}` for variables

**Rationale**: Users should be able to personalize while having good defaults.

---

## Legal & Ethical Decisions

### ✅ Contact therapie.de for API?
**Decision**: No, don't contact them preemptively

**Rationale**:
- They likely don't have ready API
- Asking might trigger preemptive "no"
- Better to build in good faith, comply if they object
- Anonymous email looks suspicious anyway

---

### ⏸️ Acknowledge therapie.de in README? (TO BE DECIDED)
**Options**:
1. **Transparent**: "Data source: therapie.de" in README
2. **Generic**: "Searches German therapist directories"

**To decide**: After main code works, before making repo public

**Considerations**:
- Transparent = good faith, harder to object to
- Generic = draws less attention
- Recommendation: Lean toward transparent (shows integrity)

---

### ✅ Compliance Strategy
**Decision**: Prepare to comply immediately if therapie.de objects

**Actions if contacted**:
1. Respond professionally and promptly
2. Take down or modify as requested
3. Frame project as healthcare access tool implementing BPtK recommendations
4. Offer to discuss concerns

**Rationale**: Compliance costs nothing, legal fight costs everything.

---

### ✅ Legal Defense Strategy
**Primary arguments**:
1. **BPtK endorsement**: Official professional chamber recommends this process
2. **Healthcare access**: Facilitating constitutionally guaranteed healthcare
3. **§13 Abs. 3 SGB V**: Legally mandated documentation process
4. **Public health benefit**: Mental health crisis in Germany
5. **No commercial use**: Personal healthcare access, not business
6. **Published contact info**: Therapists list emails to be contacted

**Rationale**: Strong ethical and legal foundation. Document this in README.

---

## Documentation Decisions

### ✅ Documentation Files
**For humans**:
- `README.md` - Public-facing documentation
- `PROJECT_PLAN.md` - Step-by-step implementation guide
- `DECISIONS.md` - This file
- `SETUP.md` - Getting started guide

**For AI assistants**:
- `CONTEXT_FOR_CLAUDE.md` - Comprehensive context for future Claude instances

**Rationale**: Comprehensive documentation for both continuity and transparency.

---

### ✅ README Contents
**Must include**:
- Problem statement
- Solution overview
- Legal basis (§13 Abs. 3 SGB V, BPtK guide)
- Installation instructions
- Usage guide
- Responsible use policy
- **PENDING**: Acknowledge therapie.de or not?

---

## Distribution Decisions

### ✅ Distribution Method (MVP)
**Decision**: GitHub repo, users run locally

**Setup**:
```bash
git clone https://github.com/username/busy_therapists
cd busy_therapists
pip install -r requirements.txt
python main.py --help
```

**Future considerations**:
- Web app (hosted online)
- Downloadable executable
- Browser extension

**Rationale**: Simplest for MVP, shows code quality for portfolio, easy for tech-savvy users.

---

## Implementation Priority

### ✅ Phase Order
1. **Phase 1**: Scraping (HIGHEST PRIORITY)
2. **Phase 2**: Email templates
3. **Phase 3**: Protocol generator
4. **Phase 4**: Documentation
5. **Phase 5**: Email sending (LOWEST PRIORITY for MVP)

**Rationale**: Scraping is foundation - nothing works without it. Email sending is last because it requires external setup.

---

## Timeline & Scope

### ✅ MVP Definition
**Minimum viable product includes**:
1. ✅ Scraping therapie.de for therapist emails
2. ✅ Email template generation
3. ✅ Kostenerstattung protocol generation
4. ✅ Professional documentation
5. ✅ Batch email sending with delays

**Optional for MVP**:
- Automated response tracking (manual is fine)
- GUI (terminal is fine)
- Cover letter generator
- Review mode

---

### ✅ Development Style
**Decision**: Iterative MVP approach

**Process**:
1. Build terminal tool with core features
2. Test with real use cases
3. Iterate based on experience
4. Add GUI/polish later if useful

**Rationale**: Fast feedback loop, working tool quickly, avoid over-engineering.

---

## Future Enhancements (Post-MVP)

### Nice-to-have features:
- [ ] Optional therapist review mode (CLI menu to approve each)
- [ ] GUI/web interface (React/Flask)
- [ ] Automated response tracking (Gmail API)
- [ ] Cover letter generator (complete insurance application)
- [ ] Multi-language support (English + German)
- [ ] Web deployment (hosted service)
- [ ] Browser extension (runs on therapie.de directly)
- [ ] PDF export for protocol
- [ ] Email statistics dashboard

---

## Questions for Future Sessions

### When implementing scraping:
- Does therapie.de use JavaScript rendering? (affects BeautifulSoup vs Selenium choice)
- What's the exact URL structure for search?
- Are emails directly visible or require clicking through to profiles?

### When implementing email:
- Which email method is most user-friendly?
- How to securely store email credentials?
- Should emails be logged for debugging?

### Before going public:
- Should we acknowledge therapie.de in README?
- Any final legal review needed?
- Test with real users first?

---

## Decision-Making Principles

**When in doubt**:
1. **Prioritize user experience** (especially for mentally unwell people)
2. **Choose simplicity** (MVP first, polish later)
3. **Be ethically defensible** (healthcare access, good faith)
4. **Stay legally compliant** (follow robots.txt, cite legal basis)
5. **Document everything** (decisions, rationale, context)

---

Last updated: 2025-10-24
