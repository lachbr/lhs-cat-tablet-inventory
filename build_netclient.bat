pyinstaller --onefile --icon=icon.ico --distpath built_netclient --name netclient_updater src\netclient_updater\main.py
pyinstaller --onefile --icon=icon.ico --distpath built_netclient --name netclient src\netclient\main.py
pause