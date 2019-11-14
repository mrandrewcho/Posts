#%%
import requests
import base64

## Enter user's API key, secret, and Stubhub login
#app_token = input('Enter app token: ')
consumer_key = '4SMrNqpjF6sxULJWWbYEQAaKXilhHC9A'
consumer_secret = 'GjogLh5JmRzDsvGz'
stubhub_username = 'andycho7@gmail.com'
stubhub_password = 'koreanguy94'

#%%
combo = consumer_key + ':' + consumer_secret
basic_authorization_token = base64.b64encode(combo.encode('utf-8'))

#%%
basic_authorization_token.decode('utf-8')

#%%
#####
#Generate Access Token
#access_token: 2biKQ67B2IYqOsdp7jX797Yf40n3
#####
#doesnt work in code for some reason; can get from here: https://developer.stubhub.com/oauth/apis/post/accesstoken
url = 'https://api.stubhub.com/sellers/oauth/accesstoken'
headers = {
        'Content-Type':'application/json',
        'Authorization':'Basic ' + basic_authorization_token.decode('utf-8')}
body = {
        'grant_type':'client_credentials',
        'username':stubhub_username,
        'password':stubhub_password}

r = requests.post(url, headers=headers, data=body)
print(r)
print(r.text)

token_response = r.json()
access_token = token_response['access_token']
user_GUID = r.headers['user_guid']

#%%
#useful APIs
#https://developer.stubhub.com/searchevent/apis/get/search/events/v3