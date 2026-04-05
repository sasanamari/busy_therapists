# Context for Claude Code (AI Assistant Instructions)

**READ THIS FIRST** when helping with this project.

---

## 🟢 COMPLETED

### Phase 1: Scraping ✅
- Email decoder (shift-1 cipher), pagination, rate limiting with 429 retry logic
- Auto-expands search radius to 25km when default radius yields too few results
- Tested end-to-end with real therapie.de data

### Phase 2: Email Templates ✅
- German and English templates (`templates/therapy_request.txt`, `therapy_request_en.txt`)
- Mail merge via `src/email_generator.py` — placeholder replacement, language detection, optional diagnosis field
- English template asks "Do you offer therapy in [language]?" — dynamically filled from CSV; falls back to "Do you offer therapy in German and English?" if no language set
- Single straightforward template (not bureaucratic) — more likely to get responses

### Phase 3: Protocol Generator ✅
- `src/protocol_generator.py` — reads filled-in `output/responses.csv` + `my_data.csv`, outputs `output/protocol.txt`
- Formal German document: patient info, search criteria, full contact list with dates/outcomes, declaration paragraph
- Run with `python main.py --protocol`

### main.py: Full end-to-end flow ✅
- Reads `my_data.csv`, scrapes, generates emails, opens `output/emails.html` in browser
- Output structure: `emails.html`, `responses.csv`, `therapists.txt`, `emails/`, `.data/` (internal JSONs)
- `emails/` cleared at start of each run to prevent stale file accumulation
- `profile_url` removed from `responses.csv` (keeps scraping source out of insurance documents)

### Search filters ✅
- All therapie.de filter params wired: availability, insurance, foreign language, therapy format, focus/topic, therapist gender
- Human-readable CSV values mapped to numeric IDs via lookup dicts in `main.py`
- Unrecognised filter values print a warning at startup AND at the end of the run
- `terminzeitraum` bug fixed: `4` = "wait over 12 months" (not "available now"); `1` = available now
- Full param reference with English translations: `docs/therapie_de_filter_params.md`

---

## Project Summary

**Name**: Therapy Finder for Kostenerstattung
**Purpose**: Automate the bureaucratic process of finding therapists and documenting contacts for German health insurance cost reimbursement (Kostenerstattung)
**Status**: MVP complete — tested end-to-end. Next: PyInstaller executable + documentation.
**Tech Stack**: Python-first, terminal application, JSON data storage

---

## The Problem (Context)

### Healthcare Crisis in Germany
- Average wait time for therapy: 3+ months
- Finding a therapist is extremely difficult
- Especially hard for mentally unwell people to navigate bureaucracy

### The Kostenerstattung Process
When public insurance holders can't find therapists with public insurance (Kassenzulassung), they can apply for **Kostenerstattung** - having insurance pay for private therapy under **§13 Absatz 3 SGB V**.

**Requirements** (per BPtK guide):
1. Document that therapy is medically necessary and urgent
2. **Prove you contacted multiple therapists** (originally 3-5, now realistically 20-30+) with public insurance
3. Document they had long wait times (3+ months)
4. Find private practice therapist who can start soon

**Additional TK-specific requirements:**
- The patient must first attend **probationary sessions** (Probatorische Sitzungen) — 1-2 initial evaluation sessions with a therapist to confirm therapy is needed
- The referring therapist must add an **urgency code** sticker/label to the form, indicating the therapy is urgent
- These two requirements must be in place before TK will process a Kostenerstattung application

**The problem**: Step 2 is tedious, requiring dozens of phone calls/emails and manual documentation. This is especially difficult for people with mental health issues.

---

## The Solution

An automated Python tool that:
1. **Scrapes therapie.de** (only directory with "Freie Plätze" filter showing availability)
2. **Extracts therapist emails** (not all have email addresses)
3. **Generates personalized emails** from templates
4. **Opens emails.html in the browser** — user sends each email via their own email client (mailto: buttons)
5. **Auto-generates the required protocol** for insurance application

---

## Legal & Ethical Considerations

### ✅ Strong Legal Foundation

**This is NOT typical web scraping - it's healthcare access automation**:

