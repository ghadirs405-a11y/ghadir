#!/usr/bin/env bash
# git_sync.sh — قانون اصلی پروژه (MAIN RULE)
# بعد از هر بار تکمیل کد یا رفع اشکال این اسکریپت اجرا می‌شود تا کد به GitHub سینک شود.
# Usage: bash /home/z/my-project/scripts/git_sync.sh "commit message"
set -e
cd /home/z/my-project

MSG="${1:-chore: sync updates}"

git add .
if git diff --cached --quiet; then
  echo "nothing to commit"
else
  git commit -m "$MSG"
fi

git push origin main && echo "SYNCED -> origin/main OK"
