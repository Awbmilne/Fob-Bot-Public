import os
import re
import json
import requests
from datetime import datetime

import gspread
import slack
from oauth2client.service_account import ServiceAccountCredentials

#Admin Update Settings
admin_updates = True
admin_name = 'Will'
admin_channel = 'REDACTED'

#Set all Global Variables
id_index = 0
fob_count_index = 1
message_list = []
list_of_values = []

#Set Google Sheet for Fob Data
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(credentials)
sheet = client.open_by_url(
    "REDACTED").sheet1

#Setuop Slack Client and Authorization
os.environ['SLACK_BOT_TOKEN'] = 'REDACTED'
slack_token = os.environ['SLACK_BOT_TOKEN']
rtm_client = slack.RTMClient(token=slack_token)


# #############################################################################
# #########################__FUNCTION_DEFINITIONS__############################

def take_and_give(take_user_id, give_user_id):

    global message_list
    removed = False
    added = False

    for i in range(list_of_values.__len__()):
        if i != 0:
            print(i)
            sublist = list_of_values[i]
            if sublist[id_index] == take_user_id and int(sublist[fob_count_index]) > 0:
                sublist[fob_count_index] = int(sublist[fob_count_index]) - 1
                sheet.update_cell(i + 1, 2, sublist[fob_count_index])
                if sublist[fob_count_index] == 0:
                    message_list.append(f"<@{take_user_id.upper()}> now has no Fobs!")
                elif sublist[fob_count_index] == 1:
                    message_list.append(f"<@{take_user_id.upper()}> now has 1 Fob!"
                                        + ':key:' * int(sublist[fob_count_index]))
                else:
                    message_list.append(f"<@{take_user_id.upper()}> now has {sublist[fob_count_index]} Fobs!"
                                        + ':key:' * int(sublist[fob_count_index]))
                removed = True
                break

            elif sublist[id_index] == take_user_id and int(sublist[fob_count_index]) == 0:
                message_list.append(f":exclamation: \n<@{take_user_id.upper()}> does not have a Fob, one \
cannot be Taken!")
                copy_to_file()
                return

    if not removed:
        sheet.append_row([take_user_id, 0])  # COMMENT BACK IN LATER
        list_of_values.append([take_user_id, 0])
        message_list.append(f":exclamation: \n<@{take_user_id.upper()}> does not have a Fob, one cannot be Taken!")
        copy_to_file()

    else:
        for i in range(list_of_values.__len__()):
            if i != 0:
                sublist = list_of_values[i]
                if sublist[id_index] == give_user_id:
                    sublist[fob_count_index] = int(sublist[fob_count_index]) + 1
                    list_of_values[i] = sublist.copy()
                    sheet.update_cell(i + 1, 2, sublist[fob_count_index])
                    if sublist[fob_count_index] == 1:
                        message_list.append(f"<@{give_user_id.upper()}> now has 1 Fob!"
                                            + ':key:' * int(sublist[fob_count_index]))
                    else:
                        message_list.append(f"<@{give_user_id.upper()}> now has {sublist[fob_count_index]} Fobs!"
                                            + ':key:' * int(sublist[fob_count_index]))
                    copy_to_file()
                    return
                
        if not added:
            sheet.append_row([give_user_id, 1])  # COMMENT BACK IN LATER
            list_of_values.append([give_user_id, 1])
            message_list.append(f"<@{give_user_id.upper()}> now has 1 Fob! :key:!")
            copy_to_file()
            

# ------------------------------------------------------------------------------


def add_fob(user_id):

    global message_list

    added = False
    for i in range(list_of_values.__len__()):
        if i != 0:
            sublist = list_of_values[i]
            if sublist[id_index] == user_id:
                sublist[fob_count_index] = int(sublist[fob_count_index]) + 1
                list_of_values[i] = sublist.copy()
                sheet.update_cell(i + 1, 2, sublist[fob_count_index])
                if sublist[fob_count_index] == 1:
                    message_list.append(f"<@{user_id.upper()}> now has 1 Fob!"
                                        + ':key:' * int(sublist[fob_count_index]))
                else:
                    message_list.append(f"<@{user_id.upper()}> now has {sublist[fob_count_index]} Fobs!"
                                        + ':key:' * int(sublist[fob_count_index]))
                copy_to_file()
                return
            
    if not added:
        sheet.append_row([user_id, 1])
        list_of_values.append([user_id, 1])
        message_list.append(f"<@{user_id.upper()}> now has 1 Fob! :key:")
        copy_to_file()


# ------------------------------------------------------------------------------


