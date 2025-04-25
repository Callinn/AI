import csv
import numpy as np
import re

# Function to transform experience into numeric value
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

# Function to perform min-max normalization
def min_max_normalize(data):
    min_val = np.min(data)
    max_val = np.max(data)
    return (data - min_val) / (max_val - min_val)

# Function to perform z-score normalization
def z_score_normalize(data):
    mean = np.mean(data)
    std_dev = np.std(data)
    return (data - mean) / std_dev

# Function to perform decimal scaling normalization
def decimal_scaling_normalize(data):
    max_abs_val = np.max(np.abs(data))
    scaling_factor = 10 ** np.ceil(np.log10(max_abs_val))
    return data / scaling_factor

# Function to get study years from education level
def get_study_years(ed_level):
    if "Doctoral degree" in ed_level:
        return 8  # 3 licență + 2 master + 3 doctorat
    elif "Master’s degree" in ed_level:
        return 5  # 3 licență + 2 master
    elif "Bachelor’s degree" in ed_level:
        return 3  # licență
    else:
        return 0  # nu are studii superioare

# Function to calculate study years for all respondents, respondents from Romania, and Romanian female respondents
def calculate_study_years(file_path):
    total_years = []


    with open(file_path, "r", encoding="utf-8") as file:
        csvreader = csv.reader(file)
        header = next(csvreader)

        for row in csvreader:

            ed_level = row[4]

            years = get_study_years(ed_level)

            # All respondents
            if years > 0:
                total_years.append(years)


    return np.array(total_years)

# Function to analyze programming experience and normalize both study years and experience
def analyze_and_normalize(file_path):
    # Calculate study years
    total_years= calculate_study_years(file_path)

    # Analyze programming experience
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

    experiences = np.array(experiences)

    # Perform normalizations
    total_years_min_max = min_max_normalize(total_years)
    total_years_z_score = z_score_normalize(total_years)
    total_years_decimal_scaling = decimal_scaling_normalize(total_years)

    experiences_min_max = min_max_normalize(experiences)
    experiences_z_score = z_score_normalize(experiences)
    experiences_decimal_scaling = decimal_scaling_normalize(experiences)

    return {
        'total_years': {
            'original': total_years,
            'min_max': total_years_min_max,
            'z_score': total_years_z_score,
            'decimal_scaling': total_years_decimal_scaling
        },
        'experiences': {
            'original': experiences,
            'min_max': experiences_min_max,
            'z_score': experiences_z_score,
            'decimal_scaling': experiences_decimal_scaling
        }
    }

def main():
    file_path = "data/surveyDataSience.csv"
    normalized_data = analyze_and_normalize(file_path)

    print("Total Years - Original:", normalized_data['total_years']['original'])
    print("Total Years - Min-Max Normalization:", normalized_data['total_years']['min_max'])
    print("Total Years - Z-Score Normalization:", normalized_data['total_years']['z_score'])
    print("Total Years - Decimal Scaling Normalization:", normalized_data['total_years']['decimal_scaling'])

    print("Experiences - Original:", normalized_data['experiences']['original'])
    print("Experiences - Min-Max Normalization:", normalized_data['experiences']['min_max'])
    print("Experiences - Z-Score Normalization:", normalized_data['experiences']['z_score'])
    print("Experiences - Decimal Scaling Normalization:", normalized_data['experiences']['decimal_scaling'])

if __name__ == "__main__":
    main()