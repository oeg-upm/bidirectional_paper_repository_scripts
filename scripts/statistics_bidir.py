import json

file = open("bidir.json","r")
json = json.load(file)

frequency = {}
total_entries = 0

for key,value in json.items():
    total_entries = total_entries + 1
    total = len(value)
    if total in frequency:
        frequency[total] = frequency[total]+1
    else:
        frequency[total] = 1

print("Total Entries:"+str(total_entries))
print (frequency)