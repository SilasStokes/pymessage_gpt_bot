# -*- mode: python ; coding: utf-8 -*-

OUTPUT_NAME = "GPT iMessage Bot"
icon = 'speech_bubble.icns' 

main_analysis = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('README.md', '.'),
        ('configs/config.json', '.'),
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

MERGE( (menubar_analysis, 'menubar', 'menubar'), (main_analysis, 'main', 'main'))
# MERGE( (main_analysis, 'main', 'main'), (menubar_analysis, 'menubar', 'menubar'))

main_pyz = PYZ(main_analysis.pure)

main_exe = EXE(
    main_pyz,
    main_analysis.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=True,
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
menubar_pyz = PYZ(menubar_analysis.pure)

menubar_exe = EXE(
    menubar_pyz,
    menubar_analysis.scripts,
    [],
    exclude_binaries=True,
    name='menubar',
    debug=False,
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

main_coll = COLLECT(
    menubar_exe,
    menubar_analysis.binaries,
    menubar_analysis.datas,
    main_exe,
    main_analysis.binaries,
    main_analysis.datas,
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
    main_coll,
    info_plist=info_plist,
    name='GPT iMessage Bot.app',
    icon=icon,
    bundle_identifier=None,
)