def remove_fob(user_id):

    global message_list
    
    removed = False
    for i in range(list_of_values.__len__()):
        if i != 0:
            sublist = list_of_values[i]
            # print(sublist)
            if sublist[id_index] == user_id and int(sublist[fob_count_index]) > 0:
                sublist[fob_count_index] = int(sublist[fob_count_index]) - 1
                sheet.update_cell(i + 1, 2, sublist[fob_count_index])
                if sublist[fob_count_index] == 0:
                    message_list.append(f"<@{user_id.upper()}> now has no Fobs!")
                elif sublist[fob_count_index] == 1:
                    message_list.append(f"<@{user_id.upper()}> now has 1 Fob!"
                                        + ':key:' * int(sublist[fob_count_index]))
                else:
                    message_list.append(f"<@{user_id.upper()}> now has {sublist[fob_count_index]} Fobs!"
                                        + ':key:' * int(sublist[fob_count_index]))
                copy_to_file()
                return

            elif sublist[id_index] == user_id and int(sublist[fob_count_index]) == 0:
                message_list.append(f"<@{user_id.upper()}> does not have a Fob, one cannot be Removed!")
                copy_to_file()
                return
            
    if not removed:
        sheet.append_row([user_id, 0])
        list_of_values.append([user_id, 0])
        message_list.append(f"<@{user_id.upper()}> does not have a Fob, one cannot be Removed!")
        copy_to_file()


# -----------------------------------------------------------------------------


def check_fobs():
    
    global message_list
    
    for i in range(list_of_values.__len__()):
        if i != 0:
            sublist = list_of_values[i]
            if int(sublist[fob_count_index]) == 1:
                message_list.append(f"<@{sublist[id_index].upper()}> has 1 Fob "
                                    + ':key:' * int(sublist[fob_count_index]))
            elif int(sublist[fob_count_index]) > 1:
                message_list.append(f"<@{sublist[id_index].upper()}> has {sublist[fob_count_index]} Fobs "
                                    + ':key:' * int(sublist[fob_count_index]))
    message_list.append("\nNobody else currently has a Fob.")

    copy_to_file()


# -----------------------------------------------------------------------------


def copy_to_file():
    
    global list_of_values
    fob_list_file = open("Fob List.txt", 'w')       # Open File

    for i in [0, len(list_of_values)-1]:            # Write Values to File in CSV Format
        for j in [0, len(list_of_values[i])-1]:
            fob_list_file.write(str(list_of_values[i][j]))
            if not j == len(list_of_values[i]) - 1:
                fob_list_file.write(',')
        fob_list_file.write('\n')
        
    fob_list_file.close()                           # Close File


# -----------------------------------------------------------------------------


def update_email_list():

    user_list = requests.get("https://slack.com/api/users.list?token=%s" % slack_token).json()['members']
    users_num = len(user_list)

    now = datetime.now()

    email_file = client.open_by_url(
        "REDACTED")
    email_sheet = email_file.add_worksheet(title=now.strftime("%B %d, %Y @ %H:%M:%S"), rows=str(users_num+5), cols="20")

    email_sheet.update_cell(1, 1, 'Names')
    email_sheet.update_cell(1, 2, 'Emails')

    cell_list = email_sheet.range('A1:B1000')

    print(cell_list)

    corrector_val = 0

    for i in range(1, users_num):
        if user_list[i]['deleted'] is False and 'email' in user_list[i]['profile']:
            cell_list[2 * (i - corrector_val)].value = user_list[i]['real_name']
            cell_list[2 * (i - corrector_val) + 1].value = user_list[i]['profile']['email']
        else:
            corrector_val += 1

    email_sheet.update_cells(cell_list)


# #############################################################################
# #########################__MAIN_PROGRAM_START__##############################


