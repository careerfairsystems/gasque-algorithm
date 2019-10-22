# Gasque-Algorithm

A simple algorithm for the placement of the ARKAD gasque

## I/O files

The program takes to inputs. One csv with the students and one with the company representatives.

input/students.csv
input/company_reps.csv

The output will be produced into the "output" folder, with a

### Input structure

Input expects a csv file with the columns, Name, Gender, Guild, Drinking package and Food pref for students and Name, Gender, Desired Programe, Company, Allergies and Drinking package for companies

The code for mapping the input csv to variables that are used in the program can currently be found on row 145-207.

```javascript
student_params = {
  name: row["Name"],
  gender: row["Gender"],
  affiliation: row["Guild"],
  type: "student",
  drinking_package: row["Drinking package"],
  food_pref: row["Food pref"]
};

company_rep_params = {
  name: name,
  gender: row["Gender"],
  affiliation: guilds,
  type: "company_rep",
  company: row["Company"],
  food_pref: row["Allergies"],
  drinking_package: drinking_package
};
```

The name of the rows can be changed, but make sure the parameter mapping above is correct, or the algorithm will not work.

### Output structure

The output produces to files, one bigger csv file and a file splitting it up into tables based on the output below that you can find on line 269

```javascript
tables = [
  { name: "Cosmic Dust", seats: 30, tables: 5, front: True },
  { name: "Quasar", seats: 30, tables: 5, front: True },
  { name: "Dark Matter", seats: 30, tables: 5, front: False },
  { name: "Nebula", seats: 30, tables: 5, front: False }
];
```
