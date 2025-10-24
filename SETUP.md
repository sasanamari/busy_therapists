# Getting Started with Therapy Finder

This guide helps you set up your development environment and start working on the project.

## Quick Start (When You Return)

1. **Review context**:
   ```bash
   cd /Users/sasan/spicy_projects/busy_therapists
   cat PROJECT_PLAN.md    # Implementation roadmap
   cat DECISIONS.md       # What's been decided
   ```

2. **Activate your Python environment** (or create one):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies** (when requirements.txt is populated):
   ```bash
   pip install -r requirements.txt
   ```

4. **Start with Phase 1** (Scraping):
   - Read PROJECT_PLAN.md Phase 1 section
   - Visit therapie.de and explore the search functionality
   - Start implementing `src/scraper.py`

---

## Python Environment Setup

### Option 1: Virtual Environment (Recommended)
```bash
cd /Users/sasan/spicy_projects/busy_therapists
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
pip install --upgrade pip
```

### Option 2: Conda
```bash
conda create -n therapy_finder python=3.10
conda activate therapy_finder
```

---

## Dependencies (To Be Installed)

### Phase 1 (Scraping):
```bash
pip install requests beautifulsoup4 lxml
```

**If BeautifulSoup doesn't work** (site uses JavaScript):
```bash
pip install selenium webdriver-manager
```

### Phase 2-3 (Templates & Protocol):
```bash
# No additional dependencies (uses standard library)
```

### Phase 5 (Email Sending):
```bash
# TBD - depends on email method chosen
# Likely: pip install secure-smtplib
```

### Development tools:
```bash
pip install pytest black flake8  # Testing and code quality
```

---

## Project Structure Overview

```
busy_therapists/
├── src/                    # Your Python code goes here
│   ├── scraper.py         # START HERE - Phase 1
│   ├── email_templates.py # Phase 2
│   ├── protocol_generator.py  # Phase 3
│   ├── email_sender.py    # Phase 5
│   └── config.py          # Configuration constants
│
├── templates/             # Email templates (text files)
│   ├── therapy_request.txt
│   └── kostenerstattung.txt
│
├── docs/                  # Reference documents
│   └── BPtK_Ratgeber_Kostenerstattung.pdf
│
├── data/                  # Runtime data (gitignored)
│   ├── therapists.json    # Scraped data
│   ├── emails.json        # Generated emails
│   └── responses.json     # Response tracking
│
├── tests/                 # Unit tests (optional for MVP)
│
├── main.py               # CLI entry point (create in Phase 5)
├── user_config.json      # Your personal info (gitignored)
├── requirements.txt      # Python dependencies
└── .gitignore           # Git ignore rules
```

---

## Development Workflow

### 1. Before Each Session
```bash
cd /Users/sasan/spicy_projects/busy_therapists
source venv/bin/activate  # If using venv
git status                # Check what's changed
```

### 2. During Development
- **Read relevant section** of PROJECT_PLAN.md
- **Check DECISIONS.md** for context on choices made
- **Implement feature** in appropriate file
- **Test manually** as you go
- **Update PROJECT_PLAN.md** checkboxes as you complete tasks

### 3. After Each Session
```bash
git add .
git commit -m "Descriptive message of what you implemented"
```

### 4. If You Need Help from Claude
- Share the relevant file (e.g., `scraper.py`)
- Reference CONTEXT_FOR_CLAUDE.md for full project context
- Mention which phase/task you're working on

---

## Testing Your Work

### Phase 1 (Scraping):
```bash
python src/scraper.py --city Berlin --insurance gesetzlich --free-slots
# Should output JSON of therapists
```

### Phase 2 (Templates):
```bash
python src/email_templates.py --therapists data/therapists.json --user-config user_config.json
# Should output personalized emails
```

### Phase 3 (Protocol):
```bash
python src/protocol_generator.py --therapists data/therapists.json
# Should output formatted protocol
```

---

## Troubleshooting

### "Module not found" error
```bash
pip install <module_name>
# Or check if venv is activated
```

### Scraping doesn't work
- Check if therapie.de structure changed (inspect HTML)
- Try Selenium instead of BeautifulSoup
- Check robots.txt: `curl https://www.therapie.de/robots.txt`

### Git not initialized
```bash
git init
git add .
git commit -m "Initial commit"
```

---

## Git Setup (When Ready)

### Initialize repository:
```bash
cd /Users/sasan/spicy_projects/busy_therapists
git init
git add .
git commit -m "Initial project setup"
```

### Create GitHub repo (when ready to publish):
```bash
# Create repo on GitHub first, then:
git remote add origin https://github.com/yourusername/busy_therapists.git
git branch -M main
git push -u origin main
```

**IMPORTANT**: Before pushing, decide whether to acknowledge therapie.de in README (see DECISIONS.md)

---

## Configuration Files

### user_config.json (Create this when needed)
```json
{
  "name": "Your Name",
  "insurance": "gesetzlich",
  "insurance_company": "TK",
  "city": "Berlin",
  "plz": "10115",
  "symptoms": "depression, anxiety",
  "previous_diagnosis": "",
  "email": "your.email@example.com"
}
```

**Add to .gitignore** (contains personal info)

---

## When You're Stuck

1. **Read PROJECT_PLAN.md** - Step-by-step guidance
2. **Read DECISIONS.md** - Context on why choices were made
3. **Read CONTEXT_FOR_CLAUDE.md** - Full project context for asking AI
4. **Check docs/BPtK_Ratgeber_Kostenerstattung.pdf** - Official requirements
5. **Ask Claude** - Share relevant files and context

---

## Next Steps After Setup

**Your first task**: Implement Phase 1 (Scraping)

1. Visit https://www.therapie.de/psychotherapie-psychologen/
2. Explore the search form
3. Inspect the HTML structure
4. Start coding `src/scraper.py`

See PROJECT_PLAN.md → Phase 1 for detailed tasks.

---

## Useful Commands

```bash
# Check Python version
python3 --version

# List installed packages
pip list

# Freeze dependencies (after installing)
pip freeze > requirements.txt

# Format code (if black installed)
black src/

# Run tests (if pytest installed)
pytest tests/

# View file structure
tree -L 2  # or: ls -R
```

---

## Resources

- **BPtK Guide**: `docs/BPtK_Ratgeber_Kostenerstattung.pdf`
- **therapie.de**: https://www.therapie.de
- **Legal basis**: §13 Absatz 3 SGB V
- **robots.txt**: https://www.therapie.de/robots.txt

---

## Notes for macOS (Your M2 MacBook)

- Use `python3` not `python` (macOS default Python is old)
- Use `pip3` if `pip` doesn't work
- Virtual env activation: `source venv/bin/activate`
- You're on Apple Silicon (M2) - most packages work fine, but if you see architecture errors, try:
  ```bash
  arch -arm64 pip install <package>
  ```

---

## Project Philosophy

**Remember**:
- Build MVP first, polish later
- Terminal tool before GUI
- Manual testing is fine for MVP
- Commit often
- Document as you go
- If therapie.de objects, comply immediately

---

Good luck! Start with Phase 1 (scraping) and work through the plan step by step.
