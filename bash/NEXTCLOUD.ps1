$fecha = Get-Date -Format "yyyy-MM-dd"
$logPath = "C:\MisCompilados\PROY_BOLSA_MX\NEXTCLOUD\LOG\NEXTCLOUD_ps1_$fecha.log"  
$folderPath = "C:\MisCompilados\PROY_BOLSA_MX\INFORMES"                    

# Asegurarse de que el directorio de logs exista
if (!(Test-Path -Path (Split-Path $logPath))) {
    New-Item -Path (Split-Path $logPath) -ItemType Directory -Force
}

# Función para escribir al log
function Log($mensaje) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $logPath -Value "$timestamp - $mensaje"
}

Log "Inicio de actualización de archivos Excel en $folderPath"

try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false

    $files = Get-ChildItem -Path $folderPath -Filter Eventos_Relevantes*.xlsx

    foreach ($file in $files) {
        try {
            Log "Procesando: $($file.Name)"
            $workbook = $excel.Workbooks.Open($file.FullName, $false)
            $workbook.RefreshAll()
            $excel.CalculateUntilAsyncQueriesDone()
            Start-Sleep -Seconds 10
            $workbook.Save()
            $workbook.Close($false)
            Log "Archivo actualizado correctamente: $($file.Name)"
        } catch {
            Log "❌ Error procesando $($file.Name): $_"
        }
    }

    $excel.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
    Remove-Variable excel
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()

    Log "Proceso completado correctamente"
} catch {
    Log "❌ Error general en el proceso: $_"
}
