import PyInstaller.__main__

options = [
    '--onefile',
    '--strip',
    '--windowed',
    'WPassGen.pyw'
]

PyInstaller.__main__.run(options)