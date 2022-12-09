## -*- coding: utf-8 -*-

## Script for using in the GOM Inspect Professional 2016 software

## Script for generating cross-sections orthogonal to one or more reference curves (e.g. derived from a defined cutting edge) on an imported 3D model (e.g. Keilmesser)
## Several times applicable with different distances and radii, depending on the setting, unique folders are created with set parameters in the name (e.g. SEC-NUM-5_SEC-R-20) 
## Anja Cramer, Guido Heinz RGZM/WissIT, März 2019

## settings
### input folder
### number of cross-sections on the reference curve
### cutting radius around the reference curve
### selected in GUI

## inputs
### 3D mesh of Keilmesser in *.stl file format
### digitised reference curve in *.iges file format

## outputs 
### generated cross-sections in single files in *.iges format (the settings like numbering of the cross-section and the position on the reference curve are indicated in the file names)
### control file for checking

import gom, os, re

RESULT=gom.script.sys.execute_user_defined_dialog (content='<dialog>' \
' <title>Select Input Folder</title>' \
' <style></style>' \
' <control id="OkCancel"/>' \
' <position>automatic</position>' \
' <embedding></embedding>' \
' <sizemode>fixed</sizemode>' \
' <size height="182" width="271"/>' \
' <content columns="2" rows="3">' \
'  <widget column="0" type="input::file" rowspan="1" columnspan="2" row="0">' \
'   <name>file</name>' \
'   <tooltip>select input folder</tooltip>' \
'   <type>directory</type>' \
'   <title>Choose File</title>' \
'   <default>E:/RGZM_Projekte/Spurenlabor/TraCEr_EAP_LisaSchunk/tests/files_for_paper</default>' \
'   <limited>false</limited>' \
'   <file_types/>' \
'   <file_types_default></file_types_default>' \
'  </widget>' \
'  <widget column="0" type="label" rowspan="1" columnspan="1" row="1">' \
'   <name>label</name>' \
'   <tooltip></tooltip>' \
'   <text>Abstand der Sectionen [mm]</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget column="1" type="input::integer" rowspan="1" columnspan="1" row="1">' \
'   <name>input_sec_dist</name>' \
'   <tooltip></tooltip>' \
'   <value>5</value>' \
'   <minimum>0</minimum>' \
'   <maximum>1000</maximum>' \
'  </widget>' \
'  <widget column="0" type="label" rowspan="1" columnspan="1" row="2">' \
'   <name>label_1</name>' \
'   <tooltip></tooltip>' \
'   <text>Radius Section [mm]</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget column="1" type="input::integer" rowspan="1" columnspan="1" row="2">' \
'   <name>sec_radius</name>' \
'   <tooltip></tooltip>' \
'   <value>10</value>' \
'   <minimum>0</minimum>' \
'   <maximum>1000</maximum>' \
'  </widget>' \
' </content>' \
'</dialog>')

input_path = RESULT.file
input_sec_dist = RESULT.input_sec_dist
sec_radius = RESULT.sec_radius

########################## searching STL- and  IGES-Files  ####################	

############## search and import STL files #############