1. **Officially endorsed**: Bundespsychotherapeutenkammer (BPtK) - the federal chamber of psychotherapists - explicitly tells patients to do this process (manually). See `docs/BPtK_Ratgeber_Kostenerstattung.pdf`

2. **Legal mandate**: §13 Absatz 3 SGB V legally requires this documentation for Kostenerstattung

3. **Public health benefit**: Helps people access constitutionally guaranteed healthcare

4. **Published contact info**: Therapist emails are publicly listed specifically to be contacted

5. **No commercial use**: Personal healthcare access, not business/profit

### ⚠️ Legal Gray Areas

1. **Automation scale**: Even legitimate requests, if automated at large scale, could raise concerns
2. **Database rights**: therapie.de claims copyright on their database (per their AGB)
3. **Mass emailing**: German UWG prohibits "unreasonable harassment" - mitigated by:
   - Emails are legitimate service requests
   - Rate limiting (2-3 min delays)
   - Personalized content
   - User authorization

### 🛡️ Risk Mitigation Strategy

1. **robots.txt compliance**: Respect their rules (main pages allowed, add delays)
2. **Rate limiting**: Built-in 2-3 min delays between requests
3. **No persistent database**: Only session data, not republishing their directory
4. **Transparency**: Document legal basis and ethical purpose
5. **Compliance readiness**: Prepared to take down immediately if therapie.de objects
6. **Good faith**: Solving real problem, not hiding intentions
7. **Generic public documentation**: Keep data sources generic in public-facing docs (README)

---

## Technical Architecture

### Python Environment Setup

**IMPORTANT**: This project uses a dedicated conda environment called `busy_therapists`.

**For Claude Code sessions:**
Use `mamba run` (confirmed working; `conda run` does not work):
```bash
mamba run -n busy_therapists python <script.py>
```

**For user (manual terminal):**
```bash
conda activate busy_therapists
python <script.py>
```

**Dependencies:** Managed via `requirements.txt` (requests, beautifulsoup4, lxml)

### Current Decisions

**Language**: Python (user is comfortable with it)
**Interface**: `python main.py` for technical users; PyInstaller executable for non-technical users (no Python install needed)
**User input**: `my_data.csv` — 3-column CSV (Field, Your data, Notes). User fills in column B. Read via Python's built-in `csv` module. Opens as a table in Excel/Numbers. `my_data.csv` is gitignored; `my_data.csv.example` is the committed template — users copy and rename it. Previous approach (user_config.json) kept as fallback.
**Data format**: JSON files internally (simple, no database)
**Scraping**: requests + BeautifulSoup (start simple, use Selenium if needed)
**Email delivery**: Generate `emails.html`, auto-open in browser. Each email displayed with a mailto: button — user sends from their own email client. No SMTP/OAuth/credentials needed. Previous approach (SMTP/OAuth batch auto-sender) kept as fallback in DECISIONS.md.

### Project Structure
```
busy_therapists/
├── src/
│   ├── scraper.py              # ✅ Phase 1
│   ├── email_generator.py      # ✅ Phase 2
│   └── protocol_generator.py   # ✅ Phase 3
├── templates/
│   ├── therapy_request.txt     # German email template
│   └── therapy_request_en.txt  # English email template
├── docs/
│   ├── BPtK_Ratgeber_Kostenerstattung.pdf
│   └── therapie_de_filter_params.md  # All URL params with EN translations
├── output/                     # gitignored — generated at runtime
│   ├── emails.html             # ← open this to send emails
│   ├── responses.csv           # ← fill in as replies come
│   ├── therapists.txt          # human-readable therapist list
│   ├── emails/                 # individual .txt files per email
│   └── .data/                  # internal JSONs (therapists, emails)
├── main.py                     # ✅ entry point
├── my_data.csv.example         # committed template — user copies & renames
├── my_data.csv                 # gitignored — user's personal data
└── requirements.txt
```

### Development Phases

- **Phase 1** ✅ Scraping
- **Phase 2** ✅ Email templates (template 1 — general inquiry)
- **Phase 2b** 🔲 Additional email templates (templates 2–6, see Next Steps)
- **Phase 3** ✅ Protocol generator
- **Phase 4** 🔲 Documentation (README legal basis, installation guide, responsible use)
- **Phase 5** ❌ Dropped — batch SMTP email sending not worth it without cloud setup; mailto: approach is sufficient
- **Phase 6** 🔲 PyInstaller executable — bundle for non-technical users (see Next Steps)

