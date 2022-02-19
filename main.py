from MochiDiscord import AutoDiscord
import openai
import time


openai.api_key = ""
discordToken = ""
channelid = ""


Mochi = AutoDiscord(discordToken)


def checkformochi(arr):
    for messages in arr:
        if messages.split(":")[0] == "mochi":
            return True
    return False


if __name__ == '__main__':
    mostrecent = ""
    while True:
        arr = Mochi.get_messages(channelid, "20")
        if len(arr) == 0:
            Mochi.send_message(channelid, "Hey, I'm Mochi!")
            arr = Mochi.get_messages(channelid, "5")
        if arr[0] != mostrecent:
            if checkformochi(arr) == False:
                Mochi.send_message(channelid, "Hey, I'm Mochi!")
                arr = Mochi.get_messages(channelid, "20")


            mostrecent = arr[0]
            arr = reversed(arr)

            compiledmessages = "The following is a conversation with a person named Mochi. Mochi is a very smart and extremely talkative person.:\n\n" + "\n".join(arr) + "\n"

            response = openai.Completion.create(
                engine="davinci",
                prompt=compiledmessages,
                temperature=0.9,
                max_tokens=200,
                top_p=1,
                frequency_penalty=0.6,
                presence_penalty=0.6,
                stop=["\n"]
            )

            aimessage = response["choices"][0]["text"]

            print(f"Message for {aimessage.split(':')[0]}")

            if aimessage.split(':')[0] == "mochi":
                Mochi.send_message(channelid, aimessage.split(':')[1])
        time.sleep(3)