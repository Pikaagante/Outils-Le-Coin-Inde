from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules("outils")

a = Analysis(
    ["app.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("templates", "templates"),
        ("static", "static"),
        ("outils", "outils"),
    ],
    hiddenimports=hiddenimports,
    excludes=[],
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name="ImageIndie",
    console=True
)