#!/bin/sh

# References
# stolen from https://gist.github.com/Kvnbbg/84871ae4d642c2dd896e0423471b1b52
# https://www.pythonguis.com/tutorials/packaging-pyqt5-applications-pyinstaller-macos-dmg/
# https://medium.com/@jackhuang.wz/in-just-two-steps-you-can-turn-a-python-script-into-a-macos-application-installer-6e21bce2ee71

# ---------------------------------------
# Clean up previous builds
# ---------------------------------------

echo "Cleaning up previous builds..."
# rm -rf build dist/*

SPEC_FILE="main.spec"
APP_NAME="main.app"
APP_INSTALLER_NAME="GPT iMessage Bot"

# ---------------------------------------
# Step 1: Convert Python script to an application bundle
# ---------------------------------------
# echo "Converting Python script to macOS app bundle..."
# The following command will create a standalone .app from your Python script
# pyinstaller ${SPEC_FILE}

# ---------------------------------------
# Step 2: Convert the application bundle to a DMG (macOS disk image)
# ---------------------------------------
echo "Creating DMG installer..."

# Prepare the folder for DMG creation
mkdir -p dist/dmg
rm -rf dist/dmg/*
cp -r "dist/${APP_NAME}" dist/dmg

# Create the DMG
# Ensure you have 'create-dmg' installed. If not, install using 'brew install create-dmg'
create-dmg \
    --volname "GPT iMessage Bot" \
    --volicon "speech_bubble.ico" \
    --window-pos 200 120 \
    --window-size 600 300 \
    --icon-size 100 \
    --app-drop-link 425 120 \
    "./dist/GPT iMessage Bot.dmg" \
    ./dist/dmg/
# --hide-extension "main.app" \
# --icon "CryptoSafePDF.app" 175 120 \

# echo "Packaging complete. You can find the DMG installer in the dist/ directory."
