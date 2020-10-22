import pytest

import data.data as data
import base.user as user
from base.error import InputError
from base.other import clear
import base.auth as auth

def test_user_profile_correct_return():
    ''' checks correct return from login'''
    clear()
    registration = auth.auth_register('valid@example.com', 'password', 'Test Person', 'Bam')

    token = registration['token']
    u_id = registration["u_id"]

    result = user.user_profile(token,u_id)

    # - Dict structure -> {u_id, token}
    assert isinstance(result, dict)
    # - u_id is an integer
    assert isinstance(result['email'], str)

    # - token is a string
    assert isinstance(result['name_first'], str)

    assert isinstance(result['name_first'], str)

    assert isinstance(result['name_last'], str)

    assert isinstance(result['handle_str'], str)

def test_user_profile_input_error_invalid_token():
    clear()
    registration = auth.auth_register('valid@example.com', 'password', 'Mate', 'Old')
    token = registration['token']
    u_id = registration["u_id"]

    # # - returns false when invalid token
    invalid_token = '500000'
    if invalid_token == token:
        raise Exception('The token in program is actually valid')
    is_success = user.user_profile(invalid_token,u_id)
    assert is_success['is_success'] is False



def test_user_profile_input_error_invalid_u_id():
    clear()
    registration = auth.auth_register('valid@example.com', 'password', 'Mate', 'Old')
    token = registration['token']
    with pytest.raises(InputError):
        user.user_profile(token, "3263fdhr")
    with pytest.raises(InputError):
        user.user_profile(token, 26157890314)