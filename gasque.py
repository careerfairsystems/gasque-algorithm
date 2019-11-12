# -*- coding: utf-8 -*-

import csv
import random
import operator
import copy
import datetime

### MAKING A DISTRUBUTION ###


def create_distribution(suits, dresses):
    # 3.1 Shuffle the lists.
    random.shuffle(suits)
    random.shuffle(dresses)
    distribution_left = []
    distribution_right = []

    min_length = min(len(suits), len(dresses))

    # 3.2 Place up to the longest student list.
    for i in range(min_length):
        even = i % 2 == 0
        distribution_left.append(suits[i] if even else dresses[i])
        distribution_right.append(dresses[i] if even else suits[i])

    # 3.3 Calculate the number of students left and place these in pairs on regular intervals.
    remaining_people = suits[min_length:] + dresses[min_length:]
    distribution_left += remaining_people[len(remaining_people)//2:]
    distribution_right += remaining_people[:len(remaining_people)//2]

    return distribution_right, distribution_left


### EVALUATING ###

def evaluate_distribution(left, right, ratio, guild_points):
    return sum(map(
        lambda i: evaluate(left, right, (False, i), ratio, guild_points),
        range(len(left))
        )) + sum(map(
                lambda i: evaluate(left, right, (True, i),
                                   ratio, guild_points),
                range(len(left))
            ))


def try_swap(left, right, pos_i, pos_j, ratio, guild_points):
    current_points = evaluate(left, right, pos_i, ratio, guild_points) + \
                              evaluate(left, right, pos_j, ratio, guild_points)
    do_swap(
        right if pos_i[0] else left,
        right if pos_j[0] else left,
        pos_i[1],
        pos_j[1]
    )
    resulting_points = evaluate(left, right, pos_i, ratio, guild_points) + \
                                evaluate(left, right, pos_j,
                                         ratio, guild_points)

    if resulting_points >= current_points:
        # Better score means we shouldn't swap back.
        return resulting_points > current_points

    # Reverse the swap
    do_swap(
        right if pos_i[0] else left,
        right if pos_j[0] else left,
        pos_i[1],
        pos_j[1]
    )
    return False


def do_swap(side_i, side_j, pos_i, pos_j):
    temp = side_i[pos_i]
    side_i[pos_i] = side_j[pos_j]
    side_j[pos_j] = temp


def list_getter(list, index):
    if index < 0 or index >= len(list):
        return None
    return list[index]


def evaluate(left, right, pos, ratio, guild_points):
    current_side, other_side = (right, left) if pos[0] else (left, right)
    return evalutate_gender(current_side, other_side, pos[1])
    + evaluate_type(current_side, other_side, pos[1], ratio)
    + evaluate_programme(current_side, other_side, pos[1], guild_points)


def evalutate_gender(current_side, other_side, index):
    current_person = current_side[index]

    relevant_people = list(filter(lambda i: i != None, [
        list_getter(current_side, index - 1),
        list_getter(current_side, index + 1),
        list_getter(other_side, index)
    ]))

    return len(list(filter(
        lambda person: current_person['gender'] != person['gender'], relevant_people
    ))) * 10


def evaluate_type(current_side, other_side, index, ratio):
    current_person = current_side[index]

    relevant_people = list(filter(lambda i: i != None, [
        list_getter(current_side, index - 1),
        list_getter(current_side, index + 1),
        list_getter(other_side, index),
        list_getter(other_side, index - 1),
        list_getter(other_side, index + 1)
    ]))

    same = len(
        list(filter(lambda i: i['type'] == current_person['type']), relevant_people))
    diff = len(
        list(filter(lambda i: i['type'] != current_person['type']), relevant_people))
    n = len(relevant_people)

    points = 50 - 4 * (abs(same - n * ratio)**2 + abs(diff - n * ratio)**2)
    print(points)
    return points


def evaluate_programme(current_side, other_side, index, guild_points):
    current_person = current_side[index]

    relevant_people = list(filter(lambda i: i != None, [
        list_getter(current_side, index - 1),
        list_getter(current_side, index + 1),
        list_getter(other_side, index),
        list_getter(other_side, index - 1),
        list_getter(other_side, index + 1)
    ]))

    if current_person['type'] == 'student':
        return len(list(
            filter(
                    lambda person: current_person['affiliation'] in person['affiliation'],
                    filter(
                        lambda person: person['type'] == 'company_rep',
                        relevant_people
                    )
                )
        )) * guild_points[current_person['affiliation']]
    elif current_person['type'] == 'company_rep':
        return sum(list(map(
            lambda person: guild_points[person['affiliation']],
            filter(
                        lambda person: person['affiliation'] in current_person['affiliation'],
                        filter(
                            lambda person: person['type'] == 'student',
                            relevant_people
                        )
                    )
            )))
    else:
        print('UNOWN TYPE ERROR!')
        print('type: ', current_person['type'])

    return 0


def avoid_zero(n):
    return n if n > 0 else 1


def evaluate_guild_points(people):
    guilds = ['F', 'E', 'M', 'V', 'A', 'K', 'D', 'Ing', 'W', 'I']
    guild_points = {}

    for guild in guilds:
        students = len(list(filter(lambda p: p['affiliation'] == guild, filter(
            lambda p: p['type'] == 'student', people))))
        reps = len(list(filter(lambda p: guild in p['affiliation'], filter(
            lambda p: p['type'] == 'company_rep', people))))
        guild_points[guild] = 20 + (10000 / avoid_zero(students * reps))**0.5

    return guild_points


def evaluate_ratio(people):
    # ratio is student per person
    students = len(list(filter(lambda p: p['type'] == 'student', people)))
    return students / len(people)

### PARSING ###


def parse_input(students_list_path, company_reps_list_path):
    suits = []
    dresses = []

    with open(students_list_path) as attending_students_csv:
        attending_students = csv.DictReader(attending_students_csv)
        for row in attending_students:
            student_params = {
                                'name': row['Name'],
                                'gender': row['Gender'],
                                'affiliation': row['Guild'],
                                'mail': row['Mail'],
                                'type': 'student',
                                'drinking_package': row['Alcohol']
                            }
            if student_params['gender'] == 'Man':
                suits.append(student_params)
            else:
                dresses.append(student_params)

    with open(company_reps_list_path) as company_reps_csv:
        comany_reps = csv.DictReader(company_reps_csv)
        company_rep_not_specified = []

        # Output of programme mapping script.
        desired_programme_guild_mapping = {'Elektroteknik': 'E', 'Industrial Design': 'A', 'Mechanical Engineering with Industrial Design': 'M', 'Civil Engineering- Road and Traffic Technology': 'Ing', 'Byggteknik med arkitektur': 'Ing', 'Engineering Mathematics': 'F', 'Kemiteknik': 'K', 'Informations- och kommunikationsteknik': 'D', 'V\xc3\xa4g- och vatttenbyggnad': 'V', 'Byggteknik med j\xc3\xa4rnv\xc3\xa4gsteknik': 'Ing', 'Mechanical Engineering': 'M', 'Byggteknik med v\xc3\xa4g- och trafikteknik': 'Ing', 'Teknisk Fysik': 'F', 'Engineering Physics': 'F', 'Teknisk Nanovetenskap': 'F', 'Fire Protection Engineering': 'V', 'Brandingenj\xc3\xb6rsutbildning': 'V', 'Industriell ekonomi': 'I', 'Bioteknik': 'K',
                                         'Information and Communication Engineering': 'D', 'Computer Science and Engineering': 'D', 'Datateknik': 'D', 'Industrial Engineering and Management': 'I', 'Engineering Nanoscience': 'F', 'Architect': 'A', 'Chemical Engineering': 'K', 'Civil Engineering - Architecture': 'Ing', 'Maskinteknik med teknisk design': 'M', 'Lantm\xc3\xa4teri': 'V', 'Biotechnology': 'K', 'Medicin och teknik': 'E', 'Biomedical Engineering': 'E', 'Industridesign': 'A', 'Maskinteknik': 'M', 'Teknisk Matematik': 'F', 'Civil Engineering': 'V', 'Ekosystemteknik': 'W', 'Surveying': 'V', 'Electrical Engineering': 'E', 'Environmental Engineering': 'W', 'Arkitekt': 'A', 'Civil Engineering - Railway Construction': 'Ing'}

        for row in comany_reps:
            if row['Alcohol'].lower == "alkoholfritt":
                drinking_package = "no"
            else:
                drinking_package = "yes"
            desired_programmes = row['Desired programme'].split(",")
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
                                  'mail': row['Mail'],
                                  'company': row['Company'],
                                  'drinking_package': drinking_package}

            if company_rep_params['gender'].lower() == 'man':
                suits.append(company_rep_params)
            elif company_rep_params['gender'].lower() == 'woman':
                dresses.append(company_rep_params)
            else:
                company_rep_not_specified.append(company_rep_params)
    while company_rep_not_specified:
        if len(suits) > len(dresses):
            dresses.append(company_rep_not_specified.pop())
        else:
            suits.append(company_rep_not_specified.pop())

    return suits, dresses

### PRINTING RESULTS ###

def file_name(name, suffix, result):
    now = datetime.datetime.now()
    return f'output/{name}_{now.hour:02}:{now.minute:02}:{now.second:02}_{result["points"]}.{suffix}'


def print_result_to_list(result, tables):
    for table in tables:
        table['table_count'] = 0

    f_name = file_name('list', 'csv', result)
    with open(f_name, "w+") as output_file:
        print('Writiing to file ...', f_name)
        output_writer = csv.writer(output_file)
        output_writer.writerow(
            ['Name', 'Table Name', 'Seat number', 'Alcohol', 'Student/Company'])
        while result['left'] and result['right']:
            current_table_placement = result['left'][:15] + \
                result['right'][:15]
            result['left'] = result['left'][15:]
            result['right'] = result['right'][15:]

            current_table = None
            for table in tables:
                if table['tables'] - table['table_count'] == 0:
                    continue

                if not current_table:
                    current_table = table
                else:
                    if table['priority'] < current_table['priority']:
                        current_table = table
                    elif table['priority'] == current_table['priority'] and (table['tables'] - table['table_count']) > (current_table['tables'] - current_table['table_count']):
                        current_table = table
            if(not current_table):
                print('UNABLE TO FINISH, NO MORE TABLES')
                return

            table_name =current_table['name'] + " " + \
                str(1 + current_table['table_count'])

            for index, person in enumerate(current_table_placement):
                output_writer.writerow([
                    person['name'],
                    table_name,
                    index+1,
                    person['drinking_package'],
                    person['type']
                ])

            current_table['table_count'] += 1


def print_result_to_email(result, tables):
    for table in tables:
        table['table_count'] = 0

    f_name = file_name('email', 'txt', result)
    with open(f_name, "w+") as output_file:
        print('Writiing to file ...', f_name)
        while result['left'] and result['right']:
            current_table_placement = result['left'][:15] + \
                result['right'][:15]
            result['left'] = result['left'][15:]
            result['right'] = result['right'][15:]

            current_table = None
            for table in tables:
                if table['tables'] - table['table_count'] == 0:
                    continue

                if not current_table:
                    current_table = table
                else:
                    if table['priority'] < current_table['priority']:
                        current_table = table
                    elif table['priority'] == current_table['priority'] and (table['tables'] - table['table_count']) > (current_table['tables'] - current_table['table_count']):
                        current_table = table
            if(not current_table):
                print('UNABLE TO FINISH, NO MORE TABLES')
                return

            table_name = current_table['name'] + " " + \
                str(1 + current_table['table_count'])

            for index, person in enumerate(current_table_placement):
                output_file.write(
                    f"""{{"toAddress":"{person['mail']}", "namn":"{person['name']}", "bord":"{table_name}", "plats":"{index+1}"}}\n""")

            current_table['table_count'] += 1

### PROGRESSBAR ###


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 80, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * \
               (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end= printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

### MAIN ###


def main(iterations, students_list_path, company_reps_list_path):
    suits, dresses = parse_input(students_list_path, company_reps_list_path)
    distribution_left, distribution_right = create_distribution(suits, dresses)

    ratio = evaluate_ratio(suits + dresses)
    guild_points = evaluate_guild_points(suits + dresses)

    r = range(len(distribution_left))
    swaps = 0

    print('Points before: ', evaluate_distribution(
        distribution_left, distribution_right, ratio, guild_points))

    for iteration in range(iterations):
        printProgressBar(iteration, iterations)
        pos_i = (random.random() < 0.5, random.choice(r))
        pos_j = (random.random() < 0.5, random.choice(r))
        if try_swap(
            distribution_left,
            distribution_right,
            pos_i,
            pos_j,
            ratio,
            guild_points
        ):
            swaps += 1

    print()
    print('Points after: ', evaluate_distribution(
        distribution_left, distribution_right, ratio, guild_points))
    print(f'Swapping procentage: {100 * swaps / iterations:3.3}%')

    result = {
        'left': distribution_left,
        'right': distribution_right,
        'points': evaluate_distribution(
            distribution_left,
            distribution_right,
            ratio, guild_points)
    }

    # 5. Write out the best result to a csv file with table number and number on the table.
    tables = [{'name': 'Summer', 'seats': 30, 'tables': 6, 'priority': 2},
              {'name': 'Autumn', 'seats': 30, 'tables': 5, 'priority': 1},
              {'name': 'Spring', 'seats': 30, 'tables': 5, 'priority': 2},
              {'name': 'Winter', 'seats': 30, 'tables': 3, 'priority': 1}]

    res_temp1 = copy.deepcopy(result)
    res_temp2 = copy.deepcopy(result)

    print_result_to_list(res_temp1, tables)
    print_result_to_email(res_temp2, tables)


if __name__ == '__main__':
    iterations = 100000
    students_list_path = "input/students.csv"
    company_reps_list_path = "input/company_reps.csv"
    main(iterations, students_list_path, company_reps_list_path)