---

## Key Implementation Details

### Email Sending Flow
- Tool generates `output/emails.html` and opens it in the browser
- Each email has an "Open in email app" button (mailto: link pre-filled with subject + body)
- User sends from their own email client — no SMTP/OAuth/credentials needed
- Batch SMTP sending was considered but dropped (not worth it without cloud setup)

### Rate Limiting
- **Scraping**: 2.5 seconds between requests (built-in, not configurable)
- Retry logic for 429 errors: waits 60s then 300s before giving up

### Data Minimization
- No persistent therapist database — only session data in `output/`
- `output/` is gitignored
- `my_data.csv` is gitignored — user's personal data stays local
- `profile_url` excluded from `responses.csv` to avoid revealing scraping source in insurance documents

### Response Tracking
- Manual: user fills in `output/responses.csv` as replies come in
- Then runs `python main.py --protocol` to generate the formal contact protocol

---

## User Profile (Important Context)

**Background**:
- Physical chemistry → data science → learning data engineering
- Comfortable with Python, new to web development
- New to macOS (M2 MacBook) after Windows/Ubuntu
- Located in Berlin

**Communication preferences**:
- Pragmatic, concise (no excessive reassurance)
- Casual tone (colleague, not formal)
- Technical topics: straight answers
- Learning mode: provide tips and context

**Project goals**:
1. **Personal use**: Help with finding therapy
2. **Portfolio**: Showcase for job applications (data engineering)
3. **Public good**: Help others facing same problem

---

## What Has Been Done

✅ Phase 1: Scraping
✅ Phase 2: Email templates
✅ Phase 3: Protocol generator
✅ main.py: full end-to-end flow, tested
✅ Search filters: all therapie.de params wired (availability, insurance, language, format, focus, gender)
✅ Output cleanup: emails/ cleared per run, internal JSONs in .data/
✅ Filter validation: warnings for unrecognised values (shown at start and end of run)
✅ Dynamic language question in English email template
✅ docs/therapie_de_filter_params.md with English translations

**Current status (2026-04-04)**: MVP complete and tested end-to-end. All phases 1–3 done and committed.

**README work in progress (2026-04-04)**: Working on Phase 4 (documentation). A user guide draft has been written collaboratively and saved to `GUIDE_DRAFT.md`. The guide covers the full Kostenerstattung process step by step, written for someone with mental health challenges. **Next session: user will review `GUIDE_DRAFT.md`, give feedback, then it gets integrated into `README.md` in the appropriate place. The README itself still needs to be fully rewritten** (current README is outdated — wrong feature list, wrong status, stale). Legal basis section intentionally omitted from README per user preference.

---

## 🐛 Known Issues / To Fix

- **Kostenerstattung filter exists but undocumented**: `Insurance filter: kostenerstattung` is already implemented (maps to ID 6 in INSURANCE_MAP). The README/user guide should mention this as the recommended filter when searching for private therapists willing to work with reimbursement. therapie.de's data for this filter may not be fully up to date, so users should still confirm with the therapist directly.

- **my_data.csv needs new optional fields** for templates 5–8 (insurance emails). Add these fields with empty defaults so they stay as visible placeholders if not filled in:
  - `Insurance number` — Versichertennummer (used in all insurance emails)
  - `Private therapist name` — name of the private therapist found (templates 5, 7, 8)
  - `Private therapist email` — email address of private therapist (template 4 sending)
  - `Insurance email` — email address of the Krankenkasse (templates 5, 6, 7, 8)
  - `Application date` — date the Kostenerstattung application was sent (templates 6, 8)
  - `Follow-up date` — date the follow-up email was sent (template 8)
  - `Rejection date` — date of the rejection letter (template 7)
  - `Max wait months` — longest wait time found among public therapists (template 5)
  All fields optional. If empty, placeholder stays visible in the email so user fills it in manually.

