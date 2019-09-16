pyinstaller --onefile --icon=icon.ico --distpath built_client --name client_updater src\client_updater\main.py
pyinstaller --onefile --icon=icon.ico --distpath built_client --name client src\client\main.py
pause