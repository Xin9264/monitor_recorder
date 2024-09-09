@echo off

REM Check if keycastow.exe is running and terminate it if found
tasklist /FI "IMAGENAME eq keycastow.exe" 2>NUL | find /I "keycastow.exe" >NUL
if not errorlevel 1 (
    echo "keycastow.exe is running, terminating..."
    taskkill /F /IM keycastow.exe
) else (
    echo "keycastow.exe is not running."
)

REM Check for .txt files in the code folder
set "txt_files_found=0"
for %%F in (code\*.txt) do (
    set "txt_files_found=1"
    goto :FILES_FOUND
)

:FILES_FOUND
if %txt_files_found%==1 (
    REM Find the most recently created subfolder in the save directory
    for /f "delims=" %%F in ('dir /b /ad-h /t:c /o-d save') do (
        set "latest_folder=save\%%F"
        goto :MOVE_FILES
    )
)

:MOVE_FILES
if defined latest_folder (
    echo "Moving .txt files to the latest folder: %latest_folder%"
    move /y code\*.txt "%latest_folder%"
) else (
    echo "No subfolder found in the save directory."
)


python3116\python.exe code\main_mul.py

REM Check if keycastow.exe is running and terminate it if found
tasklist /FI "IMAGENAME eq keycastow.exe" 2>NUL | find /I "keycastow.exe" >NUL
if not errorlevel 1 (
    echo "keycastow.exe is running, terminating..."
    taskkill /F /IM keycastow.exe
) else (
    echo "keycastow.exe is not running."
)

REM Check for .txt files in the code folder
set "txt_files_found=0"
for %%F in (code\*.txt) do (
    set "txt_files_found=1"
    goto :FILES_FOUND
)

:FILES_FOUND
if %txt_files_found%==1 (
    REM Find the most recently created subfolder in the save directory
    for /f "delims=" %%F in ('dir /b /ad-h /t:c /o-d save') do (
        set "latest_folder=save\%%F"
        goto :MOVE_FILES
    )
)

:MOVE_FILES
if defined latest_folder (
    echo "Moving .txt files to the latest folder: %latest_folder%"
    move /y code\*.txt "%latest_folder%"
) else (
    echo "No subfolder found in the save directory."
)

pause
