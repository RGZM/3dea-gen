# -*- coding: utf-8 -*-

## Script for using in the GOM Inspect Professional 2016 software

## transforms the curves of the cross sections lying in the 3D coordinate system into a 2D system to simplify calculations on the curve
## Anja Cramer, Guido Heinz RGZM/WissIT, März 2019

## settings
### input folder

## inputs
### cross sections created in script 2 in *.iges format
### the manually digitized tool edge in *.iges format

## outputs
### Views of the cross-sections 
### as *.png for quick visual control with many data sets, 
### as *.asc file with the point coordinates (x,y) for software-independent evaluation and 
### as *.iges file. 
### The GOM-Inspect-Project with the performed transformations is also saved as *_local.ginspect file.


import gom, os, re, datetime
import os.path
from os import path

RESULT=gom.script.sys.execute_user_defined_dialog (content='<dialog>' \
' <title>Select Input Folder</title>' \
' <style></style>' \
' <control id="OkCancel"/>' \
' <position>automatic</position>' \
' <embedding></embedding>' \
' <sizemode>fixed</sizemode>' \
' <size height="154" width="570"/>' \
' <content columns="1" rows="1">' \
'  <widget rowspan="1" type="input::file" row="0" column="0" columnspan="1">' \
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

input_pfad = RESULT.file

# Setting of folders and cross-sections to be aligned
# here detailed selection of folders is made .... to reduce calculation time
folder_list = [""]
sec_folder = "SEC-DIST"

# LOG-file
# text file for checking the data
now = datetime.datetime.now()
now_string = str(now.year)+str(now.month)+str(now.day)+'_'+str(now.hour)+''+str(now.minute)
print(now_string)

myfile = open(input_pfad + "/"+"Info_EAP_3_projections_" + now_string + ".csv", "w")
myfile.write ("Script started: " + str(now.day)+ "." + str(now.month) + "." + str(now.year) + " um " + str(now.hour)+ ":" +str(now.minute)+ " Uhr"+ "\n")


##########################  start  ####################

for root, dirs, files in os.walk (input_pfad):
	for mesh in files:
		if os.path.splitext(mesh)[-1]==".stl":
			print ("************************")
			print ("1 - 3d mesh: ", mesh)
			myfile.write ("************************"+ "\n")
			
									
			for root2, dirs2, files2 in os.walk (root):								
				# Regex --> tool edge
				pattern_ce = '^' + mesh[:-4] + '[_][A-Z]{1}[0-9]{1}.igs$'
				anz_ce = 0
				for curve_ce in files2:
					result = re.search(pattern_ce, curve_ce)
					if result:
						anz_ce = anz_ce +1
						print ("2 - IGES Cutting edge : ", curve_ce)

						for root3, dirs3, files3 in os.walk (root):							
							# Regex --> reference edge
							pattern_ce_re = '^' + curve_ce[:-4]+'_RE.igs$'
							anz_ce_re = 0
							for curve_ce_re in files3:
								result = re.search(pattern_ce_re, curve_ce_re)
								if result:
									anz_ce_re = anz_ce_re +1
									print ("3 - IGES Reference curve: ", curve_ce_re)
									
									# search cross sections
									
									for root4, dirs4, files4 in os.walk (root):
										# Regex -->Sections
										pattern_ce_re_sec = '^' + curve_ce_re[:-4] + '[_]SEC[\-][0-9]{2}_POS[\-](\d*.\d*).igs$'
										anz_ce_re_sec = 0										
										for curve_ce_re_sec in files4:
											result = re.search(pattern_ce_re_sec, curve_ce_re_sec)
											if result:
												anz_ce_re_sec = anz_ce_re_sec +1
												print ("4 - IGES Section: ", curve_ce_re_sec)

												# create folder for new data
												root_sec = root4 + "/" + curve_ce[:-4]
												if not (path.exists(root_sec)):
													os.mkdir (root_sec)	
													
												# use only folders selected in folder_list and in sec_folder
												for f in folder_list:
													if f in root_sec:
														if sec_folder in root_sec:
															
															# data found and start processing
															
															# write log-file
															myfile.write ("processing: " + curve_ce_re_sec +  "\n")
															now = datetime.datetime.now()
															myfile.write ("Start: " + str(now.hour)+':'+str(now.minute)+" h"+ "\n")
															
															# create GOM project
															gom.script.sys.close_project ()
															gom.script.sys.create_project ()
															gom.script.sys.switch_to_inspection_workspace ()
															
															# import iges files (reference curve and section)
															gom.script.sys.import_cad (
																files=[gom.File (root + "/" + curve_ce)], 
																filter='SHOW', 
																import_fta=False, 
																repair_mode=5, 
																triangulation_mode='high')
															gom.script.sys.import_cad (
																files=[gom.File (root4 + "/" +  curve_ce_re_sec)],
																filter='SHOW', 
																import_fta=False, 
																repair_mode=5, 
																triangulation_mode='high')
															
															# convert cad elements to actual element
															gom.script.cad.convert_to_actual_element (elements=[gom.app.project.inspection[curve_ce_re_sec[:-4]]])
															gom.script.cad.convert_to_actual_element (elements=[gom.app.project.inspection[curve_ce[:-4]]])
															
															# project section to 2d 

															# delete small elements on section curve (< 1mm)
															gom.script.cad.show_element_exclusively (elements=[gom.app.project.actual_elements[curve_ce_re_sec[:-4]]])
															gom.script.selection3d.select_all ()			
															gom.script.section.delete_segments (max_length=1.00000000e+00)
			
															# define 3 points on the curve for the 3-2-1 alignment
																											
															anzpkt = gom.app.project.actual_elements[curve_ce_re_sec[:-4]].get ('num_points')
															
															pz1_x = gom.app.project.actual_elements[curve_ce_re_sec[:-4]].get ('coordinate['+str(1)+'].x')
															pz1_y = gom.app.project.actual_elements[curve_ce_re_sec[:-4]].get ('coordinate['+str(1)+'].y')
															pz1_z = gom.app.project.actual_elements[curve_ce_re_sec[:-4]].get ('coordinate['+str(1)+'].z')
															
															pz2_x = gom.app.project.actual_elements[curve_ce_re_sec[:-4]].get ('coordinate['+str(anzpkt-2)+'].x')
															pz2_y = gom.app.project.actual_elements[curve_ce_re_sec[:-4]].get ('coordinate['+str(anzpkt-2)+'].y')
															pz2_z = gom.app.project.actual_elements[curve_ce_re_sec[:-4]].get ('coordinate['+str(anzpkt-2)+'].z')
															
															pz3_x = gom.app.project.actual_elements[curve_ce_re_sec[:-4]].get ('coordinate['+str(int(anzpkt/2))+'].x')
															pz3_y = gom.app.project.actual_elements[curve_ce_re_sec[:-4]].get ('coordinate['+str(int(anzpkt/2))+'].y')
															pz3_z = gom.app.project.actual_elements[curve_ce_re_sec[:-4]].get ('coordinate['+str(int(anzpkt/2))+'].z')
															
															MCAD_ELEMENT=gom.script.primitive.create_point (
																name='pz1', 
																point={'point': gom.Vec3d (pz1_x, pz1_y, pz1_z)}, 
																properties=gom.Binary ('eAHNV01sG0UY/QylLYYQUsqPEKKrNED4cRxXIQU3pSEkJUKkIIhKhQqW413bC/baXW9wXFTYigvixgG4IkFPEZV6QIgT4oDEAaUnqoob4oIEElWFhIRQw3szGXvXsdP2gMSu1js78837/t58M16sVVNHHx9bkfm5p2fnXpJFP+8GjWx2ruJUHS940a/VHT9wnYboKyHbZCApSRmQ5AC69vwTHi/j/ewLC9bLtWLQzPuOtW88M2nN14Kiu2JlMmri2uoO2Y9WAs+lL9LnZ/g+rt9KoOfPx+hN7MJP8c+11YTch9atIqEtrjSkLhXJS0tyaLtyUhw5dXRt9Qa5F1K3QGo2JrUgNbEh8+ojBukeyLF9G943Qb4hVeBVcH//2h8TRor6HPQ5GM1JAShV3I54EsiZaeq7HfO3q/mB+NDpSUlGL3L+NozgCiXBr7vQvDmG1pAy8JryyyfEgSbOCJfQV4PG189yFgOWCN9ncxjNwRgAFeblDZhTgDk1fLXkhy+3BpNwJ8H2AezuGNgy4ujAx6ICyilPGGUN7qLXk6Hfrgl8BOAIS8gELQGgAtgltAvyJoLjA2oZYLZ8lSLcEUg/AOlF9Fcli/swlJdgItvPtzFm0KKJ7GW7G+0ZzK/g8eX0d3RxFLi0hDp24r1xheXuHkg6n5sZoFuX3UQkdfwNAmgdC+eJa5JaUraPSceGzDEikrwkGNtILq/1Q6c/e4jfD+JjaEttVaBS87uHqIuETUJ+RvmoLTK0HlQaSH1aRHRDJw/SHjByl9/5mv1PYBxyMR9Ja09JGR7lEElSmYRoomWDX2U5uZ12WECATyF9jc96pS3541/UxQV79WVm/IqyhSTkErvyKTXuBg4yGJooH94Y/fAjapnH6CwetrN439mWZGlo4QngB5dvLw2Y0L7O/j64hyjj6EEcYzEyvK2ruJSAxiJAfrM42HL5G1pqot53ET8H6L1XhW5gobhYe1x9NlSV8c4rKpCEJjUNOXEhqnRZmRbIsXN0YoNuMq2qT68gm/pzpRVF6Wu6BdOZ92gUdWR1KWb7XJpQ/Uuiic8RuMMymvuJpvYyjmgryNz631sj7kLt3XGjhFMIUgDMijwlbOuAsU09AfRZKl/8OohaegLr2UUN4SytaRgSeiWwh+yjXAZPWmGSRy2VbUu1mBxKmPlpzG7gHoZ0EqXeUnddHsObKbPkbTxNaHTVnBRk67CrAJwsRuqwyJEUJFjV63IAfafaSFOwomMB/UrHvGTabNhnRaRonVlJxHWguaQ8zsoEWD6udHQkOvhZ+M+6p7fEA8qnKVht+M5Isa5XlAc2NOuNjxrH8VhYF526aeLI3pKKsa6h7N8LCzu3zoFGNtHpIKdUNro9jGpKRdCzwC7AGvMwnnHZqL8N2Mss2Som9NuHrdSdgt81+JkFVh2cJE58nKiBkuL+1U+KdaIIqf4SZKTJj0Ehmxh5f+Ntb8rwW8D1IUE28wCTUr9E8qCrqnyy0e8oy8m4Tr5Sql9bNdFzPG4Tfe9G6ESn12h3bAyXdHa9Td5cKxtHlL/cJbB7IyusQWSc3qe5Urk+c/CWJw3uBGQv1+rDOBXo1URPPBXXNEbs/0GEe+fgv4pwvCJMgrnXVxFGVHXRVSJAJkcRTV3XWfOG5VG1Xtk2W01OnfxY/w5iLtnKE93WGWFuNPvZMhVIV0Cyi1XP1EOzA9yhDvD3Y8fCv5QwumPp1cK/DOROYTK69W3eQBNAmB6K7lGs0i5Wlf4zoDn385NEue6z4Ae/ru/+9r39RB+DHp5bep3oc/CQO0ITOnmKZtVtyOylqOWMQ/xPA875/wKWmKiCAQG+'))
															
															MCAD_ELEMENT=gom.script.primitive.create_point (
																name='pz2', 
																point={'point': gom.Vec3d (pz2_x, pz2_y, pz2_z)}, 
																properties=gom.Binary ('eAHNV01sG0UY/QylLYYQUsqPEIJVmkL4cRxXIQU3pSEkJUKkIIhKhQqW4107Bnvt7m5wXFTYigvixgG4IkFPEZV6QIgT6qESB5SeQIgb4oIEElWFhIRQw3szHnvXsdP2gMSu1js78837/t58M16sVVNHHx9blfm5p2fnXpJFL18O/Gx2ruJUHTd40avVHS8oO77oKyHbZCApSRmQ5AC69v4THl/G+9kXFqyXa8Wgkfcca994ZtKarwXF8qqVyaiJ62s7ZD9aCTyXvkhfnOH7uH4rgZ4/H6M3sQs/xT/X1xJyH1q3ioS2lMWXulQkL03JoV2Wk+LIqaPrazfIvZC6BVKzMakFqYkNmVcfMUj3QI7t2/C+CfK+VIFXwf3ta39MGCnqc9DnYDQnBaBUcTviSiBnpqnvdszfruYH4kGnKyUZ/ZHzt2EEVygJft2F5s0xNF+WgdeQXz4hDjRxRriEvho0vn6WsxiwRPg+m8NoDsYAqDAvb8CcAsyp4asp3325NZiEOwm2D2B3x8BWEEcHPhYVUE55wihr8DJ6XRn67ZrARwCOsIRM0BIAKoBdQrsgbyI4HqBWAGbLVynCHYH0Xkgvor8qWdyHobwEE9l+vo0xgxZNZC/b3WjPYH4FjyenL9DFUeDSEurYiXfrCpe7eyDpfG5mgG5ddhOR1PFaBNA6Fi4S1yS1pGwfk44NmWNEJHlJMLaRXF4bh05/9hC/H8TH0JbaqkCl5ncPURcJm4T8jPJRW2RoPag0kPq0iOiGTi6kXWDkLr/zNfufwDjkYj6S1q6SMjzKIZKkMgnRQMsGv5bl5HbaYQEBPoX0NT7rlbbk939RFxfs1ZeZ8SvKFpKQS+zKp9S4GzjIYGiifLg1+uFH1DKP0Vk8bGfxvrMtydLQxBPADy7fXhowoX2d/X3wAaKMowdxjMXI8Lau4lICGosA+c3iYMvlb2ipiXrfRfwcoPdcFdrHQilj7XH12VC1jHdeUYEkNKnx5cQPUaUryrRAjp2jEy26ybSqPr2CbOrPlWYUpa/pFkxn3qNR1JHVpZjtc2lC9S+JJj5H4A7LaO4nmtrLOKKtInMbf2+NuAu1d8eNEk4hSAEwK/KUsK0Dxjb1BNBnqXzx6yBq6Qms5zJqCGdpTcOQ0CuBPWQf5TJ40gqTPGqqbFuqxeRQwsxPY7aPexjSSZR6S911eQxvpsySt/E0oLGs5qQgW4ddBeBkMVKHRY6kIMGqXpcD6DvVRpqCFR0L6Fc65iXTZsM+KyJF68xKIq4DzSXlcVYmwPJxpaMj0cHPwn/WPb0lHlA+TcFqw3dGinW9ojywoVlvfNQ4jsfCuujUTRNH9pZUjHUNZf8eWNi5dQ40solOBzmlstHtYVRTKoKeBXYB1piH8YzLRv31YS+zZKuY0G8PtlJ3Cn7X4GcWWHVwkjjxcaIGSor7Vz8p1okipPpLkJEmPwaFbGLkvdbb3pTht4DrQYJs5gEmpX6J5EJXVflko99RlpNxnXylVL+2aqLneNwm+t6N0IlOr9Hu2Bgu6ey6m7y5VjaOKH+5S2D3RlZYg8g4vU9zpXJ95uAtTxrcCchertWHcSrQq4meuCquaYzY/4MI987BfxXheEWYBHOvryKMqOqiq0SATI4imrqus+YNy6NqvbJttpqcOvmx/h3EXLKVJ7qtM8LcaPazZSqQroBkF6ueqYdmB7hDHeDvx46FfylhdMfSq4V/GcidwmR069u8gSaAMD0U3aNYpctYVfrPgObcz08S5brPgh/8urH7/Hv7iT4GPTy39DrR5+Ahd4QGdPIUzarry+ylqOWMQ/xPA875/wLoRqiIARoo'))
															
															MCAD_ELEMENT=gom.script.primitive.create_point (
																name='pz3', 
																point={'point': gom.Vec3d (pz3_x, pz3_y, pz3_z)}, 
																properties=gom.Binary ('eAHNV01sG0UY/QylLYYQUsqPEIJVGiAUHMdVSMFNaQhJiRApFURthQqW4107Bnvt7m5wXFTYigvixgG4IkFPEZV6QIgT4oDEAaUnEOIE4oIEElUvSAg1vDfjsXcdO20PSOxqvbMz37zv780348VaNXXs8bFVmZ97enbuRVn08uXAz2bnKk7VcYOjXq3ueEHZ8UVfCdkmA0lJyoAkB9CV+ic8uYz3sy8sWC/VikEj7znWvvHMpDVfC4rlVSuTURPX13bIfrQSeC59lr44g/fRk/qtBHr+fIjexC78FH9eX0vIfWjdKhLaUhZf6lKRvDQlh3ZZTosjZ46tr90g90LqFkjNxqQWpCY2ZF7ea5DugRzbt+F9E+R9qQKvgvvbV/6cMFLU56DPwWhOCkCp4nbElUDOTVPf7Zi/Xc0PxINOV0oy+iPnb8MIrlAS/LoLzZtjaL4sA68hv35EHGjijHAJfTVofPU8ZzFgifBdNofRHIwBUGFeXoM5BZhTw1dTvvt8azAJdxJsH8DujoGtII4OfCwqoJzyhFHW4GX0ujL0+zWBjwAcYQmZoCUAVAC7hHZBXkdwPECtAMyWL1KEOwLpByG9iP6qZHEfhvISTGT7+TbGDFo0kb1sd6M9g/kVPJ6c/YYujgKXllDHTrxbV7jc3QNJ51MzA3TrspuIpI7XIoDWsXCRuCapJWX7mHRsyJwgIslLgrGN5PLaOHT2k4f5/RA+hrbUVgUqNb99iLpI2CTkZ5SP2iJD60GlgdSnRUQ3dHIh7QIjd/mtL9n/BMYhF/ORtHaVlOFRDpEklUmIBlo2+LUsp7fTDgsI8Cmkr/FZx9uS3/9FXVywV19mxq8oW0hCLrErH1PjbuAgg6GJ8uHW6PsfUMs8RmfxsJ3F+862JEtDE08AP7h8e2nAhPZ1/o/BB4gyjh7EMRYjw9u6iksJaCwC5DeLgy2Xv6KlJup9F/FzgN5zVWgfC6WMtcfVZ0PVMt55RQWS0KTGl1M/RJWuKNMCOXGBTrToJtOq+vQKsqk/V5pRlL6mWzCdeY9GUUdWl2K2L6QJ1b8kmvgcgTsso7mfaGov44i2isxt/L014i7U3h03SjiFIAXArMhTwrYOGNvUE0CfpfLFr4OopaewnsuoIZylNQ1DQq8E9pB9lMvgSStM8qipsm2pFpNDCTM/jdk+7mFIJ1HqLXXX5TG8mTJL3sTTgMaympOCbB12FYCTxUgdFjmSggSrel0OoO9MG2kKVnQsoF/pmJdMmw37rIgUrTMribgONJeUx1mZAMvHlY6ORAc/C/9Z9/SWeED5NAWrDd8ZKdb1ivLAhma98VHjOB4L66JTN00c2VtSMdY1lP17YGHn1jnQyCY6HeSUyka3h1FNqQh6FtgFWGMexjMuG/XXh73Mkq1iQr892ErdKfhdg59ZYNXBSeLEx4kaKCnuX/2kWCeKkOovQUaa/BgUsomR91pve1OG3wCuBwmymQeYlPolkgtdVeWTjX5HWU7GdfKVUv3aqome43Gb6Hs3Qic6vUa7Y2O4pLPrbvLmWtk4ovzlLoHdG1lhDSLj9D7Nlcr1mYO3PGlwJyB7uVYfwalAryZ64qq4pjFi/w8i3DsH/1WE4xVhEsy9voowoqqLrhIBMjmKaOq6zpo3LI+q9cq22Wpy6uTH+ncQc8lWnui2zghzo9nPlqlAugKSXax6ph6aHeAOdYC/HzsW/qWE0R1Lrxb+ZSB3CpPRrW/zBpoAwvRQdI9ilS5jVek/A5pzvzxJlOs+C77328bur9/ZT/Qx6OG5pdeJPgcPuSM0oJOnaFZdX2YvRS1nHOJ/GnDO/xfv46fcAW3L'))
															
															# convert to actual elements
																
															gom.script.cad.convert_to_actual_element (elements=[gom.app.project.inspection['pz2'], gom.app.project.inspection['pz3'], gom.app.project.inspection['pz1']])
															
															## 3-2-1 alignment
																
															CAD_ALIGNMENT=gom.script.alignment.create_three_two_one (
																alignment_rule='ZZZ-YY-X', 
																line_observation_1={'actual_point': gom.app.project.actual_elements['pz1'], 'nominal_position': 0.00000000e+00}, 
																line_observation_2={'actual_point': gom.app.project.actual_elements['pz2'], 'nominal_position': 0.00000000e+00}, 
																line_positive=True, 
																name='3-2-1 alignment 1', 
																parent_alignment=gom.app.project.alignments['Original alignment'], 
																plane_observation_1={'actual_point': gom.app.project.actual_elements['pz1'], 'nominal_position': 0.00000000e+00}, 
																plane_observation_2={'actual_point': gom.app.project.actual_elements['pz3'], 'nominal_position': 0.00000000e+00}, 
																plane_observation_3={'actual_point': gom.app.project.actual_elements['pz2'], 'nominal_position': 0.00000000e+00}, 
																plane_positive=False, 
																point_observation={'actual_point': gom.app.project.actual_elements['pz1'], 'nominal_position': 0.00000000e+00})
																
															# Calculation of the point (p_e) on the cross profile that is closest to the tool edge

															# distance section and tool edge 
			
															MCAD_ELEMENT=gom.script.inspection.create_curve_curve_distance (
																first_curve=gom.app.project.actual_elements[curve_ce_re_sec[:-4]], 
																name='dist_2_curves', 
																properties=gom.Binary ('eAHNV01sG0UUfqalLYZQUn6FEF3SQMOPazsKoWxTGkpSAmoKKlGJENRyvBvHwn/d3TZJUWBzAnHjgLgiQZFQpEo9IU6ckDilhwpUOIF6K0hIvSBxaPi+GY9313ZTekDC1npmZ958733vvXkznmnUMiee3bckU5MvTkwelxmvWAl8256sujW3HrzuNZquF1RcX/QnJVulLy1p6ZN0H4YuF35+ewHty69NW2805oPFoudaw7n8qDXVCOYrS1Y+rxaur22X59BL4fn164sTc2xndasEev7s5mg/npO59bWUPILeXSKhIxXxpSlVKcqyFNCvyFlxZeXE+tpt8jCk7oTUREJqWhriQOatpwzSQ5Bj/260t0Pelxrwqvj+8M6fI5wZxsyDmHEx5mK2oOYrUpY63lz8Bhjz0Dslp6GNPUeKK7QCdspWrJ2D3gbWnzxPRNKXcIcxgWQi8BIEa23gc+OEuQfy2yDlQ5UHFXUoH7rM9QDnJ5QU3yx0QSSGRlmzhg4qyepXRDwOyb2QnFHabLHlKMwu46nD+GG820LXaYJc2cDMK11olJuBTUVIBLL0Ia0YBDYtYf8BtHdAT7cdlz5eeSwuEXnAlwVoW5Qrn23uwlT4kVEHB4XMgzkQqCIac+iX5F0Q8gB1WpH6JkO4YzDo8QTxIzC93KJ8tI1xGD0faCTIfifaS8Ct4vFk9XtaMQRcEqeOHWhbn3ChcwSS7pdmxa4uu4nIDPXAgqmgdUxfJK5xZhnjNdknkQ35WSICTeUx+63E2Di0+sVevj+BOeyhDi/FtdWASs0fHKIu7os05A8rjtois3t2qtByh9Eiops8r0O6DozCtfe/5fh+zEMuoZWs6kqqhJShBQWwZIJgHcJegRUBUuDsNtphAYEpTa7JVW+2JX/8i7pYF26+mw2veLbMK+xArn9OjfcBBxEMjZePtGY/+ZRapjA7gYd9G+39bUlWoGU8AXiwSvTSgAXtz/k/du4mSg4j8GPCRyZvm8ovZaBxYzK/WYMcufYdLTVe764ura3xKqD33BTax0apoJA2FXQBrnehyiShCY0vp36KK2WpY22ZvUASrXSTcVWHejnZ7Orry3GUbtNbhdGC6Yx73Ivas7ris38hS6gbF0fjn2Ogw0JW+IWm9jKOaEsgs/H35oi7UIW3b5FwDE4KgFmVF4R97TD2qSeAPkvFi28HZQAnA8t2Sa3SmgYgoXcCddORlMvjySpM5tGyiralegwOJYylWaz28R2AdBol1lLfpjyDliGz5D08i9DIwuxKBrJN2FVC38ZMExZxdBFtEW8HMLbSRhqDFZEF5JVNsGTYHNhnxaRondlJxHWhuawY2zKCLM8pHZFEhG+DP+uAPnkPKE5jsNrku4W8Lytv6WpITXugK/pqb7L2VxVLB9YxPcvKZznIEyOqdsbXnfbHZTIxjTb0lcDAPPRWUjbOxocmxsBRjMnKgyW0JwNWDVhoA6uJjCNOcp6ogZKqbSLFKjAPqRvjMN+M942uuJdMNkReyqjsY6x5YdCt0xXhM9DsQYLZzHtSRv3q25ANLmTtYNxV3JhxUSwyalzbPdJzPmk1vdOJEPmv12yn90wuabb1Ljb/NhsHFV+eQDi9ETfWIGaTPqe5U7k/eTPk9YknAbOX++5J3Ar0biKTuvJrFjPO/8DDvWPwX3k4WRFGb7kiDKrqoqtEgEgOwZu6rrPmDcjTKn/ZN0dNQd38WP8OYi2zlTe6zSPC2OjsZ89UIF0BmV2seqYemhPg6hmeK4/ixMKfoTB+YundYq7PpdH40dd9gKaAMN4fP6NYpXkJj98Ff3ueKLd6F7z3kr+xv//3Lf8Aq9ao4QE9Gg=='), 
																second_curve=gom.app.project.actual_elements[curve_ce[:-4]])
															
															# create point p_e
															
															p_x = gom.app.project.actual_elements['dist_2_curves'].get ('coordinate1.x')									
															p_y = gom.app.project.actual_elements['dist_2_curves'].get ('coordinate1.y')									
																	
															MCAD_ELEMENT=gom.script.primitive.create_point (
																name='p_e', 
																point={'point': gom.Vec3d (p_x, p_y, 0)}, 
																properties=gom.Binary ('eAHNV01sG0UY/QylLYYQUsqPEIJVGiAUHMdVSMFNaQhJiRApFURthQqW4107Bnvt7m5wXFTYigvixgG4IkFPEZV6QIgT4oDEAaUnEOIE4oIEElUvSAg1vDfjsXcdO20PSOxqvbMz37zv780348VaNXXs8bFVmZ97enbuRVn08uXAz2bnKk7VcYOjXq3ueEHZ8UVfCdkmA0lJyoAkB9CV+ic8uYz3sy8sWC/VikEj7znWvvHMpDVfC4rlVSuTURPX13bIfrQSeC59lr44g/fRk/qtBHr+fIjexC78FH9eX0vIfWjdKhLaUhZf6lKRvDQlh3ZZTosjZ46tr90g90LqFkjNxqQWpCY2ZF7ea5DugRzbt+F9E+R9qQKvgvvbV/6cMFLU56DPwWhOCkCp4nbElUDOTVPf7Zi/Xc0PxINOV0oy+iPnb8MIrlAS/LoLzZtjaL4sA68hv35EHGjijHAJfTVofPU8ZzFgifBdNofRHIwBUGFeXoM5BZhTw1dTvvt8azAJdxJsH8DujoGtII4OfCwqoJzyhFHW4GX0ujL0+zWBjwAcYQmZoCUAVAC7hHZBXkdwPECtAMyWL1KEOwLpByG9iP6qZHEfhvISTGT7+TbGDFo0kb1sd6M9g/kVPJ6c/YYujgKXllDHTrxbV7jc3QNJ51MzA3TrspuIpI7XIoDWsXCRuCapJWX7mHRsyJwgIslLgrGN5PLaOHT2k4f5/RA+hrbUVgUqNb99iLpI2CTkZ5SP2iJD60GlgdSnRUQ3dHIh7QIjd/mtL9n/BMYhF/ORtHaVlOFRDpEklUmIBlo2+LUsp7fTDgsI8Cmkr/FZx9uS3/9FXVywV19mxq8oW0hCLrErH1PjbuAgg6GJ8uHW6PsfUMs8RmfxsJ3F+862JEtDE08AP7h8e2nAhPZ1/o/BB4gyjh7EMRYjw9u6iksJaCwC5DeLgy2Xv6KlJup9F/FzgN5zVWgfC6WMtcfVZ0PVMt55RQWS0KTGl1M/RJWuKNMCOXGBTrToJtOq+vQKsqk/V5pRlL6mWzCdeY9GUUdWl2K2L6QJ1b8kmvgcgTsso7mfaGov44i2isxt/L014i7U3h03SjiFIAXArMhTwrYOGNvUE0CfpfLFr4OopaewnsuoIZylNQ1DQq8E9pB9lMvgSStM8qipsm2pFpNDCTM/jdk+7mFIJ1HqLXXX5TG8mTJL3sTTgMaympOCbB12FYCTxUgdFjmSggSrel0OoO9MG2kKVnQsoF/pmJdMmw37rIgUrTMribgONJeUx1mZAMvHlY6ORAc/C/9Z9/SWeED5NAWrDd8ZKdb1ivLAhma98VHjOB4L66JTN00c2VtSMdY1lP17YGHn1jnQyCY6HeSUyka3h1FNqQh6FtgFWGMexjMuG/XXh73Mkq1iQr892ErdKfhdg59ZYNXBSeLEx4kaKCnuX/2kWCeKkOovQUaa/BgUsomR91pve1OG3wCuBwmymQeYlPolkgtdVeWTjX5HWU7GdfKVUv3aqome43Gb6Hs3Qic6vUa7Y2O4pLPrbvLmWtk4ovzlLoHdG1lhDSLj9D7Nlcr1mYO3PGlwJyB7uVYfwalAryZ64qq4pjFi/w8i3DsH/1WE4xVhEsy9voowoqqLrhIBMjmKaOq6zpo3LI+q9cq22Wpy6uTH+ncQc8lWnui2zghzo9nPlqlAugKSXax6ph6aHeAOdYC/HzsW/qWE0R1Lrxb+ZSB3CpPRrW/zBpoAwvRQdI9ilS5jVek/A5pzvzxJlOs+C77328bur9/ZT/Qx6OG5pdeJPgcPuSM0oJOnaFZdX2YvRS1nHOJ/GnDO/xfv46fcAW3L'))
															
															gom.script.cad.convert_to_actual_element (elements=[gom.app.project.inspection['p_e']])
															
															# translation the point p_e to the origin of coordinates
															
															CAD_ALIGNMENT=gom.script.alignment.create_by_translation (
																name='Alignment 1', 
																new_coordinate={'point': gom.Vec3d (0.00000000e+00, 0.00000000e+00, 0.00000000e+00)}, 
																old_coordinate=gom.app.project.actual_elements['p_e'], 
																parent_alignment=gom.app.project.alignments['3-2-1 alignment 1'])
															
														######## exports
														
														# create report for screenshot
														
															gom.script.view.show_grid (enable=True)																
															name_sec_local = curve_ce_re[:-4]+ "_" + (curve_ce_re_sec.split("_")[len(curve_ce_re_sec.split("_"))-2])															
															
															gom.script.sys.switch_to_inspection_workspace ()															
															gom.script.cad.hide_element (elements=gom.ElementSelection ({'category': ['key', 'elements', 'explorer_category', 'actual']}))															
															gom.script.cad.show_element (elements=[gom.app.project.actual_elements['pz1']])
															gom.script.cad.show_element (elements=[gom.app.project.actual_elements['pz2']])
															gom.script.cad.show_element (elements=[gom.app.project.actual_elements['pz3']])
															gom.script.cad.show_element (elements=[gom.app.project.actual_elements['p_e']])
															gom.script.cad.show_element (elements=[gom.app.project.actual_elements[curve_ce_re_sec[:-4]]])
															
															gom.script.sys.switch_to_report_workspace ()															
															gom.script.cad.show_in_explorer ()															
															gom.script.sys.edit_properties (
																data=[gom.app.project.actual_elements[curve_ce_re_sec[:-4]]], 
																ps_draw_lines=True, 
																ps_draw_points=False)															
															gom.script.sys.edit_properties (
																data=gom.ElementSelection ({'category': ['key', 'elements', 'explorer_category', 'actual', 'object_family', 'geometrical_element', 'type', 'point']}), 
																label_show=True)															
															gom.script.view.set_zp (
																up_axis='Y+', 
																use_animation=False, 
																widget='3d_view')															
															gom.script.report.create_report_page (
																animated_page=False, 
																master_name='Style_a4', 
																target_index=0, 
																template_name='3D', 
																template_orientation='landscape', 
																title=curve_ce_re_sec[:-4])															
															gom.script.report.export_report_page_as_png (
																disable_transparency=True, 
																file= root_sec + "/" + name_sec_local +'_local.png', 
																height=1500, 
																reports=[gom.app.project.reports['report'].pages['page 1']], 
																stages=[], 
																use_original_size=False, 
																width=2122)																
																								
															gom.script.sys.switch_to_inspection_workspace ()
															
															# export as *.iges
															
															gom.script.sys.export_iges (
																elements=[gom.app.project.actual_elements[curve_ce_re_sec[:-4]]], 
																export_in_one_file=True, 
																file=root_sec + "/" + name_sec_local +'_local.igs',
																length_unit='default', 
																sender_company='', 
																sender_name='', 
																write_as_visualized=True)
															
															# export as *.asc

															gom.script.sys.export_ascii (
																decimal_symbol='.', 
																delimiter=' ', 
																elements=[gom.app.project.actual_elements[curve_ce_re_sec[:-4]]], 
																export_in_one_file=True, 
																export_points_on_boundary=False, 
																file=root_sec + "/" + name_sec_local +'_local.asc', 
																length_unit='default', 
																with_element_name=True)
															
															# save project as *.ginspect
															
															gom.script.sys.save_project_as (file_name=root_sec + "/" + name_sec_local +'_local.ginspect')
															
															gom.script.sys.close_project ()
															
															now = datetime.datetime.now()
															myfile.write ("End: " + str(now.hour)+':'+str(now.minute)+" h"+ "\n")
print ("fertsch :-)")

now = datetime.datetime.now()
myfile.write ("Script finished: " + str(now.day)+ "." + str(now.month) + "." + str(now.year) + " um " + str(now.hour)+ ":" +str(now.minute)+ " h"+ "\n")
myfile.close()
