@echo off

set FILE_EXT_NORMAL=*.txt,*.war,*.xml,*.js,*.jsp,*.html,*.doc,*.ppt,*.xls,*.csv,*.java,*.css,*.pdf,*.vsd,*.tar.gz,*.zip,*.rar,*.pptx,*.docx,*.xlsx,*.vsdx,*.jar,*.sql
set MODE=%1

echo ************************************
echo Converting files, please wait...
echo ************************************
if "%MODE%"=="-r" (
	echo **  Running in recursive mode  **
	for /R %%i in (%FILE_EXT_NORMAL%) do (
		call:convertNormalDocument "%%~nxi" "%%~pi"
	)		
) else (
	echo **  Running in normal mode  **
	for %%i in (%FILE_EXT_NORMAL%) do (
		call:convertNormalDocument "%%~nxi" "%%~pi"
	)
)
echo ************************************
echo done.
echo ************************************
:exit
echo.&pause&goto:eof

::--------------------------------------------------------  
::-- functions 
::--------------------------------------------------------  
:convertNormalDocument
	echo %~1
	cd "%~2"
	echo f | xcopy /Y "%~1" "%~1.txt" 1>nul 2>nul
	del /F /A /Q "%~1"
	type "%~1.txt" >> "%~1.bak" 
	del /F /A /Q "%~1.txt"
	echo f | xcopy /Y  "%~1.bak" "%~1" 1>nul 2>nul
	del /F /A /Q "%~1.bak"
goto:eof

