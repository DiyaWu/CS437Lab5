import re
import json

def parse_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    zebra_data = []

    animal_sections = content.split("=============== ")
    for section in animal_sections[1:]:
        animal_type, rest = section.strip().split(":", 1)
        animal_id, log_content = rest.strip().split(" LOG ===============\n", 1)
        data = parse_log_content(log_content)
        zebra_data.append({"animal_type":animal_type, "ID": animal_id, "data": data})
    
    return zebra_data

def parse_log_content(log_content):
    data = []
    log_lines = log_content.split('\n')

    current_data = {}
    for line in log_lines:
        if line.startswith("-- Timestamp:"):
            if current_data:
                data.append(current_data)
            current_data = {"Timestamp": float(line.split()[-1])}
        elif line.startswith('"'):
            if line.startswith('"oxygen_saturation'):
                sub = line.split(',')
                for l in sub:
                    l = l.lstrip()
                    key, value = parse_key_value(l)
                    current_data[key] = value
            else:    
                key, value = parse_key_value(line)
                current_data[key] = value

    if current_data:
        data.append(current_data)

    return data

def parse_key_value(line):
    key, value = re.match(r'"(.+?)": (.+)', line).groups()
    try:
        value = json.loads(value)
    except json.JSONDecodeError:
        pass
    return key, value

def write_to_json_file(data, output_file_path):
    with open(output_file_path, 'w') as output_file:
        json.dump(data, output_file, indent=2)

if __name__ == '__main__':
    input_file_path = '30min.txt'
    output_file_path = '30output.json'
    parsed_data = parse_file(input_file_path)
    write_to_json_file(parsed_data, output_file_path)

