import csv
from collections import Counter, defaultdict
import re

import numpy as np
import pandas

#Input:`file_path` - calea către fișierul CSV.
#Output: Numărul de linii din fișierul CSV.

def count_lines(file_path):
    with open(file_path, "r") as file:
        csvreader = csv.reader(file)
        next(csvreader)

        line_count = sum(1 for _ in csvreader)

    return line_count

#Obține informații despre coloanele dintr-un fișier CSV
#Input:`file_path` - calea către fișierul CSV.
# Output:
#  - `numar_atribute` - numărul de atribute.
#  - `header` - antetul coloanelor.
#  - `header1` - prima linie de descriere.
def get_column_info(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        csvreader = csv.reader(file)
        header1=next(csvreader)
        header = next(csvreader)
        numar_atribute = len(header)
        return numar_atribute, header,header1


#Descriere: Numără respondenții cu date complete și femeile din România cu date complete.
#Input: `file_path` - calea către fișierul CSV.
#Output:
#- `complete_respondents_woman_romania` - numărul de femei din România cu date complete.
#- `complete_respondents` - numărul total de respondenți cu date complete.
def complete_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        csvreader = csv.reader(file)
        next(csvreader)
        header = next(csvreader)

        complete_respondents = 0
        complete_respondents_woman_romania = 0

        for row in csvreader:

            if any(value == "None" for value in row):
                continue

            complete_respondents += 1

            country = row[3].strip().lower() if row[3] else ''
            gender = row[2].strip().lower() if row[2] else ''

            if gender == "woman" and country == "romania":
                complete_respondents_woman_romania += 1

        return complete_respondents_woman_romania, complete_respondents


#Descriere: Convertește nivelul educațional în ani de studii.
#Input: string:`ed_level` - nivelul educațional.
#Output: Numărul de ani de studii corespunzător nivelului educațional.
def get_study_years(ed_level):


    if "Doctoral degree" in ed_level:
        return 8  # 3 licență + 2 master + 3 doctorat
    elif "Master’s degree" in ed_level:
        return 5  # 3 licență + 2 master
    elif "Bachelor’s degree" in ed_level:
        return 3  # licență
    else:
        return 0  # nu are studii superioare



#Descriere: Calculează durata medie a anilor de studii pentru toți respondenții, respondenții din România și femeile din România.
#Input: `file_path` - calea către fișierul CSV.
#Output:
#`avg_total` - durata medie a anilor de studii pentru toți respondenții.
#`avg_romania` - durata medie a anilor de studii pentru respondenții din România.
#`avg_romania_females` - durata medie a anilor de studii pentru femeile din România.
def calculate_study_years(file_path):
    total_years = []
    years_romania = []
    years_romania_females = []

    with open(file_path, "r", encoding="utf-8") as file:
        csvreader = csv.reader(file)

        for row in csvreader:
            country = row[3].strip()
            gender = row[2].strip().lower()
            ed_level = row[4]

            years = get_study_years(ed_level)

            if years > 0:
                total_years.append(years)

            if country.lower() == "romania" and years > 0:
                years_romania.append(years)

                if gender == "woman":
                    years_romania_females.append(years)

    # Calcul medii
    avg_total = sum(total_years) / len(total_years) if total_years else 0
    avg_romania = sum(years_romania) / len(years_romania) if years_romania else 0
    avg_romania_females = sum(years_romania_females) / len(years_romania_females) if years_romania_females else 0

    return avg_total, avg_romania, avg_romania_females


#Descriere:** Analizează preferințele de limbaj de programare (Python și C++) pentru femeile din România și determină intervalele de vârstă cele mai frecvente.
#Input: `file_path` - calea către fișierul CSV.
#Output:
# `women_python` - numărul de femei din România care programează în Python.
# `python_age_ranges` - intervalul de vârstă cel mai frecvent pentru femeile care programează în Python.
# `women_c` - numărul de femei din România care programează în C++.
# `cpp_age_ranges` - intervalul de vârstă cel mai frecvent pentru femeile care programează în C++.
def analyze_languages(file_path):
    women_python = 0
    women_c = 0
    python_age_ranges = Counter()
    cplus_age_ranges = Counter()
    with open(file_path, "r", encoding="utf-8") as file:
        csvreader = csv.reader(file)
        header1 = next(csvreader)
        header = next(csvreader)

        for row in csvreader:
            country = row[3].strip().lower()
            gender = row[2].strip().lower()
            age = row[1].strip()
            python_choiche = row[7].strip()
            cplus_choiche = row[11].strip()
            if gender != "woman" or country != "romania":
                continue

            if python_choiche:
                women_python += 1
                python_age_ranges[age]+=1
            if cplus_choiche:
                women_c +=1
                cplus_age_ranges[age]+=1

        return women_python,python_age_ranges.most_common(1) ,women_c,cplus_age_ranges.most_common(1)


#Descriere: Determină domeniul de valori posibile și valorile extreme pentru fiecare atribut/proprietate.
#Input: `file_path` - calea către fișierul CSV.
#Output:
#`numeric_ranges` - domeniile valorilor numerice pentru fiecare întrebare.
#`categorical_counts` - numărul de valori unice pentru fiecare întrebare categorială.
def domain_values(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        csvreader = csv.reader(file)
        header = next(csvreader)  # Get column headers
        next(csvreader)

        numeric_ranges = defaultdict(lambda: {"min": float('inf'), "max": float('-inf')})
        categorical_values = defaultdict(set)

        question_groups = defaultdict(list)
        for col in header:
            question_match = re.match(r"(Q\d+)(_A|_B)?(_Part_\d+)?", col)

            if question_match:
                # E o intrebare cu parti
                question = question_match.group(1)
                part = question_match.group(2) if question_match.group(2) else ''
                question_groups[question + part].append(col)
            else:
                # Coloana simpla, o tratam pe cont propriu
                question_groups[col].append(col)

        for row in csvreader:
            for question, cols in question_groups.items():
                for col in cols:
                    value = row[header.index(col)].strip()
                    if value.isdigit():  # Verifica daca valoarea e numerica
                        value = float(value)
                        numeric_ranges[question]["min"] = min(numeric_ranges[question]["min"], value)
                        numeric_ranges[question]["max"] = max(numeric_ranges[question]["max"], value)
                    elif value:  # Pentru valorile non-numerice adauga in set
                        categorical_values[question].add(value)

        categorical_counts = {k: len(v) for k, v in categorical_values.items()}
     #  print(f"Categorice Q6: {categorical_values['Q6']}")

        return numeric_ranges, categorical_counts


#Descriere: Transformă experiența în programare exprimată în text în număr de ani.
#Input: `experience` - experiența în programare sub formă de text.
#Output: Numărul de ani de experiență.
def transform_experience(experience):
    if experience == 'I have never written code':
        return 0
    elif experience == '20+ years':
        return 25
    elif experience == '< 1 years':
        return 0.5
    else:
        match = re.match(r'(\d+)-(\d+) years', experience)
        if match:
            start, end = map(int, match.groups())
            return (start + end) / 2
    return None


#Descriere: Analizează experiența în programare a respondenților, calculând statistici precum minimul, maximul, media, deviația standard și mediana.
#Input: `file_path` - calea către fișierul CSV.
#Output:
# `minimum` - experiența minimă în programare.
# `maximum` - experiența maximă în programare.
# `mean` - media experienței în programare.
# `std_dev` - deviația standard a experienței în programare.
# `median` - mediana experienței în programare.
def analyze_experience(file_path):
    experiences = []

    with open(file_path, "r", encoding="utf-8") as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        next(csvreader)

        q6_index = header.index('Q6')

        for row in csvreader:
            experience = row[q6_index].strip()
            transformed_experience = transform_experience(experience)
            if transformed_experience is not None:
                experiences.append(transformed_experience)

    # Calculare statistica
    experiences = np.array(experiences)
    minimum = np.min(experiences)
    maximum = np.max(experiences)
    mean = np.mean(experiences)
    std_dev = np.std(experiences)
    median = np.median(experiences)

    return minimum, maximum, mean, std_dev, median


def main():
    file_path = "data/surveyDataSience.csv"
    while True:
        print("\n=== MENIU ===")
        print("1. Afișează numărul de participanți")
        print("2. Afișează numărul și numele atributelor pentru fiecare respondent")
        print("3. Afișează numărul de respondenți cu date complete")
        print("4. Afișează durata medie a anilor de studii (toți, România, femei din România)")
        print("5. Nr femei care programeaza in python + care programeaza in C++ si intervalul de varsta cel mai frecvent intalnit")
        print("6. Domeniul de valori posibile si valorile extreme pentru fiecare atribut/proprietate")
        print("7. Vechimea in programare in numar de ani")
        print("0. Ieșire")

        optiune = input("Alege o opțiune: ")

        if optiune == "1":
            numar_participanti = count_lines(file_path)
            print(f"Nr de participanti este: {numar_participanti}\n")

        elif optiune == "2":
          numar_atribute, nr_q,nume_atribute = get_column_info(file_path)
          print(f"Numărul de atribute pentru fiecare respondent: {numar_atribute}")
          print("Atributele sunt:")
          for atribut, q in zip(nume_atribute, nr_q):
              print(f" - {atribut} (Q: {q})")


        elif optiune == "3":
            complete_woman,complete = complete_data(file_path)
            print(f"Numărul de respondenți cu date complete: {complete}")
            print(f"Numărul de respondenți cu date complete,femei: {complete_woman}")


        elif optiune == "4":
            avg_total, avg_romania, avg_romania_females = calculate_study_years(file_path)

            print(f"Durata medie a anilor de studii pentru toți respondenții: {avg_total:.2f} ani")
            print(f"Durata medie a anilor de studii pentru respondenții din România: {avg_romania:.2f} ani")
            print(f"Durata medie a anilor de studii pentru femeile din România: {avg_romania_females:.2f} ani")

        elif optiune == "5":
            python_nr, python_avg,cplus_nr,cplus_avg = analyze_languages(file_path)
            print(f"Femeile din romania care programeaza in python: {python_nr}")
            print(f"intervalul de varsta cu cele mai multe femei care programeaza in Python: {python_avg}")
            print(f"Femeile din romania care programeaza in c++: {cplus_nr}")
            print(f"intervalul de varsta cu cele mai multe femei care programeaza in c++: {cplus_avg}")
            if python_nr > cplus_nr:
              print("\nSunt mai multe femei care programează în Python decât în C++.")
            elif cplus_nr > python_nr:
               print("\nSunt mai multe femei care programează în C++ decât în Python.")
            else:
               print("\nNumărul femeilor care programează în Python și C++ este egal.")

        elif optiune == "6":
            numeric_ranges, categorical_counts = domain_values(file_path)
            print("Numeric Ranges:")
            for col, min_max in numeric_ranges.items():
                print(f"{col}: min = {min_max['min']}, max = {min_max['max']}")


            print("\nCategorical Counts:")
            for col, count in categorical_counts.items():
                print(f"{col}: {count} unique values")


        elif optiune == "7":
            minimum, maximum, mean, std_dev, median = analyze_experience(file_path)
            print("Statistica experienta programare:")
            print(f"Minim: {minimum} ani vechime")
            print(f"Maxim: {maximum} ani vechime")
            print(f"Media: {mean} ani vechime")
            print(f"Deviatia standard: {std_dev} ani vechime")
            print(f"Mediana: {median} ani vechime")

        elif optiune == "0":
            print("\nProgram închis.")
            break


        else:
            print("\nOpțiune invalidă. Încearcă din nou.")


if __name__ == "__main__":
    main()
