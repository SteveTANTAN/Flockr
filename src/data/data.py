'''
A collection of data structures used between programs

accessed from root/src
'''

import json

def users_notes():
    '''
    initialise users as a global variable

    The User Data Structure
    Stored Like This:
    users = [
        user: {
            'u_id':
            'email': ''
            'name_first':'',
            'name_last':'',
            'handle_str': '',
            'password': ''
        }
    ]
    '''

def return_users():
    ''' return all the users in the file '''

    # declare users outside
    users = None

    # open the json file
    with open('users.json', 'r') as file:
        users = json.load(file)

    # return the json information
    return users

def append_users(user):
    ''' append user to list '''

    # declare users outside
    users = None

    # open current json file
    with open('users.json', 'r') as file:
        users = json.load(file)

    # append the user
    users.append(user)

    # write json to file
    with open('users.json', 'w') as file:
        json.dump(users, file)

def clear_users():
    ''' clear out users file '''

    # write json to file
    with open('users.json', 'w') as file:
        json.dump([], file)


##########################################################################################

channels = []

def init_channels():
    ''' initialise the channels list

    the struct using for channel
    channels = [
        channel:  {
            'name': 'Hayden',
            'channel_id':
            'owner': [
                {
                    'u_id': 1,
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                }
            ],
            'all_members': [
                {
                    'u_id': 1,
                    'name_first': 'Hayden',
                    'name_last': 'Jacobs',
                }
            ],
            'is_public': True,
            'messages':[]
        }
    ]

    '''
    global channels

def append_channels(channel):
    ''' add a channel in the channels list '''
    channels.append(channel)
