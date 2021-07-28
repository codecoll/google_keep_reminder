rem this script is needed so the scheduled script runs without a window

Dim WinScriptHost
Set WinScriptHost = CreateObject("WScript.Shell")
WinScriptHost.Run Chr(34) & "tasks.bat" & Chr(34), 0
Set WinScriptHost = Nothing
