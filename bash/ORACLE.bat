@echo off
REM === CONFIGURACIÓN GENERAL ===
set NOMBRE_JOB=ORACLE_Main.exe
set RUTA_JOB=C:\MisCompilados\PROY_BOLSA_MX
set RUTA_LOG=%RUTA_JOB%\ORACLE\LOG

REM === EJECUCIÓN DEL SCRIPT POWERSELL ===
powershell.exe -ExecutionPolicy Bypass -Command ^
"$fecha=(Get-Date).AddDays(-0).ToString('yyyy-MM-dd'); ^
 $exe=Join-Path '%RUTA_JOB%' '%NOMBRE_JOB%'; ^
 $logBase=Join-Path '%RUTA_LOG%' ([System.IO.Path]::GetFileNameWithoutExtension('%NOMBRE_JOB%') + '_' + $fecha); ^
 Start-Process -FilePath $exe -ArgumentList 'RUN','PRO',$fecha -RedirectStandardOutput ($logBase + '_out.log') -RedirectStandardError ($logBase + '_err.log') -NoNewWindow -Wait"

