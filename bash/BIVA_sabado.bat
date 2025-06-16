@echo off
REM === CONFIGURACIÓN GENERAL ===
set NOMBRE_JOB=BIVA_Main.exe
set RUTA_JOB=C:\MisCompilados\PROY_BOLSA_MX
set RUTA_LOG=%RUTA_JOB%\BIVA\LOG

REM === EJECUCIÓN DEL SCRIPT POWERSELL ===
powershell.exe -ExecutionPolicy Bypass -Command ^
"$fecha=(Get-Date).AddDays(-2).ToString('yyyy-MM-dd'); ^
 $exe=Join-Path '%RUTA_JOB%' '%NOMBRE_JOB%'; ^
 $logBase=Join-Path '%RUTA_LOG%' ([System.IO.Path]::GetFileNameWithoutExtension('%NOMBRE_JOB%') + '_' + $fecha); ^
 Start-Process -FilePath $exe -ArgumentList 'RUN-NO-EMAIL','PRO',$fecha -RedirectStandardOutput ($logBase + '_out.log') -RedirectStandardError ($logBase + '_err.log') -NoNewWindow -Wait"

