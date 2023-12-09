import json

file = open("processed_metadata.json","r",encoding="utf-8")
json = json.load(file)

frequency = {}
total_entries = 0

for key,value in json.items():
    total_entries = total_entries + 1
    urls = value["urls"]
    if len(urls) > 0:
        total = 0
        for url_entity in urls:
            total = total + len(url_entity) 
    else:
        total = 0

    if total in frequency:
        frequency[total] = frequency[total]+1
    else:
        frequency[total] = 1

print("Total Entries:"+str(total_entries))
print (frequency)