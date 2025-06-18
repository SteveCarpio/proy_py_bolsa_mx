Option Explicit

'  === SOLO SE EJECUTARÁ SI ESTA EN ESTE RANGO DE HORAS ===
Dim currentHour
currentHour = Hour(Now)
If currentHour < 11 Or currentHour > 14 Then
    WScript.Quit
End If

'======================================================================================
' Programa que Actualizará las conexiones de datos Oracle en Excel.
' Autor: Steve Carpio
'======================================================================================

Dim excelApp, workbook, fso, folder, file, logFile, logFolder, logName
Dim folderPath, logPath
Dim dateStamp, timestamp

' === CONFIGURACIÓN ===
folderPath = "C:\MisCompilados\PROY_BOLSA_MX\INFORMES\EVENTOS_RELEVANTES"  
logFolder = "C:\MisCompilados\PROY_BOLSA_MX\NEXTCLOUD\LOG"         

' === CREAR LOG FILE ===
Set fso = CreateObject("Scripting.FileSystemObject")

If Not fso.FolderExists(logFolder) Then
    On Error Resume Next
    fso.CreateFolder(logFolder)
    If Err.Number <> 0 Then
        WScript.Echo "Error: No se pudo crear la carpeta de logs: " & logFolder
        WScript.Quit
    End If
    On Error GoTo 0
End If

dateStamp = Year(Now) & "-" & Right("0" & Month(Now), 2) & "-" & Right("0" & Day(Now), 2)
logName = "NEXTCLOUD_Main_" & dateStamp & "_vbs.log"
logPath = fso.BuildPath(logFolder, logName)

On Error Resume Next
Set logFile = fso.OpenTextFile(logPath, 8, True)
If Err.Number <> 0 Then
    WScript.Echo "Error: No se pudo crear el archivo de log: " & logPath
    WScript.Quit
End If
On Error GoTo 0

Sub Log(msg)
    timestamp = Year(Now) & "-" & Right("0" & Month(Now), 2) & "-" & Right("0" & Day(Now), 2) & " " & _
                Right("0" & Hour(Now), 2) & ":" & Right("0" & Minute(Now), 2) & ":" & Right("0" & Second(Now), 2)
    logFile.WriteLine timestamp & " - " & msg
End Sub

' === INICIAR PROCESO ===
Log "Inicio de proceso"

Set excelApp = CreateObject("Excel.Application")
excelApp.DisplayAlerts = False
excelApp.Visible = False
excelApp.AskToUpdateLinks = False
excelApp.AlertBeforeOverwriting = False

If fso.FolderExists(folderPath) Then
    Set folder = fso.GetFolder(folderPath)

    For Each file In folder.Files
       'If LCase(fso.GetExtensionName(file.Name)) = "xlsx" Then  --- Actualizara todos los excel de la carpeta
	   'If LCase(file.Name) = "eventos_relevantes_monica.xlsx" Or LCase(file.Name) = "eventos_relevantes_patricia.xlsx" Then
		If LCase(file.Name) = "eventos_relevantes_patricia.xlsx" Then
		
            On Error Resume Next
            Log "Procesando archivo: " & file.Name
            Set workbook = excelApp.Workbooks.Open(file.Path, False, False)
            If Err.Number = 0 Then
                workbook.RefreshAll
                excelApp.CalculateUntilAsyncQueriesDone
                WScript.Sleep 10000
                workbook.Save
                workbook.Close False
                Log "✔ Archivo actualizado correctamente: " & file.Name
            Else
                Log "❌ Error abriendo archivo: " & file.Name & " - Código: " & Err.Number
                Err.Clear
            End If
            On Error GoTo 0
        End If
    Next
Else
    Log "❌ Carpeta no encontrada: " & folderPath
End If

excelApp.Quit
Set excelApp = Nothing
logFile.WriteLine "Fin del proceso"
logFile.Close

  