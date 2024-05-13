@echo off
setlocal

:: Get the directory of the current batch file
set "SCRIPT_PATH=%~dp0client.py"
set SERVICE_NAME=DupjoyClient

:: Define where NSSM is located. Adjust the path as necessary.
set "NSSM_PATH=%~dp0nssm.exe"


:: Check if the batch file is running as Administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Please run this batch file as an administrator.
    goto end
)

:: Automatically detect the Python executable path
for /f "delims=" %%i in ('where python') do set "PYTHON_PATH=%%i"
if "%PYTHON_PATH%"=="" (
    echo Python executable not found. Make sure Python is installed and in your PATH.
    goto end
)

:: Check if the service already exists and remove it
"%NSSM_PATH%" status %SERVICE_NAME% >nul 2>&1
if %errorlevel% equ 0 (
    echo Service exists, removing existing service...
    "%NSSM_PATH%" stop %SERVICE_NAME%
    "%NSSM_PATH%" remove %SERVICE_NAME% confirm
    goto end
)

:: Install the service using NSSM
"%NSSM_PATH%" install %SERVICE_NAME% "%PYTHON_PATH%" "%SCRIPT_PATH%"

:: Start the service
"%NSSM_PATH%" start %SERVICE_NAME%

echo The Dupjoy client has been installed and started as a service.
:end
pause
endlocal
