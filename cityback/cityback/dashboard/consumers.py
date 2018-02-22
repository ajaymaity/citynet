import json
from channels import Group
from cityback.dashboard import helpers

def ws_connect(message):

    Group("Test").add(message.reply_channel)

    message.reply_channel.send({
        'accept': True
    })

def ws_receive(message):
    data = json.loads(message.content.get("text"))
    print("received data:", data.get("data"))
    #helpers.get_data()
    #val = str(helpers.get_data())
    #Group("Test").send({"text": val})
    return None

def ws_disconnect(message):
    Group("Test").discard(message.reply_channel)