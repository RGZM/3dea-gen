# -*- coding: utf-8 -*-

## Script for using in the GOM Inspect Professional 2016 software

## Calculates angles on the cross sections in three different approaches
## Anja Cramer, Guido Heinz RGZM/WissIT, März 2019

## settings
### input folder
### The regular distance between the angle measurement positions on the curve
### The size of the segment at the angle measurement position.

## inputs
### The GOM-Inspect-Projects of the projected 2d cross section generated in script 3 (*_local.ginspect file)

## outputs
### per cross section a table as *csv-file with all angles, divided into angle measuring position and the three approaches of the angle calculation
### one GOM-Inspect-Projects file (*.ginspect) per cross-section containing all angle calculations

import gom, os, re, math, datetime

RESULT=gom.script.sys.execute_user_defined_dialog (content='<dialog>' \
' <title>Select Input Folder</title>' \
' <style></style>' \
' <control id="OkCancel"/>' \
' <position>automatic</position>' \
' <embedding></embedding>' \
' <sizemode>fixed</sizemode>' \
' <size width="271" height="182"/>' \
' <content rows="3" columns="2">' \
'  <widget type="input::file" column="0" rowspan="1" row="0" columnspan="2">' \
'   <name>file</name>' \
'   <tooltip>select input folder</tooltip>' \
'   <type>directory</type>' \
'   <title>Choose File</title>' \
'   <default>E:/RGZM_Projekte/Spurenlabor/TraCEr_EAP_LisaSchunk/tests</default>' \
'   <limited>false</limited>' \
'   <file_types/>' \
'   <file_types_default></file_types_default>' \
'  </widget>' \
'  <widget type="label" column="0" rowspan="1" row="1" columnspan="1">' \
'   <name>label</name>' \
'   <tooltip></tooltip>' \
'   <text>distance [mm]</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="input::number" column="1" rowspan="1" row="1" columnspan="1">' \
'   <name>input_dist</name>' \
'   <tooltip></tooltip>' \
'   <value>1</value>' \
'   <minimum>0</minimum>' \
'   <maximum>10</maximum>' \
'   <precision>1</precision>' \
'   <background_style></background_style>' \
'  </widget>' \
'  <widget type="label" column="0" rowspan="1" row="2" columnspan="1">' \
'   <name>label_1</name>' \
'   <tooltip></tooltip>' \
'   <text>segment [mm]</text>' \
'   <word_wrap>false</word_wrap>' \
'  </widget>' \
'  <widget type="input::number" column="1" rowspan="1" row="2" columnspan="1">' \
'   <name>input_seg</name>' \
'   <tooltip></tooltip>' \
'   <value>2</value>' \
'   <minimum>0</minimum>' \
'   <maximum>1000</maximum>' \
'   <precision>1</precision>' \
'   <background_style></background_style>' \
'  </widget>' \
' </content>' \
'</dialog>')

input_pfad = RESULT.file
dist_angles = RESULT.input_dist
dist_segment = RESULT.input_seg

# Setting of folders and cross-sections to compute
# here detailed selection of folders is made .... to reduce calculation time
folder_list = [""]
sec_folder = ""

# LOG-file
now = datetime.datetime.now()
now_string = str(now.year)+str(now.month)+str(now.day)+'_'+str(now.hour)+''+str(now.minute)
# log file which data was calculated
mylog = open(input_pfad + "/" + "Info_EAP_4_compute_edge_angles_"+str(dist_angles)+"_"+ str(dist_segment) + "_" +now_string+".csv", "w")
# Contains data whose name is incorrect and has not been calculated
myerror = open(input_pfad + "/" + "Info_EAP_4_check_filenames_"+str(dist_angles)+"_"+ str(dist_segment) + "_" +now_string+".csv", "w")


