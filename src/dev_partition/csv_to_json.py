import argparse
import json

if __name__ == "__main__":

    # command line arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Name of the csv file that contains comment codes.")
    parser.add_argument("--dataset", type=str, default="comments.json", help="The full dataset JSON to retrieve comments from.")
    parser.add_argument("--output", type=str, help="Name of the json file which will contain program output.")
    args = parser.parse_args()
    
    with open(args.dataset, 'r') as f:
        dataset = json.load(f)

    with open(args.input, "r") as in_csv:
        with open(args.output, "w") as out_json:
            out_json.write("[")
            lines = in_csv.readlines()
            last_line = len(lines)
            i = 1

            for line in lines:
                posts, responses, labels = line.split("|")
                post_list = posts.split()
                response1, response2 = responses.split()
                label1, label2 = labels.split()

                json_dict1 = {}
                json_dict1["posts"] = [dataset[p]["text"] for p in post_list] # post content
                json_dict1["post_ids"] = post_list # key number
                json_dict1["context_size"] = len(post_list)
                json_dict1["response_id"] = response1 # key number
                json_dict1["response"] = dataset[response1]["text"] # response content 
                json_dict1["label"] = label1 # 0 or 1

                json_dict2 = {}
                json_dict2["posts"] = [dataset[p]["text"] for p in post_list] # post content
                json_dict2["post_ids"] = post_list # key number
                json_dict2["context_size"] = len(post_list)
                json_dict2["response_id"] = response2 # key number
                json_dict2["response"] = dataset[response2]["text"] # response content 
                json_dict2["label"] = label2 # 0 or 1

                out_json.write(json.dumps(json_dict1))
                out_json.write(",\n")
                out_json.write(json.dumps(json_dict2))
                if i < last_line:
                    out_json.write(",\n")
                i+=1

            out_json.write("]")