# Triggered Function
@slack.RTMClient.run_on(event='message')            # Event Based Trigger
def mother_ship(**payload):
    
    global list_of_values
    global message_list

    message_list = []
    send_message = ""

    check = 0
    transfer = 0
    add = 0
    remove = 0
    _help = 0
    copy_for_oversight = False

    message_text = ""
    sender_id = ""
    message_give_id = ""
    message_take_id = ""

    # -----------------------------------------------------
    # Get Message Data

    message = payload['data']
    if "Fob-Bot" in message['text']:
        return

    if 'text' in message:
        print(f"Message received:\n{json.dumps(message, indent=2)}")
        message_text = message['text'].lower()
        sender_id = message['user'].lower()
        message_text = message_text.replace(' me', f'<@{sender_id.lower()}>')

    # -----------------------------------------------------
    # Get Google Sheet Data

    list_of_values = sheet.get_all_values()
    print("Database Run")

    # -----------------------------------------------------
    # Parse Message actions and ID's

    if re.match(r'.*(update).*', message_text, re.IGNORECASE) and re.match(r'.*(email).*', message_text, re.IGNORECASE):
        update_email_list()
        web_client = payload['web_client']
        web_client.chat_postMessage(channel=message['channel'], text="*Fob-Bot* :robot_face:\n\nEmail List Updated in \
Google Sheet:\n REDACTED")
        return
    if re.match(r'.*(help|hi|hello).*', message_text, re.IGNORECASE):
        _help = 1
    if re.match(r'.*(check|who).*', message_text, re.IGNORECASE):
        check = 1
    if re.match(r'.*(add).*', message_text, re.IGNORECASE):
        add = 1
        message_give_id = message_text[message_text.find('@') + 1:message_text.find('>')]
        # print(message_give_id)
    if re.match(r'.*(remove).*', message_text, re.IGNORECASE):
        remove = 1
        message_take_id = message_text[message_text.find('@') + 1:message_text.find('>')]
    if re.match(r'.*(transfer|give|hand).*', message_text, re.IGNORECASE):
        transfer = 1
        if 'from' in message_text:
            from_text = message_text[message_text.find('from') + 5:]
            message_take_id = from_text[from_text.find('@') + 1:from_text.find('>')]
        else:
            message_take_id = sender_id.lower()
        if 'to' in message_text:
            to_text = message_text[message_text.find('to') + 3:]
            message_give_id = to_text[to_text.find('@') + 1:to_text.find('>')]
        else:
            message_give_id = sender_id.lower()

    # -----------------------------------------------------
    #Check if User references are Proper

    if ((" " in message_give_id or not message_give_id.lower().startswith('u')) and (not message_give_id == "")) or \
            ((" " in message_take_id or not message_take_id.lower().startswith('u')) and (not message_take_id == "")):
        check = 0
        transfer = 0
        add = 0
        remove = 0
        _help = 0

    # -----------------------------------------------------
    # Run Functions

    if check + transfer + add + remove > 1:
        message_list.append("Sorry, I can only understand 1 command at a time. \nPlease send each command individually \
and wait for my reply. \n Thanks!")

    elif check == 1:
        check_fobs()

    elif transfer == 1:
        take_and_give(message_take_id, message_give_id)
        copy_for_oversight = True

    elif add == 1:
        add_fob(message_give_id)
        copy_for_oversight = True

    elif remove == 1:
        remove_fob(message_take_id)
        copy_for_oversight = True

    elif _help == 1:
        message_list.append(
            'Hello! Im Fob-Bot! \nIm here to help the WatLock team keep track of those pesky security fobs. \n\nIf you \
want to *CHECK* who has fobs, just DM me "Who has fobs" or "Check fobs" \n\n If you want to *TRANSFER* a \
fob between people, just DM me "Transfer fob from @Giver to @Receiver" or "Transfer from me to @Receiver". \
\n(Please @ people or use "Me" for proper user recognition). \n\nPlease do tell me when a Fob changes \
hands so I can inform everyone else on the team. \nThanks! :smile:')

    else:
        message_list.append(
            ':question:\nSorry, I don\'t understand. Please use Keywords *"Check"* and *"Transfer"* in your command \
messages.\n *Reference* people using @user. \n\nOr, send "Help" for more information about me and my \
commands.\n')
         
    for i in range(message_list.__len__()):
        if i != 0:
            send_message = send_message + '\n' + message_list[i]
        else:
            send_message = message_list[i]
    send_message = "*Fob-Bot* :robot_face:\n\n" + send_message
    web_client = payload['web_client']
    web_client.chat_postMessage(channel=message['channel'], text=send_message)
    print("Return Message:\n" + send_message)
    copy_to_file()

    # -----------------------------------------------------
    # Send Notification to Admin that the list has been updated
    send_message = ""
    if admin_updates and copy_for_oversight and sender_id != 'ufzh0al3g':
        for i in range(message_list.__len__()):
            if i != 0:
                send_message = send_message + '\n' + message_list[i]
            else:
                send_message = message_list[i]
        send_message = f"*Fob-Bot* :robot_face: \n\n{admin_name}, Someone has updated the Fob List. Here is the update!\
\n\n" + send_message
        web_client = payload['web_client']
        web_client.chat_postMessage(channel=admin_channel, text=send_message)
        copy_to_file()

# #########################__MAIN_PROGRAM_END__################################
# #############################################################################


# Start Client Reading Messages
rtm_client.start()