from qgis.core import QgsProject, QgsVectorLayer, QgsGeometry, QgsFeature, QgsVectorFileWriter, QgsCoordinateReferenceSystem
import processing
import os

# Input and output paths
large_vector_layer_path = "C:\\TUD\\Thesis\\Data\\building\\BAG\\9_276_592.shp"
output_folder = "C:\\TUD\\Thesis\\Data\\building\\BAG\\8_288_528\\children"

# Load the large vector layer
large_vector_layer = QgsVectorLayer(large_vector_layer_path, "Mother Layer", "ogr")
if not large_vector_layer.isValid():
    print("Layer failed to load!")
else:
    # Generate grid covering the extent of the large vector layer
    extent = large_vector_layer.extent()
    extent_string = f"{extent.xMinimum()},{extent.yMinimum()},{extent.xMaximum()},{extent.yMaximum()}"  # Format extent as string
    print(extent_string)

    grid_layer = processing.run("qgis:creategrid", {
        'TYPE': 2,  # Rectangle (Polygon)
        'EXTENT': extent,
        'HSPACING': 100,
        'VSPACING': 100,
        'HOVERLAY':0,
        'VOVERLAY':0,
        'CRS': large_vector_layer.crs(),
        'OUTPUT':'memory:'
    })['OUTPUT']
    
    QgsProject.instance().addMapLayer(grid_layer)
    QgsProject.instance().addMapLayer(large_vector_layer)
    
    # Process each grid cell
    cells = [ft for ft in grid_layer.getFeatures()]
    i = 1
    for cell in cells:
        try:
            grid_geometry = cell.geometry()  # Get the geometry of the feature
            grid_bbox = grid_geometry.boundingBox()  # Get the bounding box of the geometry
            xmin = grid_bbox.xMinimum()
            ymin = grid_bbox.yMinimum()
            clipped_layer = processing.run("native:extractbyextent", {
                'INPUT': large_vector_layer,
                'EXTENT':grid_bbox,
                'CLIP':True,
                'OUTPUT':'memory:'})['OUTPUT']
             
            # Filter out small polygons
            ids_to_delete = [f.id() for f in clipped_layer.getFeatures() if f.geometry().area() < 100]
            clipped_layer.dataProvider().deleteFeatures(ids_to_delete)
            
            total_area = sum(f.geometry().area() for f in clipped_layer.getFeatures())
            if total_area < 1000:
                continue
            
            # QgsProject.instance().addMapLayer(clipped_layer)
            print("Total Area: ", total_area)
                
            # Dissolve remaining polygons
            dissolved_layer = processing.run("native:dissolve", {
                'INPUT': clipped_layer,
                'OUTPUT': 'memory:'
            })['OUTPUT']
            
            # Filter out small polygons
            # ids_to_delete = [f.id() for f in dissolved_layer.getFeatures() if f.geometry().area() < 100]
            # dissolved_layer.dataProvider().deleteFeatures(ids_to_delete)
            
            # total_area = sum(f.geometry().area() for f in dissolved_layer.getFeatures())
            # if total_area < 1000:
            #     continue
            
            # Translate geometry to set the left bottom corner to (0, 0)
            center = dissolved_layer.extent().center()
            translated_layer = processing.run("native:translategeometry", {
                'INPUT': dissolved_layer,
                'DELTA_X': -xmin,
                'DELTA_Y': -ymin,
                'OUTPUT': 'memory:'
            })['OUTPUT']
            
            QgsProject.instance().addMapLayer(translated_layer)
            
        except QgsProcessingException as err:
            print(err)
        # Export to DXF
        # dxf_path = os.path.join(output_folder, f"industrial_{i}.dxf")
        # QgsVectorFileWriter.writeAsVectorFormat(translated_layer, dxf_path, "utf-8", dissolved_layer.crs(), "DXF", skipAttributeCreation=True)
        # dxfFile.close()
        
        # print(f"Exported DXF {i} successfully.")
        
        i = i + 1
        
    print("Process completed.")


    
    
    
