import json

datalist = []


def write_jsontolist(ip, mac, key):
    global datalist
    data = {
        "ip": ip,
        "mac": mac,
        "key": key
    }
    if data not in datalist:
        datalist.append(data)


def writetofile(filename='ac.json'):
    global datalist

    try:
        with open(filename, 'w') as file:
            json.dump(datalist, file)
    except Exception as e:
        print(f"an error {e}")

    # Open the JSON file
    with open('ac.json', 'r') as json_file:
        # Load the JSON data
        data = json.load(json_file)

    # Access a specific value from the loaded JSON data
    value = data
    print(value[0])
