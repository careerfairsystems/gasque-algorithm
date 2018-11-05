# -*- coding: utf-8 -*-

import csv
from random import shuffle
from operator import itemgetter
import copy

def create_distribution(suits, dresses): 
	# 3.1 Shuffle the lists.
	shuffle(suits)
	shuffle(dresses)
	distribution_left = []
	distribution_right = []
	if len(suits) > len(dresses):
		range_in_lists = len(dresses)
		suit_longest = True
	else:
		range_in_lists = len(suits)
		suit_longest = False
	alternating_turn = True

	# 3.2 Place up to the longest student list.
	for i in range(range_in_lists-1):
		if alternating_turn:
			distribution_left.append(suits[i])
			distribution_right.append(dresses[i])
			alternating_turn = False
		else:
			distribution_left.append(dresses[i])
			distribution_right.append(suits[i])
			alternating_turn = True

	# 3.3 Calculate the number of students left and place these in pairs on regular intervals.	
	remaining_people = []
	if suit_longest:
		## TODO THERE CAN BE SOMETHING WRONG WITH THIS ONE, VERIFY WITH THE INPUT.
		remaining_people = suits[range_in_lists:]
	else:
		remaining_people = dresses[range_in_lists:]

	remaining_people_left = remaining_people[len(remaining_people)/2:]	
	remaining_people_right = remaining_people[:len(remaining_people)/2]	
	
	alternating_turn = True
	for i in remaining_people:
		if alternating_turn:
			remaining_people_left.append(remaining_people[i])
			alternating_turn = False
		else:
			remaining_people_right.append(remaining_people[i])
			alternating_turn = True
	if len(remaining_people_left):
		quota = len(distribution_left)/len(remaining_people_left)	
		for i in range(len(distribution_left), 0, -1*qutota):
			try:
				distribution_left.insert(i, remaining_people_left.pop(0))
				distribution_right.insert(i, remaining_people_right.pop(0))
			except:
				# One of the lists is empty. Make sure all is added!
				distribution_left.append(remaining_people_left)
				distribution_right.append(remaining_people_right)	

	return distribution_right, distribution_left

def evaluate_distribution(distribution_left, distribution_right, suits, dresses):
	students = 0
	companies = 0
	for person in suits:
		if person['type'] == 'student': 
			students += 1
		else:
			companies +=1
	for person in dresses:
		if person['type'] == 'student': 
			students += 1
		else:
			companies +=1
	desired_students_at_table = int(round(30*float(students)/float(companies+students)))
	
	guild_points = {} 	
	guilds = ['F', 'E', 'M', 'V', 'A', 'K', 'D', 'Ing','W', 'I' ]
	for guild in guilds:
		nbr_company = 0
		nbr_student = 0
		for person in suits:
			if guild in person['affiliation'] and person['type'] == 'company_rep':
				nbr_company += 1
			if guild in person['affiliation'] and person['type'] == 'student':
				nbr_student += 1
		for person in dresses:
			if guild in person['affiliation'] and person['type'] == 'company_rep':
				nbr_company += 1
			if guild in person['affiliation'] and person['type'] == 'student':
				nbr_student += 1
		guild_points[guild] = (nbr_company / nbr_student) * 30

	total_points = 0
	for index in range(0, len(distribution_left)):
		if distribution_left[index]['type'] == 'student':
			points = student_points(distribution_left, distribution_right, index, guild_points)
			total_points = total_points +  points

	for index in range(0, len(distribution_right)):
		if distribution_right[index]['type'] == 'student':
			total_points = total_points + student_points(distribution_right, distribution_left, index, guild_points)

	while len(distribution_left) or len(distribution_right):
		current_table = []
		current_table.extend(distribution_left[:15])
		current_table.extend(distribution_right[:15])
		distribution_left = distribution_left[15:]
		distribution_right = distribution_right[15:]
		
		students = 0
		for chair in current_table:
			if chair['type'] == 'student':
				students += 1
		diff_students = desired_students_at_table - students
		if diff_students < 0:
			diff_students = diff_students*-1
		total_points = total_points - diff_students*100

	return total_points

# Iterate over one of the lists, lets call in a. For a[i] check a[i+1], b[i] and b[i+1].
def student_points(current_table_side, other_table_side, index, guild_points):
	points = 0
	current_person = current_table_side[index]

	try:
		if current_table_side[index+1]['type'] == 'student':
			points = points - 100
		if other_table_side[index]['type'] == 'student':
			points = points - 100
		relevant_people = [current_table_side[index+1], other_table_side[index], other_table_side[index+1], other_table_side[index-1], current_table_side[index-1]]
		for person in relevant_people:
			if person['type'] == 'company_rep' and current_person['affiliation'] in person['affiliation']:
				points += guild_points[person['affiliation']]

	except:
		# Reached the end of the array
		pass
	return points

