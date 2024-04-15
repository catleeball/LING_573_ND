# Retrieving Development Sets

The scripts in this folder retrieve SARC training data, sample 10% of it for the dev set, and retrieve the relevant comments for each sample in the dev set.

## (1) get_data.sh
- Retrieves and unzips the **full comments JSON** (about 2.5G) and the balanced training data.

## (2) partition_dev.sh
- Creates the toy and development sets:
  - Toy Set = first 10 instances from balanced training data (20 responses)
  - Dev Set = random 10% of training data (first 10 instances + random sample)
 
## (3) csv_to_json.sh
- Retrieves the text for each original post (plus any other comments in the context) and response listed in the given .csv.
- Returns a file with a list of JSONs (one per response).
- Essentially converts the condensed hash-code files into usable training data!
