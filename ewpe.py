import argparse
import base64
import sys
from typing import Tuple, Any

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import json
import socket

GENERIC_KEY = "a3K8Bx%2r8Y7#xDh"

paramlist: list[str] = ['Pow', 'Blo', 'Mod', 'mac', 'Air', 'Health', 'SwUpDn', 'Quiet', 'Tur', 'TemUn', 'TemRec',
                        'SvSt', 'HeatCoolType', 'StHt', 'SetTem', 'WdSpd']


class ScanResult:
    ip = ''
    port = 0
    id = ''
    name = '<unknown>'

    def __init__(self, ip, port, id, name=''):
        self.ip = ip
        self.port = port
        self.id = id
        self.name = name


def send_data(ip, port, data):
    s = socket.socket(type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    s.settimeout(5)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.sendto(data, (ip, port))
    return s.recv(1024)


def create_request(tcid, pack_encrypted, i=0) -> str:
    return '{"cid":"app","i":' + str(i) + ',"t":"pack","uid":0,"tcid":"' + tcid + '","pack":"' + pack_encrypted + '"}'


def create_status_request_pack(tcid):
    return '{"cols":["Pow","Mod","SetTem","WdSpd","Air","Blo","Health","SwhSlp","Lig","SwingLfRig","SwUpDn","Quiet",' \
           '"Tur","StHt","TemUn","HeatCoolType","TemRec","SvSt"],"mac":"' + tcid + '","t":"status"}'


def add_pkcs7_padding(data):
    length = 16 - (len(data) % 16)
    padded = data + chr(length) * length
    return padded


def create_cipher(key):
    return Cipher(algorithms.AES(key.encode('utf-8')), modes.ECB(), backend=default_backend())


def decrypt(pack_encoded, key):
    decryptor = create_cipher(key).decryptor()
    pack_decoded = base64.b64decode(pack_encoded)
    pack_decrypted = decryptor.update(pack_decoded) + decryptor.finalize()
    pack_unpadded = pack_decrypted[0:pack_decrypted.rfind(b'}') + 1]
    return pack_unpadded.decode('utf-8')


def decrypt_generic(pack_encoded):
    return decrypt(pack_encoded, GENERIC_KEY)


def encrypt(pack, key):
    encryptor = create_cipher(key).encryptor()
    pack_padded = add_pkcs7_padding(pack)
    pack_encrypted = encryptor.update(bytes(pack_padded, encoding='utf-8')) + encryptor.finalize()
    pack_encoded = base64.b64encode(pack_encrypted)
    # print(f"pack_encoded.decode('utf-8'): {pack_encoded.decode('utf-8')}")
    return pack_encoded.decode('utf-8')


def encrypt_generic(pack):
    return encrypt(pack, GENERIC_KEY)


def search_devices(broadcast=None):
    if broadcast is None:
        broadcast = '192.168.0.255'
    print(f'Searching for devices using broadcast address: {broadcast}')

    s = socket.socket(type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    s.settimeout(5)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(b'{"t":"scan"}', (broadcast, 7000))

    results = []

    while True:
        try:
            (data, address) = s.recvfrom(1024)
            # print(f'data: {data}\nadderss: {address[0]}')

            if len(data) == 0:
                continue

            raw_json = data[0:data.rfind(b"}") + 1]


            resp = json.loads(raw_json)
            pack = json.loads(decrypt_generic(resp['pack']))
            # print(f'pack: {pack}')
            with open('ac.json', 'w') as file:
                json.dump(pack, file)

            cid = pack['cid'] if 'cid' in pack and len(pack['cid']) > 0 else \
                resp['cid'] if 'cid' in resp else '<unknown-cid>'

            results.append(ScanResult(address[0], address[1], cid, pack['name'] if 'name' in pack else '<unknown>'))

        except socket.timeout:
            print(f'Search finished, found {len(results)} device(s)')
            break

    if len(results) > 0:
        for r in results:
            bind_device(r)

    return results


def bind_device(search_result) -> tuple[Any, Any, Any, Any]:
    keys = {
        'ac1': {
            'ip': '',
            'mac': '',
            'key': ''
        },
        'ac2': {
            'ip': '',
            'mac': '',
            'key': ''
        },
        'ac3': {
            'ip': '',
            'mac': '',
            'key': ''
        },
        'ac4': {
            'ip': '',
            'mac': '',
            'key': ''
        }
    }

    print(f'Binding device: {search_result.ip} ({search_result.name}, ID: {search_result.id})\n')

    pack = '{"mac":"%s","t":"bind","uid":0}' % search_result.id
    pack_encrypted = encrypt_generic(pack)

    request = create_request(search_result.id, pack_encrypted, 1)
    result = send_data(search_result.ip, 7000, bytes(request, encoding='utf-8'))

    response = json.loads(result)
    # print(f'response: {response}')
    if response["t"] == "pack":
        pack = response["pack"]
        pack_decrypted = decrypt_generic(pack)
        # print(f'pack_decrypted: {pack_decrypted}\n')

        bind_resp = json.loads(pack_decrypted)
        # print(f'bind_resp: {bind_resp}')

        if 't' in bind_resp and bind_resp["t"].lower() == "bindok":
            key = bind_resp['key']
            # print('Bind to %s succeeded, key = %s' % (search_result.id, key))
            # keys.update(key)
            return key


def get_param(id, key, ipclient, params=None):
    if params is None:
        params = paramlist
    print(f'Getting parameters: {", ".join(params)}')

    cols: str = ','.join(f'"{i}"' for i in params)

    pack = f'{{"cols":[{cols}],"mac":"{id}","t":"status"}}'
    pack_encrypted = encrypt(pack, key)
    # print(f'pack encrypted\n {pack_encrypted} \n\n{key}')

    request = '{"cid":"app","i":0,"pack":"%s","t":"pack","tcid":"%s","uid":0}' % (pack_encrypted, id)
    result = send_data(ipclient, 7000, bytes(request, encoding='utf-8'))
    response = json.loads(result)

    if response["t"] == "pack":
        pack = response["pack"]

        pack_decrypted = decrypt(pack, key)
        pack_json = json.loads(pack_decrypted)

        for key, value in zip(pack_json['cols'], pack_json['dat']):
            print(f'{key} : {value}')


def set_param(id, key, ipclient, params=""):
    kv_list = [i.split('=') for i in params]
    errors = [i for i in kv_list if len(i) != 2]

    if len(errors) > 0:
        print(f'Invalid parameters detected: {errors}')
        exit(1)

    print(f'Setting parameters: {", ".join("=".join(i) for i in kv_list)}')

    opts = ','.join(f'"{i[0]}"' for i in kv_list)
    ps = ','.join(i[1] for i in kv_list)

    pack = f'{{"opt":[{opts}],"p":[{ps}],"t":"cmd"}}'
    pack_encrypted = encrypt(pack, key)

    request = '{"cid":"app","i":0,"pack":"%s","t":"pack","tcid":"%s","uid":0}' % (pack_encrypted, id)

    result = send_data(ipclient, 7000, bytes(request, encoding='utf-8'))
    response = json.loads(result)

    if response["t"] == "pack":
        pack = response["pack"]

        pack_decrypted = decrypt(pack, key)
        pack_json = json.loads(pack_decrypted)

        #dump data to file
        # pack_json.json()

        if pack_json['r'] == 200:
            print('Parameter set successfully')
        else:
            print(f'Failed to set parameter. Response code: {pack_json["r"]}')
    else:
        print('Unexpected response format from the device.')


def print_menu():
    print("\nMenu Options:")
    print("1. Search devices")
    print("2. Get parameters")
    print("3. Set parameters")
    print("4. Enter client/device settings")
    print("5. Print menu")
    print("6. Exit")


if __name__ == '__main__':
    while True:
        print_menu()
        command = input('Enter your choice: ')

        if command == '1':
            broadcast = input('Enter broadcast IP address: ')
            search_devices(broadcast=None)

        elif command == '2':
            ipclient = input('Enter client IP address: ')
            device_id = input('Enter unique ID of the device: ')
            key = input('Enter unique key of the device: ')
            get_param(device_id, key, ipclient)

        elif command == '3':
            ipclient = input('Enter client IP address: ')
            device_id = input('Enter unique ID of the device: ')
            key = input('Enter unique key of the device: ')
            param_input = input("Enter the params you want to change (e.g., 'Param=Value'): ")
            set_param(device_id, key, ipclient, params=[param_input])
        elif command == '4':
            ipclient = input('Enter client IP address: ')
            device_id = input('Enter unique ID of the device: ')
            key = input('Enter unique key of the device: ')
        elif command == '5':
            print_menu()
        elif command == '6':
            exit(1)
        else:
            print("Invalid option. Please choose a valid option.")