def parse_input(students_list_path, company_reps_list_path):
	suits = []
	dresses = []

 	with open(students_list_path) as attending_students_csv:
		attending_students = csv.DictReader(attending_students_csv)
		for row in attending_students:
			student_params = {'name': row['Name'], 
							'gender': row['Gender'], 
							'affiliation': row['Guild'],
							'type': 'student',
							'drinking_package': row['Drinking package'],
							'food_pref': row['Food pref']}
			if student_params['gender'] == 'Man':
				suits.append(student_params)
			else:
				dresses.append(student_params)
		
  	with open(company_reps_list_path) as company_reps_csv:
		comany_reps = csv.DictReader(company_reps_csv)
		company_rep_not_specified = []

		# Output of programme mapping script.
		desired_programme_guild_mapping = {'Elektroteknik': 'E', 'Industrial Design': 'A', 'Mechanical Engineering with Industrial Design': 'M', 'Civil Engineering- Road and Traffic Technology': 'Ing', 'Byggteknik med arkitektur': 'Ing', 'Engineering Mathematics': 'F', 'Kemiteknik': 'K', 'Informations- och kommunikationsteknik': 'D', 'V\xc3\xa4g- och vatttenbyggnad': 'V', 'Byggteknik med j\xc3\xa4rnv\xc3\xa4gsteknik': 'Ing', 'Mechanical Engineering': 'M', 'Byggteknik med v\xc3\xa4g- och trafikteknik': 'Ing', 'Teknisk Fysik': 'F', 'Engineering Physics': 'F', 'Teknisk Nanovetenskap': 'F', 'Fire Protection Engineering': 'V', 'Brandingenj\xc3\xb6rsutbildning': 'V', 'Industriell ekonomi': 'I', 'Bioteknik': 'K', 'Information and Communication Engineering': 'D', 'Computer Science and Engineering': 'D', 'Datateknik': 'D', 'Industrial Engineering and Management': 'I', 'Engineering Nanoscience': 'F', 'Architect': 'A', 'Chemical Engineering': 'K', 'Civil Engineering - Architecture': 'Ing', 'Maskinteknik med teknisk design': 'M', 'Lantm\xc3\xa4teri': 'V', 'Biotechnology': 'K', 'Medicin och teknik': 'E', 'Biomedical Engineering': 'E', 'Industridesign': 'A', 'Maskinteknik': 'M', 'Teknisk Matematik': 'F', 'Civil Engineering': 'V', 'Ekosystemteknik': 'W', 'Surveying': 'V', 'Electrical Engineering': 'E', 'Environmental Engineering': 'W', 'Arkitekt': 'A', 'Civil Engineering - Railway Construction': 'Ing'}

		for row in comany_reps:
			if row['Drinking package'] == "alkohol":
				drinking_package = "Alcohol"
			else:
				drinking_package = "Alcohol-free"
			desired_programmes = row['Desired Programe'].split(",")
			guilds = []
			for programme in desired_programmes:
				if programme in desired_programme_guild_mapping:
					guild = desired_programme_guild_mapping[programme]
					if guild not in guilds:
						guilds.append(guild) 
			
			name = row['Name']
			if not name or name == '-':
				name = row['Company']
		
			company_rep_params = {'name': name,
								  'gender': row['Gender'],
								  'affiliation': guilds,
								  'type': 'company_rep',
								  'company': row['Company'],
								  'food_pref': row['Allergies'],
								  'drinking_package': drinking_package}
			
			if company_rep_params['gender'].lower() == 'man':
				suits.append(company_rep_params)
			elif company_rep_params['gender']:
				dresses.append(company_rep_params)
			else:
				company_rep_not_specified.append(company_rep_params)
	while company_rep_not_specified:
		if len(suits) > len(dresses):
			dresses.append(company_rep_not_specified.pop())
		else:
			suits.append(company_rep_not_specified.pop())
	
	return suits, dresses

