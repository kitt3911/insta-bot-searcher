import json
import subprocess
import time
from pprint import pprint


with open('followers.json','r') as f:
    followers = json.load(f)

pprint(followers)

command_template = """curl 'https://www.instagram.com/{username}/?__a=1' \
  -H 'authority: www.instagram.com' \
  -H 'accept: */*' \
  -H 'x-ig-www-claim: hmac.AR2_J0axe4jrkb0ktDYglyZ8rttxVvKq-VBvLCymTeldckIC' \
  -H 'x-requested-with: XMLHttpRequest' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36' \
  -H 'x-ig-app-id: 936619743392459' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://www.instagram.com/adci.russia/' \
  -H 'accept-language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'cookie: ig_did=599F7C38-136D-4C4C-BF20-A1E5949CEDEB; mid=XvWpzQAEAAE2IVvvednxMaX_7JZN; csrftoken=RNp4f3qTQf3eq4x1f8vuZz68sRmHobeW; ds_user_id=9444556890; sessionid=9444556890%3AcmMcfufPoTGJTs%3A8; shbid=1713; shbts=1593158114.676444; rur=PRN; urlgen="{{\"128.73.77.91\": 8402}}:1jomtu:VTeWTsN7rZsdLaPha_NfSiJ_McM"' \
  --compressed > temp.json"""

index = 0
followers_filled = [] 
for user in followers:
    subprocess.run(command_template.format(username=user['username']),shell=True,capture_output=True)
    with open('temp.json','r') as f:
        data = json.load(f)
    user['follows'] = data['graphql']['user']['edge_followed_by']['count']
    user['posts'] = data['graphql']['user']['edge_owner_to_timeline_media']['count']
    user['bio'] = data['graphql']['user']['biography']
    followers_filled.append(user)
    print(f'Iteration : {index}/{len(followers)}')
    time.sleep(3 if index %10!=0 else 5)
    index+=1
with open('followers_filled.csv','w') as f:
    f.write(f"Name,Username,Follow by,Posts,Bio\n")
    for user in followers_filled:
        f.write((f"{user['full_name']},{user['username']},{user['follows']},{user['posts']},{user['bio']}\n"))
        