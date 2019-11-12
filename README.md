# Gasque-Algorithm

A simple algorithm for the placement of the ARKAD gasque

## I/O files

The program takes to inputs. One csv with the students and one with the company representatives.

input/students.csv
input/company_reps.csv

The output will be produced into the "output" folder, which as of yet still is not automatically created.

### Input structure

Input expects a csv file with the columns, Name, Gender, Guild, Drinking package and Food pref for students and Name, Gender, Desired Programe, Company, Allergies and Drinking package for companies

The code for mapping the input csv to variables that are used in the program can currently be found in the function parse_input on row 195-260.

```javascript

attending_students = csv.DictReader(attending_students_csv)
for row in attending_students:
  student_params={
    'name': row['Name'],
    'gender': row['Gender'],
    'affiliation': row['Guild'],
    'mail': row['Mail'],
    'type': 'student',
    'drinking_package': row['Alcohol']
  }

comany_reps = csv.DictReader(company_reps_csv)
for row in comany_reps:
  company_rep_params = {
    'name': name,
    'gender': row['Gender'],
    'affiliation': guilds,
    'type': 'company_rep',
    'mail': row['Mail'],
    'company': row['Company'],
    'drinking_package': drinking_package
  }
```

The name of the rows can be changed, but make sure the parameter mapping above is correct, or the algorithm will not work.

### Output structure

There are two outputs from the program. From the methods print_result_to_file (row 269) and print_result_to_email (row 316)

### print_result_to_file

The first one is a csv formatted list with all seats.

```javascipt
Name,Table Name,Seat number,Alcohol,Student/Company
Alfa Alfasson,Summer 1,7,yes,Student
Beta Betasson,Summer 4,1,yes,Company
```

### print_result_to_email

The second output is a list in JSON format made specifically to help with automatic mailing in Jexpo.

```javascipt
{"toAddress":"alfa.alfasson@test.com", "namn":"Alfa Alfasson", "bord":"Summer 1", "plats":"7"}
{"toAddress":"beta.betasson@test.com", "namn":"Beta Betasson", "bord":"Summer 4", "plats":"1"}
```

Specify some table informtion in the follow structure found in the main method. Right before calling the output methods.

```javascript
tables = [
  { name: "Summer", seats: 30, tables: 6, priority: 2 },
  { name: "Autumn", seats: 30, tables: 5, priority: 1 },
  { name: "Spring", seats: 30, tables: 5, priority: 2 },
  { name: "Winter", seats: 30, tables: 3, priority: 1 }
];
```

## Algoritm

Algoritmen körs i två steg.

### Slumpmässig placering

Först organiserar den upp all personer i två listor, en för killar och en för tjejer. Detta så vi sedan kan placera ut alla personer slumpmässigt men i en struktur av varannan kille varannan tjej. Dvs enligt bordsdam / bordsherre principen.

### Många iterationer av byte

Sedan körs en loop där varje iteration så väljs två slumpmässiga personer ut. Och sedan om det anses göra fördelningen bättre så byts deras plats.

Det används flera metoder för att avgöra om ett byte är gynsamt eller ej.

Bland annat tittas på fördelning mellan killar och tjejer, vilket program studenter pluggar / företag är intresserade av att träffa och en balans funktion mellan studenter och företagsrepresentanter.

Alla dessa metoder börjar med <i>evaluate\_</i> prefixen.

## Contribution

Programmet skriven av Martin Johansson 2018
Fortsatt utveckling av Viktor Claesson 2019
