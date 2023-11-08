import json

datalist = []


def write_jsontolist(ip, mac, key):
    global datalist
    data = {
        "ip": ip,
        "mac": mac,
        "key": key,
        "status": "online"
    }

    if data not in datalist:
        datalist.append(data)
    else:
        index = datalist.index(data)

        data = {
            "ip": ip,
            "mac": mac,
            "key": key,
            "status": "offline"
        }
        datalist[index] = data




def writetofile(filename='ac.json'):
    global datalist

    try:
        with open(filename, 'a') as file:
            json.dump(datalist, file)
    except Exception as e:
        print(f"an error {e}")


def read_from_json(filename='ac.json', ac=None):
    # Open the JSON file
    with open(filename, 'r') as json_file:
        # Load the JSON data
        data = json.load(json_file)

    # Access a specific value from the loaded JSON data
    value = data
    print(value[ac])
    return value[ac]



