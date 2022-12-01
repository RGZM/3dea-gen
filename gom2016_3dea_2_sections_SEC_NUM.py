## -*- coding: utf-8 -*-

## Script for generating cross-sections orthogonal to one or more reference curves (e.g. derived from a defined cutting edge) on an imported 3D model (e.g. Keilmesser)
## Several times applicable with different distances and radii, depending on the setting, unique folders are created with set parameters in the name (e.g. SEC-NUM-5_SEC-R-20) 
## Anja Cramer, RGZM/WissIT, März 2019

## settings
### input folder
### number of cross-sections on the reference curve
### cutting radius around the reference curve

## inputs
### 3d mesh of object in *.stl file format
### digitised reference curve in *.iges file format

## outputs 
### generated cross-sections in single files in *.iges format (the settings like numbering of the cross-section and the position on the reference curve are indicated in the file names)
### control file for checking

import gom, os, re, datetime

RESULT=gom.script.sys.execute_user_defined_dialog (content='<dialog>' \
' <title>Select Input Folder</title>' \
' <style></style>' \
' <control id="OkCancel"/>' \
' <position>automatic</position>' \
' <embedding></embedding>' \
' <sizemode>fixed</sizemode>' \
' <size width="520" height="182"/>' \
' <content columns="2" rows="3">' \
'  <widget type="input::file" column="0" row="0" rowspan="1" columnspan="2">' \
'   <name>file</name>' \
'   <tooltip>select input folder</tooltip>' \
'   <type>directory</type>' \
'   <title>Choose File</title>' \
'   <default></default>' \
'   <limited>false</limited>' \
'   <file_types/>' \
'   <file_types_default></file_types_default>' \
'  </widget>' \
'  <widget type="label" column="0" row="1" rowspan="1" columnspan="1">' \
'   <name>label</name>' \
'   <tooltip></tooltip>' \
'   <text>Anzahl der Sections</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="input::integer" column="1" row="1" rowspan="1" columnspan="1">' \
'   <name>input_sec_num</name>' \
'   <tooltip></tooltip>' \
'   <value>10</value>' \
'   <minimum>0</minimum>' \
'   <maximum>1000</maximum>' \
'  </widget>' \
'  <widget type="label" column="0" row="2" rowspan="1" columnspan="1">' \
'   <name>label_1</name>' \
'   <tooltip></tooltip>' \
'   <text>Radius Section [mm]</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="input::integer" column="1" row="2" rowspan="1" columnspan="1">' \
'   <name>sec_radius</name>' \
'   <tooltip></tooltip>' \
'   <value>12</value>' \
'   <minimum>0</minimum>' \
'   <maximum>1000</maximum>' \
'  </widget>' \
' </content>' \
'</dialog>')

# settings
input_pfad = RESULT.file
input_sec_num = RESULT.input_sec_num
sec_radius = RESULT.sec_radius

# text file for checking the exported data
now = datetime.datetime.now()
now_string = str(now.year)+str(now.month)+str(now.day)+'_'+str(now.hour)+''+str(now.minute)
print(now_string)

myfile1 = open(input_pfad + "/"+"Info_EAP_2_sections_" + "SEC-NUM-"+str(input_sec_num)+"_SEC-R-"+str(sec_radius) + "_" + now_string + ".csv", "w")
myfile1.write ("3d mesh,reference curve,number of sections,radius for section,length reference curve,distance between sections,name section,length section" +"\n")			

##########################  start ####################	

############## import 3d mesh and reference curve #############

