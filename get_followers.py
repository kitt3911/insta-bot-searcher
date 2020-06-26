import subprocess
import urllib.parse
import time
import json
from pprint import pprint

url_base = 'https://www.instagram.com/graphql/query/?'

command_template = """curl '{url}' \
  -H 'authority: www.instagram.com' \
  -H 'accept: */*' \
  -H 'x-ig-www-claim: hmac.AR2_J0axe4jrkb0ktDYglyZ8rttxVvKq-VBvLCymTeldckIC' \
  -H 'x-requested-with: XMLHttpRequest' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36' \
  -H 'x-csrftoken: RNp4f3qTQf3eq4x1f8vuZz68sRmHobeW' \
  -H 'x-ig-app-id: 936619743392459' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://www.instagram.com/lugburz13/followers/' \
  -H 'accept-language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'cookie: ig_did=599F7C38-136D-4C4C-BF20-A1E5949CEDEB; mid=XvWpzQAEAAE2IVvvednxMaX_7JZN; csrftoken=RNp4f3qTQf3eq4x1f8vuZz68sRmHobeW; ds_user_id=9444556890; sessionid=9444556890%3AcmMcfufPoTGJTs%3A8; shbid=1713; shbts=1593158114.676444; rur=PRN; urlgen="{{\"128.73.77.91\": 8402}}:1joka6:TKUjfFz4yX7g5S4efysrSNr-MR0"' \
  --compressed > json/followers_{index}.json"""
index = 1
after = None
followers_in_progress = 0
while True:
    after_value = f',"after":"{after}"' if after else ''
    variables = f'{{"id":"9444556890","include_reel":true,"fetch_mutual":false,"first":50{after_value}}}'
    get_params = {
        'query_hash': 'c76146de99bb02f6415203be841dd25a',
        'variables': variables 
    }
    ws_url = url_base + urllib.parse.urlencode(get_params)
    result = subprocess.run(command_template.format(url=ws_url,index=index),shell=True,capture_output=True)
    if result.returncode !=0:
        exit('ERROR REQUEST')
    with open(f'json/followers_{index}.json','r') as f:
        data = json.load(f)

    if not data['data']['user']['edge_followed_by']['page_info']['has_next_page']: 
        break
    after = data['data']['user']['edge_followed_by']['page_info']['end_cursor']
    all_followers = data['data']['user']['edge_followed_by']['count']
    in_current_batch = len(data['data']['user']['edge_followed_by']['edges'])
    followers_in_progress += in_current_batch
    print(f'Get : {followers_in_progress} / {all_followers}')
    time.sleep(5 if index % 10 !=0 else 20)
    index +=1

print('#ready')