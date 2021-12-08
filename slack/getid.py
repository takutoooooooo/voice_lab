from slack_sdk import WebClient

token = "xoxb-2512568670836-2807914598673-5RI57681lXVI6pRncCus0PDC"

client = WebClient(token)
res = client.users_list()

for member in res['members']:
    if "ornitho" in member["name"].lower():
        print(member['name'])
        print(member['id'])
        print()
