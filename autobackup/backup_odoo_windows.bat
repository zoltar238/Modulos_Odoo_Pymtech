@echo off
setlocal EnableDelayedExpansion

REM vars
SET "BACKUP_DIR=%USERPROFILE%\odoo_backups"
SET "ODOO_URL=http://nibafa.es"
SET "ODOO_DATABASE=sandbox"
SET "ADMIN_PASSWORD=hpyc-evt9-5pwt"
SET "KEPT_BACKUPS=7"

REM create a backup directory if it doesn't exist
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM Get current date in YYYY-MM-DD format using PowerShell
for /f %%i in ('powershell -Command "Get-Date -Format 'yyyy-MM-dd'"') do set TODAY_DATE=%%i

REM create a backup
echo Creating backup file: %BACKUP_DIR%\%ODOO_DATABASE%.%TODAY_DATE%.zip
curl -X POST -F "master_pwd=%ADMIN_PASSWORD%" -F "name=%ODOO_DATABASE%" -F "backup_format=zip" -o "%BACKUP_DIR%\%ODOO_DATABASE%.%TODAY_DATE%.zip" "%ODOO_URL%/web/database/backup"
echo Backup command finished. Check the backup directory.

REM delete old backups
echo Deleting backups older than %KEPT_BACKUPS% days...
forfiles /P "%BACKUP_DIR%" /M "%ODOO_DATABASE%.*.zip" /D -%KEPT_BACKUPS% /C "cmd /c echo Deleting @file ... && del @path"
echo Cleanup finished.

endlocal