"""
This library allows you to quickly and easily use the Loyalicos Web API v1 via Python.
For more information on this library, see the README on GitHub.

For more information on the Loyalicos API, see:

For the user guide, code examples, and more, visit the main docs page:

This file provides the Loyalicos API Client.
"""

import os
import requests
from .interface import Interface
from .exceptions import *

class LoyalicosAPIClient(Interface):
    """ Loyaicos basic API client Object
        Extend these to add new objects with API interface.

        Use this object to interact with the Loyalicos API

    """

    def __init__(self, api_key=None, user_token={}, host=None):
        self.user_token = user_token
        self.host = host 
        if self.host == None:
            self.host = os.environ.get('LOYALICOS_API_HOST')
        self.api_key = api_key 
        if self.api_key == None:
            self.api_key = os.environ.get('LOYALICOS_API_KEY')
        if self.api_key != None:
            auth = 'Bearer {}'.format(self.api_key)
        else:
            api_client = os.environ.get('LOYALICOS_API_CLIENT')
            api_secret = os.environ.get('LOYALICOS_API_SECRET')
            if api_client == None or api_secret == None:
                raise NoCredentialsFoundError
            else:
                auth_response = requests.get(f'{self.host}/oauth/authapi', auth=requests.auth.HTTPBasicAuth(api_client, api_secret))
                auth_result = auth_response.json()
                self.api_key = auth_result.get('token')
                auth = 'Bearer {}'.format(self.api_key)
        super(LoyalicosAPIClient, self).__init__(self.host, auth)

class Member(LoyalicosAPIClient):
    """
        Extends API Client to add a Member
    """
    def create(self, alias=None):
        self.method = 'PUT'
        self.path = ['3PAMI', 'membership']
        self.json = {"external_id" : alias}
        self.send_request()
        if self.response.status_code != 200:
            raise HTTPRequestError
        self.access_token = self.response.body

    """
        Extends API Client to get a Member profile
    """
    def read(self, alias=None, user_token={}):
        self.user_token = user_token or self.user_token
        self.method = 'GET'
        self.path = ['3PAMI', 'membership', alias]
        user_auth = {'Access-Token' : user_token['access_token']}
        self.update_headers(user_auth)
        self.send_request()
        if self.response.status_code != 200:
            raise HTTPRequestError
        self.profile = self.response.body
        

    """
        Extends API Client to get a Member profile
    """
    def renew_token(self, user_token={}):
        self.user_token = user_token or self.user_token
        self.method = 'POST'
        self.path = ['3PAMI', 'refreshToken']
        self.json = {'grant_type' : 'refresh_token', 'refresh_token' : user_token['refresh_token']}
        self.send_request()
        if self.response.status_code != 200:
            raise HTTPRequestError
        self.access_token = self.response.body

class Transaction(LoyalicosAPIClient):
    """
        Extends API Client to send a transaction
    """
    def earn(self, partner_code, external_id, activity, type, channel, subactivity=None, subtype=None, subchannel=None, currency=None, date_activity=None, items=[]):
        self.method = 'PUT'
        self.path = ['points', 'accrue']
        self.json = {
            'partner_code': partner_code,
            'external_id' : external_id,
            'date_activity' : date_activity,
            'channel':channel,
            'subchannel':subchannel,
            'type':type,
            'subtype':subtype,
            'activity':activity,
            'subactivity':subactivity,
            'currency':currency,
            'items':items
            }
        self.send_request()
        if self.response.status_code != 200:
            raise HTTPRequestError
        self.id = self.response.body['trx_id']

    """
        Extends API Client to get a Member profile
    """
    def read(self, alias=None, user_token={}):
        self.user_token = user_token or self.user_token
        self.method = 'GET'
        self.path = ['3PAMI', 'membership', alias]
        user_auth = {'Access-Token' : user_token['access_token']}
        self.update_headers(user_auth)
        self.send_request()
        if self.response.status_code != 200:
            raise HTTPRequestError
        self.profile = self.response.body
        

    """
        Extends API Client to get a Member profile
    """
    def renew_token(self, user_token={}):
        self.user_token = user_token or self.user_token
        self.method = 'POST'
        self.path = ['3PAMI', 'refreshToken']
        self.json = {'grant_type' : 'refresh_token', 'refresh_token' : user_token['refresh_token']}
        self.send_request()
        if self.response.status_code != 200:
            raise HTTPRequestError
        self.access_token = self.response.body
        