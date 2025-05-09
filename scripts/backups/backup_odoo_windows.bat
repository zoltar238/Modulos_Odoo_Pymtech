@echo off
setlocal EnableDelayedExpansion

REM vars
SET "BACKUP_DIR=C:\\Users\\dabac\\IdeaProjects\\Modulos_Odoo_Pymtech\\autobackup"
SET "ODOO_URL=http://nibafa.es"
SET "ODOO_DATABASE=sandbox"
SET "ADMIN_PASSWORD=hpyc-evt9-5pwt"
SET "KEPT_BACKUPS=7"

REM create a backup directory if it doesn't exist
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM Get current date and time in YYYY-MM-DD_HH-MM-SS format using PowerShell
for /f %%i in ('powershell -Command "Get-Date -Format 'yyyy-MM-dd_HH-mm-ss'"') do set TIMESTAMP=%%i

REM create a backup
curl -X POST -F "master_pwd=%ADMIN_PASSWORD%" -F "name=%ODOO_DATABASE%" -F "backup_format=zip" -o "%BACKUP_DIR%\\%ODOO_DATABASE%.%TIMESTAMP%.zip" "%ODOO_URL%/web/database/backup"

REM delete old backups
forfiles /P "%BACKUP_DIR%" /M "%ODOO_DATABASE%.*.zip" /D -%KEPT_BACKUPS% /C "cmd /c echo Deleting @file ... && del @path"

endlocal