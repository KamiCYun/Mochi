import requests
import ujson
import random

class AutoDiscord:
    def __init__(self, token):
        self.token = token

    def get_messages(self, channelid, count):
        headers = {
            'authority': 'discord.com',
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'authorization': self.token,
            'accept-language': 'en-US',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'dnt': '1',
        }

        params = (
            ('limit', count),
        )

        response = requests.get(f'https://discord.com/api/v9/channels/{channelid}/messages', headers=headers,
                                params=params)


        messages = ujson.loads(response.text)

        gptarr = []
        for message in messages:
            messagecontent = message['content']
            author = message['author']['username'].lower()
            if len(message['mentions']):
                for mention in message["mentions"]:
                    messagecontent = messagecontent.replace(f"<@!{mention['id']}>", mention["username"])

            if len(message['mention_roles']):
                for roleid in message["mention_roles"]:
                    messagecontent = messagecontent.replace(f"<@&{roleid}>", "")

            if f"{author}: {messagecontent}" not in gptarr:
                gptarr.append(f"{author}: {messagecontent}")
        return gptarr


    def send_message(self, channelid, message):
        headers = {
            'authority': 'discord.com',
            'authorization': self.token,
            'accept-language': 'en-US',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9002 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36',
            'content-type': 'application/json',
            'accept': '*/*',
            'origin': 'https://discord.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
        }

        nonce = str(random.randint(847500803001155584,867500803001155584))
        data = '{"content":"' + message + '","nonce":"' + nonce +'","tts":false}'

        r = requests.post(f'https://discord.com/api/v9/channels/{channelid}/messages', headers=headers,
                                 data=data.encode('utf-8'))