#!/usr/bin/env bash
# Task G1: prepare clean git history for GitHub sync
# - sets proper git identity
# - backs up old history to backup/old-main
# - rebuilds history as ONE clean root commit WITHOUT android/sdk (250MB) and .env
set -e
cd /home/z/my-project

echo "[1/5] git identity..."
git config user.name "Ghadir Sarvari"
git config user.email "347114323+ghadirs405-a11y@users.noreply.github.com"

echo "[2/5] backup old history..."
OLD_TIP="8ded8df5b26ac89886849b89bdc94097432ddde4"
git branch -f backup/old-main "$OLD_TIP"
echo "  old main tip: $OLD_TIP"

echo "[3/5] fresh orphan history (drops android/sdk blobs)..."
git checkout -q --orphan fresh-main
git reset -q 2>/dev/null || git rm -r -q --cached .
git add .
git commit -q -m "Habits Tracker - full project sync (PWA app, Android APK source, scripts, all APK versions)

- Persian RTL single-page habit tracker: public/app.html
- Android WebView APK build pipeline: android/apk-src (SDK excluded)
- Build/patch scripts and backups: scripts/
- Released APKs: download/ (v2, v3, v4)
- User assets: upload/
Developer: Ghadir Sarvari"

echo "[4/5] rename to main..."
git branch -M fresh-main main

echo "[5/5] verify..."
echo "files tracked: $(git ls-files | wc -l)"
echo "sdk tracked:   $(git ls-files android/sdk | wc -l)"
echo "env tracked:   $(git ls-files .env | wc -l)"
git count-objects -vH | grep size-pack || true
echo "--- last commits ---"
git log --oneline
