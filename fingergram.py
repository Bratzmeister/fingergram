#!/bin/python3

import time, sys, os

from colorama import init, Fore, Style
from pyrogram import Client
from pyrogram.errors import BadRequest, FloodWait, UnknownError
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv(override=True)
print(os.environ.get("APP_ID"))

n = input(Fore.GREEN + "Enter app_name, empty for default(Fingergram): " + Style.RESET_ALL)
aId=os.environ.get("APP_ID") if os.environ.get("APP_ID") != None else input("no APP_ID set (in .env or shell)! \n" + Fore.RED + "Enter your app_id: " + Style.RESET_ALL)
aH=os.environ.get("APP_HASH") if os.environ.get("APP_HASH") != None else input("no APP_HASH set (in .env or shell)! \n" + Fore.RED + "Enter your api_hash: " + Style.RESET_ALL)

app = Client( 
    name="Fingergram" if n=="" else n,
    api_id=aId,
    api_hash=aH
)


init(autoreset=True)
print(Fore.GREEN + """

@@@@@@@@  @@@  @@@  @@@   @@@@@@@@  @@@@@@@@  @@@@@@@    @@@@@@@@  @@@@@@@    @@@@@@   @@@@@@@@@@
@@@@@@@@  @@@  @@@@ @@@  @@@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@@@@
@@!       @@!  @@!@!@@@  !@@        @@!       @@!  @@@  !@@        @@!  @@@  @@!  @@@  @@! @@! @@!
!@!       !@!  !@!!@!@!  !@!        !@!       !@!  @!@  !@!        !@!  @!@  !@!  @!@  !@! !@! !@!
@!!!:!    !!@  @!@ !!@!  !@! @!@!@  @!!!:!    @!@!!@!   !@! @!@!@  @!@!!@!   @!@!@!@!  @!! !!@ @!@
!!!!!:    !!!  !@!  !!!  !!! !!@!!  !!!!!:    !!@!@!    !!! !!@!!  !!@!@!    !!!@!!!!  !@!   ! !@!
!!:       !!:  !!:  !!!  :!!   !!:  !!:       !!: :!!   :!!   !!:  !!: :!!   !!:  !!!  !!:     !!:
:!:       :!:  :!:  !:!  :!:   !::  :!:       :!:  !:!  :!:   !::  :!:  !:!  :!:  !:!  :!:     :!:
 ::        ::   ::   ::   ::: ::::   :: ::::  ::   :::   ::: ::::  ::   :::  ::   :::  :::     ::
 :        :    ::    :    :: :: :   : :: ::    :   : :   :: :: :    :   : :   :   : :   :      :

--- v0.6.9 by @DubsCheckum ---
""")

def userID(userInput):
    if userInput.startswith("pn-") or userInput.startswith("u-"):
        return userInput.split('-')[1]
    elif userInput.startswith("id-"):
        return int(userInput.split('-')[1])
    else:
        print(Fore.RED + "[x] please specify a correct prefix (id-/u-/pn-). Exiting!" + Style.RESET_ALL)
        exit()


def chatListPrint(data):
    _id = data.id
    _type = data.type
    _title = data.title
    _dc = data.dc_id
    _username = data.username
    print("[id] {} | Title: {} | Username: {} | Type: {} | DC: {}".format(_id, _title, _username, _type, _dc))

def singleUserLookup(user):
    _id = user.id
    _contact = user.is_contact
    _first_name = user.first_name
    _last_name = user.last_name
    _fullName = _first_name + " " + _last_name if _last_name else _first_name
    _username = user.username
    _phone = user.phone_number
    _dc = user.dc_id
    _lod = user.last_online_date
    if _lod:
        _lod = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(_lod))
    print("------\n|-> ID: {}\n|-> isContact: {}\n|-> Full name: {}\n|-> Username: {}\n|-> Phone: +{}".format(_id, _contact, _fullName, _username, _phone))
    print("|-> DC: {}\n|-> Last Online Date: {}".format(_dc, _lod))



def chatMembersInfoPrint(data, total=True):
    if total:
        totalCount = len(data)
        print("[+++] Users count: {}".format(totalCount))
        userList = data
    else:
        userList = data
    print(Fore.GREEN + "[user infos]" + Style.RESET_ALL)
    for user in userList:
        singleUserLookup(user)
        _status = user['status']
        _date = None
        try:
            _date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(user['joined_date']))
        except AttributeError:
            pass
        if user['invited_by']:
            _invitedByID = user['invited_by']['id']
            _invitedByUsername = user['invited_by']['username']
            _invitedByFirstName = user['invited_by']['first_name']
            _invitedBySurname = user['invited_by']['last_name']
            _invitedByFullName = _invitedByFirstName + " " + _invitedBySurname if _invitedBySurname else _invitedByFirstName
        else:
            _invitedByID = 0
            _invitedByFullName = ""
            _invitedByUsername = ""
        print("|-> Status: {}\n|-> Join date: {}".format(_status, _date))
        print("|-> Invited by id: {} | username: {} | Full name: {}".format(_invitedByID, _invitedByUsername, _invitedByFullName))


with app:
    while True:
        choice = input(Fore.RED + "[1] => chats lookup\n[2] => users lookup\n" + 
                                   "[3] => search user in groups\n" +
                                   "[anything else] => exit\n" +
                                   "[<] " + Style.RESET_ALL)
        if choice == "1":
            dialogs = app.get_dialogs()
            i = 0
            for d in dialogs:
                chatListPrint(d.chat)
                i += 1
                if i >= 10:
                    cmd = input(Fore.RED + "[(c)/x]: " + Style.RESET_ALL)
                    i = 0
                    if cmd == 'x':
                        break
            chatID = input(Fore.RED + "[chat lookup]: " + Style.RESET_ALL)
            choice = input(Fore.RED + "[1] => Bulk search\n[2] => single user lookup\n[<]: " + Style.RESET_ALL)
            if choice == "1":
                limit = input(Fore.RED + "[# of users]: " + Style.RESET_ALL)
                members = app.get_chat_members(chat_id=int(chatID), limit=int(limit))
                chatMembersInfoPrint(members)
            elif choice == "2":
                userInput = input(Fore.RED + "[user-id (id)/username (u)/phone number (pn)]: " + Style.RESET_ALL)
                members = app.get_chat_member(chat_id=int(chatID), user_id=userID(userInput))
                chatMembersInfoPrint(members, total=False)
        elif choice == "2":
            userInput = input(Fore.RED + "[user-id: " + Style.RESET_ALL)
            lookupResult = app.get_users(userInput)
            singleUserLookup(lookupResult)
        elif choice == "3":
            dialogs = app.get_dialogs()
            userInput = input(Fore.RED + "[user-id (id)/username (u)/phone number (pn)]: " + Style.RESET_ALL)
            for d in dialogs:
                if int(d.chat.id) < 0:
                    try:
                        members = app.get_chat_member(chat_id=d.chat.id, user_id=userID(userInput))
                        if members:
                            chatListPrint(d['chat'])
                    except BadRequest as e:
                        if not ("CHAT_ADMIN_REQUIRED" or "USER_NOT_PARTICIPANT" in str(e)):
                            print(str(e))
        else:
            print(Fore.RED + "\n[x] exiting!" +Style.RESET_ALL)
            app.stop()
            exit()
