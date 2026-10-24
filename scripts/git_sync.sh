#!/usr/bin/env bash
# git_sync.sh — قانون اصلی پروژه (MAIN RULE)
# بعد از هر بار تکمیل کد یا رفع اشکال این اسکریپت اجرا می‌شود تا کد به GitHub سینک شود.
# Usage: bash /home/z/my-project/scripts/git_sync.sh "commit message"
cd /home/z/my-project

MSG="${1:-chore: sync updates}"

git add .
if git diff --cached --quiet; then
  echo "nothing to commit"
else
  git commit -m "$MSG"
fi

RC=0
if git push origin main 2>&1; then
  echo "SYNCED -> ghadir23 (origin) OK"
else
  echo "PUSH FAILED -> ghadir23 (origin)"; RC=1
fi
if git push ghadir main 2>&1; then
  echo "SYNCED -> ghadir OK"
else
  echo "PUSH FAILED -> ghadir"; RC=1
fi
exit $RC