for root, dirs, files in os.walk (input_pfad):
	for mesh in files:
		if os.path.splitext(mesh)[-1]==".stl":
			print ("******************************")
			print ("root 3d modell (stl file): ", root)
			print ("3d modell (stl file): " + mesh)
			print("prefix: " , mesh[:-4])			
			
			################  create folder for cross-sections depend on the settings
			
			for root2, dirs2, files2 in os.walk (root):												
				# Regex --> Referenzkurve / reference edges
				pattern_ce_re = '^' + mesh[:-4] + '[_][A-Z]{1}[0-9]{1}_RE.igs$'
				anz_ce_re = 0
				# if there is more than one reference curve 
				for curve_ce_re in files2:
					result = re.search(pattern_ce_re, curve_ce_re)
					if result:
						anz_ce_re = anz_ce_re +1
						print ("****2******")
						root2n = root2 + "/" + "SEC-NUM-"+str(input_sec_num)+"_SEC-R-"+str(sec_radius)		
			
						if not os.path.exists(root2n):
							
							# start with calculations
										
							# create gom project and import stl 							
							gom.script.sys.close_project ()
							gom.script.sys.create_project ()
							gom.script.sys.import_stl (
								bgr_coding=False, 
								files=[root+"/"+mesh], 
								import_mode='new_elements', 
								length_unit='mm', 
								stl_color_bit_set=False, 
								target_type='mesh')
							gom.script.manage_alignment.define_original_alignment_as_initial_alignment ()
							
							# import reference curve							
							for root2, dirs2, files2 in os.walk (root):	
								# Regex --> reference edges
								pattern_ce_re = '^' + mesh[:-4] + '[_][A-Z]{1}[0-9]{1}_RE.igs$'
								anz_ce_re = 0
								for curve_ce_re in files2:
									result = re.search(pattern_ce_re, curve_ce_re)
									if result:
										anz_ce_re = anz_ce_re +1				
										root2n = root2 + "/" + "SEC-NUM-"+str(input_sec_num)+"_SEC-R-"+str(sec_radius)
										if not os.path.isdir(root2n):
											os.mkdir(root2n)	
											
										# import reference curve										
										gom.script.sys.import_cad (
											files=[gom.File (root + "/" + curve_ce_re)], 
											filter='SHOW', 
											import_fta=False, 
											repair_mode=5, 
											triangulation_mode='high')										
																																		
										eges_lenght = gom.app.project.inspection[curve_ce_re[:-4]].get ('curve_length')
										print ("Reference curve length: ", eges_lenght)
										sec_len = 	round ((((eges_lenght) / (input_sec_num-1))-0.0049),2)
										print ("Distance of the cross sections: ", sec_len)
															
										# create sections
										gom.script.selection3d.select_all ()
				
										MCAD_ELEMENT=gom.script.section.create_multisection_by_curve (
											disc_distance= sec_len, 
											disc_radius=sec_radius, 
											name=curve_ce_re[:-7], 
											project_onto_theoretical_surface=True, 
											properties=gom.Binary ('eAHNV11oHFUUPlvTNqbG2KJVRHRIo662m2TTGGWaNmtMaiimFRtikeqy2Zkko/sz2RlNUkm7fRN88kGKb0LtU6CYBxGf9EVQKCkKivjqq6IURPCh9fvu3ZuZ/clWEcFd7s6de8/9znd+7rl3Z8rF1OxT/SsyNfnsxORLMlPJeWFg25MFt+iWwhcrZd+thJ4biP4kpEO6u6RLuqWrG0MbufNnF/F8/tS0dbo8Hy7nKq41NJgesabK4by3YqXTauHm+m55Gr0EWmb91A5HjYqYZ+214XGM7/ehZb7cXE/IQ+jdJVJ1xJNAfClITlYli74n58SVtdnN9R3yIKT2QGqiTmpaylDmyitPGqQHIMf+3XjuhHwgReAV8P3q1V+HOTOFmd42+rJY4UkJTa/MojcPPm9iLICuAlpeQvw6krxAbmAvHUCcA5sy5l+7Sj10SqL6DrtD6N4PAb24CDBS8mQBkEUAlQCXlQp6S1DjqZ4jubX24FLtJLjxXwSeB4viFvCVDGHuAYVdoBBAVQUqSlCe/IHrwZyfqiT4th/dO+uoBrIIvGX56VJ7OjVb4VrpqQOgwpy8DuvotjLeVuXaJ+3Barb1AQzMq8yJOQAU4KY59PPyBvhXAMaoOPJpinAnIf0opGeU/bbYclw5eQg9W17YwhhHj5HkKPuNaM9hfUERvagyNAlcMqGOTjxrn+pi44gkxf2IXuSKfU28aTqztQIrGCOtY/o6cY3fFxT3fok4pM8QEWgqp2MRuzV28fLjfH8Mc3vbaisClZovjFEX90gX5MeVjZqR2Uk9avdwt5ER0U12lyBdAkb2xvnPON4qNrSqpKQYak+9XR9vZd8skPJyGKyWDhobmDrsk99vw2d/CdO/j327p/Bu5+jIFx+f3p89cWhn5vIH3/RT5hnIgGVdZtRrp7ez8DFzHayRwR60hcjmc7vIyAICqkSVno44c9XLW5Lf/UFd3GG3ryvGq/FcnVfYodz8kBrvBQ7yp2pifLw2+9771DKF2Qk09m08USFrkqyFq2isOSwerTRgwdbn6s89jxBlECOIYp2PzK7xlV8WgMbyw93FuubIjc/J1MR824p2AtAHbgsdYJt6KOm+gs7C9S5UmS1gQhPI0vdxpayArIhnNmhER82sjCpPrZxsCtTN1ThKM/VaTbEAyLjHvag9q88e9jcGCLV9zTT+OQlzWMCzP5JqK3JEW4Ext/5sj7gPxXn3HVIdhZNCYBbkmLCvHcY+9YTQZ6naQQfpg+MoTrM0mqXiSCmOLCGPPUgSTTPolQGFyTxaVdG2VI/B4QojN4BVAb69kO7CWWCpry+H8GTILHkbbRnInlqTgqwPXnng2JjxodmVFCRY9n05grG1LaRRsIgY0K6BOisZNgf8rJgU2ZmdRFwXmheUZbYMI8sHlY5IIsK34RPuaH2SH1E2jYK1yXf6kqdKQVngQLM+GalxEC2aNzZG86ma1+fAhZVHV3OuPAC20ZcotMrUfkroeEU8ORaXScUQbeDlwcY0+rNeNsKx4TUyYaWjHO2ugB9Zp2B3GXbawPKRk83zRA2VVLGNFOvEPKS2x2HmmfgYXcwmer5SezpgF/Gm/W8BtwIJZi2vRyn1qy9JNiyhTQ7GXcWcGRfFK6XGNavhlvP1nGh7I0LknVazjb4xuaTzotRkzd/Nxj5lL08g3B0QFdYg5oq+JXCncn/ywsh7Dk8CZi/36hM4gfVuoiUl5dcBzDj/Aw+3jsF/5eH6ijCC/P5nFaFPVRddJUJEMglv6rrOmtcrB9V+Zd8cNfrfAOvfUaxltvI+2T4ijI3OfvZMBdIVkNnFqmfqoTkBvsa9NiEP48TC37Jq/MTSu4X/kZg7+ZH40dd8gCaAkNlLLHMH8cE4fgu9dJgI/+YWalhqZAe25lCroxsY7jBX4ixpM2tV078lc0A3AvkQ1zeDQBLX2kPhrP8LVyfligEx/A=='), 
											reference_curve=gom.app.project.inspection[curve_ce_re[:-4]], 
											separated_elements=False)														
										
										# Rename the automatically created cross-sections (depend on the settings)
										zahl = 1
										for element in gom.ElementSelection ({'category': ['key', 'elements', 'explorer_category', 'actual', 'object_family', 'geometrical_element', 'type', 'section']}):
											if element.type == "section":
												nn = curve_ce_re[:-4] + "_SEC-" + (str(zahl).zfill(2)) + "_POS-" + (element.name.split())[-1]
												print ("Section - new name: ", nn)
												zahl = zahl + 1		
												gom.script.sys.edit_properties (
														data=[gom.app.project.actual_elements[element.name]], 
														elem_name=nn)
												
												# export cross section in iges file format
												gom.script.sys.export_iges (
													elements=[gom.app.project.actual_elements[nn]], 
													export_in_one_file=True, 
													file=root2n + "/" + nn + ".igs", 
													length_unit='default', 
													sender_company='', 
													sender_name='', 
													write_as_visualized=True)
													
												sec_lenght = gom.app.project.actual_elements[nn].get ('curve_length')

												# write in control file
												myfile1.write (mesh + ",")
												myfile1.write (curve_ce_re + ",")
												myfile1.write (str(input_sec_num) + ",")
												myfile1.write (str(sec_radius) + ",")												
												myfile1.write ((str(round(eges_lenght,2))) + ",")
												myfile1.write ((str(round(sec_len,2))) + ",")
												myfile1.write (nn + ",")												
												myfile1.write ((str(round(sec_lenght,0))) + ",")												
												myfile1.write ("\n")

												gom.script.cad.delete_element (elements=[gom.app.project.actual_elements[nn]])
										gom.script.cad.delete_element (elements=[gom.app.project.inspection[curve_ce_re[:-4]]])
myfile1.close()
print ("fertsch :-)")
