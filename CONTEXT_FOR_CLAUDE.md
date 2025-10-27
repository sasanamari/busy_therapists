# Context for Claude Code (AI Assistant Instructions)

**READ THIS FIRST** when helping with this project.

---

## 🔴 KNOWN ISSUES (Session 2025-10-27)

**Email decoder bugs found during testing:**
1. **'-' character decodes incorrectly to '.'**
   - Example: `m.brockmeyer-psychotherapie@outlook.de` decoded as `m.brockmeyer.psychotherapie@outlook.de`
2. **'8' character decodes incorrectly to '7'**
   - Example: `LPJ77@gmx.de` decoded as `LPJ88@gmx.de`
3. **Investigation needed:** The decoding algorithm may have issues with numbers and special characters beyond just letters

**Other issues to fix:**
- Duplicate therapists appearing across pagination (same therapists on pages 1 and 2)
- Need retry logic for 429 Too Many Requests errors

**Current workaround:** Rate limiting increased to 2.5s to reduce 429 errors

---

## Project Summary

**Name**: Therapy Finder for Kostenerstattung
**Purpose**: Automate the bureaucratic process of finding therapists and documenting contacts for German health insurance cost reimbursement (Kostenerstattung)
**Status**: Early development / MVP phase
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

**The problem**: Step 2 is tedious, requiring dozens of phone calls/emails and manual documentation. This is especially difficult for people with mental health issues.

---

## The Solution

An automated Python tool that:
1. **Scrapes therapie.de** (only directory with "Freie Plätze" filter showing availability)
2. **Extracts therapist emails** (not all have email addresses)
3. **Generates personalized emails** from templates
4. **Sends batch emails with delays** (2-3 min between sends, respects servers)
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
To run Python code for this project, use the full path to the conda environment's Python:
```bash
/opt/homebrew/Caskroom/miniforge/base/envs/busy_therapists/bin/python <script.py>
```

**For user (manual terminal):**
```bash
conda activate busy_therapists
python <script.py>
```

**Dependencies:** Managed via `requirements.txt` (requests, beautifulsoup4, lxml)

### Current Decisions

**Language**: Python (user is comfortable with it)
**Interface**: Terminal/CLI first → GUI later
**Data format**: JSON files (simple, no database)
**Scraping**: requests + BeautifulSoup (start simple, use Selenium if needed)
**Email method**: TBD (after scraping works) - likely SMTP or OAuth

### Project Structure
```
busy_therapists/
├── src/
│   ├── scraper.py              # Phase 1: PRIORITY
│   ├── email_templates.py      # Phase 2
│   ├── protocol_generator.py   # Phase 3
│   ├── email_sender.py         # Phase 5
│   └── config.py               # Constants, rate limits
├── templates/
│   ├── therapy_request.txt     # Default email
│   └── kostenerstattung.txt    # Kostenerstattung-specific
├── docs/
│   └── BPtK_Ratgeber_Kostenerstattung.pdf  # Official guide
├── data/                        # Runtime (gitignored)
│   ├── therapists.json
│   ├── emails.json
│   └── responses.json
├── main.py                      # CLI entry point
├── user_config.json             # User's personal info (gitignored)
└── requirements.txt
```

### Development Phases (In Order)

**Phase 1**: Scraping (HIGHEST PRIORITY)
- Extract therapist data from therapie.de
- Focus on: name, email, wait time, specializations
- Handle pagination, missing fields
- **This is the foundation - nothing works without it**

**Phase 2**: Email Templates
- Template system with placeholders
- Personalization with user info
- User can customize

**Phase 3**: Protocol Generator
- Format data for insurance application
- Follow BPtK guidelines
- Export as text/PDF

**Phase 4**: Documentation
- README with legal basis
- Responsible use policy
- Installation guide

**Phase 5**: Email Sender (LOWEST PRIORITY)
- Batch sending with delays
- Manual response tracking
- **Note**: Email automation is least critical for MVP because user can copy-paste emails manually if needed

---

## Key Implementation Details

### Email Sending Flow
1. User clicks "Send All" (not 30 individual clicks)
2. App queues emails with 2-3 minute delays
3. Takes ~60-90 minutes for 30 emails
4. User can leave app running, walk away
5. Progress tracking shows status

**Rationale**: Balance between automation (useful) and rate limiting (respectful/legal)

### Rate Limiting
- **Scraping**: 2-3 seconds between requests
- **Email sending**: 2-3 minutes between emails
- **Built-in**: Not configurable by user (prevents abuse)

### Data Minimization
- No persistent therapist database
- Only store data for current session
- Don't republish therapie.de data
- User's personal data stays local

### Response Tracking
- **MVP**: Manual logging (user marks responses in JSON/CLI)
- **Future**: Gmail API integration (automated, but complex)

**Rationale**: Manual is simpler and privacy-respecting for MVP. Automated is nice showcase for portfolio.

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

✅ Project structure created
✅ Documentation written (PROJECT_PLAN.md, DECISIONS.md, SETUP.md)
✅ Development roadmap defined
✅ Legal/ethical analysis completed
✅ Technical decisions made

❌ No code written yet
❌ No dependencies installed yet
❌ Scraping not implemented
❌ No testing done

**Next step**: Implement Phase 1 (scraping)

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

Last updated: 2025-10-24