- **Insurance type not wired to scraper**: `my_data.csv` has an `Insurance type` field (public/private) used in emails, but it does NOT automatically set the scraper's insurance filter. The scraper uses the separate `Insurance filter` field. A user with private insurance who sets `Insurance type: private` won't automatically get private therapist results — they'd also need to set `Insurance filter: private`. These two fields should either be merged or `Insurance type` should auto-set the scraper filter. Raised during README writing (2026-04-04).

---

## ✅ Decisions Made

### main.py: Interactive menu (2026-04-05)
`main.py` will be refactored to show an **interactive numbered menu** instead of CLI flags. This is required for PyInstaller compatibility (double-click executable) and better UX for non-technical users.

**Design:**
- User runs the program (or double-clicks executable) → sees a numbered menu
- They type a number to select what they need today
- Each option tells the user what they need to have ready (e.g. "Make sure my_data.csv is filled in", "Make sure responses.csv is filled in")
- Technical users can still use flags (e.g. `--scrape`, `--protocol`) to skip the menu

**Menu options (mapped to templates/modes):**
1. Search for therapists + generate outreach emails (`therapy_request`) — needs: `my_data.csv`
2. Request a probationary session (`probationary_request`) — needs: `my_data.csv`
3. Contact public therapists for documentation (`kassenzulassung_contact`) — needs: `my_data.csv`
4. Find a private therapist (`private_therapist_inquiry`) — needs: `my_data.csv`
5. Generate reimbursement application letter (`insurance_application`) — needs: `my_data.csv` + private therapist details
6. Generate contact protocol (`--protocol` mode) — needs: `responses.csv` filled in
7. Follow up with insurance — no response (`insurance_followup`) — needs: `my_data.csv`
8. Appeal a rejection (`widerspruch_rejection`) — needs: `my_data.csv` + rejection letter date
9. Legal threat — being ignored (`widerspruch_ignored`) — needs: `my_data.csv`

Options 2–4 use the scraper (same as option 1 but different templates). Options 5, 7, 8, 9 are one-off documents (no scraper needed).

---

**Next steps (in order):**

### 1. Phase 4: Documentation
- Update README with:
  - Legal basis section (§13 Abs. 3 SGB V, BPtK endorsement)
  - Clear explanation of the Kostenerstattung process (see below for details)
  - Step-by-step usage instructions
  - Responsible use policy
- The README should mention the full manual process the user needs to follow, including probationary sessions and urgency code (see Kostenerstattung Process section above)

### 2. Phase 2b: Additional Email Templates

We need 8 templates in total. Template 1 already exists. The remaining 7 need to be built.

**Overview of all templates:**

| # | File | Purpose | Recipient |
|---|---|---|---|
| 1 | `therapy_request.txt` / `_en.txt` | ✅ Exists — general therapy inquiry | Any therapist (public or private) |
| 2 | `probationary_request.txt` | Ask for Probatorische Sitzungen (1-2 eval sessions) | A Kassenzulassung therapist |
| 3 | `kassenzulassung_contact.txt` | Ask public therapists for availability — for documentation purposes | Public therapists |
| 4 | `insurance_application.txt` | Formal Kostenerstattung application letter | Health insurance company (Krankenkasse) |
| 5 | `private_therapist_inquiry.txt` | Ask private therapist: can they start soon + Fachkunde in Richtlinienverfahren + willing to do Kostenerstattung paperwork? | Private practice therapists |
| 6 | `widerspruch_rejection.txt` | Formal Widerspruch after insurance **rejects** the application | Health insurance company |
| 7 | `insurance_followup.txt` | Polite follow-up after ~4 weeks of no response — asking for status update | Health insurance company |
| 8 | `widerspruch_ignored.txt` | Legal threat after being ignored even after template 7 (~5 weeks total silence) | Health insurance company |

**Notes on templates 6-8:**
- Template 6 = rejection scenario (Widerspruch — already planned, BPtK wording exists)
- Template 7 = no response after ~4 weeks → polite status enquiry before escalating
- Template 8 = still no response after ~5 weeks (1 week after template 7) → legal threat (different tone/wording from template 6, as this is about being ignored rather than a formal rejection)

**Templates provided verbatim in the BPtK PDF (use these as the basis):**

