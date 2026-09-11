@echo off
call "C:\Program Files\QGIS 3.44.12\bin\o4w_env.bat"
echo OSGEO4W_ROOT is %OSGEO4W_ROOT%
"%OSGEO4W_ROOT%\bin\qgis-ltr-bin.exe" --version
