from slack_sdk import WebClient

token = "xoxb-2512568670836-2807914598673-5RI57681lXVI6pRncCus0PDC"

client = WebClient(token)
user_id = 'U02FCL81734'

# DMを開き，channelidを取得する．
res = client.conversations_open(users=user_id)
dm_id = res['channel']['id']

# DMを送信する
client.chat_postMessage(channel=dm_id, text='馬鹿野郎')
