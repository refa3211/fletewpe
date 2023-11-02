import json



def write_json_to_file(ip, mac, key, filename='ac.json'):
    data = {
        "ip": ip,
        "mac": mac,
        "key": key
    }

    try:
        with open(filename, 'a') as file:
            if file.tell() > 0:
                file.write(",\n")
            json.dump(data, file)
    except Exception as e:
        print(f"an error {e}")

