import Authenticate
import Repos

access_token = ''
access_token = Authenticate.getAccessToken()

if(access_token != ''):
    Repos.getRepoList(access_token=access_token)  
else:
    print('failed to get access token')  