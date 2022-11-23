# EAP

The scripts provided here are used to automatically create cross-sections on a 3D model and a previously manually defined curve (e.g. cutting edge). Furthermore, angles with different approaches are automatically calculated on the cross-sections, which allow an analysis of the sharpness of the edge. The results are csv files for each profile containing the angles of the different approaches.



to create defined sections on a 3d mesh and constructs angels on the sections

usefull if you have a lot of cutting edges to analyse

## software

python scripts for the **gom insprect pro 2016** software

## data

To use the scripts you need the 3d model in stl format and a digitized cutting edge on the 3d model in iges format.
Examples of data can be found here .....

## process and methods

Detailed explanation of the methods used in the scripts are documented here.....

## python scripts

For the naming of the data specifications have been made, which are defined in the scripts by "regular expressions" (regex). These defaults can be adjusted. The variables for this are defined in the scripts with "pattern_". 

### reference curve

**gom2016_EAP-1_reference_curve.py**

create a reference curve

### create section

there are two approaches
- define the distance between the cross-sections
  - **gom2016_EAP_2_sections_SEC_NUM.py**
- define the number of cross-sections on the reference curve
-   - later.....
