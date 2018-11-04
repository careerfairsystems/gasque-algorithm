# -*- coding: utf-8 -*-

import csv
from random import shuffle
from operator import itemgetter

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
		else:
			distribution_left.append(dresses[i])
			distribution_right.append(suits[i])

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

def evaluate_distribution(distribution_left, distribution_right):
	pass

# Give points for the next person on the same side, the opposite person and the next person on the opposite side.
def company_rep_points(current_table_side, other_table_side, index):
	points = 0
	current_person = current_table_side[i]
	if index+1 > len(current_table_side)-1:
		relevant_people = [current_table_side[i+1], other_table_side[i], other_table_side[i+1]]

	for person, index in zip(relevant_people, range(0, len(relevant_people))):
		try:
			if person['type'] == 'student' and current_person['affiliation'] == person['affiliation']:
				points += 5
			if index == 2 and person['gender'] == current_person['gender']:
				points += 2
			elif person['gender'] != current_person['gender']:
				points += 2
		except:
			continue
	return points

# Iterate over one of the lists, lets call in a. For a[i] check a[i+1], b[i] and b[i+1].
def student_points(current_table_side, other_table_side, index):
	points = 0
	current_person = current_table_side[i]
	relevant_people = [current_table_side[i+1], other_table_side[i], other_table_side[i+1]]
	for person, index in zip(relevant_people, range(0, len(relevant_people))):
		if person['type'] == 'company' and current_person['affiliation'] == person['affiliation']:
			points += 5
		if index == 2 and person['gender'] == current_person['gender']:
			points += 2
		elif person['gender'] != current_person['gender']:
			points += 2
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
			if row['Drinking package'] == 'alkohol':
				drinking_package = True
			else:
				drinking_package = False
			desired_programmes = row['Desired Programe'].split(",")
			guilds = []
			for programme in desired_programmes:
				if programme in desired_programme_guild_mapping:
					guild = desired_programme_guild_mapping[programme]
					if guild not in guilds:
						guilds.append(guild) 
			
			name = row['Name']
			if not name or name == ' - ':
				name = row['Company']
			company_rep_params = {'name': name,
								  'gender': row['Gender'],
								  'affiliation': guilds,
								  'type': 'company_rep',
								  'company': row['Company'],
								  'Allergies': row['Allergies'],
								  'Drinking package': drinking_package}
			
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

def main(iterations, students_list_path, company_reps_list_path):
	suits, dresses = parse_input(students_list_path, company_reps_list_path)
	distribution_left, distribution_right = create_distribution(suits, dresses)
	for index in range(0, len(distribution_left)):
		print(distribution_right[index]['name'] + "-" + distribution_left[index]['name'])
	# result = []
	
  # for _ in iterations:
		
	# 	 distribution_left, distribution_right = create_distribution(suits, dresses)
		
	# 	# 4. Method for setting points on a given distribution. 
		
	# 	result.append({'left': distribution_left, 'right': distribution_right,
	# 				  'points': evaluate_distribution(distribution_left, distribution_right)})


	# 	# 5. Write out the best result to a csv file with table number and number on the table.
	# result = sorted(result, key=itemgetter('points'), reverse=True) 
	# for res in result[:5]:
	# 	name = "Output: " + str(res['points'])
  #   tables = [{'name': 'Cosmic Dust', 'seats': 30, 'tables': 5, 'front': True},
  #             {'name': 'Quasar', 'seats': 30, 'tables': 5, 'front': True}
  #             {'name': 'Dark Matter', 'seats': 30, 'tables': 5, 'front': False}
  #             {'name': 'Nebula', 'seats': 30, 'tables': 5, 'front': False}]
	# 	with open(name, "w+") as output_file:
	# 		fieldnames = ['Name', 'Table Name', 'Seat number', 'Food pref', 'Alcohol']
	# 		output_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
	# 		while True:


if __name__ == '__main__':
  iterations = 1000
  students_list_path = "input/students.csv"
  company_reps_list_path = "input/company_reps.csv"
  main(iterations, students_list_path, company_reps_list_path)