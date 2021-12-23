# -*- coding: utf-8 -*-
import os
import json
import requests
import sqlite3

conn = sqlite3.connect("/home/pi/speechbot/voice_lab/todo.db")
c = conn.cursor()
c.execute("select * from train")
list = c.fetchall()
conn.close()

CHECK_LIST = []
for v in list:
    dic_v = {}
    dic_v['name'] = v[1]
    CHECK_LIST.append(dic_v)

# ここを任意に変更してください。
# CHECK_LIST = [
#     {
#         'name': '常磐線各駅停車',
#         'company': 'JR東日本',
#         'website': 'https://traininfo.jreast.co.jp/train_info/kanto.aspx'
#     },
#     {
#         'name': '東西線',
#         'company': '東京メトロ',
#         'website': 'https://www.tokyometro.jp/unkou/history/touzai.html'
#     },
#     {
#         'name': '京急線',
#         'company': '京急電鉄',
#         'website': 'https://unkou.keikyu.co.jp/?from=top'
#     },
#     {
#         'name': 'ブルーライン',
#         'company': '横浜市営地下鉄',
#         'website': 'hogehoge'
#     },
# ]

JSON_ADDR = 'https://tetsudo.rti-giken.jp/free/delay.json'

# SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']


def lambda_handler():

    notify_delays = get_notify_delays()

    if not notify_delays:
        # 遅延が無ければ通知しない
        print("遅延情報はありません")
        return "遅延情報はありません"

    # Slack用のメッセージを作成して投げる
    (title, detail, voice_message) = get_message(notify_delays)
    # post_slack(title, detail)
    print(voice_message)
    return voice_message


def get_notify_delays():

    current_delays = get_current_delays()

    notify_delays = []

    for delay_item in current_delays:
        for check_item in CHECK_LIST:
            if delay_item['name'] == check_item['name']:
                notify_delays.append(check_item)

    return notify_delays


def get_current_delays():
    try:
        res = requests.get(JSON_ADDR)
    except requests.RequestException as e:
        # print(e)
        raise e

    if res.status_code == 200:
        return json.loads(res.text)
    return []


def get_message(delays):
    title = "電車の遅延があります。"
    voice_message = ""

    details = []

    for item in delays:
        name = item['name']
        # company = item['company']
        # website = item['website']
        # details.append(f'・{company}： {name}： <{website}|こちら>')
        details.append('・' + name)
        voice_message += name + ','
    voice_message += "が遅れている。これは訓練ではない。もう一度繰り返す。これは訓練ではない。"
    return title, '\n'.join(details), voice_message


def post_slack(title, detail):
    # https://api.slack.com/incoming-webhooks
    # https://api.slack.com/docs/message-formatting
    # https://api.slack.com/docs/messages/builder
    payload = {
        'attachments': [
            {
                'color': '#36a64f',
                'pretext': title,
                'text': detail
            }
        ]
    }

    # http://requests-docs-ja.readthedocs.io/en/latest/user/quickstart/
    try:
        response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))
    except requests.exceptions.RequestException as e:
        print("error")
    # else:
    #     print(response.status_code)

if __name__ == "__main__":
    lambda_handler()
