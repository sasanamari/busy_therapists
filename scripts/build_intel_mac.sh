#!/bin/bash
# Build the macOS Intel (x86_64) installer using Rosetta 2 emulation.
# Runs on an Apple Silicon Mac — no Intel Mac needed.
#
# Requirements:
#   - conda/mamba installed
#   - Rosetta 2 installed (most M-chip Macs have it; if not: softwareupdate --install-rosetta)
#
# First-time setup (run once):
#   CONDA_SUBDIR=osx-64 mamba create -n busy_therapists_intel python=3.11 -y
#   mamba run -n busy_therapists_intel conda config --env --set subdir osx-64
#   mamba run -n busy_therapists_intel pip install -r requirements.txt pyinstaller
#
# Output: TherapyFinder_macOS_intel.zip in the project root
#
# Usage:
#   chmod +x scripts/build_intel_mac.sh   (first time only)
#   ./scripts/build_intel_mac.sh

set -e  # stop on any error

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DIST_DIR="$PROJECT_DIR/dist_intel"

echo "==> Building x86_64 app with PyInstaller (via Rosetta)..."
mamba run -n busy_therapists_intel pyinstaller "$PROJECT_DIR/busy_therapists.spec" --clean -y \
    --distpath "$DIST_DIR"

echo "==> Creating launcher script..."
cat > "$DIST_DIR/Run Therapy Finder.command" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
xattr -dr com.apple.quarantine "busy_therapists.app" 2>/dev/null
"busy_therapists.app/Contents/MacOS/busy_therapists"
EOF
chmod +x "$DIST_DIR/Run Therapy Finder.command"

echo "==> Copying example data file..."
cp "$PROJECT_DIR/my_data.csv.example" "$DIST_DIR/my_data.csv.example"

echo "==> Packaging zip..."
cd "$DIST_DIR"
zip -r "$PROJECT_DIR/TherapyFinder_macOS_intel.zip" \
    busy_therapists.app \
    "Run Therapy Finder.command" \
    my_data.csv.example

echo ""
echo "Done! Output: TherapyFinder_macOS_intel.zip"
