## -*- coding: utf-8 -*-

## Skript to reduce and smooth the curve who represent den edge
## Anja Cramer, Guido Heinz RGZM/WissIT, März 2019

## settings
### input folder, selected in GUI

## input
### digitised curve of the cutting edge in *.iges file format

## outputs 
### a reduced and smoothed curve of the cutting edge, which is required for the definition of the profile lines
### output a csv file with the parameters of the cutting edge curve and the reference curve modified from it

import gom, os, re, datetime

RESULT=gom.script.sys.execute_user_defined_dialog (content='<dialog>' \
' <title>Select Input Folder</title>' \
' <style></style>' \
' <control id="OkCancel"/>' \
' <position>automatic</position>' \
' <embedding></embedding>' \
' <sizemode>fixed</sizemode>' \
' <size width="570" height="154"/>' \
' <content rows="1" columns="1">' \
'  <widget row="0" rowspan="1" type="input::file" column="0" columnspan="1">' \
'   <name>file</name>' \
'   <tooltip>select input folder</tooltip>' \
'   <type>directory</type>' \
'   <title>Choose File</title>' \
'   <default></default>' \
'   <limited>false</limited>' \
'   <file_types/>' \
'   <file_types_default></file_types_default>' \
'  </widget>' \
' </content>' \
'</dialog>')

## variable
input_pfad = RESULT.file

## csv file 
## timestamp for filename
now = datetime.datetime.now()
now_string = str(now.year)+str(now.month)+str(now.day)+'_'+str(now.hour)+''+str(now.minute)
myfile1 = open(input_pfad + "/"+"Info_EAP_1_reference_curve_" + now_string + ".csv", "w")
myfile1.write ("3d-mesh,curve,length of curve [mm],number 3d-points of curve, x start point,y start point,z start point,x end point, y end point,z end point"+"\n")
			
########################## search of STL- und IGES- files  ####################	

for root, dirs, files in os.walk (input_pfad):
	for mesh in files:
		if os.path.splitext(mesh)[-1]==".stl":			
			for root2, dirs2, files2 in os.walk (root):
								
				# Regex --> cutting edges
				pattern_ce = '^' + mesh[:-4] + '[_][A-Z]{1}[0-9]{1}.igs$'
				anz_ce = 0
				for curve_ce in files2:
					result = re.search(pattern_ce, curve_ce)
					if result:
						anz_ce = anz_ce + 1
						file_name_check = root2 + "/" + curve_ce[:-4] + "_RE.igs"

						## if the reference curve does not exist, one is created here
						if not os.path.exists(file_name_check):
							gom.script.sys.close_project ()
							gom.script.sys.create_project ()	
							
							# import cutting edge											
							gom.script.sys.import_cad (
								files=[gom.File (root + "/" +curve_ce)], 
								filter='SHOW', 
								import_fta=False, 
								repair_mode=5, 
								triangulation_mode='high')			
					
							# write parameters in csv file
							eges_lenght = gom.app.project.inspection[curve_ce[:-4]].get ('curve_length')	
							anzpkt = gom.app.project.inspection[curve_ce[:-4]].get ('num_points')						
							xa = gom.app.project.inspection[curve_ce[:-4]].get ('coordinate['+str(0)+'].x')
							ya = gom.app.project.inspection[curve_ce[:-4]].get ('coordinate['+str(0)+'].y')
							za = gom.app.project.inspection[curve_ce[:-4]].get ('coordinate['+str(0)+'].z')
							xe = gom.app.project.inspection[curve_ce[:-4]].get ('coordinate['+str(anzpkt-1)+'].x')
							ye = gom.app.project.inspection[curve_ce[:-4]].get ('coordinate['+str(anzpkt-1)+'].y')
							ze = gom.app.project.inspection[curve_ce[:-4]].get ('coordinate['+str(anzpkt-1)+'].z')
							
							myfile1.write (str(mesh)+","+ str(curve_ce)+","+str(round(eges_lenght,2))+","+str(anzpkt)+","+str(round(xa,2))+","+str(round(ya,2))+","+str(round(za,2))+","+str(round(xe,2))+","+str(round(ye,2))+","+str(round(ze,2))+"\n")
					
							# rename curve							
							re_name = curve_ce[:-4] + "_RE.igs"
						
							# resample/reduce and smooth the curve
							gom.script.cad.convert_to_actual_element (elements=[gom.app.project.inspection[curve_ce[:-4]]])							
							gom.script.sys.edit_properties (
								data=[gom.app.project.actual_elements[curve_ce[:-4]]], 
								elem_name=re_name[:-4])	
							gom.script.cad.show_element_exclusively (elements=[gom.app.project.actual_elements[re_name[:-4]]])							
							gom.script.selection3d.select_all ()							
							gom.script.section.resample_section (sample_distance=1.00000000e+00)							
							gom.script.selection3d.select_all ()							
							gom.script.section.smooth_section (filter_radius='high')							
							
							# export reference curve
							gom.script.sys.export_iges (
								elements=[gom.app.project.actual_elements[re_name[:-4]]], 
								export_in_one_file=True, 
								file=root2 + "/" + re_name, 
								length_unit='default', 
								sender_company='', 
								sender_name='', 
								write_as_visualized=True)							
	
					
							# write parameters in csv file
							eges_lenght = gom.app.project.actual_elements[re_name[:-4]].get ('curve_length')
							anzpkt = gom.app.project.actual_elements[re_name[:-4]].get ('num_points')							
							xa = gom.app.project.actual_elements[re_name[:-4]].get ('coordinate['+str(0)+'].x')
							ya = gom.app.project.actual_elements[re_name[:-4]].get ('coordinate['+str(0)+'].y')
							za = gom.app.project.actual_elements[re_name[:-4]].get ('coordinate['+str(0)+'].z')
							xe = gom.app.project.actual_elements[re_name[:-4]].get ('coordinate['+str(anzpkt-1)+'].x')
							ye = gom.app.project.actual_elements[re_name[:-4]].get ('coordinate['+str(anzpkt-1)+'].y')
							ze = gom.app.project.actual_elements[re_name[:-4]].get ('coordinate['+str(anzpkt-1)+'].z')
							
							myfile1.write (str(mesh)+","+ str(re_name)+","+str(round(eges_lenght,2)) + ","+str(anzpkt)+","+str(round(xa,2))+","+str(round(ya,2))+","+str(round(za,2))+","+str(round(xe,2))+","+str(round(ye,2))+","+str(round(ze,2))+"\n")
													
							gom.script.sys.close_project ()

myfile1.close()
print ("fertsch :-)")
