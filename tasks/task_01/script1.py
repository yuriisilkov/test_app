import os

root_dir = os.path.abspath(os.curdir)
file_path = os.path.join(root_dir, "prices.txt")

_dict = {}
number_of_titles = 0

with open(file_path, 'r') as file:
    file_lines = file.readlines()
    for line in file_lines:
        if number_of_titles not in _dict.keys():
            _dict.update({number_of_titles: {}})
        if line.strip():
            key = line.split(":")[0].strip()
            value = line.split(":")[1].strip()
            _dict[number_of_titles].update({key: value})
            if "unitprice" in line:
                number_of_titles = number_of_titles + 1

for i in _dict:
    _dict[i]['sum'] = int(_dict[i]['quantity']) * int(_dict[i]['unitprice'])


print(f"total_amount: {sum([_dict[i]['sum'] for i in _dict])} $")

