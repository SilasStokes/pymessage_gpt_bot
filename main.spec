# -*- mode: python ; coding: utf-8 -*-


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

MERGE( (main_analysis, 'main', 'main'), (menubar_analysis, 'menubar', 'menubar'))

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
    console=True,
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
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

main_coll = COLLECT(
    main_exe,
    main_analysis.binaries,
    main_analysis.datas,
    menubar_exe,
    menubar_analysis.binaries,
    menubar_analysis.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
