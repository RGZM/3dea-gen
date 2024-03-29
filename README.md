# 3D-EdgeAngle Generator (3dea-gen)

The scripts provided here are used to automatically create cross-sections on a 3D model with previously manually defined curve(s) (digitalisation of the edge, e.g. active edge of a lithic). Furthermore, with different measuring procedures, the edge angles are automatically calculated on the cross-sections, which allows an analysis of the edge. The results are csv files for each section containing the edge angle values of the different measuring procedures. These scripts are part of the project 3D-EdgeAngle – A semi-automated 3D digital method to systematically quantify stone tool edge angle and design.

Contributors: [![ORCID ID](http://info.orcid.org/wp-content/uploads/2019/11/orcid_16x16.png)](http://orcid.org/0000-0002-5232-1944) Anja Cramer, [![ORCID ID](http://info.orcid.org/wp-content/uploads/2019/11/orcid_16x16.png)](http://orcid.org/0000-0003-2175-9908) Guido Heinz, [![ORCID ID](https://info.orcid.org/wp-content/uploads/2019/11/orcid_16x16.png)](http://orcid.org/0000-0002-2193-7340) Lisa Schunk

## software

The scripts were created with the Python Interface for the software GOM Insprect Professional 2016. The scripts must be executed within this software environment. A detailed description of the method used can be found on Protocols.io: [![DOI](https://zenodo.org/badge/DOI/10.5281/xxx.svg)](https://doi.org/10.5281/zenodo.xxx)

## data

To use the scripts, you need a 3D model in stl-file format and a digitalised edge on the 3D model in iges-file format.

You can download a sample dataset with the results of the scripts here: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7360011.svg)](https://doi.org/10.5281/zenodo.7360011)

## python scripts

For the naming of the data, specifications have been made, which are defined in the scripts by "regular expressions" (regex). These defaults can be adjusted. The variables for this are defined in the scripts with "pattern_".

**gom2016_3dea_1_reference_curve.py**

Creates a thinned and smoothed reference curve from the curve of the digitalised edge. This is the basis for the cross-sections.

**gom2016_3dea_2_sections_SEC_NUM.py**

Calculates cross-sections based on the reference curve and the 3D model. 
The number of cross sections can be specified here. The distance between them is distributed evenly along the reference curve.

**gom2016_3dea_2_sections_SEC_DIST.py**

Calculates cross-sections based on the reference curve and the 3D model. 
The distance between the cross profiles can be specified. The number of cross-sections is calculated automatically depending on the length of the reference curve.

**gom2016_3dea_3_sections_2d_projection.py**

Projects the cross-sections into a 2D plane and saves profiles as iges-file and csv-file. The cross-sections can thus also be analysed outside the GOM software.

**gom2016_3dea_4_compute_edge_angles.py**

Calculates angles on the cross sections based on three different measuring procedures. Angles are calculated at regular intervals from the digitalised edge. All calculated angles are saved in a csv-file.

