# Fingergram 

## What is this for?
Search users in groups (and in which groups is the user) by id, username or phone number (if it's in your contacts).

## What do I need?
To use this tool you need to setup an API login for your Telegram Account over here: [Telegram API](https://my.telegram.org/) the fields you put there don't matter but make sure to copy app_id and app_hash. Best way to do this is to either create a file in this directory called .env, load them into your environment before starting fingergram or you enter it manually every time like a simpleton when asked to.

```
.
├── .env
└── foo.py
```

```bash
APP_ID=<your few digit app_id>
APP_HASH=<your long ass string hash>
```

## Usage

clone this repo
`git clone https://github.com/Bratzmeister/fingergram.git && cd fingergram`

create venv
`python -m venv .`

activate venv
`source bin/activate`

install dependencies
`pip install -r requirements.txt`

...
`python fingergram.py`

profit

## Limitations
To know if a user is in a group, you have to be in that group too. You can't know which users are in a specific channel if you are not an administrator.

## Credits
© @DubsCheckum on the 'gram
