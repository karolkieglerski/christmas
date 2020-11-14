import sys
import ast
import getpass
import logging
import fbchat
from fbchat.models import *
import random
import time

### see https://github.com/fbchat-dev/fbchat/issues/615#issuecomment-710127001 
import re
fbchat._util.USER_AGENTS    = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"]
fbchat._state.FB_DTSG_REGEX = re.compile(r'"name":"fb_dtsg","value":"(.*?)"')

if len(sys.argv) < 4:
    print("Email and password needed!")
    sys.exit(1)

user        = sys.argv[1] 
password    = sys.argv[2]
my_id       = sys.argv[3]
file_path   = sys.argv[4]
big_value   = '50'
small_value = '10'

def open_file(path):
    file = open(path, "r")
    contents = file.read()
    dictionary = ast.literal_eval(contents)
    file.close()

    return dictionary

def shuffle(users):
    users_from = [*users]
    final = {}

    for user in [*users]:
        selected = random.choice(users_from)
        
        while user == selected:
            selected = random.choice(users_from)
        users_from.remove(selected)
        
        final[user] = selected

    return final

def messages(users_shuffle, number):
    messages_list = {}

    for user, user_found in users_shuffle.items():
        messages_list[user] = f"{user} wylosowałaś/eś na prezent za {number}: {user_found}"

    return messages_list

def send_message(client, users_map, money, my_id):
    shaffle_users = shuffle(users_map)
    messages_list = messages(shaffle_users, money)

    for user, message in messages_list.items():
        fbuser = client.searchForUsers(users_map[user])[0]
        client.send(Message(text=message), thread_id=fbuser.uid, thread_type=ThreadType.USER)
        time.sleep(3)

        if my_id != fbuser.uid:
            client.deleteThreads(thread_ids=fbuser.uid)
            time.sleep(1)  

def main(user, password, my_id, file_path):
    users_map = open_file(file_path)

    uag = fbchat._util.USER_AGENTS[0] # choose deterministic to prevent alerts from FB
    client = fbchat.Client(email=user, password=password, user_agent=uag)

    send_message(client, users_map, big_value, my_id)
    send_message(client, users_map, small_value, my_id)

main(user, password, my_id, file_path, small_value, big_value)
