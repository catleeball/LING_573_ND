import sys
import json
from pandas import DataFrame, concat

# command line:
# python error_analysis.py dev-comments-balanced.json /outputs/D2/d2.out

test_data_file = sys.argv[1]
model_out_file = sys.argv[2]

# ------------------------------------Load data--------------------------------------
with open(test_data_file, 'r') as f:
    test_data = json.load(f)

with open(model_out_file, 'r') as f:
    # save output file in dict
    model_out = {'pred':[], 'gold':[], 'prob_negative':[], 'prob_positive':[]}

    for line in f:
        lst = line.replace(',', '').split()
        # index labels and probabilities from each line, store in dict
        model_out['pred'].append(lst[1])
        model_out['gold'].append(lst[3])
        model_out['prob_negative'].append(lst[5])
        model_out['prob_positive'].append(lst[6])

# ------------------------------------Create table--------------------------------------
df1 = DataFrame.from_dict(model_out)
df2 = DataFrame.from_records(test_data)

table = concat([df2['response'], df1], axis=1)

# ------------------------------------Query table--------------------------------------
# prints simple table summary
print(table.describe())

# prints 20 of the incorrectly classified examples
print(table.loc[table['pred'] != table['gold']].head(20))

# explore false positives
false_pos = table.loc[(table['pred'] == '1') & (table['gold'] == '0')]
print(false_pos.head(20))
print('count false positives:', false_pos.shape[0])

# explore false negatives
false_neg = table.loc[(table['pred'] == '0') & (table['gold'] == '1')]
print(false_neg.head(20))
print('count false negatives:', false_neg.shape[0])