import json
import random
import re
import sys

if len(sys.argv) != 2:
    print("Usage: python script.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

sarc_ids = []
srs_ids = []
unmarked_ids = []

# Read sarcastic authors
sarc_authors = set()
with open("sarc_authors.txt", "r") as f:
    for line in f:
        parts = line.strip().split('"')
        if len(parts) > 3 and parts[2] == ": ":
            sarc_authors.add(parts[3])

print(sarc_authors)

# Function to remove URLs from text
def remove_urls(text):
    url_pattern = re.compile(r'http\S+|www\.\S+')
    return url_pattern.sub(r'', text)

# Read input data
data_dict = {}
with open(input_file, "r") as data:
    for line_num, line in enumerate(data):
        line = line.strip()
        if not line or not line.startswith('{') or not line.endswith('}'):
            continue

        try:
            json_line = json.loads(line)
        except Exception as e:
            print(f'[WARN] Skipping line {line_num} due to json error: {e}\n')
            continue

        id = json_line.get('id')
        sarc = json_line.get('sarcastic')
        ser = json_line.get('serious')
        author = json_line.get('author')
        text = json_line.get('text')

        if text == "deleted" or text == "removed" or "I am a bot" in text:
            continue

        # Remove URLs from the text
        text = remove_urls(text)

        data_dict[id] = {"text": text, "label": None}

        if sarc == 1 and ser == 0:
            sarc_ids.append(id)
            data_dict[id]["label"] = 1
        elif ser == 1:
            srs_ids.append(id)
            data_dict[id]["label"] = 0
        elif sarc == 0 and ser == 0 and author in sarc_authors:
            unmarked_ids.append(id)
            data_dict[id]["label"] = 0

print(f"Number of sarcastic instances: {len(sarc_ids)}")
print(f"Number of serious instances: {len(srs_ids)}")
print(f"Number of unmarked instances: {len(unmarked_ids)}")

random.seed(13)

# Match the number of unmarked instances to the number of sarcastic instances
if len(unmarked_ids) > len(sarc_ids):
    unmarked_ids = random.sample(unmarked_ids, len(sarc_ids))

print(f"Number of unmarked instances after matching: {len(unmarked_ids)}")

# Combine all ids
all_ids = sarc_ids + srs_ids + unmarked_ids

# Shuffle the combined list
random.shuffle(all_ids)

# Calculate the sizes for each partition
total_instances = len(all_ids)
train_size = int(0.8 * total_instances)
dev_size = int(0.1 * total_instances)
test_size = total_instances - train_size - dev_size

# Split into partitions
train_data = all_ids[:train_size]
dev_data = all_ids[train_size:train_size + dev_size]
test_data = all_ids[train_size + dev_size:]

# Function to write JSON data to a file
def write_json_data(filename, data_ids):
    output_data = {id: {"text": data_dict[id]["text"], "label": data_dict[id]["label"]} for id in data_ids}
    with open(filename, "w") as out_file:
        json.dump(output_data, out_file, indent=2)

# Write to files
write_json_data("train.json", train_data)
write_json_data("dev.json", dev_data)
write_json_data("test.json", test_data)

# Output the count of sarcastic and unmarked instances included
print(f"Number of sarcastic instances included: {len(sarc_ids)}")
print(f"Number of unmarked instances included: {len(unmarked_ids)}")
