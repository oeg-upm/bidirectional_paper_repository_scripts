import pandas as pd
import json

def overlap_counter (results_file, bidir_json):
    # Count the arxivs that are in common
    in_common = []
    in_common_count = 0
    
    # IDs that have been found to both be bidirectional
    overlapped_ids = []
    overlapped_count = 0
    
    # Ones detected in nicola and not SSKG
    weird = []
    weird_count = 0
    
    # Ones detected in SSKG and not Nicola
    sskg_different = []
    sskg_different_count = 0
    
    # Uh oh's, Githubs where nicola detected it and not us:
    uh_oh = []
    uh_oh_count = 0
    
    count = 0
    # Open the folders:
    df = pd.read_csv(results_file, dtype=str)
    with open(bidir_json, "r") as f:
        bidir_dict = json.load(f)

    nic_ids = []
    
    for index, row in df.iterrows():
        arxiv_id = row["ArXiV id"]
        found = row["Result"]
        found = found == "Found"
        
        nic_ids.append(arxiv_id)
        
        if found: # See if they both agree that its bidir
            if arxiv_id in bidir_dict.keys():
                overlapped_ids.append(arxiv_id)
                overlapped_count += 1
            else: # Nicola found it to be bidir while we didn't
                weird_count += 1
                reason = row["Where"]
                weird.append((arxiv_id, reason))
                if "github" in reason:
                    uh_oh.append(arxiv_id)
                    uh_oh_count += 1
        else:
                if arxiv_id in bidir_dict.keys(): # RSEF/SSKG considered it to be bidirectional Nicola did not 
                    
                    sskg_different.append(arxiv_id)
                    sskg_different_count += 1 
        
    for arxiv_id in bidir_dict.keys():  
        if arxiv_id not in nic_ids:
            sskg_different.append(arxiv_id)
            sskg_different_count += 1 
    return overlapped_count, overlapped_ids, weird, weird_count, sskg_different, sskg_different_count, uh_oh, uh_oh_count

results_csv = "../results_sources_2023-11-30_09-20-32.csv"
sskg_bidir = "../bidir.json"

overlapped_count, list_overlapped, weird, weird_count, sskg_different, sskg_different_count, uh_oh, uh_oh_count = overlap_counter(results_csv, sskg_bidir)

#print(overlapped_count, list_overlapped, weird, weird_count, sskg_different, sskg_different_count, uh_oh, uh_oh_count)

# Writing results to files
with open('overlapped_ids.txt', 'w') as f:
    f.write("Number of Bidir ID's in common: " + str(overlapped_count) + "\n")
    for id in list_overlapped:
        f.write(f"{id}\n")

with open('found_in_nicola_NOT_sskg.txt', 'w') as f:
    f.write("Number IDs Nicola detected and not SSKG/RSEF: " + str(weird_count) + "\n")
    for item in weird:
        f.write(f"{item}\n")

with open('found_in_sskg_NOT_nicola.txt', 'w') as f:
    f.write("Number IDs SSKG detected and not Nicola: " + str(sskg_different_count) + "\n")
    for id in sskg_different:
        f.write(f"{id}\n")

with open('git_nicola_won.txt', 'w') as f:
    f.write("Github that nicola detected not SSKG: " + str(uh_oh_count) + "\n")
    for id in uh_oh:
        f.write(f"{id}\n")
