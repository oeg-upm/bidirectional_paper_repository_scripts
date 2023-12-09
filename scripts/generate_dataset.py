import json
import pandas as pd
import re

file = open("bidir.json","r")
json_bidir = json.load(file)

df = pd.DataFrame(columns=["arxiv_id","url"])

new_records = []

records_pdf = 0
records_latex = 0
records_overlap = 0
records_only_latex = 0


pattern = r'\((.*?)\)'

for key,value in json_bidir.items():
    records_pdf = records_pdf + 1
    for url_entity in value:
        new_records.append({"arxiv_id":key,"url":url_entity["url"]})
        

file.close()
df = pd.concat([df, pd.DataFrame(new_records)], ignore_index=True)


csv_file_latex = open("results_sources_2023-11-30_09-20-32.csv", "r")
csv_file_latex.readline()
data = []
for row in csv_file_latex:
    tokens = row.strip().split(",")
    arxiv_id = tokens[0]
    found = tokens[1]
    url_field = tokens[2]
    if len(tokens) == 4:
        url_field = url_field +","+ tokens[3]
        url_field.replace("'","")
    if found=="Found" and url_field.find("github") > 0:
        records_latex = records_latex + 1
        matches = re.findall(pattern, url_field)
        if len(matches) > 0:
            tokens_url= matches[0].strip().split(",")
            url_field = "https://github.com/"+tokens_url[0].strip().replace("'","")+"/"+tokens_url[1].strip().replace("'","")
        record = {"arxiv_id":tokens[0],"url":url_field}
        query = "arxiv_id=='"+tokens[0]+"' and url=='"+url_field+"'"
        potential_matches = df.query(query)
        if len(potential_matches) > 0:
            print("***********MATCH**************")
            print("PDF:"+str(potential_matches))
            print("Latex:"+str(record))
            records_overlap = records_overlap + 1
        else:
            print("*********** NOT MATCH**************")
            print("PDF:"+str(potential_matches))
            print("Latex:"+str(record)) 
            records_only_latex = records_only_latex + 1
            data.append(record)

csv_file_latex.close()
df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)

df.to_csv("bidir_dataset.csv", index = False)

print("Records PDF:"+str(records_pdf))
print("Num Latex:"+str(records_latex))
print("Overlap:"+str(records_overlap))
print("Only Latex:"+str(records_only_latex))