*Template 4 — Insurance application letter (from PDF p.8):*
```
[Anschrift des Versicherten]
[Anschrift der Krankenkasse]          Ort, Datum

Versichertennummer: [Nummer]

Antrag auf ambulante Psychotherapie und Kostenerstattung nach § 13 Absatz 3 SGB V

Sehr geehrte Damen und Herren,

hiermit beantrage ich, dass Sie die Kosten, die mir durch die ambulante Psychotherapie
bei Frau/Herrn [Name Therapeut:in] entstehen, übernehmen und mir dies zusichern.
Frau/Herr [Name] ist ein approbierter Psychotherapeut/eine approbierte Psychotherapeutin
in einem Richtlinienverfahren, verfügt aber nicht über eine Zulassung zur gesetzlichen
Krankenversicherung.

Wie Sie meinem beigelegten Protokoll entnehmen können, habe ich mich mehrfach vergeblich
bemüht, einen Psychotherapeuten mit Kassenzulassung zu finden, der mich rechtzeitig
behandeln kann. Meine Psychotherapeutensuche ergab, dass ich mehr als [X] Monate auf
einen ersten Termin warten müsste. Dagegen besteht die Möglichkeit, dass ich bei
Frau/Herrn [Name] kurzfristig mit einer Behandlung beginnen könnte. Eine entsprechende
Bescheinigung lege ich bei. Ich lege Ihnen des Weiteren eine Bescheinigung eines
[Hausarztes/Facharztes/Psychotherapeuten] bei, der mir dringend eine ambulante
Psychotherapie empfiehlt.

Falls Sie meinem Antrag nicht zustimmen, nennen Sie mir bitte – so schnell wie möglich –
einen zugelassenen Psychotherapeuten in der Nähe meines Wohnortes, bei dem ich
kurzfristig einen Termin erhalte.

Mit freundlichen Grüßen
[Unterschrift]
```

*Template 6 — Widerspruch / formal appeal (from PDF p.9):*
```
[Anschrift des Versicherten]
[Anschrift der Krankenkasse]          Ort, Datum

Versichertennummer: [Nummer]

Widerspruch
Ihr Schreiben vom [Datum des Ablehnungsschreibens]

Sehr geehrte Damen und Herren,

hiermit lege ich Widerspruch gegen Ihr Schreiben vom [Datum] ein, mit dem Sie es ablehnen,
die Kosten, die mir durch die ambulante Psychotherapie bei Frau/Herrn [Name] entstehen,
zu übernehmen. Meinem Antrag lagen die erforderlichen Unterlagen bei, aus denen hervorgeht,
dass die Anspruchsvoraussetzungen vorliegen.

Ich bitte Sie deshalb erneut, meinen Antrag zu genehmigen. Sollten Sie dem Antrag nicht
stattgeben, werde ich meinen Anspruch gerichtlich durchsetzen und die Aufsichtsbehörde
sowie den Patientenbeauftragten der Bundesregierung informieren.

Mit freundlichen Grüßen
[Unterschrift]
```

**Template details:**

**Template 2 — Probationary session request:**
- Ask if therapist can offer Probatorische Sitzungen (1-2 sessions)
- These sessions result in a written certificate that therapy is medically necessary
- Tone: warm, personal — not bureaucratic

**Template 3 — Public therapist contact (for documentation):**
- Short email asking if they have capacity for a Kassenzulassung patient
- Expectation is they won't — the point is building the *Protokoll der vergeblichen Suche*
- Must feel like a genuine inquiry, not a form letter
- This is the template most likely to be sent in bulk (20-30 emails)

**Template 4 — Insurance application letter:**
- Formal letter to Krankenkasse requesting Kostenerstattung under §13 Abs. 3 SGB V
- BPtK guide provides exact wording — use it as the basis
- Needs placeholders for: patient info, private therapist name, wait time found, attachments list
- Key line: "Falls Sie meinem Antrag nicht zustimmen, nennen Sie mir bitte – so schnell wie möglich – einen zugelassenen Psychotherapeuten in der Nähe meines Wohnortes, bei dem ich kurzfristig einen Termin erhalte."
- This is a letter (not an email) — output as a formatted .txt for printing

