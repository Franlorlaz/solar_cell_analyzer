Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c run_script.bat"
oShell.Run strArgs, 0, false
