@echo off
cd .\
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%userprofile%\Desktop\SolarCellAnalyzer.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = ".\run_script.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = ".\" >> CreateShortcut.vbs
echo oLink.Description = "Solar Cell Analyzer" >> CreateShortcut.vbs
echo oLink.IconLocation = "D:\Proyectos\solar_cell_analyzer\src\interface\icon3_EcT_icon.ico" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs