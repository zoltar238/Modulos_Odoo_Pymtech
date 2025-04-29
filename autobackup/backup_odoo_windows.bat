@echo off
setlocal EnableDelayedExpansion

REM vars
SET "BACKUP_DIR=~\odoo_backups"
SET "ODOO_URL=http://nibafa.es"
SET "ODOO_DATABASE=sandbox"
SET "ADMIN_PASSWORD=hpyc-evt9-5pwt"
SET "KEPT_BACKUPS=7"

REM create a backup directory
mkdir "-p" "%BACKUP_DIR%"

REM create a backup
SET _INTERPOLATION_0=
FOR /f "delims=" %%a in ('date +%F') DO (SET "_INTERPOLATION_0=!_INTERPOLATION_0! %%a")
curl "-X" "POST" "-F" "master_pwd=%ADMIN_PASSWORD%" "-F" "name=%ODOO_DATABASE%" "-F" "backup_format=zip" "-o" "!BACKUP_DIR!/!ODOO_DATABASE!.!_INTERPOLATION_0:~1!.zip" "!ODOO_URL!\web\database\backup"


REM delete old backups
find "!BACKUP_DIR!" "-type" "f" "-mtime" "+!KEPT_BACKUPS!" "-name" "!ODOO_DATABASE!.*.zip" "-delete"