import json

def open_json(json_path):
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
        return data
    except:
        return None
    
def count_urls_bidir(bidir_json: str, output_file: str):
        
    try: 
        count_bidirs = 0
                
        count_github = 0
        count_gitlab = 0
        count_zenodo = 0

        bidir_data = open_json(bidir_json)
        
        for arxiv_id in bidir_data:
            count_bidirs += 1
            print(arxiv_id)
            bidir_entries = bidir_data[arxiv_id]
            for entry in bidir_entries:
                arxiv_id_url = entry["url"]
                if "github" in arxiv_id_url:
                    count_github += 1
                elif "gitlab" in arxiv_id_url:
                    count_gitlab += 1
                elif "zenodo" in arxiv_id_url:
                    count_zenodo += 1
                else:
                    print(f"Something weird for {arxiv_id}, {arxiv_id_url}")
        print("===========")
        # Open an output file in write mode
        with open(output_file, 'w') as file:
            # Print statements with file argument
            print("here is the counts:", file=file)
            print(f"Count bidir_arxiv: {count_bidirs}", file=file)
            print(f"Count github: {count_github}", file=file)
            print(f"Count gitlab: {count_gitlab}", file=file)
            print(f"Count Zenodo: {count_zenodo}", file=file)

        
        return 
    except Exception as e:
        print(e)
        return

bidir = "bidir_new_regex_without_zenodo.json"
output_file = "after_regex_no_zenodo.txt"
count_urls_bidir(bidir, output_file)