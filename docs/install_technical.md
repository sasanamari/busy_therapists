# Technical Install

> For users comfortable with the terminal and Python package management.

---

## Requirements

- Python 3.8+
- [conda](https://docs.conda.io/en/latest/miniconda.html) or [mamba](https://mamba.readthedocs.io/) for environment management

---

## Clone the repository

```bash
git clone https://github.com/sasanamari/busy_therapists.git
cd busy_therapists
```

---

## Set up the environment

```bash
conda create -n busy_therapists python=3.11
conda activate busy_therapists
pip install -r requirements.txt
```

---

## Configure your data

```bash
cp my_data.csv.example my_data.csv
```

Open `my_data.csv` in Excel, Numbers, or any text editor and fill in the **Your data** column. If there is a `my_data.numbers`, the program reads that instead of `my_data.csv` for ease of use in macos.
See [my_data.csv reference](my_data_reference.md) for a field-by-field explanation.

---

## Run the tool

```bash
conda activate busy_therapists
python main.py
```

You'll see a numbered menu — choose the option that matches your current step. The [step-by-step guide](guide.md) explains which option to use and when.

---

## Output files

All generated files go into the `output/` folder:

| File | What it is |
|---|---|
| `busy_therapists.csv` | Therapists contacted for general outreach (options 1 & 4) |
| `probationary_therapists.csv` | Therapists contacted for probationary sessions (option 3) |
| `private_therapists.csv` | Private therapists contacted for Kostenerstattung (option 2) |
| `contact_log.pdf` | Formatted PDF of your contact log, generated when you run option 5 — attach this to your insurance application |
| `emails.html` | Your generated emails — open in a browser to send |
| `therapists.txt` | Human-readable list of therapists found in the most recent scraper run |

Each CSV **appends** new results on every run — useful if you're building up your contact list over multiple sessions. The tool will warn you if a CSV already exists before running.

**If you want a fresh start:** Delete the relevant CSV from `output/` before running. The next run will create a new one.
