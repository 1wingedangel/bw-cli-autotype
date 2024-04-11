import requests
import sys
import json
from urllib.parse import quote  # 导入quote函数进行URL编码
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL=os.getenv('BASE_URL')
MASTER_PASS=os.getenv('MASTER_PASS')

def send_post_request(url, data=None):
    response = requests.post(url, json=data)
    if response.status_code != 200:
        print("POST请求失败，状态码：", response.status_code)

def send_get_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("GET请求失败，状态码：", response.status_code)
        return None

def extract_and_format_data(data):
    result = {"result": []}
    for item in data['data']['data']:
        result['result'].append({"id": item['id'], "name": item['name']})
    return result

def main(search_term):
    post_url_unlock = f"{BASE_URL}/unlock"
    post_data = {"password": f"{MASTER_PASS}"}
    send_post_request(post_url_unlock, post_data) # 解锁数据库
    
    post_url_sync = f"{BASE_URL}/sync"
    send_post_request(post_url_sync) # 同步数据库

    encoded_search_term = quote(search_term)  # 对search_term进行URL编码
    get_url = f"{BASE_URL}/list/object/items?search={encoded_search_term}"
    data = send_get_request(get_url)
    # print(data)
    if data:
        formatted_data = extract_and_format_data(data)
        print(json.dumps(formatted_data, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("请提供一个搜索词作为参数",file=sys.stderr)
    else:
        search_term = sys.argv[1]
        main(search_term)