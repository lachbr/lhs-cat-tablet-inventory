Name "Tablet Inventory 2020"

OutFile "tablet_inventory_installer.exe"

InstallDir "$PROGRAMFILES\Lakewood High School CAT\Tablet Inventory 2020"

RequestExecutionLevel admin

Section
    SetShellVarContext all
	SetOutPath $INSTDIR
	WriteUninstaller "$INSTDIR\uninstall.exe"
	File "built_client\client.exe"
	File "built_client\client_updater.exe"
	File "built_netclient\netclient.exe"
	File "built_netclient\netclient_updater.exe"
	
	CreateShortCut "$DESKTOP\Tablet Inventory - Net Assistants.lnk" "$INSTDIR\netclient_updater.exe"
	CreateShortCut "$DESKTOP\Tablet Inventory - Students.lnk" "$INSTDIR\client_updater.exe"
SectionEnd

Section "uninstall"
	SetShellVarContext all
	Delete "$INSTDIR\client.exe"
	Delete "$INSTDIR\client_updater.exe"
	Delete "$INSTDIR\netclient.exe"
	Delete "$INSTDIR\netclient_updater.exe"
	Delete "$INSTDIR\uninstall.exe"
	Delete "$DESKTOP\Tablet Inventory - Net Assistants.lnk"
	Delete "$DESKTOP\Tablet Inventory - Students.lnk"
SectionEnd