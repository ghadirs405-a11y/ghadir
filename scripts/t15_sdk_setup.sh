#!/bin/bash
# Task 15: Re-download Android SDK (env was reset) - build-tools 34, platform 34, ECJ
set -x
SDK=/home/z/my-project/android/sdk
mkdir -p $SDK/cmdline-tools
cd $SDK

# 1. cmdline-tools
if [ ! -f $SDK/cmdline-tools/latest/bin/sdkmanager ]; then
  curl -sSL -o /tmp/clt.zip https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip
  unzip -q /tmp/clt.zip -d $SDK/cmdline-tools
  mv $SDK/cmdline-tools/cmdline-tools $SDK/cmdline-tools/latest
fi

# 2. Accept licenses + install build-tools & platform
yes | $SDK/cmdline-tools/latest/bin/sdkmanager --sdk_root=$SDK --licenses > /dev/null 2>&1
$SDK/cmdline-tools/latest/bin/sdkmanager --sdk_root=$SDK "build-tools;34.0.0" "platforms;android-34" > /tmp/sdk_install.log 2>&1

# 3. ECJ compiler (no javac on this box - JRE only)
curl -sSL -o $SDK/ecj.jar https://repo1.maven.org/maven2/org/eclipse/jdt/ecj/3.36.0/ecj-3.36.0.jar

echo "=== DONE ==="
ls $SDK/build-tools/34.0.0/ | head -5
ls $SDK/platforms/android-34/android.jar
ls -la $SDK/ecj.jar
