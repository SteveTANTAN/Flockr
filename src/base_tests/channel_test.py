# this file is using for pytest of channel.py .
from src.base.channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner
from src.base.channels import channels_create
from src.base.message import message_send
from src.base.auth import auth_login, auth_register, auth_logout
from src.base.error import InputError, AccessError
import src.data.data as data
import pytest
import src.base.other as other
# from base.message import message_send


#########################################################################
#
#                     test for channel_invite function
#
##########################################################################
# Xingyu TAN working on channel_test.py for channel_invite function
# 29 SEP 2020

"""
channel_invite()
the function Invites a user (with user id u_id) to join a channel with ID channel_id.

RETURNS:
none


THEREFORE, TEST EVERYTHING BELOW:
1. inputError
- the channel id we had is invalid

- the user id we had is invalid

- the user token is invalid

2. accessError
- the auth user is not in this channel.

3. repeated invite
- repeated invite one person who is already in.

"""

def test_channel_invite_work():
    '''
    this test is using for check the function can work normally when no Errors bring.
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_id1 = user1['u_id']
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com","check_test","steve","TAN")
    user2 = auth_login("test2@test.com","check_test")
    u_id2 = user2['u_id']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True).get('channel_id')

    # testing for channel invite function
    channel_invite(u_token1,channel_test_id,u_id2)

    # Assuming we the function running correctly, then we do check the channel details
    # expecially, the member infomation
    channel_member_num = 0

    for i in data.return_channels():
        if i['channel_id'] == channel_test_id:
            channel_member_num = len(i['all_members'])
            break

    # check the totoal members number is 2
    assert channel_member_num == 2
    # check the diff people info correct
    assert u_id1 ==  i['all_members'][0]['u_id']
    assert u_id2 ==  i['all_members'][1]['u_id']

###########################################################################################
def test_channel_repeate_invite():
    '''
    This test is using for check when the user has been in the program
    when repeat invite, just skip it.
    '''

    # create 2 users
    other.clear()

    user1 = auth_register("test41@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test41@test.com","check_test")
    u_token1 = user1['token']

    user2 = auth_register("test42@test.com","check_test","steve","TAN")
    user2 = auth_login("test42@test.com","check_test")
    u_id2 = user2['u_id']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True).get('channel_id')

    # invite people first time
    channel_invite(u_token1,channel_test_id,u_id2)

    # testing for invite people second time
    channel_invite(u_token1,channel_test_id, u_id2)

    channel_member_num = 0

    for i in data.return_channels():
        if i['channel_id'] == channel_test_id:
            channel_member_num = len(i['all_members'])
            break

    # check the totoal members number is still 2
    assert channel_member_num ==2


##########  test for input error #####################################
def test_channel_invite_invalid_channelId_input_error():
    '''
    This test is using for check when the channel id we had is invalid
    inputError
    '''
    # create 2 users
    other.clear()

    user1 = auth_register("test5@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test5@test.com","check_test")
    u_token1 = user1['token']

    user2 = auth_register("test6@test.com","check_test","steve","TAN")
    user2 = auth_login("test6@test.com","check_test")
    u_id2 = user2['u_id']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True).get('channel_id')

    # testing for channel invite function for invalid channel id inputError
    with pytest.raises(InputError):
        channel_invite(u_token1,channel_test_id + 0xf, u_id2)
###########################################################################################
def test_channel_invite_invalid_tokenid():
    '''
    This test is using for check when token we had is invalid

    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_id2 = user2['u_id']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')


    # testing for channel message function for invalid channel id inputError
    with pytest.raises(InputError):
        channel_invite(u_token1+ 'abc', channel_test_id, u_id2)

    auth_logout(u_token1)
##########################################################################
def test_channel_invite_invalid_userId_input_error():
    '''
    This test is using for check when the user id we had is invalid
    inputError
    '''
    # create 2 users
    other.clear()

    user1 = auth_register("test3@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test3@test.com","check_test")
    u_token1 = user1['token']

    user2 = auth_register("test4@test.com","check_test","steve","TAN")
    user2 = auth_login("test4@test.com","check_test")
    u_id2 = user2['u_id']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True).get('channel_id')

    # testing for channel invite function for invalid user id inputError
    with pytest.raises(InputError):
        channel_invite(u_token1,channel_test_id, u_id2 + 0xf)

#################### test for access error #############################
def test_channel_non_member_invite():
    '''
    This test is using for check when the authorised user
    is not already a member of the channel
    AccessError
    '''
    # create 2 users and author people
    other.clear()

    user1 = auth_register("test11@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test11@test.com","check_test")
    u_token1 = user1['token']

    user2 = auth_register("test22@test.com","check_test","steve","TAN")
    user2 = auth_login("test22@test.com","check_test")
    u_id2 = user2['u_id']

    user3 = auth_register("test33@test.com","check_test","test","TAN")
    user3 = auth_login("test33@test.com","check_test")
    u_token3 = user3['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True).get('channel_id')

    # testing for channel invite function for invalid token people.
    with pytest.raises(InputError):
        channel_invite(u_token3,channel_test_id, u_id2)

#########################################################################
#
#                     test for channel_detail function
#
##########################################################################

# Xingyu TAN working on channel_details.py for channel_details function
# 29 SEP 2020

"""
channel_details()
Given a Channel with ID channel_id that the authorised user is part of

RETURNS:
provide basic details about the channel


THEREFORE, TEST EVERYTHING BELOW:
1. inputError
- the channel is invalid
- the user_token is invalid


2. accessError
- the auth user is not in this channel.

"""

def test_channel_details_work():
    '''
    this test is using for check the function can work normally when no Errors bring.
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_id1 = user1['u_id']
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com","check_test","steve","TAN")
    user2 = auth_login("test2@test.com","check_test")
    u_id2 = user2['u_id']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True).get('channel_id')

    # testing for channel invite function
    channel_invite(u_token1,channel_test_id,u_id2)
    channel_test_details = channel_details(u_token1,channel_test_id)

    # Assuming we the function running correctly, then we do check the channel details
    # expecially, the member infomation
    # check for channel_id
    assert channel_test_details['name'] == 'channel_test'

    # check for owner
    assert channel_test_details['owner_members'][0]['u_id'] == u_id1

    # check for members
    assert channel_test_details['all_members'][0]['u_id'] == u_id1
    assert channel_test_details['all_members'][1]['u_id'] == u_id2

###########################################################################################
def test_channel_details_invalid_channelId():
    '''
    This test is using for check when the user id we had is invalid
    inputError
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com","check_test","steve","TAN")
    user2 = auth_login("test2@test.com","check_test")
    u_id2 = user2['u_id']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True).get('channel_id')

    channel_invite(u_token1,channel_test_id, u_id2)

    # testing for channel invite function for invalid channel id inputError
    with pytest.raises(InputError):
        channel_details(u_token1,channel_test_id + 0xf)
