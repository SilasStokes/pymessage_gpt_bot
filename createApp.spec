# -*- mode: python ; coding: utf-8 -*-

OUTPUT_NAME = "GPT iMessage Bot"
icon = './assets/speech_bubble.icns'
DEBUG = True

bot_analysis = Analysis(
    ['bot.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('README.md', './assets/'),
        ('configs/config.json', './assets/'),
        ('assets/instructions.txt', './assets/'),
        ('assets/send-imessage.shortcut', './assets/'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

menubar_analysis = Analysis(
    ['menubar.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

error_popup_analysis = Analysis(
    ['error_popup.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

MERGE( (menubar_analysis, 'menubar', 'menubar'), (bot_analysis, 'bot', 'bot'), (error_popup_analysis, 'error_popup', 'error_popup'))

bot_pyz = PYZ(bot_analysis.pure)
menubar_pyz = PYZ(menubar_analysis.pure)
error_popup_pyz = PYZ(error_popup_analysis.pure)

bot_exe = EXE(
    bot_pyz,
    bot_analysis.scripts,
    [],
    exclude_binaries=True,
    name='bot',
    debug=DEBUG,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True, # try changing me
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

menubar_exe = EXE(
    menubar_pyz,
    menubar_analysis.scripts,
    [],
    exclude_binaries=True,
    name='menubar',
    debug=DEBUG,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    # console=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
error_popup_exe = EXE(
    error_popup_pyz,
    error_popup_analysis.scripts,
    [],
    exclude_binaries=True,
    name='error_popup',
    debug=DEBUG,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    # console=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

bot_coll = COLLECT(
    menubar_exe,
    menubar_analysis.binaries,
    menubar_analysis.datas,
    bot_exe,
    bot_analysis.binaries,
    bot_analysis.datas,
    error_popup_exe,
    error_popup_analysis.binaries,
    error_popup_analysis.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=OUTPUT_NAME,
)

# from: https://github.com/pyinstaller/pyinstaller/pull/3566
# Without Info.plist: display normally with icon in the Dock.
# With Info.plist LSUIElement=True: display normally with no icon in the Dock.
# With Info.plist LSBackgroundOnly=True: no display nor icon in the Dock.

info_plist = {
    # "LSUIElement" : True,
    "LSBackgroundOnly" : True
}
app = BUNDLE(
    bot_coll,
    info_plist=info_plist,
    name='GPT iMessage Bot.app',
    icon=icon,
    bundle_identifier=None,
)