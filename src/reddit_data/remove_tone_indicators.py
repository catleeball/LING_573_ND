# Remove tone indicator tokens from text fields of jsonl data
import json
import re
import sys


INPUT_FILE = '/Media/Data/reddit/Tone_Indicator_Data/good_data.jsonl'
OUTPUT_FILE = '/Media/Data/reddit/Tone_Indicator_Data/gooder_data.jsonl'

SARCASM_INDICATOR_REGEX = re.compile(r'([^\s]?[/\\]s[\s$.,?!]?|[^\s]?[/\\]sarcasm[\s$.,?!]?|[^\s]?[/\\]sarcastic[\s$.,?!]?)')
SERIOUS_INDICATOR_REGEX = re.compile(r'([^\s]?[/\\]serious[\s$.,?!]?|[^\s]?[/\\]srs[\s$.,?!]?)')


def main():
    json_buffer = []
    with open(INPUT_FILE, 'r') as f:
        for line in f:
            try:
                json_line = json.loads(line)
            except Exception as e:
                sys.stderr.write(f'[ERROR] Failed to parse json line: {json_line}\n[ERROR][cont] Error: {e}')
                continue
            if not json_line:
                continue
            if 'text' not in json_line:
                sys.stderr.write(f'[WARN] Text field not in json line: {json_line}\n')
                continue
            if 'sarcastic' not in json_line:
                sys.stderr.write(f'[WARN] Sarcastic field not in json line: {json_line}\n')
                continue
            if 'serious' not in json_line:
                sys.stderr.write(f'[WARN] Serious field not in json line: {json_line}\n')
                continue
            if json_line['sarcastic'] == '1' or json_line['sarcastic'] == 1:
                json_line['text'] = re.sub(SARCASM_INDICATOR_REGEX, '', json_line['text'])
            if json_line['serious'] == '1' or json_line['serious'] == 1:
                json_line['text'] = re.sub(SERIOUS_INDICATOR_REGEX, '', json_line['text'])
            json_buffer.append(json_line)

    output_buffer = []
    for json_line in json_buffer:
        try:
            output_buffer.append(json.dumps(json_line))
        except Exception as e:
            sys.stderr.write(f'[ERROR] Failed to serialize json line: {json_line}\n[ERROR][cont] Error: {e}')
            continue

    output_buffer = '\n'.join(output_buffer)
    with open(OUTPUT_FILE, 'w') as f:
        f.write(output_buffer)


if __name__ == '__main__':
    main()
