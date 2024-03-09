# Workflow
## Download 2D BAG (.gpkg) from 3D BAG website
3D BAG website address: https://3dbag.nl/  
Data tile index: 8_288_528, 8_727_600, 8-232-560, 9_264_588, 9_268_604, 9_276_592
## Clip tiles
Using qgisClipAndTranslate script. Choose clips with different features and export as DXF file.  
Extent: 100 m x 100 m
Center coordinate: (50, 50)  
Feature classes: attached, detached, mixed, industrial, highrise(?)
## Ansys Fluent simulation
### Geometry
Import CAD file (.dxf) INTO DesignModeler, produce the domain of wind simulation. Create named selections for: inlet, outlet, symmetry, windzone.
### Mesh
Set element size.   
❗Need improvement
### Fluent setup
Using ansysFluent script:  
  Viscous method: realizable k-epsilon  
  Inlet velocity magnitude: 10 m/s  
  Solution method: SIMPLE
  Initialization method: Hybrid
  Number of iterations: 600
  Data sampling for steady statistics: Sampling interval: 20
  Output format: .txt
## Convert building layout and simulation result to Raster
In ArcGIS, Conversion tool.
  Raster resolution: 0.8 m  
❗Need higher lisence of ArcGIS. Tried to do with QGIS, result's not satisfied
## Training Machine Learning models
(For now) ViT, Swin Transformer