def print_result_to_file(result):
	name = "output/Output: " + str(result['points']) + ".csv"

	name_tables = "output/tables: " + str(result['points']) + ".csv"
	tables = [{'name': 'Cosmic Dust', 'seats': 30, 'tables': 5, 'front': True},
			  {'name': 'Quasar', 'seats': 30, 'tables': 5, 'front': True},
			  {'name': 'Dark Matter', 'seats': 30, 'tables': 5, 'front': False},
			  {'name': 'Nebula', 'seats': 30, 'tables': 5, 'front': False}]

	with open(name, "w+") as output_file:
		output_writer = csv.writer(output_file)
		output_writer.writerow(['Name', 'Table Name', 'Seat number', 'Food pref', 'Alcohol', 'Student/Company'])
		first_front_table_done = False
		front_tables_done = False
		while result['left'] and result['right']:
			current_table_placement = []
			current_table_placement.extend(result['left'][:15])
			current_table_placement.extend(result['right'][:15])
			result['left'] = result['left'][15:]
			result['right'] = result['right'][15:]
			
			tables = sorted(tables, key=itemgetter('tables'), reverse=True)
			current_table = None

			for table in tables:
				if not front_tables_done:
					if table['front']:
						if current_table:
							if  table['tables'] > current_table['tables']: 
								current_table = table
						else:
							current_table = table
				else:
					if not table['front']:
						if current_table:
							if  table['tables'] > current_table['tables']: 
								current_table = table
						else:
							current_table = table

			if current_table['front']:
				table_name = current_table['name'] + " " + str(7 - current_table['tables'])
			else:
				table_name = current_table['name'] + " " + str(6 - current_table['tables'])
			
 			for chair, index in zip(current_table_placement, range(1, len(current_table_placement)+1)):
				if chair['type'] != 'student': 
					chair_type = 'Company'
				else:
					chair_type = 'Student'
				output_writer.writerow([chair['name'], table_name, index, chair['food_pref'], chair['drinking_package'], chair_type])
			current_table['tables'] = current_table['tables'] - 1 
			if current_table['tables'] == 0:
				if first_front_table_done:
					front_tables_done = True
				else:
					first_front_table_done = True
			output_writer.writerow(" ")

def print_result_to_file_tables(result):
	name_tables = "output/tables: " + str(result['points']) + ".csv"
	tables = [{'name': 'Cosmic Dust', 'seats': 30, 'tables': 5, 'front': True},
			  {'name': 'Quasar', 'seats': 30, 'tables': 5, 'front': True},
			  {'name': 'Dark Matter', 'seats': 30, 'tables': 5, 'front': False},
			  {'name': 'Nebula', 'seats': 30, 'tables': 5, 'front': False}]

	with open(name_tables, "w+") as output_file:
		output_writer = csv.writer(output_file)
		output_writer.writerow(['Table name', 'Student/Company', 'Seat number', 'name1 ', 'name2', 'Student/Company', 'Seat number', 'Student/Company'])

		first_front_table_done = False
		front_tables_done = False
		while result['left'] and result['right']:
			current_table_placement = []
			current_table_placement.extend(result['left'][:15])
			current_table_placement.extend(result['right'][:15])
			result['left'] = result['left'][15:]
			result['right'] = result['right'][15:]

			tables = sorted(tables, key=itemgetter('tables'), reverse=True)
			current_table = None

			for table in tables:
				if not front_tables_done:
					if table['front']:
						if current_table:
							if  table['tables'] > current_table['tables']: 
								current_table = table
						else:
							current_table = table
				else:
					if not table['front']:
						if current_table:
							if  table['tables'] > current_table['tables']: 
								current_table = table
						else:
							current_table = table

			if current_table['front']:
				table_name = current_table['name'] + " " + str(7 - current_table['tables'])
			else:
				table_name = current_table['name'] + " " + str(6 - current_table['tables'])
			
			for index in range(len(current_table_placement)/2):
				output_writer.writerow([table_name, current_table_placement[index]['type'], index+1, current_table_placement[index]['name'], current_table_placement[index+(len(current_table_placement)/2)]['name'], index+16, current_table_placement[index+(len(current_table_placement)/2)]['type']])
			current_table['tables'] = current_table['tables'] - 1 
			if current_table['tables'] == 0:
				if first_front_table_done:
					front_tables_done = True
				else:
					first_front_table_done = True
			output_writer.writerow(" ")

def main(iterations, students_list_path, company_reps_list_path):
	suits, dresses = parse_input(students_list_path, company_reps_list_path)
	result = []

	for iteration in range(iterations):
		if iteration % 1000 == 0:
			print(iteration)
		distribution_left, distribution_right = create_distribution(suits, dresses)
		
		# 4. Method for setting points on a given distribution. 
		result.append({'left': distribution_left, 'right': distribution_right,
					  'points': evaluate_distribution(distribution_left, distribution_right, suits, dresses)})


		# 5. Write out the best result to a csv file with table number and number on the table.
	result = sorted(result, key=itemgetter('points'), reverse=True)
	
	res_temp1 = copy.deepcopy(result[0])
	res_temp2 = copy.deepcopy(result[0])
	print_result_to_file(res_temp1)
	print_result_to_file_tables(res_temp2)
	print("Points: " + str(result[0]['points']) + ", " + str(result[1]['points']) + ", " + str(result[2]['points']))

if __name__ == '__main__':
  iterations = 1000000
  students_list_path = "input/students.csv"
  company_reps_list_path = "input/company_reps.csv"
  main(iterations, students_list_path, company_reps_list_path)