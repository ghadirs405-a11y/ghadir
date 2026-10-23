#!/bin/bash
# Task 16: build signed APK v3 (aapt2 -> ECJ -> d8 -> package -> zipalign -> apksigner)
set -e
SDK=/home/z/my-project/android/sdk
BT=$SDK/build-tools/34.0.0
PLAT=$SDK/platforms/android-34/android.jar
SRC=/home/z/my-project/android/apk-src
OUT=/home/z/my-project/android/build
KS=/home/z/my-project/android/debug.keystore

rm -rf $OUT
mkdir -p $OUT/compiled $OUT/gen $OUT/obj $OUT/dex

echo "== 1. aapt2 compile =="
$BT/aapt2 compile --dir $SRC/res -o $OUT/compiled/res.zip

echo "== 2. aapt2 link =="
$BT/aapt2 link -o $OUT/base.apk -I $PLAT --manifest $SRC/AndroidManifest.xml \
  -A $SRC/assets --java $OUT/gen $OUT/compiled/res.zip --auto-add-overlay

echo "== 3. ECJ compile =="
java -jar $SDK/ecj.jar -nowarn -source 1.8 -target 1.8 -encoding UTF-8 \
  -cp $PLAT -d $OUT/obj \
  $SRC/src/com/habits/tracker/MainActivity.java \
  $OUT/gen/com/habits/tracker/R.java
ls $OUT/obj/com/habits/tracker/

echo "== 4. d8 dex =="
$BT/d8 --release --lib $PLAT --min-api 24 --output $OUT/dex $OUT/obj/com/habits/tracker/*.class

echo "== 5. package dex =="
(cd $OUT/dex && zip -q $OUT/base.apk classes.dex)

echo "== 6. zipalign =="
$BT/zipalign -f 4 $OUT/base.apk $OUT/aligned.apk

echo "== 7. keystore + sign =="
if [ ! -f $KS ]; then
  keytool -genkeypair -keystore $KS -alias androiddebugkey -storepass android -keypass android \
    -dname "CN=Habit Tracker Debug,O=Habits,C=IR" -keyalg RSA -keysize 2048 -validity 10000
fi
$BT/apksigner sign --ks $KS --ks-pass pass:android --key-pass pass:android \
  --out /home/z/my-project/download/habits-tracker-v3.apk $OUT/aligned.apk

echo "== 8. verify =="
$BT/apksigner verify --print-certs /home/z/my-project/download/habits-tracker-v3.apk | head -4
$BT/aapt2 dump badging /home/z/my-project/download/habits-tracker-v3.apk | head -3
ls -la /home/z/my-project/download/habits-tracker-v3.apk
echo "BUILD OK"
