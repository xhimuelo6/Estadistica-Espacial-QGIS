import sys
import os
from qgis.core import (
    QgsApplication, QgsProject, QgsRasterLayer, QgsVectorLayer,
    QgsColorRampShader, QgsRasterShader, QgsSingleBandPseudoColorRenderer,
    QgsMapSettings, QgsMapRendererParallelJob, QgsCoordinateReferenceSystem,
    QgsRectangle, QgsCategorizedSymbolRenderer, QgsRendererCategory,
    QgsSymbol, QgsPalLayerSettings, QgsVectorLayerSimpleLabeling,
    QgsTextFormat, QgsTextBufferSettings
)
from PyQt5.QtCore import QSize, QEventLoop
from PyQt5.QtGui import QColor, QImage, QPainter

# Initialize QGIS Application without GUI
qgs = QgsApplication([], False)
qgs.initQgis()

project = QgsProject.instance()
project.setTitle("Proyecto Estadística Espacial - Puno (UNAP)")
crs = QgsCoordinateReferenceSystem("EPSG:4326")
project.setCrs(crs)

# 1. Add Raster Layer
raster_path = os.path.abspath("evidencias/02_capa_raster/datos/DEM_Puno_Altiplano_SRTM.tif")
rlayer = QgsRasterLayer(raster_path, "DEM_Puno_Altiplano_SRTM", "gdal")

if rlayer.isValid():
    # Configure Color Ramp Shader for DEM
    fcn = QgsColorRampShader()
    fcn.setColorRampType(QgsColorRampShader.Interpolated)
    lst = [
        QgsColorRampShader.ColorRampItem(3812, QColor(43, 108, 176), "3,812 m - Lago Titicaca"),
        QgsColorRampShader.ColorRampItem(3950, QColor(142, 189, 102), "3,950 m - Altiplano / Pastizales"),
        QgsColorRampShader.ColorRampItem(4500, QColor(194, 139, 82), "4,500 m - Laderas y Puna"),
        QgsColorRampShader.ColorRampItem(5100, QColor(212, 177, 133), "5,100 m - Cordillera Carabaya"),
        QgsColorRampShader.ColorRampItem(5800, QColor(255, 255, 255), "5,800 m - Cumbres Nevadas")
    ]
    fcn.setColorRampItemList(lst)
    shader = QgsRasterShader()
    shader.setRasterShaderFunction(fcn)
    renderer = QgsSingleBandPseudoColorRenderer(rlayer.dataProvider(), 1, shader)
    rlayer.setRenderer(renderer)
    rlayer.triggerRepaint()
    project.addMapLayer(rlayer)
    print("Raster layer added successfully.")
else:
    print("Failed to load raster layer:", raster_path)

# 2. Add Vector Layer: Provincias
vec_prov_path = os.path.abspath("evidencias/03_capa_vectorial/datos/provincias_puno.geojson")
vlayer_prov = QgsVectorLayer(vec_prov_path, "Provincias_Puno", "ogr")

if vlayer_prov.isValid():
    # Setup Categorized renderer for provinces
    categories = []
    palette = [
        ("#fed976", "Puno"), ("#b3de69", "San Román"), ("#bebada", "Azángaro"),
        ("#fdb462", "Chucuito"), ("#80b1d3", "El Collao"), ("#fb8072", "Melgar"),
        ("#8dd1e1", "Huancané"), ("#d9d9d9", "Carabaya"), ("#ccebc5", "Sandia"),
        ("#bc80bd", "Lampa"), ("#ffed6f", "Yunguyo"), ("#ffffb3", "Moho"),
        ("#fccde5", "San Antonio de Putina")
    ]
    for col_hex, prov_name in palette:
        sym = QgsSymbol.defaultSymbol(vlayer_prov.geometryType())
        sym.setColor(QColor(col_hex))
        sym.setOpacity(0.8)
        categories.append(QgsRendererCategory(prov_name, sym, prov_name))
    
    prov_renderer = QgsCategorizedSymbolRenderer("PROVINCIA", categories)
    vlayer_prov.setRenderer(prov_renderer)
    
    # Labels
    pal = QgsPalLayerSettings()
    pal.fieldName = "PROVINCIA"
    t_format = QgsTextFormat()
    t_format.setSize(9)
    t_format.setColor(QColor(20, 20, 20))
    buffer = QgsTextBufferSettings()
    buffer.setEnabled(True)
    buffer.setSize(1)
    buffer.setColor(QColor(255, 255, 255))
    t_format.setBuffer(buffer)
    pal.setFormat(t_format)
    vlayer_prov.setLabeling(QgsVectorLayerSimpleLabeling(pal))
    vlayer_prov.setLabelsEnabled(True)
    vlayer_prov.triggerRepaint()
    project.addMapLayer(vlayer_prov)
    print("Provinces vector layer added successfully.")
