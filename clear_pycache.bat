echo off
set foldername=__pycache__
FOR /d /r . %%d IN (%foldername%) DO @IF EXIST "%%d" echo %%d
FOR /d /r . %%d IN (%foldername%) DO @IF EXIST "%%d" rd /s /q %%d
pause