for root, dirs, files in os.walk (input_path):
	for mesh in files:
		if os.path.splitext(mesh)[-1]==".stl":
			print ("******************************")
			print ("folder STL-files: ", root)
			print("prefix: " , mesh[:-4])
			print ("3D-model: ", mesh)
						
			# import stl into gom-project
			
			gom.script.sys.close_project ()
			gom.script.sys.create_project ()
			gom.script.sys.import_stl (
				bgr_coding=False, 
				files=[root+"/"+mesh], 
				import_mode='new_elements', 
				length_unit='mm', 
				stl_color_bit_set=False, 
				target_type='mesh')
				
			# define orientation of models as current orientation
			gom.script.manage_alignment.define_original_alignment_as_initial_alignment ()
			
		#### look in currentfolder for igs-files
			
			for root2, dirs2, files2 in os.walk (root):
				
												
				# Regex --> reference edges
				pattern_ce_re = '^' + mesh[:-4] + '[_][A-Z]{1}[0-9]{1}_RE.igs$'
				anz_ce_re = 0
				for curve_ce_re in files2:
					result = re.search(pattern_ce_re, curve_ce_re)
					if result:
						anz_ce_re = anz_ce_re +1
						print ("**********")	

						root2n = root2 + "/" + "SEC-DIST-"+str(input_sec_dist)+"_SEC-R-"+str(sec_radius)
						if not os.path.isdir(root2n):
							os.mkdir(root2n)				
						
						#------------------------------------------------------
						
						# import first reference curve
						
						gom.script.sys.import_cad (
							files=[gom.File (root + "/" + curve_ce_re)], 
							filter='SHOW', 
							import_fta=False, 
							repair_mode=5, 
							triangulation_mode='high')
						
						print ("IGES reference curve ipmorted: ", curve_ce_re)
																														
						# create sections
						gom.script.selection3d.select_all ()

						MCAD_ELEMENT=gom.script.section.create_multisection_by_curve (
							disc_distance= input_sec_dist, 
							disc_radius=sec_radius, 
							name=curve_ce_re[:-7], 
							project_onto_theoretical_surface=True, 
							properties=gom.Binary ('eAHNV11oHFUUPlvTNqbG2KJVRHRIo662m2TTGGWaNmtMaiimFRtikeqy2Zkko/sz2RlNUkm7fRN88kGKb0LtU6CYBxGf9EVQKCkKivjqq6IURPCh9fvu3ZuZ/clWEcFd7s6de8/9znd+7rl3Z8rF1OxT/SsyNfnsxORLMlPJeWFg25MFt+iWwhcrZd+thJ4biP4kpEO6u6RLuqWrG0MbufNnF/F8/tS0dbo8Hy7nKq41NJgesabK4by3YqXTauHm+m55Gr0EWmb91A5HjYqYZ+214XGM7/ehZb7cXE/IQ+jdJVJ1xJNAfClITlYli74n58SVtdnN9R3yIKT2QGqiTmpaylDmyitPGqQHIMf+3XjuhHwgReAV8P3q1V+HOTOFmd42+rJY4UkJTa/MojcPPm9iLICuAlpeQvw6krxAbmAvHUCcA5sy5l+7Sj10SqL6DrtD6N4PAb24CDBS8mQBkEUAlQCXlQp6S1DjqZ4jubX24FLtJLjxXwSeB4viFvCVDGHuAYVdoBBAVQUqSlCe/IHrwZyfqiT4th/dO+uoBrIIvGX56VJ7OjVb4VrpqQOgwpy8DuvotjLeVuXaJ+3Barb1AQzMq8yJOQAU4KY59PPyBvhXAMaoOPJpinAnIf0opGeU/bbYclw5eQg9W17YwhhHj5HkKPuNaM9hfUERvagyNAlcMqGOTjxrn+pi44gkxf2IXuSKfU28aTqztQIrGCOtY/o6cY3fFxT3fok4pM8QEWgqp2MRuzV28fLjfH8Mc3vbaisClZovjFEX90gX5MeVjZqR2Uk9avdwt5ER0U12lyBdAkb2xvnPON4qNrSqpKQYak+9XR9vZd8skPJyGKyWDhobmDrsk99vw2d/CdO/j327p/Bu5+jIFx+f3p89cWhn5vIH3/RT5hnIgGVdZtRrp7ez8DFzHayRwR60hcjmc7vIyAICqkSVno44c9XLW5Lf/UFd3GG3ryvGq/FcnVfYodz8kBrvBQ7yp2pifLw2+9771DKF2Qk09m08USFrkqyFq2isOSwerTRgwdbn6s89jxBlECOIYp2PzK7xlV8WgMbyw93FuubIjc/J1MR824p2AtAHbgsdYJt6KOm+gs7C9S5UmS1gQhPI0vdxpayArIhnNmhER82sjCpPrZxsCtTN1ThKM/VaTbEAyLjHvag9q88e9jcGCLV9zTT+OQlzWMCzP5JqK3JEW4Ext/5sj7gPxXn3HVIdhZNCYBbkmLCvHcY+9YTQZ6naQQfpg+MoTrM0mqXiSCmOLCGPPUgSTTPolQGFyTxaVdG2VI/B4QojN4BVAb69kO7CWWCpry+H8GTILHkbbRnInlqTgqwPXnng2JjxodmVFCRY9n05grG1LaRRsIgY0K6BOisZNgf8rJgU2ZmdRFwXmheUZbYMI8sHlY5IIsK34RPuaH2SH1E2jYK1yXf6kqdKQVngQLM+GalxEC2aNzZG86ma1+fAhZVHV3OuPAC20ZcotMrUfkroeEU8ORaXScUQbeDlwcY0+rNeNsKx4TUyYaWjHO2ugB9Zp2B3GXbawPKRk83zRA2VVLGNFOvEPKS2x2HmmfgYXcwmer5SezpgF/Gm/W8BtwIJZi2vRyn1qy9JNiyhTQ7GXcWcGRfFK6XGNavhlvP1nGh7I0LknVazjb4xuaTzotRkzd/Nxj5lL08g3B0QFdYg5oq+JXCncn/ywsh7Dk8CZi/36hM4gfVuoiUl5dcBzDj/Aw+3jsF/5eH6ijCC/P5nFaFPVRddJUJEMglv6rrOmtcrB9V+Zd8cNfrfAOvfUaxltvI+2T4ijI3OfvZMBdIVkNnFqmfqoTkBvsa9NiEP48TC37Jq/MTSu4X/kZg7+ZH40dd8gCaAkNlLLHMH8cE4fgu9dJgI/+YWalhqZAe25lCroxsY7jBX4ixpM2tV078lc0A3AvkQ1zeDQBLX2kPhrP8LVyfligEx/A=='), 
							reference_curve=gom.app.project.inspection[curve_ce_re[:-4]], 
							separated_elements=False)
						
										
						
						# new name
						zahl = 1
						for element in gom.ElementSelection ({'category': ['key', 'elements', 'explorer_category', 'actual', 'object_family', 'geometrical_element', 'type', 'section']}):
							if element.type == "section":
								nn = curve_ce_re[:-4] + "_SEC-" + (str(zahl).zfill(2)) + "_POS-" + (element.name.split())[-1]
								print ("Section - new name: ", nn)
								zahl = zahl + 1
						
								# rename
								gom.script.sys.edit_properties (
										data=[gom.app.project.actual_elements[element.name]], 
										elem_name=nn)
								
								# exporexport 
								gom.script.sys.export_iges (
									elements=[gom.app.project.actual_elements[nn]], 
									export_in_one_file=True, 
									file=root2n + "/" + nn + ".igs", 
									length_unit='default', 
									sender_company='', 
									sender_name='', 
									write_as_visualized=True)
								
								# delete
								gom.script.cad.delete_element (elements=[gom.app.project.actual_elements[nn]])
						# delete
						gom.script.cad.delete_element (elements=[gom.app.project.inspection[curve_ce_re[:-4]]])

print ("fertsch :-)")
