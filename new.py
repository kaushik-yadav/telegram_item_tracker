import re
import requests
import json
from datetime import datetime,timedelta
from telethon.sync import TelegramClient

API_ID = "api_id"
API_HASH = "your ap_hash"
CHANNEL_USERNAME = "channel_link"
CHANNEL_TO_SEND = "channel_id"
TOKEN='channel_token'
CHANNEL_TO_SEND_LINK = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
client = TelegramClient('tracky_session', API_ID, API_HASH)

async def main():
    await client.start()
    channel = await client.get_entity(CHANNEL_USERNAME)
    messages = await client.get_messages(channel, limit=30)
    my_dict={"Date":"","Link":""}
    to_find="shirt" #Enter any product
    file_name="tracker.json"
    link_format="https?://[^\n]*"
    time_format="%Y-%m-%d %H:%M:%S"
    working=True
    ## personal chat id:
    # chat_id = "5236419855"
    message=f"No {to_find} found"
    params = {
        'chat_id': CHANNEL_TO_SEND,
        'text': message,
        }
    for i in range(len(messages)):
        if(to_find in messages[i].text.lower()):
            time_line=messages[i].date
            time_line=str(time_line)[:-6]

            with open(file_name,"r") as file:
                file_content=file.read()
                data=json.loads(file_content)

            prev_date=data["Date"]
            time_line_in_format=datetime.strptime(time_line,time_format)
            prev_in_date=datetime.strptime(prev_date,time_format)
            to_add_time=timedelta(hours=5,minutes=30)
            result=time_line_in_format+to_add_time
            if(result>prev_in_date):
                working=False
                link=re.findall(link_format,messages[i].text)[0]
                my_dict["Date"]=str(result)
                my_dict["Link"]=link
                string_dict=json.dumps(my_dict)
                with open(file_name,"w") as file:
                    file.write(string_dict)
                print(f"New {to_find} found")
                print("Message sent to the telegram bot")
                message = f'New {to_find} found\nLink :{my_dict["Link"]}'
                # Parameters for sending message
                params = {
                    'chat_id': CHANNEL_TO_SEND,
                    'text': message,
                    }
                requests.post(CHANNEL_TO_SEND_LINK, params=params)
                # this can send personal messages : 
                #url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
                #requests.get(url).json()


    if(working):
        message=f"No more {to_find} found"
        print(message)
        params["text"]=message
        print("Message sent to the telegram bot")
        requests.post(CHANNEL_TO_SEND_LINK, params=params)
        
        # this can send personal messages : 
        #url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
        #requests.get(url).json()

    await client.disconnect()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
