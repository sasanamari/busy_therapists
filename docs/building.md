# Building installers

This document explains how to build the installable app for each platform after making code changes.

---

## macOS Apple Silicon (arm64)

Run on your M-chip Mac:

```bash
chmod +x scripts/build_arm_mac.sh   # first time only
./scripts/build_arm_mac.sh
```

Output: `TherapyFinder_macOS_arm64.zip` in the project root.

**Requirements:** `busy_therapists` conda environment (see [install_technical.md](install_technical.md)).

---

## macOS Intel (x86_64)

Run on your M-chip Mac using Rosetta 2 emulation:

```bash
chmod +x scripts/build_intel_mac.sh   # first time only
./scripts/build_intel_mac.sh
```

Output: `TherapyFinder_macOS_intel.zip` in the project root.

**First-time environment setup (run once):**
```bash
CONDA_SUBDIR=osx-64 mamba create -n busy_therapists_intel python=3.11 -y
mamba run -n busy_therapists_intel conda config --env --set subdir osx-64
mamba run -n busy_therapists_intel pip install -r requirements.txt pyinstaller
```

---

## Windows

Triggered manually via GitHub Actions (no Windows machine needed):

1. Go to the repo on GitHub → **Actions** tab → **Build Windows installer**
2. Click **Run workflow**
3. Wait for it to finish (~5 minutes)
4. Download the `TherapyFinder_Windows` artifact from the completed run

The downloaded zip contains `busy_therapists/`, `Run Therapy Finder.bat`, and `my_data.csv.example` — ready to upload to a release.

---

## Uploading to a GitHub release

After building all three platforms:

1. Go to the repo → **Releases** → edit the existing release (or create a new one)
2. Upload the three zip files:
   - `TherapyFinder_macOS_arm64.zip`
   - `TherapyFinder_macOS_intel.zip`
   - `TherapyFinder_Windows.zip` (downloaded from GitHub Actions artifacts)
3. Update the release notes if needed
