import jsonlines
import random
import sys

if len(sys.argv) != 2:
    print("Usage: python script.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

sarc_ids = []
srs_ids = []

with open(input_file, "r") as data:
    reader = jsonlines.Reader(data)
    for line_num, line in enumerate(reader, start=1):
        try:
            id = line["id"]
            sarc = line["sarcastic"]
            ser = line["serious"]

            if sarc == "1" and ser == "0":
                sarc_ids.append(id)
            elif sarc == "1" and ser == "1":
                srs_ids.append(id)
        except (jsonlines.jsonlines.InvalidLineError, ValueError, KeyError) as e:
            # Skip the line if it is not properly formatted or if keys are missing
            print(f"Skipping line {line_num} due to error: {e}")
            continue

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
