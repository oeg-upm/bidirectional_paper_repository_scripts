import re
import json

def find_first_two_digits(input_string):
    # Use regular expression to find the first two digits in the string
    match = re.search(r'\d{2}', input_string)
    if match:
        # Extract the matched digits and convert them to an integer
        try:
            digits = int(match.group())
            return digits
        except:
            return -1
    else:
        # Return a default value (e.g., -1) if no digits are found
        return -1


def convert_arxiv_to_year(input_string):
    int_year = find_first_two_digits(input_string)
    if int_year == -1:
        return None

    if int_year > 90:
        return int_year + 1900
    else:
        return int_year + 2000

def add_year_to_json(data):
    for key, items in data.items():
        for item in items:
            # Assuming the year is the first 4 digits of the key (e.g., "1111" from "1111.3806")
            year = convert_arxiv_to_year(key)
            # Adding the 'year' key to the item
            item['year'] = int(year) 
    return data




with open("../bidir.json", "r") as bidir_json:
    dict_bidir = json.load(bidir_json)

with_year_dict = add_year_to_json(dict_bidir)

with open("bidir_with_years.json", "w") as f:
    json.dump(with_year_dict, f, indent=4)