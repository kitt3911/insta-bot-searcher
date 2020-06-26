import glob
import json
from pprint import pprint 


files = glob.glob("json/*.json")
followers = {}
for f in files:
    with open(f, 'r') as f:
        data = json.load(f)
        for user in data['data']['user']['edge_followed_by']['edges']:
            user_info = user['node']
            followers[user_info['id']]={
                'id' : user_info['id'],
                'username' : user_info['username'] ,
                'followed_by_viewer' : user_info['followed_by_viewer'],
                'full_name' : user_info['full_name']
            }

followers = list(followers.values())
with open('followers.json', 'w') as f:
    json.dump(followers,f)

print('#ready')