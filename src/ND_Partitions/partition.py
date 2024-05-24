import json
import random
import sys

if len(sys.argv) != 2:
    print("Usage: python script.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

sarc_ids = []
srs_ids = []

with open(input_file, "r") as data:
    for line_num, line in enumerate(data):
        line = line.strip()

        if not line:
            continue
        if not line.startswith('{'):
            continue
        if not line.endswith('}'):
            continue

        try:
            json_line = json.loads(line)
        except Exception as e:
            sys.stderr.write(f'[WARN] Skipping line {line_num} due to json error: {e}\n')
            continue

        id = None
        sarc = None
        ser = None

        if 'id' in json_line:
            id = json_line['id']
        if not 'metadata' in json_line:
            continue
        if 'sarcastic' in json_line['metadata']:
            sarc = json_line['metadata']['sarcastic']
        if 'serious' in json_line['metadata']:
            ser = json_line['metadata']['serious']

        if sarc == "1" and ser == "0":
            sarc_ids.append(id)
        if ser == "1":
            srs_ids.append(id)

random.seed(13)

# SARCASTIC

# Calculate the sizes for each partition
sarc_instances = len(sarc_ids)
train_size = int(0.8 * sarc_instances)
dev_size = int(0.1 * sarc_instances)
test_size = sarc_instances - train_size - dev_size

# Shuffle the data instances
random.shuffle(sarc_ids)

# Split into partitions
train_data = sarc_ids[:train_size]
dev_data = sarc_ids[train_size:train_size + dev_size]
test_data = sarc_ids[train_size + dev_size:]

with open("s1_srs0_train.txt", "w") as train_out:
    for id in train_data:
        train_out.write(id + ": 1\n")

with open("s1_srs0_dev.txt", "w") as dev_out:
    for id in dev_data:
        dev_out.write(id + ": 1\n")

with open("s1_srs0_test.txt", "w") as test_out:
    for id in test_data:
        test_out.write(id + ": 1\n")

# SERIOUS

# Calculate the sizes for each partition
srs_instances = len(srs_ids)
train_size = int(0.8 * srs_instances)
dev_size = int(0.1 * srs_instances)
test_size = srs_instances - train_size - dev_size

# Shuffle the data instances
random.shuffle(srs_ids)

# Split into partitions
train_data = srs_ids[:train_size]
dev_data = srs_ids[train_size:train_size + dev_size]
test_data = srs_ids[train_size + dev_size:]

with open("s1_srs1_train.txt", "w") as train_out:
    for id in train_data:
        train_out.write(id + ": 0\n")

with open("s1_srs1_dev.txt", "w") as dev_out:
    for id in dev_data:
        dev_out.write(id + ": 0\n")

with open("s1_srs1_test.txt", "w") as test_out:
    for id in test_data:
        test_out.write(id + ": 0\n")