###########################################################################################
def test_channel_details_invite_invalid_tokenid():
    '''
    This test is using for check when token we had is invalid

    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_id2 = user2['u_id']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')
    channel_invite(u_token1, channel_test_id, u_id2)

    # testing for channel message function for invalid channel id inputError
    with pytest.raises(InputError):
        channel_details(u_token1+ 'abc', channel_test_id)

    auth_logout(u_token1)
###########################################################################################

def test_channel_non_member_call_details():
    '''
    This test is using for check when the authorised user
    is not already a member of the channel
    AccessError
    '''
    # create 2 users and author people
    other.clear()
    user1 = auth_register("test1@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_token1 = user1['token']



    user3 = auth_register("test3@test.com","check_test","test","TAN")
    user3 = auth_login("test3@test.com","check_test")
    u_token3 = user3['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True).get('channel_id')


    # testing for channel invite function for invalid token people.
    with pytest.raises(InputError):
        channel_details(u_token3,channel_test_id)


#########################################################################
#
#                     test for channel_messages function
#
##########################################################################


# Xingyu TAN working on channel_test.py for channel_messages function
# 29 SEP 2020

"""
channel_messages()
Given a Channel with ID channel_id that the authorised user is part of channel,
and return no more than 50 messages

RETURNS:
-1 : for no more message after start
0< number && number <= 50: exist messages after start and no more than 50 messages.
50 : the exist messages after start more than 50, just return the top 50 ones.


THEREFORE, TEST EVERYTHING BELOW:
1. inputError
- the channel id we had is invalid

- start is greater than the total number of messages in the channel

2. accessError
- the auth user is not in this channel.

"""
################################
#
#   help function for sending msg
#
################################
'''
    this function is using for create new message and send into our channel
'''
def msg_send(channel_id, msg_id, u_id, msg, time):
    return_message = {
        'message_id': msg_id,
        'u_id': u_id,
        'message': msg,
        'time_created': time,
    }

    channels = data.return_channels()

    for i in channels:
        if i['channel_id'] == channel_id:
            i['message'].insert(0, return_message)
            break

    data.replace_channels(channels)

###################     INPUT ERROR        ##################
def test_inputError_channel_message_channelId_start_invalid():
    '''
    This test is using for check when channel id we had is invalid
    inputError
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com","check_test","steve","TAN")
    user2 = auth_login("test2@test.com","check_test")
    u_id2 = user2['u_id']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True).get('channel_id')
    channel_invite(u_token1,channel_test_id, u_id2)

    # testing for channel message function for invalid message start
    with pytest.raises(InputError):
        channel_messages(u_token1,channel_test_id, 10)

###########################################################################################
def test_inputError_channel_message_invalid_channelId():
    '''
    This test is using for check when channel id we had is invalid
    inputError
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com","check_test","steve","TAN")
    user2 = auth_login("test2@test.com","check_test")
    u_id2 = user2['u_id']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True).get('channel_id')
    channel_invite(u_token1,channel_test_id, u_id2)

    # testing for channel message function for invalid channel id inputError
    with pytest.raises(InputError):
        channel_messages(u_token1,channel_test_id + 0xf, 0)

###########################################################################################
def test_channel_msg_invite_invalid_tokenid():
    '''
    This test is using for check when token we had is invalid

    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    user2 = auth_register("test2@test.com", "check_test", "steve", "TAN")
    user2 = auth_login("test2@test.com", "check_test")
    u_id2 = user2['u_id']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')
    channel_invite(u_token1, channel_test_id, u_id2)

    # testing for channel message function for invalid channel id inputError
    with pytest.raises(InputError):
        channel_messages(u_token1 + 'abc',channel_test_id, 0)

    auth_logout(u_token1)

