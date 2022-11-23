# 3D Edge Angle Generator (3dea-gen)

The scripts provided here are used to automatically create cross-sections on a 3D model and a previously manually defined curve (e.g. cutting edge). Furthermore, angles with different approaches are automatically calculated on the cross-sections, which allow an analysis of the sharpness of the edge. The results are csv files for each profile containing the angles of the different approaches.

## software

The scripts were created for the software **gom insprect pro 2016**. The execution of the scripts must take place in this software.

## data

To use the scripts you need a 3d model in stl format and a digitized cutting edge on the 3d model in iges format.

## python scripts

For the naming of the data specifications have been made, which are defined in the scripts by "regular expressions" (regex). These defaults can be adjusted. The variables for this are defined in the scripts with "pattern_". 

**gom2016_3DEA_1_reference_curve.py**

Creates a thinned and smoothed reference curve from the curve of the digitised cutting edge. This is the basis for the cross profiles.

**gom2016_EAP_2_sections_SEC_NUM.py**

Calculates cross-sections based on the reference curve and the 3D model. 
The number of cross sections can be specified here. The distance between them is distributed evenly over the reference curve. 

**gom2016_3DEA_2_sections_SEC_DIST.py**

Calculates cross-sections based on the reference curve and the 3D model. The distance between the cross profiles can be specified. The number of cross-sections is calculated automatically depending on the length of the reference curve.

**gom2016_3DEA_3_sections_2d_projection.py**

Projects the cross-sections into a 2D plane and saves profiles as *.iges and *.csv. The cross-sections can thus also be analysed outside the GOM software.

**gom2016_3DEA_4_compute_edge_angles.py**

