@echo off
call "C:\Program Files\QGIS 3.44.12\bin\o4w_env.bat"
path C:\Program Files\QGIS 3.44.12\apps\qgis-ltr\bin;%PATH%
set QGIS_PREFIX_PATH=C:/Program Files/QGIS 3.44.12/apps/qgis-ltr
set QT_PLUGIN_PATH=C:\Program Files\QGIS 3.44.12\apps\qgis-ltr\qtplugins;C:\Program Files\QGIS 3.44.12\apps\qt5\plugins
start "QGIS Desktop" "C:\Program Files\QGIS 3.44.12\bin\qgis-ltr-bin.exe" %*