###################        Access error      ################################
def test_channel_message_non_member_call_details():
    '''
    This test is using for check when the authorised user
    is not already a member of the channel
    AccessError
    '''
    # create 2 users and author people
    other.clear()
    user1 = auth_register("test1@test.com","check_test","Xingyu","TAN")
    user1 = auth_login("test1@test.com","check_test")
    u_token1 = user1['token']

    user3 = auth_register("test3@test.com","check_test","test","TAN")
    user3 = auth_login("test3@test.com","check_test")
    u_token3 = user3['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1,"channel_test",True).get('channel_id')

    # testing for channel invite function for invalid token people.
    with pytest.raises(InputError):
        channel_messages(u_token3,channel_test_id,0)

######   test  for normally channel_messsge work and correct message_send return #########
# case 1: return -1 : for no more message after start
def test_channel_message_return_negative_one():
    '''
    this test using for check if the channel function can return correctly

    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')

    # 1. return -1 : for no more message after start
    check_return_negative_one = channel_messages(u_token1, channel_test_id, 0)
    assert check_return_negative_one['end'] == -1

    auth_logout(u_token1)
###########################################################################################

# case 2: return 50; check the end return alway (start + 50) when message less than 50
def test_channel_message_return_negetive_one_end():
    '''
    this test using for check if the channel function can return correctly

    3. 0< number && number <= 50: exist messages after start and no more than 50 messages.
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']


    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')

    # check the function can return the message correctly.
    message_send(u_token1, channel_test_id, "msg test 01")

    check_work_msg = channel_messages(u_token1, channel_test_id, 0)
    #0< number && number <= 50: exist messages after start and no more than 50 messages.
    assert check_work_msg['end'] == -1

    auth_logout(u_token1)
###########################################################################################

# case 3: return 50; test for the newest one when total msg more than 50
def test_channel_message_newest_one_index():
    '''
    this test using for check if the channel function can return correctly

    return 50 : the exist messages after start more than 50, just return the top 50 ones.
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']

    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')


    # the exist messages after start more than 50, just return the top 50 ones.
    for _ in range(1, 60):
        message_send(u_token1, channel_test_id, 'list more than 50 msgs')

    # update the last one
    assert isinstance(message_send(u_token1, channel_test_id, 'the next one'), dict)

    # check the uodatest msg in [0] is the last update one.
    check_work_msg = channel_messages(u_token1, channel_test_id, 0)
    assert check_work_msg['messages'][0]['message'] == 'the next one'

    auth_logout(u_token1)
###########################################################################################
# case 4: test if we can show the correct message_send information
def test_channel_message_correct_message_infors():
    '''
    this test using for check if the channel function can return correctly
    2. check the function can return the message correctly.
    2.1 the [0] always the top fresh one
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']


    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')

    #create test message we needed
    message_send(u_token1, channel_test_id, "msg test 01")
    message_send(u_token1, channel_test_id, "msg test 02")
    message_send(u_token1, channel_test_id, "msg test 03")

    # 2. check the function can return the message correctly.
    check_work_msg = channel_messages(u_token1, channel_test_id, 0)
    assert check_work_msg['messages'][0]['message'] == 'msg test 03'
    assert check_work_msg['messages'][1]['message'] == 'msg test 02'
    assert check_work_msg['messages'][2]['message'] == 'msg test 01'

    auth_logout(u_token1)
###########################################################################################
# case 5: test if we can show the correct messsage_send return
def test_channel_message_correct_send_return_id():
    '''
    this test using for check if the channel function can return correctly
    2. check the function can return the message correctly.
    2.1 the [0] always the top fresh one
    '''
    # create 2 users
    other.clear()
    user1 = auth_register("test1@test.com", "check_test", "Xingyu", "TAN")
    user1 = auth_login("test1@test.com", "check_test")
    u_token1 = user1['token']


    # create channel for testing
    channel_test_id = channels_create(u_token1, "channel_test", True).get('channel_id')

    #create test message we needed and check return
    assert message_send(u_token1, channel_test_id, "msg test 01")['message_id'] == 1
    assert message_send(u_token1, channel_test_id, "msg test 02")['message_id'] == 2
    assert message_send(u_token1, channel_test_id, "msg test 03")['message_id'] == 3
    auth_logout(u_token1)
################################################################################
# Tests for channel_join()
################################################################################

def test_channel_join_normal():
    """
    InputError: when any of Channel ID is not a valid channel.
    AccessError: when channel_id refers to a channel that is private (when the authorised user is not a global owner).
    """
    other.clear()

    # Create the owner account to access channel.
    auth_register('owner@test.com', 'Iampassword', 'Hao', 'Ren')
    login_owner = auth_login('owner@test.com', 'Iampassword')
    assert type(login_owner) is dict
    u_id_owner = login_owner['u_id']
    assert u_id_owner
    token_owner = login_owner['token']
    assert token_owner
    assert type(u_id_owner) is int
    assert type(token_owner) is str

    # Create the user to join and leave the channel.
    auth_register('user@test.com', 'Iampassword', 'Zhiyuan', 'Liu')
    login_user = auth_login('user@test.com', 'Iampassword')
    assert type(login_user) is dict
    u_id_user = login_user['u_id']
    assert u_id_user
    token_user = login_user['token']
    assert token_user
    assert type(u_id_user) is int
    assert type(token_user) is str

    # Owner creates a test channel.
    chan_id = channels_create(token_owner, "Test_Channel", True).get('channel_id')
    assert chan_id
    assert type(chan_id) is int

    # Normal case:
    # If the function executed correctly, it would return a 'None'
    assert channel_join(token_user, chan_id) == {}
def test_channel_join_invalid_token():
    """
    InputError: when any of Channel ID is not a valid channel.
    AccessError: when channel_id refers to a channel that is private (when the authorised user is not a global owner).
    """
    other.clear()

    # Create the owner account to access channel.
    auth_register('owner@test.com', 'Iampassword', 'Hao', 'Ren')
    login_owner = auth_login('owner@test.com', 'Iampassword')
    assert type(login_owner) is dict
    u_id_owner = login_owner['u_id']
    assert u_id_owner
    token_owner = login_owner['token']
    assert token_owner
    assert type(u_id_owner) is int
    assert type(token_owner) is str

    # Create the user to join and leave the channel.
    auth_register('user@test.com', 'Iampassword', 'Zhiyuan', 'Liu')
    login_user = auth_login('user@test.com', 'Iampassword')
    assert type(login_user) is dict
    u_id_user = login_user['u_id']
    assert u_id_user
    token_user = login_user['token']
    assert token_user
    assert type(u_id_user) is int
    assert type(token_user) is str

    # Owner creates a test channel.
    chan_id = channels_create(token_owner, "Test_Channel", True).get('channel_id')
    assert chan_id
    assert type(chan_id) is int

    with pytest.raises(InputError):
        channel_join(token_user + 'abc', chan_id)

def test_channel_join_invalid_channel_id():

    other.clear()

    # Create the owner account to access channel.
    auth_register('owner@test.com', 'Iampassword', 'Hao', 'Ren')
    login_owner = auth_login('owner@test.com', 'Iampassword')
    assert type(login_owner) is dict
    u_id_owner = login_owner['u_id']
    assert u_id_owner
    token_owner = login_owner['token']
    assert token_owner
    assert type(u_id_owner) is int
    assert type(token_owner) is str

    # Create the user to join and leave the channel.
    auth_register('user@test.com', 'Iampassword', 'Zhiyuan', 'Liu')
    login_user = auth_login('user@test.com', 'Iampassword')
    assert type(login_user) is dict
    u_id_user = login_user['u_id']
    assert u_id_user
    token_user = login_user['token']
    assert token_user
    assert type(u_id_user) is int
    assert type(token_user) is str

    # Owner creates a test channel.
    chan_id = channels_create(token_owner, "Test_Channel", True).get('channel_id')
    assert chan_id
    assert type(chan_id) is int

    # For any input error:
    wrong_id = 3141592653
    with pytest.raises(InputError):
        channel_join(token_user, wrong_id)

def test_channel_join_for_private():

    other.clear()

    # Create the owner account to access channel.
    auth_register('owner@test.com', 'Iampassword', 'Hao', 'Ren')
    login_owner = auth_login('owner@test.com', 'Iampassword')
    assert type(login_owner) is dict
    u_id_owner = login_owner['u_id']
    assert u_id_owner
    token_owner = login_owner['token']
    assert token_owner
    assert type(u_id_owner) is int
    assert type(token_owner) is str

    # Create the user to join and leave the channel.
    auth_register('user@test.com', 'Iampassword', 'Zhiyuan', 'Liu')
    login_user = auth_login('user@test.com', 'Iampassword')
    assert type(login_user) is dict
    u_id_user = login_user['u_id']
    assert u_id_user
    token_user = login_user['token']
    assert token_user
    assert type(u_id_user) is int
    assert type(token_user) is str

    # Owner creates a test channel.
    # However, this case we need a PRIVATE channel.
    chan_id = channels_create(token_owner, "Test_Channel", False).get('channel_id')
    assert chan_id
    assert type(chan_id) is int

    with pytest.raises(InputError):
        channel_join(token_user, chan_id)

################################################################################
# Tests for channel_leave()
# Now, we did 3 passed test for channel_join(), so we use it to initialize our struct.
################################################################################

def test_channel_leave_normal():
    """
    InputError: when any of:Channel ID is not a valid channel
    AccessError: when Authorised user is not a member of channel with channel_id

    After above tests, we could trust our initialize conditions are correct, so
    we just try to make them clearly with simple test for users.
    """
    other.clear()

    # Create the owner account to access channel.
    auth_register('owner@test.com', 'Iampassword', 'Hao', 'Ren')
    login_owner = auth_login('owner@test.com', 'Iampassword')
    token_owner = login_owner['token']

    # Create the user1.
    auth_register('user1@test.com', 'Iampassword', 'Zhiyuan', 'Liu')
    login_user1 = auth_login('user1@test.com', 'Iampassword')
    token_user1 = login_user1['token']


    # Create the user2.
    auth_register('user2@test.com', 'Iampassword', 'Jiaqi', 'Lu')
    login_user2 = auth_login('user2@test.com', 'Iampassword')
    token_user2 = login_user2['token']


    # Create the user3.
    auth_register('user3@test.com', 'Iampassword', 'Tingyu', 'Jiang')
    login_user3 = auth_login('user3@test.com', 'Iampassword')
    token_user3 = login_user3['token']


    # Owner creates a test channel.
    chan_id = channels_create(token_owner, "Test_Channel", True).get('channel_id')
    assert chan_id
    assert type(chan_id) is int

    channel_join(token_user1, chan_id)
    channel_join(token_user2, chan_id)
    channel_join(token_user3, chan_id)

    # Normal case:
    channel_leave(token_user1, chan_id)
    channel_leave(token_user2, chan_id)


    # We removed user2 and user3, so the owner and user should be remaining here.
    # The total number of members in the channel should be 2.

    channel_test_details = channel_details(token_owner,chan_id)
    assert len(channel_test_details['all_members']) == 2

def test_channel_leave_normal_two_oweners():
    """
    InputError: when any of:Channel ID is not a valid channel
    AccessError: when Authorised user is not a member of channel with channel_id

    After above tests, we could trust our initialize conditions are correct, so
    we just try to make them clearly with simple test for users.
    """
    other.clear()

    # Create the owner account to access channel.
    auth_register('owner@test.com', 'Iampassword', 'Hao', 'Ren')
    login_owner = auth_login('owner@test.com', 'Iampassword')
    token_owner = login_owner['token']

    # Create the user1.
    auth_register('user1@test.com', 'Iampassword', 'Zhiyuan', 'Liu')
    login_user1 = auth_login('user1@test.com', 'Iampassword')
    token_user1 = login_user1['token']


    # Create the user2.
    auth_register('user2@test.com', 'Iampassword', 'Jiaqi', 'Lu')
    login_user2 = auth_login('user2@test.com', 'Iampassword')
    u_id_user2 = login_user2['u_id']
    token_user2 = login_user2['token']


    # Create the user3.
    auth_register('user3@test.com', 'Iampassword', 'Tingyu', 'Jiang')
    login_user3 = auth_login('user3@test.com', 'Iampassword')
    token_user3 = login_user3['token']


    # Owner creates a test channel.
    chan_id = channels_create(token_owner, "Test_Channel", True).get('channel_id')
    assert chan_id
    assert type(chan_id) is int

    channel_join(token_user1, chan_id)
    channel_join(token_user2, chan_id)
    channel_join(token_user3, chan_id)
    channel_addowner(token_owner, chan_id, u_id_user2)
    # Normal case:
    channel_leave(token_user1, chan_id)
    channel_leave(token_user2, chan_id)


    # We removed user2 and user3, so the owner and user should be remaining here.
    # The total number of members in the channel should be 2.

    channel_test_details = channel_details(token_owner,chan_id)
    assert len(channel_test_details['all_members']) == 2
def test_channel_leave_normal_no_owner():
    """
    InputError: when any of:Channel ID is not a valid channel
    AccessError: when Authorised user is not a member of channel with channel_id

    After above tests, we could trust our initialize conditions are correct, so
    we just try to make them clearly with simple test for users.
    """
    other.clear()

    # Create the owner account to access channel.
    auth_register('owner@test.com', 'Iampassword', 'Hao', 'Ren')
    login_owner = auth_login('owner@test.com', 'Iampassword')
    token_owner = login_owner['token']

    # Create the user1.
    auth_register('user1@test.com', 'Iampassword', 'Zhiyuan', 'Liu')
    login_user1 = auth_login('user1@test.com', 'Iampassword')
    token_user1 = login_user1['token']


    # Create the user2.
    auth_register('user2@test.com', 'Iampassword', 'Jiaqi', 'Lu')
    login_user2 = auth_login('user2@test.com', 'Iampassword')
    token_user2 = login_user2['token']


    # Create the user3.
    auth_register('user3@test.com', 'Iampassword', 'Tingyu', 'Jiang')
    login_user3 = auth_login('user3@test.com', 'Iampassword')
    token_user3 = login_user3['token']


    # Owner creates a test channel.
    chan_id = channels_create(token_owner, "Test_Channel", True).get('channel_id')
    assert chan_id
    assert type(chan_id) is int

    channel_join(token_user1, chan_id)
    channel_join(token_user2, chan_id)
    channel_join(token_user3, chan_id)

    # Normal case:
    channel_leave(token_user1, chan_id)
    channel_leave(token_owner, chan_id)


    # We removed user2 and user3, so the owner and user should be remaining here.
    # The total number of members in the channel should be 2.

    with pytest.raises(InputError):
        channel_details(token_owner,chan_id)


def test_channel_leave_invalid_channel():
    """
    InputError: when any of:Channel ID is not a valid channel
    AccessError: when Authorised user is not a member of channel with channel_id

    After above tests, we could trust our initialize conditions are correct, so
    we just try to make them clearly with simple test for users.
    """
    other.clear()

    # Create the owner account to access channel.
    auth_register('owner@test.com', 'Iampassword', 'Hao', 'Ren')
    login_owner = auth_login('owner@test.com', 'Iampassword')
    token_owner = login_owner['token']

    # Create the user1.
    auth_register('user1@test.com', 'Iampassword', 'Zhiyuan', 'Liu')
    login_user1 = auth_login('user1@test.com', 'Iampassword')
    u_id_user1 = login_user1['u_id']
    token_user1 = login_user1['token']
    assert login_user1
    assert u_id_user1
    assert token_user1

    # Create the user2.
    auth_register('user2@test.com', 'Iampassword', 'Jiaqi', 'Lu')
    login_user2 = auth_login('user2@test.com', 'Iampassword')
    u_id_user2 = login_user2['u_id']
    token_user2 = login_user2['token']
    assert login_user2
    assert u_id_user2
    assert token_user2

    # Create the user3.
    auth_register('user3@test.com', 'Iampassword', 'Tingyu', 'Jiang')
    login_user3 = auth_login('user3@test.com', 'Iampassword')
    u_id_user3 = login_user3['u_id']
    token_user3 = login_user3['token']
    assert login_user3
    assert u_id_user3
    assert token_user3

    # Owner creates a test channel.
    chan_id = channels_create(token_owner, "Test_Channel", True).get('channel_id')
    assert chan_id
    assert type(chan_id) is int

    channel_join(token_user1, chan_id)
    channel_join(token_user2, chan_id)
    channel_join(token_user3, chan_id)

    # Normal case:
    channel_leave(token_user1, chan_id)
    channel_leave(token_user2, chan_id)

    wrong_id = 3141592653
    with pytest.raises(InputError):
        channel_leave(token_user3, wrong_id)
def test_channel_leave_invalid_token():
    """
    InputError: when any of:Channel ID is not a valid channel
    AccessError: when Authorised user is not a member of channel with channel_id

    After above tests, we could trust our initialize conditions are correct, so
    we just try to make them clearly with simple test for users.
    """
    other.clear()

    # Create the owner account to access channel.
    auth_register('owner@test.com', 'Iampassword', 'Hao', 'Ren')
    login_owner = auth_login('owner@test.com', 'Iampassword')
    token_owner = login_owner['token']

    # Create the user1.
    auth_register('user1@test.com', 'Iampassword', 'Zhiyuan', 'Liu')
    login_user1 = auth_login('user1@test.com', 'Iampassword')
    u_id_user1 = login_user1['u_id']
    token_user1 = login_user1['token']
    assert login_user1
    assert u_id_user1
    assert token_user1

    # Create the user2.
    auth_register('user2@test.com', 'Iampassword', 'Jiaqi', 'Lu')
    login_user2 = auth_login('user2@test.com', 'Iampassword')
    u_id_user2 = login_user2['u_id']
    token_user2 = login_user2['token']
    assert login_user2
    assert u_id_user2
    assert token_user2

    # Create the user3.
    auth_register('user3@test.com', 'Iampassword', 'Tingyu', 'Jiang')
    login_user3 = auth_login('user3@test.com', 'Iampassword')
    u_id_user3 = login_user3['u_id']
    token_user3 = login_user3['token']
    assert login_user3
    assert u_id_user3
    assert token_user3

    # Owner creates a test channel.
    chan_id = channels_create(token_owner, "Test_Channel", True).get('channel_id')
    assert chan_id
    assert type(chan_id) is int

    channel_join(token_user1, chan_id)
    channel_join(token_user2, chan_id)
    channel_join(token_user3, chan_id)

    # Normal case:
    channel_leave(token_user1, chan_id)
    channel_leave(token_user2, chan_id)


    with pytest.raises(InputError):
        channel_leave(token_user2 + 'abc', chan_id)


def test_channel_leave_not_a_member():
    """
    InputError: when any of:Channel ID is not a valid channel
    AccessError: when Authorised user is not a member of channel with channel_id

    After above tests, we could trust our initialize conditions are correct, so
    we just try to make them clearly with simple test for users.
    """
    other.clear()

    # Create the owner account to access channel.
    auth_register('owner@test.com', 'Iampassword', 'Hao', 'Ren')
    login_owner = auth_login('owner@test.com', 'Iampassword')
    token_owner = login_owner['token']

    # Create the user1.
    auth_register('user1@test.com', 'Iampassword', 'Zhiyuan', 'Liu')
    login_user1 = auth_login('user1@test.com', 'Iampassword')
    u_id_user1 = login_user1['u_id']
    token_user1 = login_user1['token']
    assert login_user1
    assert u_id_user1
    assert token_user1

    # Create the user2.
    auth_register('user2@test.com', 'Iampassword', 'Jiaqi', 'Lu')
    login_user2 = auth_login('user2@test.com', 'Iampassword')
    u_id_user2 = login_user2['u_id']
    token_user2 = login_user2['token']
    assert login_user2
    assert u_id_user2
    assert token_user2

    # Create the user3.
    auth_register('user3@test.com', 'Iampassword', 'Tingyu', 'Jiang')
    login_user3 = auth_login('user3@test.com', 'Iampassword')
    u_id_user3 = login_user3['u_id']
    token_user3 = login_user3['token']
    assert login_user3
    assert u_id_user3
    assert token_user3

    # Owner creates a test channel.
    chan_id = channels_create(token_owner, "Test_Channel", True).get('channel_id')
    assert chan_id
    assert type(chan_id) is int

    channel_join(token_user1, chan_id)
    channel_join(token_user2, chan_id)
    channel_join(token_user3, chan_id)

    # Normal case:
    channel_leave(token_user1, chan_id)
    channel_leave(token_user2, chan_id)

    # User had left channel by the above code.
    # If we re-leave him, there should be an access error.
    with pytest.raises(InputError):
        channel_leave(token_user2, chan_id)

################################################################################
# test of channel_addowner
################################################################################
"""
 Standard situation
"""
def test_channel_addowner_standard_situation():
    other.clear()
    # user1 login
    auth_register('test1@example.com', 'Amyisthebest', 'Yuhan', 'Yan')
    flock_auth1 = auth_login('test1@example.com', 'Amyisthebest')
    u_id1 = flock_auth1['u_id']
    token1 = flock_auth1['token']

    # user2 login
    auth_register('test2@example.com', 'Amyisthebestever', 'Vic', 'Yan')
    flock_auth2 = auth_login('test2@example.com', 'Amyisthebestever')
    u_id2 = flock_auth2['u_id']

    # user1 create a channel
    cid = channels_create(token1, "Vicmnss", True).get('channel_id')

    # user2 join in
    channel_invite(token1, cid, u_id2)

    # add user 2 as owner
    channel_addowner(token1, cid, u_id2)
    # Check if success
    owner_num = 0

    for cnl in data.return_channels():
        if cnl['channel_id'] == cid:
            owner_num = len(cnl['owner_members'])
            break
    assert owner_num == 2
    assert u_id1 == cnl['owner_members'][0]['u_id']
    assert u_id2 == cnl['owner_members'][1]['u_id']

###########################################################################################
"""
    Channel ID is not a valid channel
"""
def test_channel_addowner_valid_channel():
    other.clear()
    # user1 login
    auth_register('test1@example.com', 'Amyisthebest', 'Yuhan', 'Yan')
    flock_auth1 = auth_login('test1@example.com', 'Amyisthebest')
    u_id1 = flock_auth1['u_id']
    token1 = flock_auth1['token']

    # user2 login
    auth_register('test2@example.com', 'Amyisthebestever', 'Vic', 'Yan')
    flock_auth2 = auth_login('test2@example.com', 'Amyisthebestever')
    u_id2 = flock_auth2['u_id']

    # user1 create a channel
    cid = channels_create(token1, "Vicmnss", True).get('channel_id')
    assert cid != 1234567

    #user2 join in
    channel_invite(token1, cid, u_id2)

    # Raise error when add invalid channel ID
    with pytest.raises(InputError):
        channel_addowner(token1, 1234567, u_id2)

    # Check if success
    owner_num = 0

    for cnl in data.return_channels():
        if cnl['channel_id'] == cid:
            owner_num = len(cnl['owner_members'])
            break
    assert owner_num == 1
    assert u_id1 == cnl['owner_members'][0]['u_id']
###########################################################################################
"""
    Token not valid.
"""
def test_channel_addowner_valid_token():
    other.clear()
    # user1 login
    auth_register('test1@example.com', 'Amyisthebest', 'Yuhan', 'Yan')
    flock_auth1 = auth_login('test1@example.com', 'Amyisthebest')
    u_id1 = flock_auth1['u_id']
    token1 = flock_auth1['token']

    # user2 login
    auth_register('test2@example.com', 'Amyisthebestever', 'Vic', 'Yan')
    flock_auth2 = auth_login('test2@example.com', 'Amyisthebestever')
    u_id2 = flock_auth2['u_id']

    # user1 create a channel
    cid = channels_create(token1, "Vicmnss", True).get('channel_id')

    #user2 join in
    channel_invite(token1, cid, u_id2)

    # Raise error when add invalid channel ID
    with pytest.raises(InputError):
        channel_addowner(token1 + 'abc', cid, u_id2)

    # Check if success
    owner_num = 0

    for cnl in data.return_channels():
        if cnl['channel_id'] == cid:
            owner_num = len(cnl['owner_members'])
            break
    assert owner_num == 1
    assert u_id1 == cnl['owner_members'][0]['u_id']
###########################################################################################
"""
    user(u_id) is already the owner
"""
def test_channel_addowner_already_owner():
    other.clear()
    # user1 login
    auth_register('test1@example.com', 'Amyisthebest', 'Yuhan', 'Yan')
    flock_auth1 = auth_login('test1@example.com', 'Amyisthebest')
    u_id1 = flock_auth1['u_id']
    token1 = flock_auth1['token']

    # user2 login
    auth_register('test2@example.com', 'Amyisthebestever', 'Vic', 'Yan')
    flock_auth2 = auth_login('test2@example.com', 'Amyisthebestever')
    u_id2 = flock_auth2['u_id']

    # user1 create a channel
    cid = channels_create(token1, "Vicmnss", True).get('channel_id')

    #user2 join in and become an owner
    channel_invite(token1, cid, u_id2)
    channel_addowner(token1, cid, u_id2)

    # Check if success
    owner_num = 0

    for cnl in data.return_channels():
        if cnl['channel_id'] == cid:
            owner_num = len(cnl['owner_members'])
            break
    assert owner_num == 2
    assert u_id1 == cnl['owner_members'][0]['u_id']
    assert u_id2 == cnl['owner_members'][1]['u_id']

    # Raise error when add it again
    with pytest.raises(InputError):
        channel_addowner(token1, cid, u_id2)
###########################################################################################

"""
    authorized user(u_id) is not an owner of the channel
"""
def test_channel_addowner_not_owner():
    other.clear()
    # user1 login
    auth_register('test1@example.com', 'Amyisthebest', 'Yuhan', 'Yan')
    flock_auth1 = auth_login('test1@example.com', 'Amyisthebest')
    u_id1 = flock_auth1['u_id']
    token1 = flock_auth1['token']

    # user2 login
    auth_register('test2@example.com', 'Amyisthebestever', 'Vic', 'Yan')
    flock_auth2 = auth_login('test2@example.com', 'Amyisthebestever')
    u_id2 = flock_auth2['u_id']
    token2 = flock_auth2['token']

    # user3 login
    auth_register('test3@example.com', 'Amyisallthebest', 'Victor', 'Yan')
    flock_auth_3 = auth_login('test3@example.com', 'Amyisallthebest')
    u_id3 = flock_auth_3['u_id']

    # user1 create a channel and user2 join
    cid1 = channels_create(token1, "Vicmnss", True).get('channel_id')
    channel_invite(token1, cid1, u_id2)
    channel_invite(token1, cid1, u_id3)

    # user2 create a channel and user1 join
    cid2 = channels_create(token2, "Team4", True).get('channel_id')
    channel_invite(token2, cid2, u_id1)
    # Check the owners
    owner_num = 0

    for cnl in data.return_channels():
        if cnl['channel_id'] == cid1:
            owner_num = len(cnl['owner_members'])
            break
    assert owner_num == 1
    assert u_id1 == cnl['owner_members'][0]['u_id']

    owner_num = 0
    for cnl in data.return_channels():
        if cnl['channel_id'] == cid2:
            owner_num = len(cnl['owner_members'])
            break
    assert owner_num == 2
    assert u_id2 == cnl['owner_members'][0]['u_id']

    # raise input error for unexist owner
    with pytest.raises(InputError):
        channel_addowner(token2, cid1, u_id3)

###########################################################################################
"""
    authorized user(u_id) is not an owner of the flocker
"""
def test_channel_addowner_not_flockrowner():
    other.clear()
    # user1 login
    auth_register('test1@example.com', 'Amyisthebest', 'Yuhan', 'Yan')
    flock_auth1 = auth_login('test1@example.com', 'Amyisthebest')
    token1 = flock_auth1['token']

    # user2 login
    auth_register('test2@example.com', 'Amyisthebestever', 'Vic', 'Yan')
    flock_auth2 = auth_login('test2@example.com', 'Amyisthebestever')
    u_id2 = flock_auth2['u_id']
    token2 = flock_auth2['token']

    # user3 login
    auth_register('test3@example.com', 'Amyisallthebest', 'Victor', 'Yan')
    flock_auth_3 = auth_login('test3@example.com', 'Amyisallthebest')
    u_id3 = flock_auth_3['u_id']

    # user1 create a channel and user2 join
    cid1 = channels_create(token1, "Vicmnss", True).get('channel_id')
    channel_invite(token1, cid1, u_id2)
    channel_invite(token1, cid1, u_id3)

    # user2 is neither flockr owner nor this channel's owner
    with pytest.raises(InputError):
        channel_addowner(token2, cid1, u_id3)

###########################################################################################
"""
    authorized user(u_id) is an owner of the flocker, but not owner of this channel
"""
def test_channel_addowner_is_flockr_owner():
    other.clear()
    # user1 login
    auth_register('test1@example.com', 'Amyisthebest', 'Yuhan', 'Yan')
    flock_auth1 = auth_login('test1@example.com', 'Amyisthebest')
    token1 = flock_auth1['token']

    # user2 login
    auth_register('test2@example.com', 'Amyisthebestever', 'Vic', 'Yan')
    flock_auth2 = auth_login('test2@example.com', 'Amyisthebestever')
    u_id2 = flock_auth2['u_id']
    token2 = flock_auth2['token']

    # user3 login
    auth_register('test3@example.com', 'Amyisallthebest', 'Victor', 'Yan')
    flock_auth_3 = auth_login('test3@example.com', 'Amyisallthebest')
    u_id3 = flock_auth_3['u_id']

    # user2 create a channel and user3 join
    cid = channels_create(token2, "Team4", True).get('channel_id')
    channel_invite(token2, cid, u_id3)

    channel_addowner(token1, cid, u_id3)

    # Check if success
    owner_num = 0

    for cnl in data.return_channels():
        if cnl['channel_id'] == cid:
            owner_num = len(cnl['owner_members'])
            break
    assert owner_num == 2
    assert u_id2 == cnl['owner_members'][0]['u_id']
    assert u_id3 == cnl['owner_members'][1]['u_id']
###########################################################################################
# test of channel_removeowner
###########################################################################################
"""
    Standard situation
"""
def test_channel_removeowner_standard_situation():
    other.clear()
    # user1 login
    auth_register('test1@example.com', 'Amyisthebest', 'Yuhan', 'Yan')
    flock_auth1 = auth_login('test1@example.com', 'Amyisthebest')
    assert type(flock_auth1) is dict
    u_id1 = flock_auth1['u_id']
    token1 = flock_auth1['token']
    assert u_id1
    assert type(u_id1) is int
    assert token1
    assert type(token1) is str

    # user2 login
    auth_register('test2@example.com', 'Amyisthebestever', 'Vic', 'Yan')
    flock_auth2 = auth_login('test2@example.com', 'Amyisthebestever')
    assert type(flock_auth2) is dict
    u_id2 = flock_auth2['u_id']
    token2 = flock_auth2['token']
    assert u_id2
    assert type(u_id2) is int
    assert token2
    assert type(token2) is str

    # user1 create a channel
    cid = channels_create(token1, "Vicmnss", True).get('channel_id')
    assert cid
    assert type(cid) is int

    # Check if success
    channel_addowner(token1, cid, u_id2)
    owner_num = 0

    for cnl in data.return_channels():
        if cnl['channel_id'] == cid:
            owner_num = len(cnl['owner_members'])
            break
    assert owner_num == 2
    assert u_id1 == cnl['owner_members'][0]['u_id']
    assert u_id2 == cnl['owner_members'][1]['u_id']

    # Delete the added owner
    channel_removeowner(token1, cid, u_id2)

    # assert the user has been moved
    owner_num = 0
    for cnl in data.return_channels():
        if cnl['channel_id'] == cid:
            owner_num = len(cnl['owner_members'])
            break
    assert owner_num == 1
    assert u_id1 == cnl['owner_members'][0]['u_id']

###########################################################################################

"""
    Channel ID is not a valid channel
"""
def test_channel_removeowner_valid_channel():
    other.clear()
    # user1 login
    auth_register('test1@example.com', 'Amyisthebest', 'Yuhan', 'Yan')
    flock_auth1 = auth_login('test1@example.com', 'Amyisthebest')
    assert type(flock_auth1) is dict
    u_id1 = flock_auth1['u_id']
    token1 = flock_auth1['token']
    assert u_id1
    assert type(u_id1) is int
    assert token1
    assert type(token1) is str

    # user2 login
    auth_register('test2@example.com', 'Amyisthebestever', 'Vic', 'Yan')
    flock_auth2 = auth_login('test2@example.com', 'Amyisthebestever')
    assert type(flock_auth2) is dict
    u_id2 = flock_auth2['u_id']
    token2 = flock_auth2['token']
    assert u_id2
    assert type(u_id2) is int
    assert token2
    assert type(token2) is str

    # user1 create a channel
    cid = channels_create(token1, "Vicmnss", True).get('channel_id')
    assert cid
    assert type(cid) is int
    assert cid != 1234567

    owner_num = 0

    for cnl in data.return_channels():
        if cnl['channel_id'] == cid:
            owner_num = len(cnl['owner_members'])
            break
    assert owner_num == 1
    assert u_id1 == cnl['owner_members'][0]['u_id']

    # user1 invite and add user2 as an owner
    channel_invite(token1, cid, u_id2)
    channel_addowner(token1, cid, u_id2)

    # Raise error when having a invalid channel id
    with pytest.raises(InputError):
        channel_removeowner(token1, 1234567, u_id2)

    # assert the user hasnot been moved
    owner_num = 0
    for cnl in data.return_channels():
        if cnl['channel_id'] == cid:
            owner_num = len(cnl['owner_members'])
            break
    assert owner_num == 2
    assert u_id1 == cnl['owner_members'][0]['u_id']
    assert u_id2 == cnl['owner_members'][1]['u_id']

###########################################################################################

"""
    Channel ID is not a valid token
"""
def test_channel_removeowner_valid_token():
    other.clear()
    # user1 login
    auth_register('test1@example.com', 'Amyisthebest', 'Yuhan', 'Yan')
    flock_auth1 = auth_login('test1@example.com', 'Amyisthebest')
    u_id1 = flock_auth1['u_id']
    token1 = flock_auth1['token']

    # user2 login
    auth_register('test2@example.com', 'Amyisthebestever', 'Vic', 'Yan')
    flock_auth2 = auth_login('test2@example.com', 'Amyisthebestever')
    u_id2 = flock_auth2['u_id']

    # user1 create a channel
    cid = channels_create(token1, "Vicmnss", True).get('channel_id')


    owner_num = 0

    for cnl in data.return_channels():
        if cnl['channel_id'] == cid:
            owner_num = len(cnl['owner_members'])
            break
    assert owner_num == 1
    assert u_id1 == cnl['owner_members'][0]['u_id']

    # user1 invite and add user2 as an owner
    channel_invite(token1, cid, u_id2)
    channel_addowner(token1, cid, u_id2)

    # Raise error when having a invalid channel id
    with pytest.raises(InputError):
        channel_removeowner(token1 + 'abc', cid, u_id2)

    # assert the user hasnot been moved
    owner_num = 0
    for cnl in data.return_channels():
        if cnl['channel_id'] == cid:
            owner_num = len(cnl['owner_members'])
            break
    assert owner_num == 2
    assert u_id1 == cnl['owner_members'][0]['u_id']
    assert u_id2 == cnl['owner_members'][1]['u_id']
###########################################################################################

"""
    Channel ID is not a valid user
"""
def test_channel_removeowner_valid_user():
    other.clear()
    # user1 login
    auth_register('test1@example.com', 'Amyisthebest', 'Yuhan', 'Yan')
    flock_auth1 = auth_login('test1@example.com', 'Amyisthebest')
    assert type(flock_auth1) is dict
    u_id1 = flock_auth1['u_id']
    token1 = flock_auth1['token']
    assert u_id1
    assert type(u_id1) is int
    assert token1
    assert type(token1) is str

    # user2 login
    auth_register('test2@example.com', 'Amyisthebestever', 'Vic', 'Yan')
    flock_auth2 = auth_login('test2@example.com', 'Amyisthebestever')
    assert type(flock_auth2) is dict
    u_id2 = flock_auth2['u_id']
    token2 = flock_auth2['token']
    assert u_id2
    assert type(u_id2) is int
    assert token2
    assert type(token2) is str

    # user1 create a channel
    cid = channels_create(token1, "Vicmnss", True).get('channel_id')
    assert cid
    assert type(cid) is int


    owner_num = 0

    for cnl in data.return_channels():
        if cnl['channel_id'] == cid:
            owner_num = len(cnl['owner_members'])
            break
    assert owner_num == 1
    assert u_id1 == cnl['owner_members'][0]['u_id']

    # user1 invite and add user2 as an owner
    channel_invite(token1, cid, u_id2)
    channel_addowner(token1, cid, u_id2)

    # Raise error when having a invalid channel id
    with pytest.raises(InputError):
        channel_removeowner(token1, cid, u_id2 + 0xf)

    # assert the user hasnot been moved
    owner_num = 0
    for cnl in data.return_channels():
        if cnl['channel_id'] == cid:
            owner_num = len(cnl['owner_members'])
            break
    assert owner_num == 2
    assert u_id1 == cnl['owner_members'][0]['u_id']
    assert u_id2 == cnl['owner_members'][1]['u_id']

###########################################################################################

"""
    user(u_id) is not the owner
"""
def test_channel_removeowner_not_owner():
    other.clear()
    # user1 login
    auth_register('test1@example.com', 'Amyisthebest', 'Yuhan', 'Yan')
    flock_auth1 = auth_login('test1@example.com', 'Amyisthebest')
    u_id1 = flock_auth1['u_id']
    token1 = flock_auth1['token']

    # user2 login
    auth_register('test2@example.com', 'Amyisthebestever', 'Vic', 'Yan')
    flock_auth2 = auth_login('test2@example.com', 'Amyisthebestever')
    u_id2 = flock_auth2['u_id']

    # user1 create a channel and invite user2
    cid = channels_create(token1, "Vicmnss", True).get('channel_id')
    channel_invite(token1, cid, u_id2)

    owner_num = 0

    for cnl in data.return_channels():
        if cnl['channel_id'] == cid:
            owner_num = len(cnl['owner_members'])
            break
    assert owner_num == 1
    assert u_id1 == cnl['owner_members'][0]['u_id']

    # raise input error for unexist owner
    with pytest.raises(InputError):
        channel_removeowner(token1, cid, u_id2)
###########################################################################################

"""
    authorized user(u_id) is not an owner of this channel
"""
def test_channel_removeowner_nonchannel_owner():
    other.clear()
    # user1 login
    auth_register('test1@example.com', 'Amyisthebest', 'Yuhan', 'Yan')
    flock_auth1 = auth_login('test1@example.com', 'Amyisthebest')
    u_id1 = flock_auth1['u_id']
    token1 = flock_auth1['token']

    # user2 login
    auth_register('test2@example.com', 'Amyisthebestever', 'Vic', 'Yan')
    flock_auth2 = auth_login('test2@example.com', 'Amyisthebestever')
    u_id2 = flock_auth2['u_id']
    token2 = flock_auth2['token']

    # user1 create a channel and user2 join
    cid1 = channels_create(token1, "Vicmnss", True).get('channel_id')
    channel_invite(token1, cid1, u_id2)

    owner_num = 0

    for cnl in data.return_channels():
        if cnl['channel_id'] == cid1:
            owner_num = len(cnl['owner_members'])
            break
    assert owner_num == 1
    assert u_id1 == cnl['owner_members'][0]['u_id']

    # user2 create a channel and user1 join
    cid2 = channels_create(token2, "Team4", True).get('channel_id')
    assert cid2
    assert type(cid2) is int
    channel_invite(token2, cid2, u_id1)

    owner_num = 0
    for cnl in data.return_channels():
        if cnl['channel_id'] == cid2:
            owner_num = len(cnl['owner_members'])
            break
    assert owner_num == 2
    assert u_id2 == cnl['owner_members'][0]['u_id']

    # raise input error for unexist owner
    with pytest.raises(InputError):
        channel_removeowner(token2, cid1, u_id1)

################################################################################
"""
    authorized user(u_id) is not an owner of the flocker
"""
def test_channel_rmowner_not_flockrowner():
    other.clear()
    # user1 login
    auth_register('test1@example.com', 'Amyisthebest', 'Yuhan', 'Yan')
    flock_auth1 = auth_login('test1@example.com', 'Amyisthebest')
    token1 = flock_auth1['token']

    # user2 login
    auth_register('test2@example.com', 'Amyisthebestever', 'Vic', 'Yan')
    flock_auth2 = auth_login('test2@example.com', 'Amyisthebestever')
    u_id2 = flock_auth2['u_id']
    token2 = flock_auth2['token']

    # user3 login
    auth_register('test3@example.com', 'Amyisallthebest', 'Victor', 'Yan')
    flock_auth_3 = auth_login('test3@example.com', 'Amyisallthebest')
    u_id3 = flock_auth_3['u_id']

    # user1 create a channel and user2 join
    cid1 = channels_create(token1, "Vicmnss", True).get('channel_id')
    channel_invite(token1, cid1, u_id2)
    channel_invite(token1, cid1, u_id3)
    channel_addowner(token1, cid1, u_id3)

    # user2 is neither flockr owner nor this channel's owner
    with pytest.raises(InputError):
        channel_removeowner(token2, cid1, u_id3)

################################################################################
"""
    authorized user(u_id) is an owner of the flocker, but not owner of this channel
"""
def test_channel_rmowner_is_flockr_owner():
    other.clear()
    # user1 login
    auth_register('test1@example.com', 'Amyisthebest', 'Yuhan', 'Yan')
    flock_auth1 = auth_login('test1@example.com', 'Amyisthebest')
    token1 = flock_auth1['token']

    # user2 login
    auth_register('test2@example.com', 'Amyisthebestever', 'Vic', 'Yan')
    flock_auth2 = auth_login('test2@example.com', 'Amyisthebestever')
    u_id2 = flock_auth2['u_id']
    token2 = flock_auth2['token']

    # user3 login
    auth_register('test3@example.com', 'Amyisallthebest', 'Victor', 'Yan')
    flock_auth_3 = auth_login('test3@example.com', 'Amyisallthebest')
    u_id3 = flock_auth_3['u_id']

    # user2 create a channel and user3 join
    cid = channels_create(token2, "Team4", True).get('channel_id')
    channel_invite(token2, cid, u_id3)
    channel_addowner(token2, cid, u_id3)
    channel_removeowner(token1, cid, u_id3)

    # Check if success
    owner_num = 0

    for cnl in data.return_channels():
        if cnl['channel_id'] == cid:
            owner_num = len(cnl['owner_members'])
            break
    assert owner_num == 1
    assert u_id2 == cnl['owner_members'][0]['u_id']