else:
    print("Failed to load provinces layer:", vec_prov_path)

# 3. Add Vector Layer: Estaciones
vec_est_path = os.path.abspath("evidencias/03_capa_vectorial/datos/estaciones_meteorologicas_puno.geojson")
vlayer_est = QgsVectorLayer(vec_est_path, "Estaciones_Meteorologicas", "ogr")

if vlayer_est.isValid():
    sym_est = QgsSymbol.defaultSymbol(vlayer_est.geometryType())
    sym_est.setColor(QColor(220, 38, 38))
    vlayer_est.setRenderer(QgsCategorizedSymbolRenderer())
    
    # Labels
    pal_est = QgsPalLayerSettings()
    pal_est.fieldName = "NOMBRE"
    t_format_est = QgsTextFormat()
    t_format_est.setSize(8.5)
    t_format_est.setColor(QColor(153, 27, 27))
    buf_est = QgsTextBufferSettings()
    buf_est.setEnabled(True)
    buf_est.setSize(1.2)
    buf_est.setColor(QColor(255, 255, 255))
    t_format_est.setBuffer(buf_est)
    pal_est.setFormat(t_format_est)
    vlayer_est.setLabeling(QgsVectorLayerSimpleLabeling(pal_est))
    vlayer_est.setLabelsEnabled(True)
    vlayer_est.triggerRepaint()
    project.addMapLayer(vlayer_est)
    print("Weather stations vector layer added successfully.")
else:
    print("Failed to load weather stations layer:", vec_est_path)

# Save QGIS project
project_file = os.path.abspath("Proyecto_Estadistica_Espacial_Puno.qgs")
project.write(project_file)
print(f"QGIS project saved to {project_file}")

# Render Raster-only Map Image with QGIS Core Engine
extent = QgsRectangle(-71.4, -17.1, -68.7, -13.5)
settings = QgsMapSettings()
settings.setLayers([rlayer])
settings.setDestinationCrs(crs)
settings.setExtent(extent)
settings.setOutputSize(QSize(1540, 924))
settings.setBackgroundColor(QColor(245, 247, 250))

job = QgsMapRendererParallelJob(settings)
loop = QEventLoop()
job.finished.connect(loop.quit)
job.start()
loop.exec_()

img_raster = job.renderedImage()
img_raster.save("evidencias/02_capa_raster/mapa_renderizado_qgis_core.png")
print("Saved mapa_renderizado_qgis_core.png")

# Render Vector-only Map Image with QGIS Core Engine
settings_vec = QgsMapSettings()
settings_vec.setLayers([vlayer_est, vlayer_prov])
settings_vec.setDestinationCrs(crs)
settings_vec.setExtent(extent)
settings_vec.setOutputSize(QSize(1540, 606))
settings_vec.setBackgroundColor(QColor(248, 250, 252))

job_vec = QgsMapRendererParallelJob(settings_vec)
loop_vec = QEventLoop()
job_vec.finished.connect(loop_vec.quit)
job_vec.start()
loop_vec.exec_()

img_vec = job_vec.renderedImage()
img_vec.save("evidencias/03_capa_vectorial/mapa_vectorial_renderizado_qgis_core.png")
print("Saved mapa_vectorial_renderizado_qgis_core.png")

qgs.exitQgis()
print("PyQGIS project build completed successfully!")
