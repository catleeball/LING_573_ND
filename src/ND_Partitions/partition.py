# spit out id into file with the label so we can reverse lookup from the id to the text, that way we can put partitions into github repo
import jsonlines
import random

with open("data.jsonl", "r") as data:
    sarc_ids = []
    for line in jsonlines.Reader(data):
        id = line.get("id")
        sarc = line.get("sarcastic")
        ser = line.get("serious")

        if sarc == "1" and ser == "0":
            sarc_ids.append(id)
        
random.seed(13)

# Calculate the sizes for each partition
total_instances = len(sarc_ids)
train_size = int(0.8 * total_instances)
dev_size = int(0.1 * total_instances)
test_size = total_instances - train_size - dev_size

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
