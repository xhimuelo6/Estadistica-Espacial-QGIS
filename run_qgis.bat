@echo off
call "C:\Program Files\QGIS 3.44.12\bin\o4w_env.bat"
path %OSGEO4W_ROOT%\apps\qgis-ltr\bin;%PATH%
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT:\=/%/apps/qgis-ltr
set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis-ltr\qtplugins;%OSGEO4W_ROOT%\apps\qt5\plugins
echo Launching QGIS from %OSGEO4W_ROOT%...
start "QGIS" "%OSGEO4W_ROOT%\bin\qgis-ltr-bin.exe" %*