**Template 5 — Private therapist inquiry:**
- Ask two specific things (per BPtK guide):
  1. Can they start treatment soon (kurzfristig)?
  2. Do they have *Fachkunde in einem Richtlinienverfahren*?
- Ask them to confirm both in writing if yes
- Richtlinienverfahren = Analytische Psychotherapie, tiefenpsychologisch fundierte Psychotherapie, or Verhaltenstherapie

**Template 6 — Widerspruch (formal appeal):**
- BPtK guide provides exact wording — use it as the basis
- Formal objection to rejection of Kostenerstattung application
- States: will pursue in court + notify *Aufsichtsbehörde* + *Patientenbeauftragter der Bundesregierung*
- Needs placeholders for: rejection letter date, patient info, private therapist name
- Also a letter for printing, not an email

**Implementation notes:**
- All templates need German + English versions (same pattern as template 1)
- Templates 4 and 6 are letters (for printing), not emails — the HTML viewer should show them differently (no mailto: button, just a "Copy text" or "Print" button)
- The `my_data.csv` will need new fields: private therapist name + address (for templates 4-6), insurance rejection letter date (for template 6)
- The scraper flow is only relevant for templates 1, 3, and 5 — templates 2, 4, 6 are one-off documents

### 3. Phase 4: Documentation
- Bundle into a double-clickable executable for non-technical users (no Python install needed)
- **Critical**: `my_data.csv` must live **outside** the bundle — next to the executable — so users can edit it
- `templates/` must be bundled as data files (PyInstaller `--add-data`)
- Path handling: use `sys._MEIPASS` when frozen, `Path(__file__).parent` otherwise — apply this pattern wherever `base_dir` is used in `main.py`
- Ship as: executable + `my_data.csv.example` (user renames to `my_data.csv`) + short README
- Target platforms: macOS (`.app`) first, Windows (`.exe`) later

---

## How to Help the User

### When They Return to Work

1. **Check their question/task** - What phase are they working on?
2. **Reference PROJECT_PLAN.md** - Is this in the plan?
3. **Check DECISIONS.md** - Has this been decided?
4. **Provide concrete code** - They want to build, not just discuss
5. **Be concise** - No long preambles

### Common Scenarios

**"Help me implement scraping"**:
- Ask what they've tried (if anything)
- Inspect therapie.de structure with them
- Provide working code example
- Explain key concepts concisely
- Test together

**"This isn't working"**:
- Check error message
- Verify therapie.de structure hasn't changed
- Try alternative approach (BeautifulSoup → Selenium)
- Debug step by step

**"Should I do X or Y?"**:
- Check if DECISIONS.md addresses it
- If decided: remind them of decision and rationale
- If not decided: discuss briefly, make recommendation, document decision

**"How do I...?"** (technical question):
- Answer directly with code example
- Brief explanation of why/how
- Link to docs if needed

### Code Review Requests
- Check against project principles (simple, MVP-first)
- Verify rate limiting is present
- Check error handling
- Suggest improvements concisely

### Testing Help
- Provide test commands
- Help debug issues
- Verify output format matches expectations

---

## Important Constraints & Principles

### Must Follow:
- ✅ Respect robots.txt
- ✅ Rate limiting (2-3 min between emails, 2-3 sec between scraping requests)
- ✅ No persistent database of therapists
- ✅ Prepared to take down if therapie.de objects
- ✅ Document legal/ethical basis clearly

### Development Principles:
- **MVP first**: Terminal tool before GUI
- **Simple over complex**: JSON over database, BeautifulSoup before Selenium
- **Test as you go**: Manual testing is fine
- **Document decisions**: Update DECISIONS.md when making new choices
- **Commit regularly**: Git history helps track progress

### Don't:
- ❌ Over-engineer (keep it simple for MVP)
- ❌ Skip rate limiting (legal/ethical requirement)
- ❌ Build features not in the plan without discussing
- ❌ Assume decisions - check DECISIONS.md first

---

## Helping with Phase 1 (Scraping) - Most Likely Next Task

### Key Questions to Answer:
1. What's the search URL structure?
2. Is it GET or POST request?
3. What are the form parameters? (city, insurance type, "Freie Plätze")
4. Does it use JavaScript rendering? (affects tool choice)
5. What's the HTML structure of results?
6. Where are emails displayed? (directly in results or need to click through?)
7. How many results per page? Pagination?

