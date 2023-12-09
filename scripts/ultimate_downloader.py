import requests
import xml.etree.ElementTree as ET
from time import sleep
import re
import os
import csv
import io
import logging 
import datetime
#Creates the url
BASE_URL = "http://export.arxiv.org/api/query?"
MAX_RESULTS_P_REQUEST = 2000
START = 0
CATEGORY = "cs.SE"
# END URL CREATION
# ================
NUM_PDF_SUCC, NUM_PDF_FAIL = 0, 0
NUM_LAT_SUCC, NUM_LAT_FAIL = 0, 0
LIST_LAT_FAILS, LIST_PDF_FAILS = [], []
# ================
CSV_FILE = 'corpus.csv'

logging.basicConfig(filename='error.txt', level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
arxiv_ids = []

def make_request(url):
    try:
        response = requests.get(url)
        # Necessary sleep, arxiv api limitation (1request / 3secs)
        sleep(3)
        if response.status_code == 200:
            return response
        elif response.status_code == 404:
            logging.error(f"NOT FOUND. URL: {url}")
            return None
        else:
            logging.error(f"Rejected with code: {response.status_code}. URL: {url}")
            return None
            
    except Exception as e:
        logging.error(f"Exception: {e} Issue while trying to preform request with: {url}")
        return None


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
    

def create_path_directory_from_arxiv(arxiv_directory):
    if not arxiv_directory:
        return None
    if not (year := convert_arxiv_to_year(arxiv_directory)):
        logging.error(f"{arxiv_directory}: Issue while creating the filepath for the arxiv, issue while converting to year")
        return None
    try:
            if not os.path.exists(str(year)):
                os.makedirs(str(year))
    except Exception as e:
            logging.error(f"{arxiv_directory}: Issue while creating year directory for given arxiv. Exception: {e}")
            return None
    try:
            path_directory = os.path.join(str(year), arxiv_directory)
            if os.path.exists(path_directory):
                logging.info(f"{arxiv_directory}: Path already exists")
                return path_directory
            os.makedirs(path_directory)
            return path_directory
    except Exception as e:
            logging.error(f"{arxiv_directory}: Issue while creating arxiv directory for given arxiv. Exception: {e}")
            return None


def download_file(url, filepath):
    if not (response := make_request(url)):
        return False
    try:    
            with open(filepath, 'wb') as file:
                file.write(response.content)
            return True
    except Exception as e:
            logging.error(f"{url}: Issue while writing file. Exception: {e}.")
            return False

def download_latex(arxiv_id):
    global NUM_LAT_FAIL
    global NUM_LAT_SUCC
    global LIST_LAT_FAILS
    if not arxiv_id:
        return None
    # Create path to directory of the arxiv
    directory_name = arxiv_id.replace('/','')
    if not(dir_path_arxiv := create_path_directory_from_arxiv(directory_name)):
        return None
    latex_url = f"https://arxiv.org/e-print/{arxiv_id}"
    latex_path = os.path.join(dir_path_arxiv, f"{directory_name}.zip")
    if os.path.exists(latex_path):
        latex_success = True
    else:
        latex_success = download_file(latex_url, latex_path) 
    if latex_success:
        NUM_LAT_SUCC += 1
        return latex_path
    else:
        logging.error(f"Failed to donwload latex for {arxiv_id}")
        NUM_LAT_FAIL += 1
        LIST_LAT_FAILS.append(arxiv_id)
        return None
         

def download_pdf(arxiv_id):
    global NUM_PDF_FAIL
    global NUM_PDF_SUCC
    global LIST_PDF_FAILS
    if not arxiv_id:
        return None
    # Create path to directory of the arxiv
    directory_name = arxiv_id.replace('/','')
    if not(dir_path_arxiv := create_path_directory_from_arxiv(directory_name)):
        return None
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    pdf_path = os.path.join(dir_path_arxiv, f"{directory_name}.pdf")
    if os.path.exists(pdf_path):
        pdf_success = True
    else:
        pdf_success = download_file(pdf_url, pdf_path)
    if pdf_success:
        NUM_PDF_SUCC += 1
        return pdf_path
    else:
        logging.error(f"Failed to download pdf for {arxiv_id}")
        NUM_PDF_FAIL += 1
        LIST_PDF_FAILS.append(arxiv_id)
        return None



def find_entry_metadata(entry):
    try:
        arxiv_id = entry.find("{http://www.w3.org/2005/Atom}id").text.split('/abs/')[-1]
        title = entry.find("{http://www.w3.org/2005/Atom}title").text

        #DOI
        doi = None
        mo_da_one_doi = []
        for arxiv in entry.findall(".//{http://arxiv.org/schemas/atom}doi"):
            mo_da_one_doi.append(arxiv.text)
        if len(mo_da_one_doi) > 1:
            logging.warning(f"{arxiv_id}: has more than one doi, have only returned the first!")
        elif len(mo_da_one_doi) > 0:
            doi = mo_da_one_doi[0]
        #End DOI

        return {"arxiv_id": arxiv_id, "title": title, "doi": doi}
    

    except Exception as e:
        if not arxiv_id:
            logging.error(f"Error while trying to extract metadata from arxiv entry: {e}")
            return None
        else:
            logging.error(f"{arxiv_id}: Error while trying to extract metadata from arxiv entry: {e}")
            return None


def iterate_entries(root):
    rows = []
    try:
        for entry in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
            metadata = find_entry_metadata(entry)
            if not metadata:
                continue
            if (arxiv := metadata['arxiv_id']) is None:
                logging.error(f"Error no arxiv ID for {str(entry)}")
                continue
            print(f"{arxiv}: Metadata worked, downloading")
            try:
                if pdf_path := download_pdf(arxiv):
                    pdf_path = os.path.abspath(pdf_path)
                if latex_path := download_latex(arxiv):
                    latex_path = os.path.abspath(latex_path)
                if latex_path and pdf_path:
                    print(f"{arxiv}: Successfully downloaded both files")
            except Exception as e:
                logging.error(f"Iterate_entries: Issue while dowloading the files {e}")
                latex_path = None
                pdf_path = None
            rows.append([safe_dic(metadata,"arxiv_id"), safe_dic(metadata,"title"), safe_dic(metadata,"doi"), latex_path, pdf_path])
        return rows
    except Exception as e:
        logging.error(f"Issue while trying to create rows. Exception: {e}")
        return None

def update_csv(csv_file, rows):
    if rows:
        try:
            with open(csv_file, 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerows(rows)
        except Exception as e:
                logging.error(f"Issue while updating the csv. Exception: {e}")
    else:
        logging.error(f"Issue while updating the csv, the rows trying to be written are empty {rows}")
        try:
            with open("results.txt", "w") as file:
                if not res:
                    logging.error("All is none in rows")
                for res in rows:
                    file.write("%s, " % res)
        except:
            logging.error(f" BACK UP FAIL Issue while updating the csv, the rows trying to be written are empty {rows}")




def safe_dic(dictionary, key):
    try:
        return dictionary[key]
    except:
        return None


# DECLARE CSV
headers = ['arxiv', 'title', 'doi', 'path_latex', 'path_pdf']
with open(CSV_FILE, 'w+', newline='\n') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)

    # Write the headers to the CSV file
    csv_writer.writerow(headers)

manual_backup = 14674 #Checked from query 
counter = 0
while True:
    # Constructs the url for the current page of results, START will be updated later.
    url = f"{BASE_URL}search_query=cat:{CATEGORY}&start={START}&max_results={MAX_RESULTS_P_REQUEST}"
    #url = f"{BASE_URL}search_query=cat:{CATEGORY}+AND+submittedDate:[19910801+TO+20231107]&start={START}&max_results={MAX_RESULTS_P_REQUEST}"
    #url = f"{BASE_URL}search_query=cat:{CATEGORY}&start={START}&max_results={MAX_RESULTS_P_REQUEST}&sortBy=submittedDate&sortOrder=ascending"
    
    # Verify if the request was successful
    if not (response := make_request(url)):
        logging.error("Error while requesting current page of results in arxiv")

    root = ET.fromstring(response.text)

    rows = iterate_entries(root)

    update_csv(CSV_FILE, rows)
    
    total_results = int(root.find(".//{http://a9.com/-/spec/opensearch/1.1/}totalResults").text)

   # Check the last publication date in the current batch
    last_entry_date = root.findall(".//{http://www.w3.org/2005/Atom}published")[-1].text
    last_entry_date_obj = datetime.datetime.strptime(last_entry_date, '%Y-%m-%dT%H:%M:%SZ')

    # Compare with the target date (1 November 2023)
    # if last_entry_date_obj < datetime.datetime(2023, 11, 1):
    #     print("Broke due to the date_time")
    #     break
    

    START += MAX_RESULTS_P_REQUEST
    counter += 1
    if START >= total_results:
        print(f"Start is :{START}, total_results is: {total_results}")
        break
        
    if counter > 50000:
        print("Broke due to manual break")
try:
    with open("results.txt", "w") as file:
        file.write(f"Total Number of possible PDFs/Latex = {total_results}\n")
        file.write(f"Successfully downloaded PDFs = {NUM_PDF_SUCC}\n")
        file.write(f"Failed PDFs = {NUM_PDF_FAIL}\n")
        if len(LIST_PDF_FAILS) > 0:
            file.write("Failed pdfs: \n")
            for arxiv in LIST_PDF_FAILS:
                file.write("%s, " % arxiv)
            file.write("\n")
        file.write(f"Successfully downloaded Latex's = {NUM_LAT_SUCC}\n")
        file.write(f"Failed Latex = {NUM_LAT_FAIL}\n")
        if len(LIST_LAT_FAILS) > 0:
            file.write("Failed Latex: \n")
            for arxiv in LIST_LAT_FAILS:
                file.write("%s, " % arxiv)
            file.write("\n")
except:
        print("issue creating results.txt file")
