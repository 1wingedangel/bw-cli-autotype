import requests
import pyperclip
import sys
import random
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL=os.getenv('BASE_URL')

def fetch_data(item_id):
    url = f"{BASE_URL}/object/item/{item_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data")
        sys.exit(1)

def copy_to_clipboard(data):
    if data:
        pyperclip.copy(data)

def extract_random_substring(data):
    if not data:
        return "", "", ""
    start = random.randint(1, len(data)-2)
    end = random.randint(start+1, len(data)-2)
    substring = data[start:end]
    head = data[:start]
    tail = data[end:]
    return substring, head, tail

def handle_operation(item_id, operation):
    if operation in ['copypass', 'copyuser', 'typeuser', 'typepass']:
        data = fetch_data(item_id)
        if operation in ['copypass', 'typepass']:
            target_data = data.get('data', {}).get('login', {}).get('password')
        elif operation in ['copyuser', 'typeuser']:
            target_data = data.get('data', {}).get('login', {}).get('username')
        
        if operation.startswith('copy'):
            copy_to_clipboard(target_data)
            print("copy success")
        else:
            substring, head, tail = extract_random_substring(target_data)
            copy_to_clipboard(substring)
            print(json.dumps({"head": head, "tail": tail}))
    elif operation == 'copytotp':
        url = f"{BASE_URL}/object/totp/{item_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                totp = data.get('data', {}).get('data')
                copy_to_clipboard(totp)
                print("copy success")
            else:
                print("No TOTP Available")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: script.py <item_id> <operation>")
        sys.exit(1)
    
    item_id = sys.argv[1]
    operation = sys.argv[2]
    
    handle_operation(item_id, operation)