##########################  start  ####################


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
						anz_ce = anz_ce +1
						print ("2 - IGES cutting edge : ", curve_ce)

						# time for logfile
						now = datetime.datetime.now()
						now_string_s = str(now.year)+str(now.month)+str(now.day)+'_'+str(now.hour)+''+str(now.minute)
						mylog.write ("projected cross section: " + str(curve_ce[:-4])+" started "+str(now.day)+"."+str(now.month)+"."+str(now.year)+", "+str(now.hour)+":"+ (str("%.2o"% (now.minute))) + "\n")
											
						for root3, dirs3, files3 in os.walk (root2):							
							# Regex --> reference edges
							pattern_ce_re = '^' + curve_ce[:-4]+'_RE.igs$'
							anz_ce_re = 0
							for curve_ce_re in files3:
								result = re.search(pattern_ce_re, curve_ce_re)
								if result:
									anz_ce_re = anz_ce_re +1
									print ("3 - IGES reference curve: ", curve_ce_re)	
									
									for root4, dirs4, files4 in os.walk (root3):										
										# Regex --> Sections
										pattern_ce_re_sec = '^' + curve_ce_re[:-4] + '[_]SEC[\-][0-9]{2}_POS[\-](\d*.\d*).igs$'
										anz_ce_re_sec = 0										
										for curve_ce_re_sec in files4:
											result = re.search(pattern_ce_re_sec, curve_ce_re_sec)
											if result:
												anz_ce_re_sec = anz_ce_re_sec +1
												print ("4 - IGES Section: ", curve_ce_re_sec)
												
												for root5, dirs5, files5 in os.walk (root4):	
													# Regex --> Sections
													pattern_ce_re_sec_l = '^' + curve_ce_re[:-4]+ "_" + (curve_ce_re_sec.split("_")[len(curve_ce_re_sec.split("_"))-2]) + '_local.ginspect$'
													anz_ce_re_sec_l = 0									
													for curve_ce_re_sec_l in files5:
														result = re.search(pattern_ce_re_sec_l, curve_ce_re_sec_l)
														if result:
															
															# use only folders selected in folder_list and in sec_folder
															for f in folder_list:
																if f in root5:
																	print (root5)
																	if sec_folder in root5:
																		print ("processing here")
															
																		try:																				
																			anz_ce_re_sec_l = anz_ce_re_sec_l +1
																			print ("5 - IGES Section local: ", curve_ce_re_sec_l)																			
																		
																			file_name_check = root5 + "/"+  str(curve_ce_re_sec_l[:-9]) + "_w_"+ str(format(dist_angles,'.1f')) + "_" + str(format(dist_segment,'.1f')) + ".csv"
																			
																			# if not exists, create table file
																			if not os.path.exists(file_name_check):
																				print ("computung: " + file_name_check)
																				myfile = open(root5 + "/"+  str(curve_ce_re_sec_l[:-9]) + "_w_"+ str(format(dist_angles,'.1f')) + "_" + str(format(dist_segment,'.1f')) + ".csv", "w")
																				
																				# write columns to table file
																				myfile.write ("section")
																				myfile.write (",angel_number")
																				myfile.write (",dist to origin on curve [mm]")
																				myfile.write (",segment on section [mm]")
																				myfile.write (",angle 1 (3-points) [degree]")
																				myfile.write (",angle 2 (2-constructed-lines) [degree]")
																				myfile.write (",angle 3 (2-BestFit-lines) [degree]")																				
																				myfile.write ("\n")
																				
																				# open gom project from projected 2d cross section
																				file_proj = str(root5) + "/" + str(curve_ce_re_sec_l)
																				gom.script.sys.close_project ()
																				gom.script.sys.load_project (file=file_proj)
																				
																				# name of projected 2d cross section
																				curve_data = curve_ce_re_sec[:-4]
																				
																				
																				##### step 1
																				##### Calculation of the intersection point w_0 between the cross section and the digitized edge
																				
																				# all points of cross sections
																				num_points = gom.app.project.actual_elements[curve_data].get ('num_points')	
																				min_dist = 999.999
																				min_dist_index = -999
																				index = 0

																				# searches for the point closest to the origin of the coordinates																			
																				while index < num_points:
																					x = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(index)+'].x')
																					y = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(index)+'].y')
																					dist = math.sqrt((x*x) + (y*y))
																					if dist < min_dist:
																						min_dist = dist
																						min_dist_index = index
																					index = index + 1
							
																				# create w_0
																				pn = []
																				for i in gom.ElementSelection ({'category': ['key', 'elements', 'explorer_category', 'actual', 'object_family', 'geometrical_element', 'type', 'point']}):
																					pn.append(i.get ('name'))
																				if not 'w_0' in pn:
																					print ('create w_0')
																					pn_x = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(min_dist_index)+'].x')
																					pn_y = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(min_dist_index)+'].y')
																					pn_z = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(min_dist_index)+'].z')
																					MCAD_ELEMENT=gom.script.primitive.create_point (
																						name='w_0', 
																						point={'point': gom.Vec3d (pn_x, pn_y, pn_z)}, 
																						properties=gom.Binary ('eAHNV01sG0UY/QylLYYQUsqPEIJVGiAUHMdVSMFNaQhJiRApFURthQqW4107Bnvt7m5wXFTYigvixgG4IkFPEZV6QIgT4oDEAaUnEOIE4oIEElUvSAg1vDfjsXcdO20PSOxqvbMz37zv780348VaNXXs8bFVmZ97enbuRVn08uXAz2bnKk7VcYOjXq3ueEHZ8UVfCdkmA0lJyoAkB9CV+ic8uYz3sy8sWC/VikEj7znWvvHMpDVfC4rlVSuTURPX13bIfrQSeC59lr44g/fRk/qtBHr+fIjexC78FH9eX0vIfWjdKhLaUhZf6lKRvDQlh3ZZTosjZ46tr90g90LqFkjNxqQWpCY2ZF7ea5DugRzbt+F9E+R9qQKvgvvbV/6cMFLU56DPwWhOCkCp4nbElUDOTVPf7Zi/Xc0PxINOV0oy+iPnb8MIrlAS/LoLzZtjaL4sA68hv35EHGjijHAJfTVofPU8ZzFgifBdNofRHIwBUGFeXoM5BZhTw1dTvvt8azAJdxJsH8DujoGtII4OfCwqoJzyhFHW4GX0ujL0+zWBjwAcYQmZoCUAVAC7hHZBXkdwPECtAMyWL1KEOwLpByG9iP6qZHEfhvISTGT7+TbGDFo0kb1sd6M9g/kVPJ6c/YYujgKXllDHTrxbV7jc3QNJ51MzA3TrspuIpI7XIoDWsXCRuCapJWX7mHRsyJwgIslLgrGN5PLaOHT2k4f5/RA+hrbUVgUqNb99iLpI2CTkZ5SP2iJD60GlgdSnRUQ3dHIh7QIjd/mtL9n/BMYhF/ORtHaVlOFRDpEklUmIBlo2+LUsp7fTDgsI8Cmkr/FZx9uS3/9FXVywV19mxq8oW0hCLrErH1PjbuAgg6GJ8uHW6PsfUMs8RmfxsJ3F+862JEtDE08AP7h8e2nAhPZ1/o/BB4gyjh7EMRYjw9u6iksJaCwC5DeLgy2Xv6KlJup9F/FzgN5zVWgfC6WMtcfVZ0PVMt55RQWS0KTGl1M/RJWuKNMCOXGBTrToJtOq+vQKsqk/V5pRlL6mWzCdeY9GUUdWl2K2L6QJ1b8kmvgcgTsso7mfaGov44i2isxt/L014i7U3h03SjiFIAXArMhTwrYOGNvUE0CfpfLFr4OopaewnsuoIZylNQ1DQq8E9pB9lMvgSStM8qipsm2pFpNDCTM/jdk+7mFIJ1HqLXXX5TG8mTJL3sTTgMaympOCbB12FYCTxUgdFjmSggSrel0OoO9MG2kKVnQsoF/pmJdMmw37rIgUrTMribgONJeUx1mZAMvHlY6ORAc/C/9Z9/SWeED5NAWrDd8ZKdb1ivLAhma98VHjOB4L66JTN00c2VtSMdY1lP17YGHn1jnQyCY6HeSUyka3h1FNqQh6FtgFWGMexjMuG/XXh73Mkq1iQr892ErdKfhdg59ZYNXBSeLEx4kaKCnuX/2kWCeKkOovQUaa/BgUsomR91pve1OG3wCuBwmymQeYlPolkgtdVeWTjX5HWU7GdfKVUv3aqome43Gb6Hs3Qic6vUa7Y2O4pLPrbvLmWtk4ovzlLoHdG1lhDSLj9D7Nlcr1mYO3PGlwJyB7uVYfwalAryZ64qq4pjFi/w8i3DsH/1WE4xVhEsy9voowoqqLrhIBMjmKaOq6zpo3LI+q9cq22Wpy6uTH+ncQc8lWnui2zghzo9nPlqlAugKSXax6ph6aHeAOdYC/HzsW/qWE0R1Lrxb+ZSB3CpPRrW/zBpoAwvRQdI9ilS5jVek/A5pzvzxJlOs+C77328bur9/ZT/Qx6OG5pdeJPgcPuSM0oJOnaFZdX2YvRS1nHOJ/GnDO/xfv46fcAW3L'))
																				gom.script.cad.convert_to_actual_element (elements=[gom.app.project.inspection['w_0']])
																				
																				# distance between p_e and next point on curve
																				# p_e_x = gom.app.project.actual_elements['p_e'].get ('center_coordinate.x')																				
																				# dx = (gom.app.project.actual_elements['p_e'].get ('center_coordinate.x')) - (gom.app.project.actual_elements['w_0'].get ('center_coordinate.x'))
																				# dy = (gom.app.project.actual_elements['p_e'].get ('center_coordinate.y')) - (gom.app.project.actual_elements['w_0'].get ('center_coordinate.y'))
																				# dist_e = math.sqrt((dx * dx) + (dy * dy))
																				# print ('calculated distance: ' + str(dist_e))
																				# print ('calculated distance: ' + str(min_dist))


																				##### step 2
																				##### Calculation of the angular measurement positions on the cross section, starting from the point w_0 and in the regular distance entered as parameter
																				##### Calculation of the start and end points of the segments at the angle measurement positions
																				
																				
																				
																				# calculate the number of angular measurement positions and their segments on the cross section (steps)															
																				dist_start = 0
																				i = 0																				
																				while i < min_dist_index:
																					dx = (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(i+1)+'].x')) - (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(i)+'].x'))
																					dy = (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(i+1)+'].y')) - (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(i)+'].y'))
																					dist_start = dist_start + math.sqrt((dx * dx) + (dy * dy))
																					i +=1 																					
																				dist_end = 0
																				i = min_dist_index
																				while i < num_points-1:
																					dx = (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(i+1)+'].x')) - (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(i)+'].x'))
																					dy = (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(i+1)+'].y')) - (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(i)+'].y'))
																					dist_end = dist_end + math.sqrt((dx * dx) + (dy * dy))
																					i +=1
																				
																				print ('distance to start: '+str(dist_start))
																				print ('distance to end: '+str(dist_end))
																				distance = min(dist_start, dist_end)
																				print ('min distance: '+str(distance))				
																																				
																				dist_to_go = 0
																				steps_to_go = 0
																				dist_max = 0
																				while dist_max < (distance - dist_angles):
																					steps_to_go +=1  
																					dist_to_go = steps_to_go * dist_angles
																					dist_max = dist_to_go  + (dist_segment / 2.0)
																				print ('steps_to_go: '+str(steps_to_go))																				
																				
																				print ("************************************************")

																				# start the calculation of the points of the angular measurement position for every step
																				i = 1
																				while i <= steps_to_go:
																					current_dist_p = round((i * dist_angles),2)
																					current_dist_p1 = (i * dist_angles) - (dist_segment / 2.0)
																					current_dist_p2 = (i * dist_angles) + (dist_segment / 2.0)
																					print ("***********************")
																					print ('schrittnummer i: ' + str(i))
																					print ("current_dist_p: " + str(current_dist_p))
																					print ("current_dist_p1: " + str(current_dist_p1))
																					print ("current_dist_p2: " + str(current_dist_p2))
																					
																					# point 1 / Center of the angular measurement position on the left side of the cross section
																					my_dist = 0	
																					j = min_dist_index
																					while my_dist < current_dist_p:
																						dx = (gom.app.project.actual_elements[curve_data].get ('coordinate['+str((j-1))+'].x')) - (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].x'))
																						dy = (gom.app.project.actual_elements[curve_data].get ('coordinate['+str((j-1))+'].y')) - (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].y'))
																						my_dist_diff = math.sqrt((dx * dx) + (dy * dy))
																						my_dist = my_dist + my_dist_diff
																						j -=1
																						
																					j +=1	
																					pn1 = 'w_'+ str(current_dist_p)+'_1'
																					#pn1 = 'w_'+ str(i)+'_1'
																					pn1_x = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].x')
																					pn1_y = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].y')
																					pn1_z = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].z')
																					MCAD_ELEMENT=gom.script.primitive.create_point (
																						name=str(pn1), 
																						point={'point': gom.Vec3d (pn1_x, pn1_y, pn1_z)}, 
																						properties=gom.Binary ('eAHNV01sG0UY/QylLYYQUsqPEIJVGiAUHMdVSMFNaQhJiRApFURthQqW4107Bnvt7m5wXFTYigvixgG4IkFPEZV6QIgT4oDEAaUnEOIE4oIEElUvSAg1vDfjsXcdO20PSOxqvbMz37zv780348VaNXXs8bFVmZ97enbuRVn08uXAz2bnKk7VcYOjXq3ueEHZ8UVfCdkmA0lJyoAkB9CV+ic8uYz3sy8sWC/VikEj7znWvvHMpDVfC4rlVSuTURPX13bIfrQSeC59lr44g/fRk/qtBHr+fIjexC78FH9eX0vIfWjdKhLaUhZf6lKRvDQlh3ZZTosjZ46tr90g90LqFkjNxqQWpCY2ZF7ea5DugRzbt+F9E+R9qQKvgvvbV/6cMFLU56DPwWhOCkCp4nbElUDOTVPf7Zi/Xc0PxINOV0oy+iPnb8MIrlAS/LoLzZtjaL4sA68hv35EHGjijHAJfTVofPU8ZzFgifBdNofRHIwBUGFeXoM5BZhTw1dTvvt8azAJdxJsH8DujoGtII4OfCwqoJzyhFHW4GX0ujL0+zWBjwAcYQmZoCUAVAC7hHZBXkdwPECtAMyWL1KEOwLpByG9iP6qZHEfhvISTGT7+TbGDFo0kb1sd6M9g/kVPJ6c/YYujgKXllDHTrxbV7jc3QNJ51MzA3TrspuIpI7XIoDWsXCRuCapJWX7mHRsyJwgIslLgrGN5PLaOHT2k4f5/RA+hrbUVgUqNb99iLpI2CTkZ5SP2iJD60GlgdSnRUQ3dHIh7QIjd/mtL9n/BMYhF/ORtHaVlOFRDpEklUmIBlo2+LUsp7fTDgsI8Cmkr/FZx9uS3/9FXVywV19mxq8oW0hCLrErH1PjbuAgg6GJ8uHW6PsfUMs8RmfxsJ3F+862JEtDE08AP7h8e2nAhPZ1/o/BB4gyjh7EMRYjw9u6iksJaCwC5DeLgy2Xv6KlJup9F/FzgN5zVWgfC6WMtcfVZ0PVMt55RQWS0KTGl1M/RJWuKNMCOXGBTrToJtOq+vQKsqk/V5pRlL6mWzCdeY9GUUdWl2K2L6QJ1b8kmvgcgTsso7mfaGov44i2isxt/L014i7U3h03SjiFIAXArMhTwrYOGNvUE0CfpfLFr4OopaewnsuoIZylNQ1DQq8E9pB9lMvgSStM8qipsm2pFpNDCTM/jdk+7mFIJ1HqLXXX5TG8mTJL3sTTgMaympOCbB12FYCTxUgdFjmSggSrel0OoO9MG2kKVnQsoF/pmJdMmw37rIgUrTMribgONJeUx1mZAMvHlY6ORAc/C/9Z9/SWeED5NAWrDd8ZKdb1ivLAhma98VHjOB4L66JTN00c2VtSMdY1lP17YGHn1jnQyCY6HeSUyka3h1FNqQh6FtgFWGMexjMuG/XXh73Mkq1iQr892ErdKfhdg59ZYNXBSeLEx4kaKCnuX/2kWCeKkOovQUaa/BgUsomR91pve1OG3wCuBwmymQeYlPolkgtdVeWTjX5HWU7GdfKVUv3aqome43Gb6Hs3Qic6vUa7Y2O4pLPrbvLmWtk4ovzlLoHdG1lhDSLj9D7Nlcr1mYO3PGlwJyB7uVYfwalAryZ64qq4pjFi/w8i3DsH/1WE4xVhEsy9voowoqqLrhIBMjmKaOq6zpo3LI+q9cq22Wpy6uTH+ncQc8lWnui2zghzo9nPlqlAugKSXax6ph6aHeAOdYC/HzsW/qWE0R1Lrxb+ZSB3CpPRrW/zBpoAwvRQdI9ilS5jVek/A5pzvzxJlOs+C77328bur9/ZT/Qx6OG5pdeJPgcPuSM0oJOnaFZdX2YvRS1nHOJ/GnDO/xfv46fcAW3L'))
																					gom.script.cad.convert_to_actual_element (elements=[gom.app.project.inspection[str(pn1)]])
																																					
																					# point 2 / Start point of the segment of the angle measurement position on the left side of the cross profile.
																					my_dist = 0
																					j = min_dist_index
																					while my_dist < current_dist_p1:
																						dx = (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j-1)+'].x')) - (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].x'))
																						dy = (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j-1)+'].y')) - (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].y'))
																						#dx = (round(gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j-1)+'].x'),8)) - (round(gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].x'),8))
																						#dy = (round(gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j-1)+'].y'),8)) - (round(gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].y'),8))
																						my_dist_diff = math.sqrt((dx * dx) + (dy * dy))
																						my_dist = my_dist + my_dist_diff
																						j -=1
																					
																					j +=1	
																					pn2 ='w_'+ str(current_dist_p)+'_2'
																					pn2_x = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].x')
																					pn2_y = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].y')
																					pn2_z = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].z')
																					MCAD_ELEMENT=gom.script.primitive.create_point (
																						name=str(pn2), 
																						point={'point': gom.Vec3d (pn2_x, pn2_y, pn2_z)}, 
																						properties=gom.Binary ('eAHNV01sG0UY/QylLYYQUsqPEIJVGiAUHMdVSMFNaQhJiRApFURthQqW4107Bnvt7m5wXFTYigvixgG4IkFPEZV6QIgT4oDEAaUnEOIE4oIEElUvSAg1vDfjsXcdO20PSOxqvbMz37zv780348VaNXXs8bFVmZ97enbuRVn08uXAz2bnKk7VcYOjXq3ueEHZ8UVfCdkmA0lJyoAkB9CV+ic8uYz3sy8sWC/VikEj7znWvvHMpDVfC4rlVSuTURPX13bIfrQSeC59lr44g/fRk/qtBHr+fIjexC78FH9eX0vIfWjdKhLaUhZf6lKRvDQlh3ZZTosjZ46tr90g90LqFkjNxqQWpCY2ZF7ea5DugRzbt+F9E+R9qQKvgvvbV/6cMFLU56DPwWhOCkCp4nbElUDOTVPf7Zi/Xc0PxINOV0oy+iPnb8MIrlAS/LoLzZtjaL4sA68hv35EHGjijHAJfTVofPU8ZzFgifBdNofRHIwBUGFeXoM5BZhTw1dTvvt8azAJdxJsH8DujoGtII4OfCwqoJzyhFHW4GX0ujL0+zWBjwAcYQmZoCUAVAC7hHZBXkdwPECtAMyWL1KEOwLpByG9iP6qZHEfhvISTGT7+TbGDFo0kb1sd6M9g/kVPJ6c/YYujgKXllDHTrxbV7jc3QNJ51MzA3TrspuIpI7XIoDWsXCRuCapJWX7mHRsyJwgIslLgrGN5PLaOHT2k4f5/RA+hrbUVgUqNb99iLpI2CTkZ5SP2iJD60GlgdSnRUQ3dHIh7QIjd/mtL9n/BMYhF/ORtHaVlOFRDpEklUmIBlo2+LUsp7fTDgsI8Cmkr/FZx9uS3/9FXVywV19mxq8oW0hCLrErH1PjbuAgg6GJ8uHW6PsfUMs8RmfxsJ3F+862JEtDE08AP7h8e2nAhPZ1/o/BB4gyjh7EMRYjw9u6iksJaCwC5DeLgy2Xv6KlJup9F/FzgN5zVWgfC6WMtcfVZ0PVMt55RQWS0KTGl1M/RJWuKNMCOXGBTrToJtOq+vQKsqk/V5pRlL6mWzCdeY9GUUdWl2K2L6QJ1b8kmvgcgTsso7mfaGov44i2isxt/L014i7U3h03SjiFIAXArMhTwrYOGNvUE0CfpfLFr4OopaewnsuoIZylNQ1DQq8E9pB9lMvgSStM8qipsm2pFpNDCTM/jdk+7mFIJ1HqLXXX5TG8mTJL3sTTgMaympOCbB12FYCTxUgdFjmSggSrel0OoO9MG2kKVnQsoF/pmJdMmw37rIgUrTMribgONJeUx1mZAMvHlY6ORAc/C/9Z9/SWeED5NAWrDd8ZKdb1ivLAhma98VHjOB4L66JTN00c2VtSMdY1lP17YGHn1jnQyCY6HeSUyka3h1FNqQh6FtgFWGMexjMuG/XXh73Mkq1iQr892ErdKfhdg59ZYNXBSeLEx4kaKCnuX/2kWCeKkOovQUaa/BgUsomR91pve1OG3wCuBwmymQeYlPolkgtdVeWTjX5HWU7GdfKVUv3aqome43Gb6Hs3Qic6vUa7Y2O4pLPrbvLmWtk4ovzlLoHdG1lhDSLj9D7Nlcr1mYO3PGlwJyB7uVYfwalAryZ64qq4pjFi/w8i3DsH/1WE4xVhEsy9voowoqqLrhIBMjmKaOq6zpo3LI+q9cq22Wpy6uTH+ncQc8lWnui2zghzo9nPlqlAugKSXax6ph6aHeAOdYC/HzsW/qWE0R1Lrxb+ZSB3CpPRrW/zBpoAwvRQdI9ilS5jVek/A5pzvzxJlOs+C77328bur9/ZT/Qx6OG5pdeJPgcPuSM0oJOnaFZdX2YvRS1nHOJ/GnDO/xfv46fcAW3L'))
																					gom.script.cad.convert_to_actual_element (elements=[gom.app.project.inspection[str(pn2)]])
																					
																					
																					print ('p2 (guido 1) x: ' + str(pn2_x ))
																					print ('p2 (guido 1) y: ' + str(pn2_y ))
																					
																					# point 3 / End point of the segment of the angle measurement position on the left side of the cross profile.
																					my_dist = 0
																					j = min_dist_index
																					while my_dist < current_dist_p2:
																						dx = (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j-1)+'].x')) - (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].x'))
																						dy = (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j-1)+'].y')) - (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].y'))
																						#dx = (round(gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j-1)+'].x'),8)) - (round(gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].x'),8))
																						#dy = (round(gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j-1)+'].y'),8)) - (round(gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].y'),8))
																						my_dist_diff = math.sqrt((dx * dx) + (dy * dy))
																						my_dist = my_dist + my_dist_diff
																						j -=1
																						
																					j +=1	
																					pn3 ='w_'+ str(current_dist_p)+'_3'
																					pn3_x = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].x')
																					pn3_y = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].y')
																					pn3_z = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].z')
																					MCAD_ELEMENT=gom.script.primitive.create_point (
																						name=str(pn3), 
																						point={'point': gom.Vec3d (pn3_x, pn3_y, pn3_z)}, 
																						properties=gom.Binary ('eAHNV01sG0UY/QylLYYQUsqPEIJVGiAUHMdVSMFNaQhJiRApFURthQqW4107Bnvt7m5wXFTYigvixgG4IkFPEZV6QIgT4oDEAaUnEOIE4oIEElUvSAg1vDfjsXcdO20PSOxqvbMz37zv780348VaNXXs8bFVmZ97enbuRVn08uXAz2bnKk7VcYOjXq3ueEHZ8UVfCdkmA0lJyoAkB9CV+ic8uYz3sy8sWC/VikEj7znWvvHMpDVfC4rlVSuTURPX13bIfrQSeC59lr44g/fRk/qtBHr+fIjexC78FH9eX0vIfWjdKhLaUhZf6lKRvDQlh3ZZTosjZ46tr90g90LqFkjNxqQWpCY2ZF7ea5DugRzbt+F9E+R9qQKvgvvbV/6cMFLU56DPwWhOCkCp4nbElUDOTVPf7Zi/Xc0PxINOV0oy+iPnb8MIrlAS/LoLzZtjaL4sA68hv35EHGjijHAJfTVofPU8ZzFgifBdNofRHIwBUGFeXoM5BZhTw1dTvvt8azAJdxJsH8DujoGtII4OfCwqoJzyhFHW4GX0ujL0+zWBjwAcYQmZoCUAVAC7hHZBXkdwPECtAMyWL1KEOwLpByG9iP6qZHEfhvISTGT7+TbGDFo0kb1sd6M9g/kVPJ6c/YYujgKXllDHTrxbV7jc3QNJ51MzA3TrspuIpI7XIoDWsXCRuCapJWX7mHRsyJwgIslLgrGN5PLaOHT2k4f5/RA+hrbUVgUqNb99iLpI2CTkZ5SP2iJD60GlgdSnRUQ3dHIh7QIjd/mtL9n/BMYhF/ORtHaVlOFRDpEklUmIBlo2+LUsp7fTDgsI8Cmkr/FZx9uS3/9FXVywV19mxq8oW0hCLrErH1PjbuAgg6GJ8uHW6PsfUMs8RmfxsJ3F+862JEtDE08AP7h8e2nAhPZ1/o/BB4gyjh7EMRYjw9u6iksJaCwC5DeLgy2Xv6KlJup9F/FzgN5zVWgfC6WMtcfVZ0PVMt55RQWS0KTGl1M/RJWuKNMCOXGBTrToJtOq+vQKsqk/V5pRlL6mWzCdeY9GUUdWl2K2L6QJ1b8kmvgcgTsso7mfaGov44i2isxt/L014i7U3h03SjiFIAXArMhTwrYOGNvUE0CfpfLFr4OopaewnsuoIZylNQ1DQq8E9pB9lMvgSStM8qipsm2pFpNDCTM/jdk+7mFIJ1HqLXXX5TG8mTJL3sTTgMaympOCbB12FYCTxUgdFjmSggSrel0OoO9MG2kKVnQsoF/pmJdMmw37rIgUrTMribgONJeUx1mZAMvHlY6ORAc/C/9Z9/SWeED5NAWrDd8ZKdb1ivLAhma98VHjOB4L66JTN00c2VtSMdY1lP17YGHn1jnQyCY6HeSUyka3h1FNqQh6FtgFWGMexjMuG/XXh73Mkq1iQr892ErdKfhdg59ZYNXBSeLEx4kaKCnuX/2kWCeKkOovQUaa/BgUsomR91pve1OG3wCuBwmymQeYlPolkgtdVeWTjX5HWU7GdfKVUv3aqome43Gb6Hs3Qic6vUa7Y2O4pLPrbvLmWtk4ovzlLoHdG1lhDSLj9D7Nlcr1mYO3PGlwJyB7uVYfwalAryZ64qq4pjFi/w8i3DsH/1WE4xVhEsy9voowoqqLrhIBMjmKaOq6zpo3LI+q9cq22Wpy6uTH+ncQc8lWnui2zghzo9nPlqlAugKSXax6ph6aHeAOdYC/HzsW/qWE0R1Lrxb+ZSB3CpPRrW/zBpoAwvRQdI9ilS5jVek/A5pzvzxJlOs+C77328bur9/ZT/Qx6OG5pdeJPgcPuSM0oJOnaFZdX2YvRS1nHOJ/GnDO/xfv46fcAW3L'))
																					gom.script.cad.convert_to_actual_element (elements=[gom.app.project.inspection[str(pn3)]])
																						
																						
																					# point 4 / Center of the angular measurement position on the right side of the cross section
																					my_dist = 0	
																					j = min_dist_index
																					while my_dist < current_dist_p:
																						dx = (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j+1)+'].x')) - (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].x'))
																						dy = (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j+1)+'].y')) - (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].y'))
																						my_dist_diff = math.sqrt((dx * dx) + (dy * dy))
																						my_dist = my_dist + my_dist_diff
																						j +=1
																						
																					j -=1	
																					pn4 ='w_'+ str(current_dist_p)+'_4'
																					pn4_x = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].x')
																					pn4_y = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].y')
																					pn4_z = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].z')
																					MCAD_ELEMENT=gom.script.primitive.create_point (
																						name=str(pn4), 
																						point={'point': gom.Vec3d (pn4_x, pn4_y, pn4_z)}, 
																						properties=gom.Binary ('eAHNV01sG0UY/QylLYYQUsqPEIJVGiAUHMdVSMFNaQhJiRApFURthQqW4107Bnvt7m5wXFTYigvixgG4IkFPEZV6QIgT4oDEAaUnEOIE4oIEElUvSAg1vDfjsXcdO20PSOxqvbMz37zv780348VaNXXs8bFVmZ97enbuRVn08uXAz2bnKk7VcYOjXq3ueEHZ8UVfCdkmA0lJyoAkB9CV+ic8uYz3sy8sWC/VikEj7znWvvHMpDVfC4rlVSuTURPX13bIfrQSeC59lr44g/fRk/qtBHr+fIjexC78FH9eX0vIfWjdKhLaUhZf6lKRvDQlh3ZZTosjZ46tr90g90LqFkjNxqQWpCY2ZF7ea5DugRzbt+F9E+R9qQKvgvvbV/6cMFLU56DPwWhOCkCp4nbElUDOTVPf7Zi/Xc0PxINOV0oy+iPnb8MIrlAS/LoLzZtjaL4sA68hv35EHGjijHAJfTVofPU8ZzFgifBdNofRHIwBUGFeXoM5BZhTw1dTvvt8azAJdxJsH8DujoGtII4OfCwqoJzyhFHW4GX0ujL0+zWBjwAcYQmZoCUAVAC7hHZBXkdwPECtAMyWL1KEOwLpByG9iP6qZHEfhvISTGT7+TbGDFo0kb1sd6M9g/kVPJ6c/YYujgKXllDHTrxbV7jc3QNJ51MzA3TrspuIpI7XIoDWsXCRuCapJWX7mHRsyJwgIslLgrGN5PLaOHT2k4f5/RA+hrbUVgUqNb99iLpI2CTkZ5SP2iJD60GlgdSnRUQ3dHIh7QIjd/mtL9n/BMYhF/ORtHaVlOFRDpEklUmIBlo2+LUsp7fTDgsI8Cmkr/FZx9uS3/9FXVywV19mxq8oW0hCLrErH1PjbuAgg6GJ8uHW6PsfUMs8RmfxsJ3F+862JEtDE08AP7h8e2nAhPZ1/o/BB4gyjh7EMRYjw9u6iksJaCwC5DeLgy2Xv6KlJup9F/FzgN5zVWgfC6WMtcfVZ0PVMt55RQWS0KTGl1M/RJWuKNMCOXGBTrToJtOq+vQKsqk/V5pRlL6mWzCdeY9GUUdWl2K2L6QJ1b8kmvgcgTsso7mfaGov44i2isxt/L014i7U3h03SjiFIAXArMhTwrYOGNvUE0CfpfLFr4OopaewnsuoIZylNQ1DQq8E9pB9lMvgSStM8qipsm2pFpNDCTM/jdk+7mFIJ1HqLXXX5TG8mTJL3sTTgMaympOCbB12FYCTxUgdFjmSggSrel0OoO9MG2kKVnQsoF/pmJdMmw37rIgUrTMribgONJeUx1mZAMvHlY6ORAc/C/9Z9/SWeED5NAWrDd8ZKdb1ivLAhma98VHjOB4L66JTN00c2VtSMdY1lP17YGHn1jnQyCY6HeSUyka3h1FNqQh6FtgFWGMexjMuG/XXh73Mkq1iQr892ErdKfhdg59ZYNXBSeLEx4kaKCnuX/2kWCeKkOovQUaa/BgUsomR91pve1OG3wCuBwmymQeYlPolkgtdVeWTjX5HWU7GdfKVUv3aqome43Gb6Hs3Qic6vUa7Y2O4pLPrbvLmWtk4ovzlLoHdG1lhDSLj9D7Nlcr1mYO3PGlwJyB7uVYfwalAryZ64qq4pjFi/w8i3DsH/1WE4xVhEsy9voowoqqLrhIBMjmKaOq6zpo3LI+q9cq22Wpy6uTH+ncQc8lWnui2zghzo9nPlqlAugKSXax6ph6aHeAOdYC/HzsW/qWE0R1Lrxb+ZSB3CpPRrW/zBpoAwvRQdI9ilS5jVek/A5pzvzxJlOs+C77328bur9/ZT/Qx6OG5pdeJPgcPuSM0oJOnaFZdX2YvRS1nHOJ/GnDO/xfv46fcAW3L'))
																					gom.script.cad.convert_to_actual_element (elements=[gom.app.project.inspection[str(pn4)]])	
																					
																					# point 5 / Start point of the segment of the angle measurement position on the right side of the cross profile.
																					my_dist = 0	
																					j = min_dist_index
																					while my_dist < current_dist_p1:
																						dx = (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j+1)+'].x')) - (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].x'))
																						dy = (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j+1)+'].y')) - (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].y'))
																						#dx = (round(gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j+1)+'].x'),8)) - (round(gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].x'),8))
																						#dy = (round(gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j+1)+'].y'),8)) - (round(gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].y'),8))
																						my_dist_diff = math.sqrt((dx * dx) + (dy * dy))
																						my_dist = my_dist + my_dist_diff
																						j +=1
																						
																					j -=1	
																					pn5 ='w_'+ str(current_dist_p)+'_5'
																					pn5_x = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].x')
																					pn5_y = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].y')
																					pn5_z = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].z')
																					MCAD_ELEMENT=gom.script.primitive.create_point (
																						name=str(pn5), 
																						point={'point': gom.Vec3d (pn5_x, pn5_y, pn5_z)}, 
																						properties=gom.Binary ('eAHNV01sG0UY/QylLYYQUsqPEIJVGiAUHMdVSMFNaQhJiRApFURthQqW4107Bnvt7m5wXFTYigvixgG4IkFPEZV6QIgT4oDEAaUnEOIE4oIEElUvSAg1vDfjsXcdO20PSOxqvbMz37zv780348VaNXXs8bFVmZ97enbuRVn08uXAz2bnKk7VcYOjXq3ueEHZ8UVfCdkmA0lJyoAkB9CV+ic8uYz3sy8sWC/VikEj7znWvvHMpDVfC4rlVSuTURPX13bIfrQSeC59lr44g/fRk/qtBHr+fIjexC78FH9eX0vIfWjdKhLaUhZf6lKRvDQlh3ZZTosjZ46tr90g90LqFkjNxqQWpCY2ZF7ea5DugRzbt+F9E+R9qQKvgvvbV/6cMFLU56DPwWhOCkCp4nbElUDOTVPf7Zi/Xc0PxINOV0oy+iPnb8MIrlAS/LoLzZtjaL4sA68hv35EHGjijHAJfTVofPU8ZzFgifBdNofRHIwBUGFeXoM5BZhTw1dTvvt8azAJdxJsH8DujoGtII4OfCwqoJzyhFHW4GX0ujL0+zWBjwAcYQmZoCUAVAC7hHZBXkdwPECtAMyWL1KEOwLpByG9iP6qZHEfhvISTGT7+TbGDFo0kb1sd6M9g/kVPJ6c/YYujgKXllDHTrxbV7jc3QNJ51MzA3TrspuIpI7XIoDWsXCRuCapJWX7mHRsyJwgIslLgrGN5PLaOHT2k4f5/RA+hrbUVgUqNb99iLpI2CTkZ5SP2iJD60GlgdSnRUQ3dHIh7QIjd/mtL9n/BMYhF/ORtHaVlOFRDpEklUmIBlo2+LUsp7fTDgsI8Cmkr/FZx9uS3/9FXVywV19mxq8oW0hCLrErH1PjbuAgg6GJ8uHW6PsfUMs8RmfxsJ3F+862JEtDE08AP7h8e2nAhPZ1/o/BB4gyjh7EMRYjw9u6iksJaCwC5DeLgy2Xv6KlJup9F/FzgN5zVWgfC6WMtcfVZ0PVMt55RQWS0KTGl1M/RJWuKNMCOXGBTrToJtOq+vQKsqk/V5pRlL6mWzCdeY9GUUdWl2K2L6QJ1b8kmvgcgTsso7mfaGov44i2isxt/L014i7U3h03SjiFIAXArMhTwrYOGNvUE0CfpfLFr4OopaewnsuoIZylNQ1DQq8E9pB9lMvgSStM8qipsm2pFpNDCTM/jdk+7mFIJ1HqLXXX5TG8mTJL3sTTgMaympOCbB12FYCTxUgdFjmSggSrel0OoO9MG2kKVnQsoF/pmJdMmw37rIgUrTMribgONJeUx1mZAMvHlY6ORAc/C/9Z9/SWeED5NAWrDd8ZKdb1ivLAhma98VHjOB4L66JTN00c2VtSMdY1lP17YGHn1jnQyCY6HeSUyka3h1FNqQh6FtgFWGMexjMuG/XXh73Mkq1iQr892ErdKfhdg59ZYNXBSeLEx4kaKCnuX/2kWCeKkOovQUaa/BgUsomR91pve1OG3wCuBwmymQeYlPolkgtdVeWTjX5HWU7GdfKVUv3aqome43Gb6Hs3Qic6vUa7Y2O4pLPrbvLmWtk4ovzlLoHdG1lhDSLj9D7Nlcr1mYO3PGlwJyB7uVYfwalAryZ64qq4pjFi/w8i3DsH/1WE4xVhEsy9voowoqqLrhIBMjmKaOq6zpo3LI+q9cq22Wpy6uTH+ncQc8lWnui2zghzo9nPlqlAugKSXax6ph6aHeAOdYC/HzsW/qWE0R1Lrxb+ZSB3CpPRrW/zBpoAwvRQdI9ilS5jVek/A5pzvzxJlOs+C77328bur9/ZT/Qx6OG5pdeJPgcPuSM0oJOnaFZdX2YvRS1nHOJ/GnDO/xfv46fcAW3L'))
																					gom.script.cad.convert_to_actual_element (elements=[gom.app.project.inspection[str(pn5)]])	
																					
																					# point 6 / End point of the segment of the angle measurement position on the right side of the cross profile.
																					my_dist = 0	
																					j = min_dist_index
																					while my_dist < current_dist_p2:
																						dx = (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j+1)+'].x')) - (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].x'))
																						dy = (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j+1)+'].y')) - (gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].y'))
																						#dx = (round(gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j+1)+'].x'),8)) - (round(gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].x'),8))
																						#dy = (round(gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j+1)+'].y'),8)) - (round(gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].y'),8))
																						my_dist_diff = math.sqrt((dx * dx) + (dy * dy))
																						my_dist = my_dist + my_dist_diff
																						j +=1
																						
																					j -=1	
																					pn6 ='w_'+ str(current_dist_p)+'_6'
																					pn6_x = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].x')
																					pn6_y = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].y')
																					pn6_z = gom.app.project.actual_elements[curve_data].get ('coordinate['+str(j)+'].z')
																					MCAD_ELEMENT=gom.script.primitive.create_point (
																						name=str(pn6), 
																						point={'point': gom.Vec3d (pn6_x, pn6_y, pn6_z)}, 
																						properties=gom.Binary ('eAHNV01sG0UY/QylLYYQUsqPEIJVGiAUHMdVSMFNaQhJiRApFURthQqW4107Bnvt7m5wXFTYigvixgG4IkFPEZV6QIgT4oDEAaUnEOIE4oIEElUvSAg1vDfjsXcdO20PSOxqvbMz37zv780348VaNXXs8bFVmZ97enbuRVn08uXAz2bnKk7VcYOjXq3ueEHZ8UVfCdkmA0lJyoAkB9CV+ic8uYz3sy8sWC/VikEj7znWvvHMpDVfC4rlVSuTURPX13bIfrQSeC59lr44g/fRk/qtBHr+fIjexC78FH9eX0vIfWjdKhLaUhZf6lKRvDQlh3ZZTosjZ46tr90g90LqFkjNxqQWpCY2ZF7ea5DugRzbt+F9E+R9qQKvgvvbV/6cMFLU56DPwWhOCkCp4nbElUDOTVPf7Zi/Xc0PxINOV0oy+iPnb8MIrlAS/LoLzZtjaL4sA68hv35EHGjijHAJfTVofPU8ZzFgifBdNofRHIwBUGFeXoM5BZhTw1dTvvt8azAJdxJsH8DujoGtII4OfCwqoJzyhFHW4GX0ujL0+zWBjwAcYQmZoCUAVAC7hHZBXkdwPECtAMyWL1KEOwLpByG9iP6qZHEfhvISTGT7+TbGDFo0kb1sd6M9g/kVPJ6c/YYujgKXllDHTrxbV7jc3QNJ51MzA3TrspuIpI7XIoDWsXCRuCapJWX7mHRsyJwgIslLgrGN5PLaOHT2k4f5/RA+hrbUVgUqNb99iLpI2CTkZ5SP2iJD60GlgdSnRUQ3dHIh7QIjd/mtL9n/BMYhF/ORtHaVlOFRDpEklUmIBlo2+LUsp7fTDgsI8Cmkr/FZx9uS3/9FXVywV19mxq8oW0hCLrErH1PjbuAgg6GJ8uHW6PsfUMs8RmfxsJ3F+862JEtDE08AP7h8e2nAhPZ1/o/BB4gyjh7EMRYjw9u6iksJaCwC5DeLgy2Xv6KlJup9F/FzgN5zVWgfC6WMtcfVZ0PVMt55RQWS0KTGl1M/RJWuKNMCOXGBTrToJtOq+vQKsqk/V5pRlL6mWzCdeY9GUUdWl2K2L6QJ1b8kmvgcgTsso7mfaGov44i2isxt/L014i7U3h03SjiFIAXArMhTwrYOGNvUE0CfpfLFr4OopaewnsuoIZylNQ1DQq8E9pB9lMvgSStM8qipsm2pFpNDCTM/jdk+7mFIJ1HqLXXX5TG8mTJL3sTTgMaympOCbB12FYCTxUgdFjmSggSrel0OoO9MG2kKVnQsoF/pmJdMmw37rIgUrTMribgONJeUx1mZAMvHlY6ORAc/C/9Z9/SWeED5NAWrDd8ZKdb1ivLAhma98VHjOB4L66JTN00c2VtSMdY1lP17YGHn1jnQyCY6HeSUyka3h1FNqQh6FtgFWGMexjMuG/XXh73Mkq1iQr892ErdKfhdg59ZYNXBSeLEx4kaKCnuX/2kWCeKkOovQUaa/BgUsomR91pve1OG3wCuBwmymQeYlPolkgtdVeWTjX5HWU7GdfKVUv3aqome43Gb6Hs3Qic6vUa7Y2O4pLPrbvLmWtk4ovzlLoHdG1lhDSLj9D7Nlcr1mYO3PGlwJyB7uVYfwalAryZ64qq4pjFi/w8i3DsH/1WE4xVhEsy9voowoqqLrhIBMjmKaOq6zpo3LI+q9cq22Wpy6uTH+ncQc8lWnui2zghzo9nPlqlAugKSXax6ph6aHeAOdYC/HzsW/qWE0R1Lrxb+ZSB3CpPRrW/zBpoAwvRQdI9ilS5jVek/A5pzvzxJlOs+C77328bur9/ZT/Qx6OG5pdeJPgcPuSM0oJOnaFZdX2YvRS1nHOJ/GnDO/xfv46fcAW3L'))
																					gom.script.cad.convert_to_actual_element (elements=[gom.app.project.inspection[str(pn6)]])	
																					
																					
																					##### step 3
																					##### Calculation of the angles of the edge at the angle measurement positions

																					## Angle 1: via three points (angular measurement positions on the left and right side of the cross section and the point w_0, which represents the digitized cutting edge)

																					MCAD_ELEMENT=gom.script.inspection.create_angle_by_3_points (
																					angle_point=gom.app.project.actual_elements['w_0'], 
																					name='Angle-1_'+str(current_dist_p), 																
																					point1=gom.app.project.actual_elements['w_'+ str(current_dist_p)+'_1'], 
																					point2=gom.app.project.actual_elements['w_'+ str(current_dist_p)+'_4'], 
																					properties=gom.Binary ('eAHNV01oXFUUPmNiW1NrTeofpegjjRqtk58aY32NbaxJDWIS0RCLVIdk3pvJo/OX916cpBKd7nSnFNGdgj8IqZGuxIWtG0ER4kKU0p24VBC7UHDR+H335s68N5km6UJwhjdz5t5zv3POd849985EMZ+cfKRrXkaGnxgafk4m/CkvDGx7OOfm3UL4rF8suX7ouYHoV0KaZVeLtMguadmFob+WL5+cwfdT46PW88VMWJ7yXetgT2+/NVIMM9681durFq4sbZdHISXwvPXZvlH1fVJ/K4WGH3s4ehue8vjKUkL2QbpZpOKIJ4GUJCdTsiApyJ6cFlcWJ1eWbpC90NoJraGY1qgUxYHOiw8apLugR/kWfN8I/UDywMvh/e1Lf/Rx5iBm7sSMizEXsyk170lWCvjl4jPEmA9pVuZgjZIjU4v0An5KM9ZOw24R619eJiLDlsoO4wKDqYGnoZivAn88SJhbob8NWgFM+TBRgPHOS1wPcL4qkuCvDojQjaA50J+SMhwsqpVZtfqrMaLeAe2boJ1VFrtkEo6n5WE4P3uAaPdhvh0PZdIkcvbsyPtjF0U+/a6tKYlv+frShfELeffzVupYGACNDa2b5OztisbjwPKcTCti35sgxg5gnHvz3PipnTJ45BOOGC9rDAUyg3Vl+fXdjSlOVN4gwEOARPVE3JpDrbigJK0yma4j5/vMlmA7Adu2CayJenppS5AmfazoaXiYg2fTkNNyCgn3FVkFpOeLJOHG4MC9cGBCpc8WW44juVnUK+VnqhjHIDFejlKuR3sS63N4fDnzDfliYPSENpiOtVdlpn4Emu5HZgWpiPtNRAd2fcW0sTH6A3FNUk3p1XzoPUFEoKkdSblZO7B69MyH9/M3y7J1Q2t5REPLrx+lLZZuC/SPqRi1R6YP7FbFzV5Bj4hudmwB2gVgpK689iXHD2EeerEYuVULSiuNjcl4U2CS25PVVYbkYHxGTm+jHxYQuD0Ya3zVC1XNn/6mLXa4zfuSiSvKekZhh3L1A1pkz0QGqxv8+Nrs2+/Qyghmh/BQtvF9e1WTvXQBT4g42O8aWcCC6mv59933EKUHI+AxxpGp25LiJQs0dkzWN7upI1cu0lPD+vo+ubaJnwb0/k2hA2wUD0dCSUGnQL0LU6YITWoCmf05apRNm038xHkGsVZuMqg6aiOSTf+5uhBFWe/6Wou34DrzHmVRM6vPLsrnuwl17TZv+BlDODxzUpfpaiPniDaPYFb/2RixDefJ9iapDICkEJg5OSKUNWGUaSeEPUvli78ex3Ewiyr30EO4Sltqh4beCRwhkdTrxdOtMFlHCyrblpKYHGqY9d1YHeDdDu0WHEiWepfQty2s8vD5Kp4yLHpqTRK6JfiVBo6NmRI8ciUJDR51JTmMscUq0gC8qHnAuLpjUTJtDvyzIlr0zuwk4rqwnFUR29KHKu9RNmoaNXwb8bMP6DvEYRXTALw29V5vhdZNl0wqFnUntlHsadgxD2OK60ZtBkAhU47yi7Z9+MuiTsJ2EZzYwCqhLogTnydqqLTyG2hxr2agdW0cVoXhyNhiZUS9NnXBeuHplqtmUl9pOJ9UlcN12QgfnNkPD2pvXXUahdXg4F1D6aky76saDDFbz/0r8MFHTKxm3viS6lPf62ywRD4djLuKtbiNpBrXjPQ1nI/zQd7rEWqZaTRbnxdTS7r2C+ui2Wo1dqh4eQLh9EZFsAexBvU5zZ3K/ck7Lm8aPAlYvdyrD+BWoHcTIykoXrsx4/wPGG6cg/+K4XhH6L/ujtChuovuEiEy2Qk2dV9nz2uXA2oPUDZHTQrX5AIyx96agS53zmYZYW509VMyHUh3QFYXu57ph+YEyP7Jc+VunFj4W1eJnlh6t/BCy9pJ90ePvvUHaAIIg+pPgTmj2KU97Creus1d8JfHiHK9d8E9Pwarh1p/a/oXhaPXXgEkYg=='))
																				
																					w1 = (gom.app.project.actual_elements['Angle-1_'+str(current_dist_p)].get ('angle'))*180/math.pi
																					print ('Angle 1 in grad: ' + str(round(w1,1)))
																					
																					## Angle 2: Intersection angle of the two segments constructed from the start and end points of the segments
																					
																					# line 11 / line on the left side between the segment points 2 and 3
																					MCAD_ELEMENT=gom.script.primitive.create_line_by_2_points (
																					name='Line_'+str(current_dist_p)+'_11', 
																					point1=gom.app.project.actual_elements['w_'+ str(current_dist_p)+'_3'], 
																					point2=gom.app.project.actual_elements['w_'+ str(current_dist_p)+'_2'], 
																					properties=gom.Binary ('eAHNV01MXFUUPlOwrVSs1N80TX1SVGwdBipifcWCLVTSFDRKsJrqBOa9GV6cP957yI9Bpyu7dWF0aWJdEYl1oy4MKxMTE0w0mqY748JoTYzd2JhY/L57uTNvhinQhYkzeTNn7j33O+d859xz74wWcvGxxztmZWjw6YHB52XUH/fCwLYHs27OzYfP+YWi64eeG4h+xaRRmpukSZqlqRlDB5cun53E9zPPDlsvFNLhzLjvWoc7u3qsoUKY9matri61cGVxhzwBKYbnk4/3Davvs/pbKdT9aODoXXiCEyuLMdkH6TaRkiOeBFKUrIzLnCQhezIvriyMrSxuk73Q2gWtgSqtYSmIA52XDxqk+6BH+XZ83wL9QHLAy+L99St/dHPmMGbuxYyLMRezSTXvSUby+OXiM8SYD2lKpmGNkiPjC/QCfkoj1k7AbgHrX10iIsOW0k7jAoOpgKegmCsDf9RPmDugvx1aAUz5MJGH8fZLXA9wvkoS4682iNCNoDnQH5cZOFhQKzNq9ZcjRL0H2rdCO6MsdsgYHE/JY3B+6hDRHsJ8Kx7KpOnSL6O7MvPXltu/29+8cvqfZQyVtl0bOnbqt/ZPqWNhADTWtW6Ss7cjGo8Dy9MyoYh9f5QYO4GRuBJ+/vb5X/seeIkjxssKQ4FMYt2M/PzexhTHSucJ8CggUT0Rt6ZRKy4oSalMpmrI+Sa9Jdh2wO7ZBNZEPbG4JUiTPlb0BDzMwrMJyCl5DQn3FVl5pOezOOFG4MCDcGBUpc8WW04iuRnUK+XTZYzjkBgvRynXop3A+iweX859Rb4YGD2hDaZj7VWarB2BpnvBrCAV1X4T0YFdXzFtbAx/S1yTVFN6FR+6zhARaGpHUm7UDqz2nfvwYf5mWbZsaC2HaGj5rT7aYuk2Qf+4ilF7ZPrAblXc7BX0iOhmx+ahnQdG8uqbX3D8COahVxUjt2peaaWwMRlvEkxye7K6ZiA5GJ+U+e30wwICtwdjrV71Ylnzh79oix1u875k4oqynlbYoVz/gBbZM5HB8gY/uTb7zru0MoTZATyUbXzfXdZkL53DEyIO9rt6FrCg/Fr6fff9ROnECHis4sjUbVHxkgEaOybrm93UkavL9NSwvr5Prm3iU4A+sCl0gI3i4UgoKugkqHdhyhShSU0gUz9GjbJps4mfucgg1spN+lVHrUey6T/X56Io611fa/EWXGfeoyxqZvXZRfliglA3bvOGnxGEwzMneZmu1nOOaLMIZvXvjRH34DzZ0SClXpAUAjMrx4SyJowy7YSwZ6l88ddTOA6mUOUeeghXaUut0NA7gSMkknpdeBIKk3U0p7JtKYnJoYZZn8DqAO9WaDfhQLLUu4i+bWGVh8838MzAoqfWxKFbhF8p4NiYKcIjV+LQ4FFXlKMYWygj9cKLigeMK1EVJdPmwD8rokXvzE4irgvLGRWxLd2o8k5lo6JRwbcRP/uAvkMcVTH1wmtT77VWaN10ybhiUXdiG8Wegh3zMKZq3ajNAChkylF+0bYPf1nUcdgugBMbWEXUBXGq54kaKq3cBlrcq2lo3RiHVWE4MrZYGVGvTV2wXni6ZcuZ1FcazsdV5XBdJsIHZw7Ag8pbV51GYTU4eFdQOsvM+6oGQ8zWcv86fPARE6uZN764+tT3OhsskU8H465irdpGXI1rRrrrzlfzQd5rESqZqTdbmxdTS7r28+ui2Wo1tql4eQLh9EZFsAexBvU5zZ3K/ck7Lm8aPAlYvdyrj+BWoHcTI8krXhOYcf4HDNfPwX/FcHVH6LnpjtCmuovuEiEy2Q42dV9nz2uVQ2oPUDZHTRLX5Dwyx96ahi53zmYZYW509VMyHUh3QFYXu57ph+YEyPzJc2U/Tiz8rStFTyy9W3ihZe2keqJH3/oDNAaE/pboGcUu7WFX8dZt7oI/PUmUm70L3vl9sHqk5UrDvzYm2h0Bd3c='))
																					
																					# check azimuth of line 11
																					aze_11 = (math.atan2((pn3_y - pn2_y), (pn3_x - pn2_x)) * 180.0 / math.pi) + 90.0
																					print ("azimuth_11: " + str(aze_11))
																					az_11 = -(math.atan2((pn2_y - pn3_y), (pn2_x - pn3_x)) * 180.0 / math.pi) + 90.0
																					if az_11 < 0:
																						az_11 = az_11 + 360
																					print ("Azimut line from two points: " + str(round(az_11,2)))
																					
																					# line 12 / line on the right side between the segment points 5 and 6
																					MCAD_ELEMENT=gom.script.primitive.create_line_by_2_points (
																					name='Line_'+str(current_dist_p)+'_12', 
																					point1=gom.app.project.actual_elements['w_'+ str(current_dist_p)+'_6'], 
																					point2=gom.app.project.actual_elements['w_'+ str(current_dist_p)+'_5'], 
																					properties=gom.Binary ('eAHNV01MXFUUPlOwrVSs1N80TX1SVGwdBipifcWCLVTSFDRKsJrqBOa9GV6cP957yI9Bpyu7dWF0aWJdEYl1oy4MKxMTE0w0mqY748JoTYzd2JhY/L57uTNvhinQhYkzeTNn7j33O+d859xz74wWcvGxxztmZWjw6YHB52XUH/fCwLYHs27OzYfP+YWi64eeG4h+xaRRmpukSZqlqRlDB5cun53E9zPPDlsvFNLhzLjvWoc7u3qsoUKY9matri61cGVxhzwBKYbnk4/3Davvs/pbKdT9aODoXXiCEyuLMdkH6TaRkiOeBFKUrIzLnCQhezIvriyMrSxuk73Q2gWtgSqtYSmIA52XDxqk+6BH+XZ83wL9QHLAy+L99St/dHPmMGbuxYyLMRezSTXvSUby+OXiM8SYD2lKpmGNkiPjC/QCfkoj1k7AbgHrX10iIsOW0k7jAoOpgKegmCsDf9RPmDugvx1aAUz5MJGH8fZLXA9wvkoS4682iNCNoDnQH5cZOFhQKzNq9ZcjRL0H2rdCO6MsdsgYHE/JY3B+6hDRHsJ8Kx7KpOnSL6O7MvPXltu/29+8cvqfZQyVtl0bOnbqt/ZPqWNhADTWtW6Ss7cjGo8Dy9MyoYh9f5QYO4GRuBJ+/vb5X/seeIkjxssKQ4FMYt2M/PzexhTHSucJ8CggUT0Rt6ZRKy4oSalMpmrI+Sa9Jdh2wO7ZBNZEPbG4JUiTPlb0BDzMwrMJyCl5DQn3FVl5pOezOOFG4MCDcGBUpc8WW04iuRnUK+XTZYzjkBgvRynXop3A+iweX859Rb4YGD2hDaZj7VWarB2BpnvBrCAV1X4T0YFdXzFtbAx/S1yTVFN6FR+6zhARaGpHUm7UDqz2nfvwYf5mWbZsaC2HaGj5rT7aYuk2Qf+4ilF7ZPrAblXc7BX0iOhmx+ahnQdG8uqbX3D8COahVxUjt2peaaWwMRlvEkxye7K6ZiA5GJ+U+e30wwICtwdjrV71Ylnzh79oix1u875k4oqynlbYoVz/gBbZM5HB8gY/uTb7zru0MoTZATyUbXzfXdZkL53DEyIO9rt6FrCg/Fr6fff9ROnECHis4sjUbVHxkgEaOybrm93UkavL9NSwvr5Prm3iU4A+sCl0gI3i4UgoKugkqHdhyhShSU0gUz9GjbJps4mfucgg1spN+lVHrUey6T/X56Io611fa/EWXGfeoyxqZvXZRfliglA3bvOGnxGEwzMneZmu1nOOaLMIZvXvjRH34DzZ0SClXpAUAjMrx4SyJowy7YSwZ6l88ddTOA6mUOUeeghXaUut0NA7gSMkknpdeBIKk3U0p7JtKYnJoYZZn8DqAO9WaDfhQLLUu4i+bWGVh8838MzAoqfWxKFbhF8p4NiYKcIjV+LQ4FFXlKMYWygj9cKLigeMK1EVJdPmwD8rokXvzE4irgvLGRWxLd2o8k5lo6JRwbcRP/uAvkMcVTH1wmtT77VWaN10ybhiUXdiG8Wegh3zMKZq3ajNAChkylF+0bYPf1nUcdgugBMbWEXUBXGq54kaKq3cBlrcq2lo3RiHVWE4MrZYGVGvTV2wXni6ZcuZ1FcazsdV5XBdJsIHZw7Ag8pbV51GYTU4eFdQOsvM+6oGQ8zWcv86fPARE6uZN764+tT3OhsskU8H465irdpGXI1rRrrrzlfzQd5rESqZqTdbmxdTS7r28+ui2Wo1tql4eQLh9EZFsAexBvU5zZ3K/ck7Lm8aPAlYvdyrj+BWoHcTI8krXhOYcf4HDNfPwX/FcHVH6LnpjtCmuovuEiEy2Q42dV9nz2uVQ2oPUDZHTRLX5Dwyx96ahi53zmYZYW509VMyHUh3QFYXu57ph+YEyPzJc2U/Tiz8rStFTyy9W3ihZe2keqJH3/oDNAaE/pboGcUu7WFX8dZt7oI/PUmUm70L3vl9sHqk5UrDvzYm2h0Bd3c='))
																				
																					# check azimuth of line 12
																					az_12 = -(math.atan2((pn5_y - pn6_y), (pn5_x - pn6_x)) * 180.0 / math.pi) + 90.0
																					print ("Azimut line from two points: " + str(round(az_12,2)))
																					if az_12 < 0:
																						az_12 = az_12 + 360
																					print ("Azimut line from two points: " + str(round(az_12,2)))
																					
																					# Calculation of the intersection angle of the line 11 and line 12
																					MCAD_ELEMENT=gom.script.inspection.create_angle_by_2_directions (
																					direction1={'glue_transformed': False, 'inverted': True, 'target': gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_11'], 'type': 'direction'}, 
																					direction2={'glue_transformed': False, 'inverted': True, 'target': gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_12'], 'type': 'direction'}, 
																					name='Angle-2_'+str(current_dist_p), 
																					properties=gom.Binary ('eAHNV01MXFUUPtNii2htaetPmqY+ARWtw18R6ysWrNCiETRKsDHVEea9GSbOH+89BGrQ6c7oykWjyya1bohNWRkXRjcmGhNcGI3pSuOmSTXGRmNiIvh993Jn3humQBcmzuTNnLn33O+c851zz70zWsjFxx5um5WhwccHBp+TUW88E/i2PZh1c24+eNYrFF0vyLi+6FdM6mRHgzTIDmnYgaF3Fi+fmsT3iWeGrecLqWBm3HOtro7OHmuoEKQys1Znp1q4tLBdHoEUw3Puo/3D6vuU/lYKNT/2cHQvnqknlxZish/SrSIlRzLiS1GyMi5zkoCckdPiyvzY0sIW2QetW6A1ENEaloI40HnxQYN0F/Qo34bvm6DvSw54Wby/fOm3bs50YeZOzLgYczGbUPMZSUsev1x8BhjzIE3JNKxRcmR8nl7AT6nD2gnYLWD9yxeJyLClVG9cYDAV8CQUc2XgC/2E2QX9bdDyYcqDiTyMt/7A9QDnqyQx/mqBCN0QmgP9cZmBgwW1Mq1WfzpC1DugfTO008pim4zB8aQcgvNTB4l2H+ab8FAmTbvqu5Yv2J/3XWnZ+2Hxn+W+S68c+PHElsGj/b9ePUQdCzqgsaZ1k5x9beF4HFielglF7PujxKgHxqWv/rjnz7NX+prf5ojxssKQL5NYNyM/v7c+xbHSWwR4CJConpBb06gVF5QkVSaTVeR8ndoUbCtgd28Aa6KeWNgUpEkfK3oCHmbh2QTkpLyKhHuKrDzS83GccCNw4F44MKrSZ4stx5HcNOqV8tNljGOQGC9HKVejPYH1WTyenPmCfDEwekIbTMfqqzRZPQJN9wOzglRE/SaiA7ueYtrYGP6GuCappvQqPnSeJCLQ1I6kXKcdWOk7c/5+/mZZNq5rLYdoaPnNPtpi6TZA/5iKUXtk+sBOVdzsFfSI6GbH5qGdB0bi2hufcPww5qEXiZFbNa+0ktiYjDcBJrk9WV0zkByMT8rpbfTDAgK3B2ONrnqhrPndX7TFDrdxXzJxhVlPKexAls/RInsmMlje4MdXZ989SytDmB3AQ9nG9+1lTfbSOTwB4mC/q2UBC8qvi7/svJsoHRgBjxGOTN0WFS9poLFjsr7ZTR259hk9Nayv7ZOrm/gpQDdvCO1jo2RwJBQVdALUuzBlitCkxpep78NG2bTZxE8uMojVcpN+1VFrkWz6z/JcGGWt66st3oLrzHuYRc2sPrsoL7YT6vpt3vAzgnB45iQu09VazhFtFsGs/L0+4m6cJ9u3SqkXJAXAzMpRoawJo0w7AexZKl/89RiOgylUeQY9hKu0pSZo6J3AERJJvU487QqTdTSnsm0picmhhlnfjtU+3k3QbsCBZKl3EX3bwqoMPl/HMwOLGbUmDt0i/EoCx8ZMER65EocGj7qiHMHYfBmpF15UPGBc7ZEomTYH/lkhLXpndhJxXVhOq4ht6UaVdygbFY0Kvo342Qf0HeKIiqkXXpt6r7ZC66ZLxhWLuhPbKPYk7JiHMUV1wzZ9oJApR/lF2x78ZVHHYbsATmxgFVEXxInOEzVQWrl1tLhXU9C6Pg6rwnBkbLEywl6bumC98HTLljOprzScj6vK4bp0iA/ONMODyltXnUZhNTh4V1A6ysx7qgYDzFZz/xp88BATq5k3vrj61Pc6GyyRTwfjrmItaiOuxjUj3TXno3yQ92qESmZqzVbnxdSSrv38mmg2W40tKl6eQDi9URHsQaxBfU5zp3J/8o7LmwZPAlYv9+oDuBXo3cRI8orXdsw4/wOGa+fgv2I42hF6brgjtKjuortEgEy2gk3d19nzmuSg2gOUzVGTwDU5j8yxt6agy52zUUaYG139lEwH0h2Q1cWuZ/qhOQHSv/NcOYATC3/rSuETS+8WXmhZO8me8NG39gCNAaG/MXxGsUtnsKt46zZ3wZ8eJcqN3gX3fOuvHG68uvVfieXbZgFYOg=='))
																					
																					w2 = (gom.app.project.actual_elements['Angle-2_'+str(current_dist_p)].get ('angle'))*180/math.pi
																					print ('Angle 2 in grad: ' + str(round(w2,1)))
																					
																					w2_x = gom.app.project.actual_elements['Angle-2_'+str(current_dist_p)].get ('center_coordinate.x')
																					w2_y = gom.app.project.actual_elements['Angle-2_'+str(current_dist_p)].get ('center_coordinate.y')
																					w2_dist = math.sqrt((w2_x * w2_x) + (w2_y * w2_y))
																					
																					
																					## Angle 3: Intersection angle from two lines, constructed as BestFit on the points of the cross section in the area of the segment
																					
																					# line 21 / BestFit of the cross-section at point 1 in the size of the segment
																					gom.script.cad.show_element_exclusively (elements=[gom.app.project.actual_elements[curve_data]])
																					gom.script.selection3d.select_inside_sphere (
																						center=gom.app.project.actual_elements['w_'+ str(current_dist_p)+'_1'], 
																						radius=(dist_segment/2))
																					MCAD_ELEMENT=gom.script.primitive.create_fitting_line (
																						method='best_fit', 
																						name='Line_'+str(current_dist_p)+'_21', 
																						properties=gom.Binary ('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'), 
																						sigma=2)
																					
																					# check azimuth of line 21
																					# start point line 21
																					pA_x =  gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_21'].get ('coordinate1.x')
																					pA_y =  gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_21'].get ('coordinate1.y')
																					# end  point line 21
																					pE_x =  gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_21'].get ('coordinate2.x')
																					pE_y =  gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_21'].get ('coordinate2.y')
																					
																					az_21 = -(math.atan2((pE_y - pA_y), (pE_x - pA_x)) * 180.0 / math.pi) + 90.0
																					if az_21 < 0:
																						az_21 = az_21 + 360
																					print ("Azimut BestFit line 21: " + str(round(az_21,2)))
																					
																					# Direction of line 21 analyze in relation to line 11
																					if (az_21 - az_11) > 45 or (az_21 - az_11) < -45:										
																						# delete line 21
																						gom.script.cad.delete_element (elements=[gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_21']])
																						# create new line 21 with reversed direction
																						gom.script.cad.show_element_exclusively (elements=[gom.app.project.actual_elements[curve_data]])
																						gom.script.selection3d.select_inside_sphere (
																							center=gom.app.project.actual_elements['w_'+ str(current_dist_p)+'_1'], 
																							radius=(dist_segment/2))
																						MCAD_ELEMENT=gom.script.primitive.create_fitting_line (
																							invert_calculated_direction=True, 
																							method='best_fit', 
																							name='Line_'+str(current_dist_p)+'_21', 
																							properties=gom.Binary ('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'), 
																							sigma=2)
																					
																					# start point line 21
																					pA_x =  gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_21'].get ('coordinate1.x')
																					pA_y =  gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_21'].get ('coordinate1.y')
																					# end  point line 21
																					pE_x =  gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_21'].get ('coordinate2.x')
																					pE_y =  gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_21'].get ('coordinate2.y')
																					
																					az_21 = -(math.atan2((pE_y - pA_y), (pE_x - pA_x)) * 180.0 / math.pi) + 90.0
																					if az_21 < 0:
																						az_21 = az_21 + 360
																					print ("Azimut BestFit line 21: " + str(round(az_21,2)))



																					# line 22 / BestFit of the cross-section at point 4 in the size of the segment
																					gom.script.cad.show_element_exclusively (elements=[gom.app.project.actual_elements[curve_data]])
																					gom.script.selection3d.select_inside_sphere (
																						center=gom.app.project.actual_elements['w_'+ str(current_dist_p)+'_4'], 
																						radius=(dist_segment/2))
																					MCAD_ELEMENT=gom.script.primitive.create_fitting_line (
																						method='best_fit', 
																						name='Line_'+str(current_dist_p)+'_22', 
																						properties=gom.Binary ('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'), 
																						sigma=2)
																					
																					# check azimuth of line 22
																					# start point line 22
																					pA_x =  gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_22'].get ('coordinate1.x')
																					pA_y =  gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_22'].get ('coordinate1.y')
																					# end point line 22
																					pE_x =  gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_22'].get ('coordinate2.x')
																					pE_y =  gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_22'].get ('coordinate2.y')
																					
																					az_22 = -(math.atan2((pE_y - pA_y), (pE_x - pA_x)) * 180.0 / math.pi) + 90.0
																					print ("Azimut BestFit line: " + str(round(az_22,2)))
																					if az_22 < 0:
																						az_22 = az_22 + 360
																					print ("Azimut BestFit line: " + str(round(az_22,2)))
																					
																					# Direction of line 22 analyze in relation to line 12
																					if (az_22 - az_12) > 45 or (az_22 - az_12) < -45:																	
																						# delete line 22
																						gom.script.cad.delete_element (elements=[gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_22']])
																						# # create new line 21 with reversed direction
																						gom.script.cad.show_element_exclusively (elements=[gom.app.project.actual_elements[curve_data]])
																						gom.script.selection3d.select_inside_sphere (
																							center=gom.app.project.actual_elements['w_'+ str(current_dist_p)+'_4'], 
																							radius=(dist_segment/2))
																						MCAD_ELEMENT=gom.script.primitive.create_fitting_line (
																							invert_calculated_direction=True, 
																							method='best_fit', 
																							name='Line_'+str(current_dist_p)+'_22', 
																							properties=gom.Binary ('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'), 
																							sigma=2)
																							
																					# start point line 22
																					pA_x =  gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_22'].get ('coordinate1.x')
																					pA_y =  gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_22'].get ('coordinate1.y')
																					# end point line 22
																					pE_x =  gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_22'].get ('coordinate2.x')
																					pE_y =  gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_22'].get ('coordinate2.y')
																					
																					az_22 = -(math.atan2((pE_y - pA_y), (pE_x - pA_x)) * 180.0 / math.pi) + 90.0
																					if az_22 < 0:
																						az_22 = az_22 + 360
																					print ("Azimut BestFit line 22: " + str(round(az_22,2)))		
																							
																					# Calculation of the intersection angle of the line 21 and line 22																					
																					MCAD_ELEMENT=gom.script.inspection.create_angle_by_2_directions (
																						direction1={'glue_transformed': False, 'inverted': True, 'target': gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_21'], 'type': 'direction'}, 
																						direction2={'glue_transformed': False, 'inverted': True, 'target': gom.app.project.actual_elements['Line_'+str(current_dist_p)+'_22'], 'type': 'direction'}, 
																						name='Angle-3_'+str(current_dist_p), 
																						properties=gom.Binary ('eAHNV01MXFUUPtNii2htaetPmqY+ARWtw18R6ysWrNCiETRKsDHVEea9GSbOH+89BGrQ6c7oykWjyya1bohNWRkXRjcmGhNcGI3pSuOmSTXGRmNiIvh993Jn3humQBcmzuTNnLn33O+c851zz70zWsjFxx5um5WhwccHBp+TUW88E/i2PZh1c24+eNYrFF0vyLi+6FdM6mRHgzTIDmnYgaF3Fi+fmsT3iWeGrecLqWBm3HOtro7OHmuoEKQys1Znp1q4tLBdHoEUw3Puo/3D6vuU/lYKNT/2cHQvnqknlxZish/SrSIlRzLiS1GyMi5zkoCckdPiyvzY0sIW2QetW6A1ENEaloI40HnxQYN0F/Qo34bvm6DvSw54Wby/fOm3bs50YeZOzLgYczGbUPMZSUsev1x8BhjzIE3JNKxRcmR8nl7AT6nD2gnYLWD9yxeJyLClVG9cYDAV8CQUc2XgC/2E2QX9bdDyYcqDiTyMt/7A9QDnqyQx/mqBCN0QmgP9cZmBgwW1Mq1WfzpC1DugfTO008pim4zB8aQcgvNTB4l2H+ab8FAmTbvqu5Yv2J/3XWnZ+2Hxn+W+S68c+PHElsGj/b9ePUQdCzqgsaZ1k5x9beF4HFielglF7PujxKgHxqWv/rjnz7NX+prf5ojxssKQL5NYNyM/v7c+xbHSWwR4CJConpBb06gVF5QkVSaTVeR8ndoUbCtgd28Aa6KeWNgUpEkfK3oCHmbh2QTkpLyKhHuKrDzS83GccCNw4F44MKrSZ4stx5HcNOqV8tNljGOQGC9HKVejPYH1WTyenPmCfDEwekIbTMfqqzRZPQJN9wOzglRE/SaiA7ueYtrYGP6GuCappvQqPnSeJCLQ1I6kXKcdWOk7c/5+/mZZNq5rLYdoaPnNPtpi6TZA/5iKUXtk+sBOVdzsFfSI6GbH5qGdB0bi2hufcPww5qEXiZFbNa+0ktiYjDcBJrk9WV0zkByMT8rpbfTDAgK3B2ONrnqhrPndX7TFDrdxXzJxhVlPKexAls/RInsmMlje4MdXZ989SytDmB3AQ9nG9+1lTfbSOTwB4mC/q2UBC8qvi7/svJsoHRgBjxGOTN0WFS9poLFjsr7ZTR259hk9Nayv7ZOrm/gpQDdvCO1jo2RwJBQVdALUuzBlitCkxpep78NG2bTZxE8uMojVcpN+1VFrkWz6z/JcGGWt66st3oLrzHuYRc2sPrsoL7YT6vpt3vAzgnB45iQu09VazhFtFsGs/L0+4m6cJ9u3SqkXJAXAzMpRoawJo0w7AexZKl/89RiOgylUeQY9hKu0pSZo6J3AERJJvU487QqTdTSnsm0picmhhlnfjtU+3k3QbsCBZKl3EX3bwqoMPl/HMwOLGbUmDt0i/EoCx8ZMER65EocGj7qiHMHYfBmpF15UPGBc7ZEomTYH/lkhLXpndhJxXVhOq4ht6UaVdygbFY0Kvo342Qf0HeKIiqkXXpt6r7ZC66ZLxhWLuhPbKPYk7JiHMUV1wzZ9oJApR/lF2x78ZVHHYbsATmxgFVEXxInOEzVQWrl1tLhXU9C6Pg6rwnBkbLEywl6bumC98HTLljOprzScj6vK4bp0iA/ONMODyltXnUZhNTh4V1A6ysx7qgYDzFZz/xp88BATq5k3vrj61Pc6GyyRTwfjrmItaiOuxjUj3TXno3yQ92qESmZqzVbnxdSSrv38mmg2W40tKl6eQDi9URHsQaxBfU5zp3J/8o7LmwZPAlYv9+oDuBXo3cRI8orXdsw4/wOGa+fgv2I42hF6brgjtKjuortEgEy2gk3d19nzmuSg2gOUzVGTwDU5j8yxt6agy52zUUaYG139lEwH0h2Q1cWuZ/qhOQHSv/NcOYATC3/rSuETS+8WXmhZO8me8NG39gCNAaG/MXxGsUtnsKt46zZ3wZ8eJcqN3gX3fOuvHG68uvVfieXbZgFYOg=='))
																																									
																					w3 = (gom.app.project.actual_elements['Angle-3_'+str(current_dist_p)].get ('angle'))*180/math.pi
																					print ('Winkel 3 in grad: ' + str(round(w3,1)))
																					
																					w3_x = gom.app.project.actual_elements['Angle-3_'+str(current_dist_p)].get ('center_coordinate.x')
																					w3_y = gom.app.project.actual_elements['Angle-3_'+str(current_dist_p)].get ('center_coordinate.y')
																					w3_dist = math.sqrt((w3_x * w3_x) + (w3_y * w3_y))

																					# write all angles in table
																					myfile.write ( str(curve_ce_re_sec_l[:-9]))
																					myfile.write (","+str(i))
																					myfile.write (","+str(current_dist_p))																
																					myfile.write (","+str(dist_segment))
																					myfile.write (","+str(format(w1,'.1f')))
																					myfile.write (","+str(format(w2,'.1f')))
																					myfile.write (","+str(format(w3,'.1f')))
																					
																					myfile.write ("\n")
																					i += 1
																					
																					gom.script.sys.save_project_as (file_name=str(root5) + "/" + str(curve_ce_re_sec_l[:-9]+"_w_"+ str(format(dist_angles,'.1f')) + "_" + str(format(dist_segment,'.1f')) + ".ginspect"))
																	
																		except:
																			print ("does not work")
																			myerror.write ("Section: " + str(curve_ce_re_sec_l[:-9]) + " angle / azimuth could not be calculated" + "\n")
														
myerror.close()
mylog.close()

print ("fertsch :-)")
