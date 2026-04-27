#!/bin/bash
# Build the macOS Apple Silicon (arm64) installer.
#
# Requirements:
#   - conda/mamba installed
#   - busy_therapists conda environment exists (see README for setup)
#
# Output: TherapyFinder_macOS_arm64.zip in the project root
#
# Usage:
#   chmod +x scripts/build_arm_mac.sh   (first time only)
#   ./scripts/build_arm_mac.sh

set -e  # stop on any error

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DIST_DIR="$PROJECT_DIR/dist"

echo "==> Building arm64 app with PyInstaller..."
mamba run -n busy_therapists pyinstaller "$PROJECT_DIR/busy_therapists.spec" --clean -y \
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
zip -r "$PROJECT_DIR/TherapyFinder_macOS_arm64.zip" \
    busy_therapists.app \
    "Run Therapy Finder.command" \
    my_data.csv.example

echo ""
echo "Done! Output: TherapyFinder_macOS_arm64.zip"