### Approach:
1. Visit therapie.de together (via WebFetch or user shares screenshots)
2. Inspect the search form and results
3. Start with simple requests + BeautifulSoup
4. If that fails, switch to Selenium
5. Build incrementally: first get ANY data, then refine
6. Add error handling once basic scraping works

### Success Criteria:
- Can search with parameters
- Extracts list of therapists
- Gets name, email (critical), wait time
- Handles missing emails gracefully
- Respects rate limits
- Outputs clean JSON

---

## Legal Defense Summary (If Asked)

**Primary arguments**:
1. BPtK (official chamber) recommends this exact process
2. §13 Abs. 3 SGB V legally mandates this documentation
3. Public health benefit (mental health crisis)
4. No commercial use (personal healthcare access)
5. Published contact info (therapists listed to be contacted)
6. Good faith implementation (rate limits, compliance ready)

**If therapie.de objects**:
- Comply immediately
- Respond professionally
- Frame as healthcare access tool
- Cite BPtK endorsement
- Offer to discuss modifications

---

## File Reading Priority (For Context)

When the user asks for help, read these in order if needed:

1. **DECISIONS.md** - Check if question is already answered
2. **PROJECT_PLAN.md** - Understand what phase they're in
3. **Their code file** (if they've started coding)
4. **SETUP.md** - If they're having environment issues

Only read BPtK PDF if needed for specific Kostenerstattung questions.

---

## Useful Commands for Helping

```bash
# Check project status
ls -la /Users/sasan/spicy_projects/busy_therapists/

# See what's been implemented
find /Users/sasan/spicy_projects/busy_therapists/src/ -name "*.py"

# Check their current git state
cd /Users/sasan/spicy_projects/busy_therapists && git status

# Test their scraper
python /Users/sasan/spicy_projects/busy_therapists/src/scraper.py --city Berlin
```

---

## Common Issues & Solutions

### "Scraping returns nothing"
- Check if therapie.de structure changed
- Verify CSS selectors/XPath
- Check if JavaScript rendering needed (use Selenium)
- Inspect actual HTML vs. expected

### "Getting blocked / 403 errors"
- Add delays between requests
- Add User-Agent header
- Check robots.txt compliance
- Consider using Selenium (looks more like real browser)

### "Can't find emails"
- Emails might be in separate detail pages (need two-step scraping)
- Emails might be obfuscated (check HTML carefully)
- Not all therapists have emails (filter appropriately)

### "Dependencies won't install"
- Check Python version (needs 3.8+)
- Use venv (isolation)
- On M2 Mac: might need `arch -arm64 pip install`

---

## Success Metrics

### MVP is successful when:
- ✅ Can scrape 30+ therapists with emails from therapie.de
- ✅ Can generate personalized email templates
- ✅ Can produce proper Kostenerstattung protocol
- ✅ Can send batch emails with delays
- ✅ Documentation is clear and professional

### Ready for portfolio when:
- ✅ All MVP features work reliably
- ✅ README is polished
- ✅ Code is clean (formatted, commented where needed)
- ✅ Has been tested with real searches
- ✅ Legal/ethical basis is well-documented

---

## When in Doubt

1. **Check DECISIONS.md** - Is this already decided?
2. **Reference PROJECT_PLAN.md** - Is this in scope?
3. **Keep it simple** - MVP first, polish later
4. **Be pragmatic** - User wants working code, not perfect code
5. **Stay ethical** - Healthcare access, good faith, rate limits

---

## Final Notes

- This is a **legitimate healthcare access tool**, not malicious scraping
- User is **acting in good faith** to solve a real problem
- **Legal foundation is strong** (BPtK endorsement, §13 Abs. 3 SGB V)
- **Goal is portfolio-worthy** code that helps people
- **If unclear, ask** the user rather than make assumptions

---

**Remember**: The user wants concise, actionable help. Provide code examples, not just explanations. Reference the plan documents, but don't repeat them unnecessarily. Be a pragmatic coding partner.

---

Last updated: 2026-04-04
