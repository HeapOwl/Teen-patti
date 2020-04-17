import json
json_read = json.load(open('templates/temp.json','r'))
json_read["money"]+=0
json.dump(json_read,(open('templates/temp.json','w')))
print(json_read)