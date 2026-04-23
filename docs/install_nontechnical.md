# Getting Started (No coding required)

> You don't need to install Python or use a terminal. Just download the app, fill in one file, and double-click to run.
>
> **This app currently runs on macOS (Apple Silicon only — M1, M2, M3 etc chips). Windows and Intel Mac support is planned.**

---

## Step 1: Download the app

1. Go to the [latest release on GitHub](https://github.com/sasanamari/busy_therapists/releases/latest)
2. Download `TherapyFinder_macOS.zip`
3. Double-click the zip file to unzip it — a folder called `busy_therapists` will appear
4. Move that folder somewhere convenient, like your Desktop or Documents

---

## Step 2: Set up your data file

The tool reads your personal details from a file called `my_data.csv` (or `my_data.numbers`). A template is included in the download.

1. Open the `busy_therapists` folder — you should see these files:

   ![Folder contents showing busy_therapists folder, busy_therapists.app, my_data.csv, and Run Therapy Finder.command](screenshots/01_folder_contents.png)

2. Make a copy of `my_data.csv.example` and rename the copy to `my_data.csv`
   - **How to copy on Mac:** right-click the file → Duplicate, then rename it
   - The file must be named exactly `my_data.csv` — the tool won't find it otherwise

3. Open your `my_data.csv`:
   - **Easiest option:** double-click — it opens in Numbers. Numbers will save it automatically in its own format, and the tool will still find it. No need to export back to CSV.
   - **Alternatively:** right-click → Open With → Excel or Google Sheets

4. Fill in the **Your data** column. The **Notes** column explains each field. You don't need to fill everything in right away — come back and update it as you progress through the process.

5. Save the file (Cmd+S, or just close Numbers — it saves automatically).

For a full explanation of every field, see the [my_data.csv reference](my_data_reference.md).

> `my_data.csv` stays on your computer — it is never uploaded anywhere.

---

## Step 3: Run the tool

Double-click `Run Therapy Finder.command`.

**The first time you run it, macOS will block it** — this is normal for apps downloaded from the internet that aren't from the App Store.

### One-time security approval (macOS only)

**1.** When you double-click `Run Therapy Finder.command`, you'll see this warning:

![macOS warning: "Run Therapy Finder.command" Not Opened](screenshots/02_security_warning.png)

Click **Done** (not "Move to Trash").

---

**2.** Open **System Settings** → **Privacy & Security**. Scroll down to the **Security** section. You'll see a message saying the file was blocked, with an **Open Anyway** button next to it:

![Privacy & Security settings showing "Open Anyway" button](screenshots/03_privacy_and_security.png)

Click **Open Anyway**.

---

**3.** A second confirmation dialog will appear:

![Second confirmation dialog with "Open Anyway" button](screenshots/04_open_anyway.png)

Click **Open Anyway** again.

---

**4.** You'll be asked to confirm with your password or Touch ID:

![Password/Touch ID prompt](screenshots/05_password_prompt.png)

Use Touch ID or click **Use Password...** and enter your Mac login password.

---

**That's it — you only need to do this once.** After the first approval, double-clicking `Run Therapy Finder.command` will launch the tool directly.

---

## Step 4: Use the tool

A terminal window opens and the tool loads your data, then shows a numbered menu:

![App running showing the numbered menu](screenshots/06_app_running.png)

Type a number and press Enter to run that option. Read the [step-by-step guide](guide.md) to understand which option to use and when.

When the tool finishes, the terminal window stays open showing `[Process completed]`. You can close it with **Cmd+W**.

---

## Output files

After the first run, a folder called `output/` will appear next to the app. The tool manages this automatically — you don't need to touch it to follow the guide.

**If you want to start fresh:** delete the relevant file from `output/` before running the tool again. The next run will create a new one. (For example, if you ran option 4 with the wrong filters, delete `output/busy_therapists.csv` and run again.)

For reference, here's what each file is:

| File | What it is |
|---|---|
| `busy_therapists.csv` | Therapists contacted for general outreach (options 1 & 4) |
| `probationary_therapists.csv` | Therapists contacted for probationary sessions (option 3) |
| `private_therapists.csv` | Private therapists contacted for Kostenerstattung (option 2) |
| `contact_log.pdf` | Formatted PDF of your contact log, generated when you run option 5 — attach this to your insurance application |
| `emails.html` | Your generated emails — open in a browser to send |
| `therapists.txt` | Human-readable list of therapists found in the most recent scraper run |

Each CSV **appends** new results on every run — useful if you're building up your contact list over multiple sessions.
