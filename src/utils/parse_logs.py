import re 


filename = "train_roberta_context.logs"

input_file = f"logs/training/{filename}"
output_file = f"logs/parsed/{filename}"
with open(input_file) as f_in, open(output_file, "w") as f_out:
    for l in f_in.readlines():
        metrics = re.search("{.+}", l)
        if metrics:
            f_out.write(metrics.group() + '\n')
            